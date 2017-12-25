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

"""Archive posts to CSV format."""

__author__ = "Jakob L. Kreuze <jakob@memeware.net>"
__licence__ = "GPLv3"
__version__ = "0.1.0"

import argparse
import csv

import aiohttp

from chandere.cli import wrap
from chandere.errors import ChandereError, check_http_status

PARSER = argparse.ArgumentParser(add_help=False)
PARSER.add_argument(
    "-o",
    "--output",
    metavar="PATH",
    default="./posts.csv",
    help=wrap(
        "A template for output filenames. Defaults to './posts.csv'. See the "
        "manpage for specific details on usage."
    )
)
PARSER.add_argument(
    "--data-format",
    metavar="FMT",
    default="",
    help=wrap(
        "Document me!"
    )
)
PARSER.add_argument(
    "--no-header",
    action="store_true",
    help=wrap(
        "Document me!"
    )
)


def _parse_format_string(data_format: str):
    return data_format.split(",")


async def invoke(scraper: object, targets: list, argv: list):
    if not hasattr(scraper, "collect_posts"):
        msg = "'{}' module cannot collect posts.".format(scraper.__name__)
        raise ChandereError(msg)

    if not hasattr(scraper, "FIELD_NAMES"):
        msg = "'{}' module cannot serialize to csv.".format(scraper.__name__)
        raise ChandereError(msg)

    args, _ = PARSER.parse_known_args(argv)
    handles = {}

    if args.data_format == "":
        fields = scraper.FIELD_NAMES
    else:
        fields = _parse_format_string(args.data_format)

    for target in targets:
        async for post in scraper.collect_posts(target):
            out_path = args.output.format(**post)

            if out_path not in handles:
                handle = open(out_path, "w+", newline="")
                writer = csv.DictWriter(handle, fieldnames=fields,
                                        extrasaction="ignore")

                if not args.no_header:
                    writer.writeheader()

                handles[out_path] = (handle, writer)
            else:
                _, writer = handles.get(out_path)

            writer.writerow(post)

    for handle, _ in handles.values():
        handle.close()
