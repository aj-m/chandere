# Copyright (C) 2017 Jakob Kreuze, All Rights Reserved.
#
# This file is part of Chandere.
#
# Chandere is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Chandere is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with Chandere. If not, see <http://www.gnu.org/licenses/>.

"""Entry point for the command-line interface to Chandere."""

import asyncio
import sys

from chandere import output
from chandere.cli import PARSER, reorder_args
from chandere.errors import ChandereError
from chandere.loader import load_action, load_custom_action
from chandere.loader import load_custom_scraper, load_scraper


def main():
    # There are a handful of code paths that aren't called from this
    # entry routine. See `cli.py` for routines such as --list-actions
    args, _ = PARSER.parse_known_args(reorder_args(sys.argv[1:]))
    loop = asyncio.get_event_loop()

    try:
        if args.custom_action is not None:
            action = load_custom_action(args.custom_action)
        else:
            action = load_action(args.action)

        if args.custom_scraper is not None:
            scraper = load_custom_scraper(args.custom_scraper)
        else:
            scraper = load_scraper(args.website)

        if not hasattr(scraper, "parse_target"):
            raise ChandereError("Scraper module lacks a target parser.")

        targets = [scraper.parse_target(target) for target in args.targets]
        loop.run_until_complete(action.invoke(scraper, targets, sys.argv))

    except ChandereError as e:
        output.error(str(e))
        sys.exit(1)

    except KeyboardInterrupt:
        pass

    finally:
        loop.close()
