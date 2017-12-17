"""Entry point for the command-line interface to Chandere."""

import asyncio
import concurrent.futures
import importlib
import os
import re
from urllib.parse import quote

import aiohttp

from chandere.cli import PARSER
from chandere.errors import ChandereException, handle_anomalous_http_status


def get_scraper(website: str) -> object:
    module_name = "chandere.websites.{}".format(website)
    return importlib.import_module(module_name).Scraper


def strip_target(target: str) -> tuple:
    """Uses regular expressions to strip the given target string for a
    board initial and, if found, a thread number. None will be returned
    as the thread if there wasn't one in the target string, and None
    will be returned as the board if the string was invalid.
    """
    # The target should be quoted and stripped prior to further
    # handing, as Python has difficulty with some Unicode.
    target = quote(target, safe="/ ", errors="ignore").strip()

    # The regular expression pattern matches a sequence of
    # characters not containing whitespace or a forward slash,
    # optionally preceded and succeeded by a forward slash.
    match = re.search(r"(?<=\/)?[^\s\/]+(?=[\/ ])?", target)
    board = match.group() if match else None

    # The regular expression pattern matches a sequence of digits
    # preceded by something that might look like a board and a
    # forward slash or space character, optionally succeeded by a
    # forward slash.
    match = re.search(r"(?<=[^\s\/][\/ ])\d+(?=\/)?", target)
    thread = match.group() if match else None

    return (board, thread)


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
        scraper.tidy_post_fields(template_data)
        pairs.append((out.format(**template_data), uri))
    print("Queued {} downloads...".format(len(pairs)))
    await download_files(pairs)


def main():
    args = PARSER.parse_args()
    scraper = get_scraper(args.website)
    targets = [strip_target(target) for target in args.targets]
    ## IDEA: strip_target in each website class.

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_all_files(args.output, targets, scraper))
    except concurrent.futures._base.CancelledError:
        pass
    except concurrent.futures._base.TimeoutError:
        pass
    except ChandereException as e:
        ## TODO: Better output.
        print("Critical error: {}".format(e))
    finally:
        loop.close()
