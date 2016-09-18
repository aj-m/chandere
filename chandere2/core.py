"""Core module and entry point to Chandere2, parses command-line
arguments and handles the asynchronous event loop.
"""

import asyncio
import sys

from chandere2.cli import parser
from chandere2.connection import test_connection
from chandere2.output import Console
from chandere2.uri import (generate_uri, strip_target)


def main():
    """Primary entry-point to Chandere2."""
    args = parser.parse_args()
    output = Console(debug=args.debug)
    event_loop = asyncio.get_event_loop()

    # A hashmap is used for faster, more efficient lookups.
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

    ## TODO: Clean up. <jakob@memeware.net>
    # args.mode will only be None if no other mode
    # of operation is specified by the user.
    if args.mode is None:
        event_loop.run_until_complete(test_connection(target_uris, args.ssl, output))

    try:
        pass
    except KeyboardInterrupt:
        output.write("Quitting...")
    finally:
        event_loop.close()
