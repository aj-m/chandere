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

"""Download every file present."""

__author__ = "Jakob L. Kreuze <jakob@memeware.net>"
__licence__ = "GPLv3"
__version__ = "0.1.0"

import argparse

import aiohttp

from chandere import output
from chandere.errors import check_http_status

PARSER = argparse.ArgumentParser(
    add_help=False,
)

PARSER.add_argument(
    "-t",
    "--test",
    help="Test argument."
)


async def download_files(files: iter):
    async with aiohttp.ClientSession() as session:
        for filename, uri in files:
            async with session.get(uri) as response:
                check_http_status(response.status, uri)
                ## TODO: Perform chunked writing.
                with open(filename, "wb+") as out:
                    out.write(await response.read())


async def invoke(scraper: object, targets: list, out: str, argv: list):
    args, _ = PARSER.parse_known_args(argv)
    print(args)
    return

    files = []
    for board, thread in targets:
        files += await scraper.collect_files(board, thread)
    pairs = []
    for i, pair in enumerate(files):
        post, uri = pair
        template_data = post
        template_data["index"] = i + 1
        pairs.append((out.format(**template_data), uri))
    output.info("Queued {} downloads...".format(len(pairs)))
    await download_files(pairs)
