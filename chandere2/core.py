"""Core module and entry point to Chandere2, parses command-line
arguments and handles the asynchronous event loop.
"""

import asyncio
import sys

from chandere2.cli import PARSER
from chandere2.connection import test_connection
from chandere2.context import CONTEXTS
from chandere2.output import Console
from chandere2.scrape import (get_threads, poll_targets)
from chandere2.uri import (generate_uri, strip_target)
from chandere2.write import get_path


def main():
    """Primary entry-point to Chandere2."""
    args = PARSER.parse_args()
    output = Console(debug=args.debug)

    imageboard_context = CONTEXTS.get(args.imageboard)

    target_uris = {}

    for target in args.targets:
        board, thread = strip_target(target)
        if board is not None:
            uri = generate_uri(board, thread, args.imageboard)
            target_uris[uri] = [board, thread != "threads", ""]
        else:
            output.write_error("Invalid target: %s" % target)

    if not target_uris:
        output.write_error("No valid targets provided.")
        sys.exit(1)


    output_path = get_path(args.output, args.mode, args.output_format)

    if output_path is None:
        output.write_error("The given output path is not writeable.")
        sys.exit(1)

    loop = asyncio.get_event_loop()

    try:
        if args.mode is None:
            target_operation = test_connection(target_uris, args.ssl, output)
            loop.run_until_complete(target_operation)

        else:
            thread_listing_queue = asyncio.Queue()
            post_queue = asyncio.Queue()
            filtered_posts_queue = asyncio.Queue()
            write_queue = asyncio.Queue()

            filters = [] ## TODO
            poll_operation = poll_targets(target_uris, args.ssl, post_queue,
                                          thread_listing_queue, args.run_once,
                                          output)

            thread_operation = get_threads(target_uris, thread_listing_queue,
                                           args.imageboard, output)

            # filter_operation = filter_posts(filters, posts_queue,
            #                                 filtered_queue, output)
            # scrape_operation = scrape_posts(target_uris, args.mode,
            #                                 args.imageboard, posts_queue,
            #                                 write_queue, output)

            loop.run_until_complete(poll_operation)
            loop.run_until_complete(thread_operation)
    except KeyboardInterrupt:
        output.write("Quitting...")
    finally:
        loop.close()
