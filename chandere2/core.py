"""Core module and entry point to Chandere2, parses command-line
arguments and handles the asynchronous event loop.
"""

import asyncio
import functool
import sys

from chandere2.cli import PARSER
from chandere2.connection import test_connection
from chandere2.output import Console
from chandere2.handle_targets import scrape_target
from chandere2.validate_input import (generate_uri, get_path,
                                      strip_target)


async def main_loop(target_uris: dict, args, output):
    """[Document me!]"""
    target_operation = functools.partial(scrape_target, target_uris,
                                         args.ssl, output)

    operations = [target_operation(uri) for uri in target_uris]


def main():
    """Primary entry-point to Chandere2."""
    args = PARSER.parse_args()
    output = Console(debug=args.debug)

    # Get targets.
    target_uris = {}

    for target in args.targets:
        board, thread = strip_target(target)
        if board is not None:
            uri = generate_uri(board, thread, args.imageboard)
            target_uris[uri] = [board, thread, ""]
        else:
            output.write_error("Invalid target: %s" % target)

    if not target_uris:
        output.write_error("No valid targets provided.")
        sys.exit(1)


    # Get the output path.
    output_path = get_path(args.output, args.mode, args.output_format)

    if output_path is None:
        output.write_error("The given output path is not valid.")
        sys.exit(1)


    try:
        loop = asyncio.get_event_loop()

        if args.mode is None:
            target_operation = test_connection(target_uris, args.ssl, output)
            loop.run_until_complete(target_operation)
        else:
            target_operation = main_loop(target_uris, args, output)
            loop.run_until_complete(target_operation)
    except KeyboardInterrupt:
        output.write("Quitting...")
    finally:
        loop.close()
