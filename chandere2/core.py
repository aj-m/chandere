"""Core module and entry point to Chandere2, vaildates command-line
input and controls the asynchronous event loop.
"""

import asyncio
import signal
import sys

from chandere2.cli import PARSER
from chandere2.connection import (download_file, fetch_uri, try_connection,
                                  wrap_semaphore)
from chandere2.output import Console
from chandere2.post import (cache_posts, find_files, filter_posts,
                            get_threads, iterate_posts)
from chandere2.validate import (get_filters, get_path, get_targets)
from chandere2.write import (archive_plaintext, archive_sqlite, create_archive)

MAX_CONNECTIONS = 8


def main(args=PARSER.parse_args(), output=None):
    """Command-line entry-point to Chandere2."""
    output = output or Console(debug=args.debug)

    target_uris, failed = get_targets(args.targets, args.imageboard)
    for pattern in failed:
        output.write_error("Invalid target \"%s\"" % pattern)
    if not target_uris:
        output.write_error("No valid targets provided.")
        sys.exit(1)

    path = get_path(args.output, args.mode, args.output_format)
    if path is None:
        output.write_error("The given output path cannot be written to.")
        sys.exit(1)

    filters, failed = get_filters(args.filters, args.imageboard)
    for argument in failed:
        output.write_error("Invalid filter pattern \"%s\"" % argument)

    try:
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, clean_up)

        if args.mode is None:
            target_operation = try_connection(target_uris, args.ssl, output)
            loop.run_until_complete(target_operation)
        else:
            target_operation = main_loop(target_uris, path, filters,
                                         args, output)
            loop.run_until_complete(target_operation)
    finally:
        loop.close()


def clean_up():
    """General subroutine to safely clean up after a signal interrupt
    has been received, cancelling all tasks in the event loop.
    """
    for task in asyncio.Task.all_tasks():
        task.cancel()


async def main_loop(target_uris: dict, path: str, filters: list, args, output):
    """Loop that continually iterates over targets, processing them
    respective to the mode of operation and stopping when finished.
    """
    output.write_debug("Entering main loop")

    iterations = 0
    imageboard = args.imageboard
    create_archive(args.mode, args.output_format, path)

    cache = []

    while True:
        iterations += 1
        operations = []

        output.write_debug("Iteration %d." % iterations)

        if args.nocap:
            for uri in target_uris:
                last_load = target_uris[uri][2]
                operations.append(fetch_uri(uri, last_load, args.ssl))
        else:
            connection_cap = asyncio.Semaphore(MAX_CONNECTIONS)
            for uri in target_uris:
                last_load = target_uris[uri][2]
                target_operation = fetch_uri(uri, last_load, args.ssl)
                wrapped = wrap_semaphore(target_operation, connection_cap)
                operations.append(wrapped)


        for future in asyncio.as_completed(operations):
            content, error, last_load, uri = await future
            board, thread, _ = target_uris[uri]
            output.write_debug("Connected to %s..." % uri)

            if error:
                if error == 404:
                    output.write_error("%s does not exist." % uri)
                else:
                    output.write_error("Could not connect to server.")
                del target_uris[uri]
                continue


            if thread and args.mode == "fd":
                posts = iterate_posts(content, imageboard)
                posts = filter_posts(posts, filters)
                posts = cache_posts(posts, cache, imageboard)
                for image, filename in find_files(posts, board, imageboard):
                    output.write("Downloading \"%s\"..." % filename)
                    await download_file(image, path, filename, args.ssl)
            elif thread and args.mode == "ar":
                posts = iterate_posts(content, imageboard)
                posts = filter_posts(posts, filters)
                posts = cache_posts(posts, cache, imageboard)
                if args.output_format == "sqlite":
                    archive_sqlite(posts, path, imageboard)
                else:
                    archive_plaintext(posts, path, imageboard)
            else:
                for uri in get_threads(content, board, args.imageboard):
                    target_uris[uri] = [board, True, ""]

            if last_load is not None:
                target_uris[uri][2] = last_load

        if args.continuous:
            pass
        elif all(thread for _, thread, _ in target_uris.values()):
            break
        elif iterations > 1:
            break
