"""Core module and entry point to Chandere2, parses command-line
arguments and handles the asynchronous event loop.
"""

import asyncio
import signal
import sys

from chandere2.cli import PARSER
from chandere2.connection import (test_connection, wrap_semaphore)
from chandere2.output import Console
from chandere2.post import (get_images, get_image_uri, get_threads)
from chandere2.validate import (get_path, get_targets)

MAX_CONNECTIONS = 8


def main():
    """Entry-point to Chandere2."""
    args = PARSER.parse_args()
    output = Console(debug=args.debug)

    target_uris = get_targets(args.targets, args.imageboard, output)

    if not target_uris:
        output.write_error("No valid targets provided.")
        sys.exit(1)

    ## TODO: Rename to output_path?
    # Get the output path.
    path = get_path(args.output, args.mode, args.output_format)

    if path is None:
        output.write_error("The given output path is not valid.")
        sys.exit(1)


    try:
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, clean_up)

        if args.mode is None:
            target_operation = test_connection(target_uris, args.ssl, output)
            loop.run_until_complete(target_operation)
        else:
            target_operation = main_loop(target_uris, path, args, output)
            loop.run_until_complete(target_operation)
    finally:
        loop.close()


## FIXME: Cleaner, but still raises ~ 6 exceptions. <jakob@memeware.net>
def clean_up():
    """General subroutine to safely clean up after a signal interrupt
    has been received, cancelling all tasks in the event loop.
    """
    for task in asyncio.Task.all_tasks():
        task.cancel()


async def main_loop(target_uris: dict, path: str, args, output):
    """Main scraping loop."""
    while True:
        imageboard = args.imageboard
        operations = []

        if args.nocap:
            for uri in target_uris:
                last_load = target_uris[uri][2]
                operations.append(fetch_uri(uri, last_load, args.ssl, output))
        else:
            connection_cap = asyncio.Semaphore(MAX_CONNECTIONS)
            for uri in target_uris:
                last_load = target_uris[uri][2]
                target_operation = fetch_uri(uri, last_load, args.ssl, output)
                wrapped = wrap_semaphore(target_operation, connection_cap)
                operations.append(wrapped)


        for future in asyncio.as_completed(operations):
            board, thread, _ = target_uris[uri]
            content, error, last_load, uri = await future

            if error:
                del target_uris[uri]
                continue

            ## TODO: Separate into subroutines? <jakob@memeware.net>
            if thread and args.mode == "fd":
                ## TODO: Add support for contexts. <jakob@memeware.net>
                for post in content.get("posts"):
                    images = get_images(post, imageboard)
                    for original_filename, server_filename in images:
                        ## TODO: Clean up. <jakob@memeware.net>
                        image_uri = get_image_uri(server_filename, board,
                                                  imageboard)
                        output.write("Downloading %s..." % original_filename)

                        ## TODO: Clean up. <jakob@memeware.net>
                        await download_file(image_uri, path, original_filename,
                                            args.ssl)
            elif thread and args.mode == "ar":
                ## TODO: Add support for contexts. <jakob@memeware.net>
                for post in content.get("posts"):
                    pass
            else:
                for uri in get_threads(content, board, args.imageboard):
                    target_uris[uri] = [board, True, ""]

            target_uris[uri][2] = last_load

        break ##
