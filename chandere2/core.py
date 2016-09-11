"""Core module and entry point to Chandere2, parses command-line
arguments and handles the asynchronous event loop.
"""

import asyncio
import sys

from chandere2.cli import parser
from chandere2.connection import (generate_uri, test_connection)
from chandere2.output import Console


def main():
    """Primary entry-point to Chandere2."""
    args = parser.parse_args()
    output = Console(args.debug)
    event_loop = asyncio.get_event_loop()

    uris = list(map(generate_uri, args.targets))

    if all(item is None for item in uris):
        output.write_error("No valid targets provided.")
        sys.exit(1)

    if args.mode is None:
        test_connection(uris, args.ssl, output)
        sys.exit(0)

    try:
        pass
    except KeyboardInterrupt:
        output.write("Quitting...")
    finally:
        event_loop.close()
