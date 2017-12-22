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

from chandere.cli import wrap
from chandere.errors import ChandereError, check_http_status

PARSER = argparse.ArgumentParser(add_help=False)
PARSER.add_argument(
    "-o",
    "--output",
    metavar="DIR",
    default="./{filename}.{ext}",
    help=wrap(
        "A template for output filenames. Defaults to './{filename}.{ext}', "
        "which preserves the original filename and saves it to the current "
        "working directory. See the manpage for specific details on usage."
    )
)


async def _download_file(uri: str, out_path: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(uri) as response:
            check_http_status(response.status, uri)
            # TODO: Perform chunked writing.;
            with open(out_path, "wb+") as out:
                out.write(await response.read())


def _tidy_post_fields(post: dict, seq_index: int):
    if "ext" in post and post["ext"][0] == ".":
        post["ext"] = post["ext"][1:]
    post["index"] = seq_index


async def invoke(scraper: object, targets: list, argv: list):
    if not hasattr(scraper, "collect_files"):
        msg = "'{}' module cannot collect files.".format(scraper.__name__)
        raise ChandereError(msg)

    args, _ = PARSER.parse_known_args(argv)
    seq_index = 1

    for target in targets:
        async for parsed_file in scraper.collect_files(target):
            post, uri = parsed_file
            _tidy_post_fields(post, seq_index)
            out_path = args.output.format(**post)
            seq_index += 1
            await _download_file(uri, out_path)
