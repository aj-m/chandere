"""Core module and entry point to Chandere2, parses command-line
arguments and handles the asynchronous event loop.
"""

import asyncio
import signal
import sys

from chandere2.cli import PARSER
from chandere2.connection import test_connection
from chandere2.handle_targets import main_loop
from chandere2.output import Console
from chandere2.validate_input import (generate_uri, get_path, strip_target)


## FIXME: Cleaner, but still raises ~ 6 exceptions. <jakob@memeware.net>
def clean_up():
    """General subroutine to safely clean up after a signal interrupt
    has been received, cancelling all tasks in the event loop.
    """
    for task in asyncio.Task.all_tasks():
        task.cancel()


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
            target_uris[uri] = [board, bool(thread), ""]
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
        loop.add_signal_handler(signal.SIGINT, clean_up)

        if args.mode is None:
            target_operation = test_connection(target_uris, args.ssl, output)
            loop.run_until_complete(target_operation)
        else:
            target_operation = main_loop(target_uris, args, output)
            loop.run_until_complete(target_operation)
    finally:
        loop.close()
