"""Core module and entry point to Chandere2, parses command-line
arguments and handles the asynchronous event loop.
"""

import asyncio
import sys

from chandere2.cli import parser
from chandere2.output import Console
from chandere2.uri import generate_url


def main():
    """Primary entry-point to Chandere2."""
    args = parser.parse_args()
    output = Console(args.debug)

    event_loop = asyncio.get_event_loop()
    try:
        output.write_debug(str(vars(args)))
        output.write_debug(generate_url(args.targets[0]))
    except KeyboardInterrupt:
        output.write("Quitting...")
    finally:
        event_loop.close()
