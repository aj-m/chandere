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

"""Scraper for 4chan.org"""

__author__ = "Jakob L. Kreuze <jakob@memeware.net>"
__licence__ = "GPLv3"
__version__ = "0.1.0"

from urllib.parse import quote
import re

import aiohttp

from chandere.errors import handle_anomalous_http_status

API_BASE = "https://a.4cdn.org"
RES_BASE = "https://i.4cdn.org"


def _catalog_url(board: str) -> str:
    return API_BASE + "/{}/catalog.json".format(quote(board))


def _thread_url(board: str, thread: str) -> str:
    return API_BASE + "/{}/thread/{}.json".format(board, thread)


def _file_url(board: str, tim: str, ext: str) -> str:
    return RES_BASE + "/{}/{}{}".format(board, tim, ext)


def _threads_from_page(page: dict) -> list:
    return [int(thread.get("no")) for thread in page.get("threads")]


def parse_target(target: str) -> tuple:
    target = quote(target, safe="/ ", errors="ignore").strip()

    match = re.search(r"(?<=\/)?[^\s\/]+(?=[\/ ])?", target)
    board = match.group() if match else None

    match = re.search(r"(?<=[^\s\/][\/ ])\d+(?=\/)?", target)
    thread = match.group() if match else None

    return (board, thread)


async def collect_threads(board: str) -> list:
    uri = _catalog_url(board)
    threads = []
    async with aiohttp.ClientSession() as session:
        async with session.get(uri) as response:
            handle_anomalous_http_status(response.status, uri)
            for page in await response.json():
                if "threads" not in page:
                    continue
                threads += _threads_from_page(board, page)
            return threads


async def collect_posts(board: str, thread: int) -> list:
    uri = _thread_url(board, thread)
    async with aiohttp.ClientSession() as session:
        async with session.get(uri) as response:
            handle_anomalous_http_status(response.status, uri)
            json = await response.json()
            return json.get("posts", [])


async def _collect_files_thread(board: str, thread: int):
    files = []
    for post in await collect_posts(board, thread):
        if "tim" in post and "filename" in post and "ext" in post:
            url = _file_url(board, post.get("tim"), post.get("ext"))
            files.append((post, url))
    return files


async def _collect_files_board(board: str):
    files = []
    for thread in await collect_threads(board):
        files += await _collect_files_thread(board, thread)
    return files


async def collect_files(board: str, thread=None) -> list:
    if thread is not None:
        return await _collect_files_thread(board, thread)
    return await _collect_files_board(board)
