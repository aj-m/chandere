"""Entry point for the command-line interface to Chandere."""

import asyncio

from chandere.cli import PARSER

## concurrent.futures._base.TimeoutError
## concurrent.futures._base.CancelledError

def main():
    args = PARSER.parse_args()
