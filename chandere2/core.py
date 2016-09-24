"""Core module and entry point to Chandere2, parses command-line
arguments and handles the asynchronous event loop.
"""

import asyncio
import sys

from chandere2.cli import PARSER
from chandere2.connection import test_connection
from chandere2.context import CONTEXTS
from chandere2.output import Console
from chandere2.scrape import scrape_targets
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
            target_uris[uri] = [board, bool(thread), ""]
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

        ## Unfinished.
        else:
            scrape = scrape_targets(target_uris, args.ssl, output)
            loop.run_until_complete(scrape)
    except KeyboardInterrupt:
        output.write("Quitting...")
    finally:
        loop.close()
