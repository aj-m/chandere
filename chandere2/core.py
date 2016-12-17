"""Entry point to Chandere2. Parses command-line input
and initializes data structures for use in scraping.
"""

import asyncio
import concurrent.futures
import signal
import sys
import time

from chandere2.cli import PARSER
from chandere2.connection import try_connection
from chandere2.output import Console
from chandere2.validate import (get_filters, get_path, get_targets)
from chandere2.write import create_archive

MAX_CONNECTIONS = 8
WAIT_TIME = 30


def main(parser=PARSER, output=None):
    """Command-line entry-point to Chandere2."""
    args = parser.parse_args()
    output = output or Console(debug=args.debug)

    target_uris, failed = get_targets(args.targets, args.imageboard, args.ssl)
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

    create_archive(args.mode, args.output_format, path)
    try:
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, clean_up)
        if args.mode is None:
            target_operation = try_connection(target_uris, output)
            loop.run_until_complete(target_operation)
        else:
            target_operation = main_loop(target_uris, path, filters,
                                         args, output)
            loop.run_until_complete(target_operation)
    except concurrent.futures._base.CancelledError:
        pass
    finally:
        loop.close()


def clean_up():
    """Safe clean up function to cancel pending tasks."""
    for task in asyncio.Task.all_tasks():
        task.cancel()
