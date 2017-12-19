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
import concurrent.futures

import aiohttp

from chandere.cli import PARSER
from chandere.errors import ChandereError, handle_anomalous_http_status
from chandere.util import load_custom_scraper, load_scraper


async def download_files(files: iter):
    async with aiohttp.ClientSession() as session:
        for filename, uri in files:
            async with session.get(uri) as response:
                handle_anomalous_http_status(response.status, uri)
                ## TODO: Perform chunked writing.
                with open(filename, "wb+") as out:
                    out.write(await response.read())


async def download_all_files(out: str, targets: list, scraper: object):
    files = []
    for board, thread in targets:
        files += await scraper.collect_files(board, thread)
    pairs = []
    for i, pair in enumerate(files):
        post, uri = pair
        template_data = post
        template_data["index"] = i + 1
        pairs.append((out.format(**template_data), uri))
    print("Queued {} downloads...".format(len(pairs)))
    await download_files(pairs)


def main():
    args = PARSER.parse_args()
    loop = asyncio.get_event_loop()

    try:
        if args.custom_scraper is not None:
            scraper = load_custom_scraper(args.custom_scraper)
        else:
            scraper = load_scraper(args.website)
        targets = [scraper.parse_target(target) for target in args.targets]

        loop.run_until_complete(download_all_files(args.output, targets, scraper))
    except concurrent.futures._base.CancelledError:
        pass
    except concurrent.futures._base.TimeoutError:
        pass
    except ChandereError as e:
        ## TODO: Better output.
        print("Critical error: {}".format(e))
    finally:
        loop.close()
