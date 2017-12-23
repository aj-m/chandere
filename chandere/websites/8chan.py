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

"""Scraper for 8ch.net"""

__author__ = "Jakob L. Kreuze <jakob@memeware.net>"
__licence__ = "GPLv3"
__version__ = "0.1.0"

from urllib.parse import quote
import re

import aiohttp

from chandere.errors import check_http_status

API_BASE = "https://8ch.net"
RES_BASE = "https://media.8ch.net"


def _catalog_url(board: str) -> str:
    return API_BASE + "/{}/catalog.json".format(quote(board))


def _thread_url(board: str, thread: str) -> str:
    return API_BASE + "/{}/res/{}.json".format(board, thread)


def _file_url(board: str, tim: str, ext: str) -> str:
    if len(tim) == 64:
        return RES_BASE + "/file_store/{}{}".format(tim, ext)
    return RES_BASE + "/{}/src/{}{}".format(board, tim, ext)


def _threads_from_page(page: dict) -> list:
    return [int(thread.get("no")) for thread in page.get("threads")]


async def _collect_threads(board: str):
    uri = _catalog_url(board)
    async with aiohttp.ClientSession() as session:
        async with session.get(uri) as response:
            check_http_status(response.status, uri)
            for page in await response.json():
                if "threads" not in page:
                    continue
                for thread in _threads_from_page(page):
                    yield thread


async def _collect_files_thread(board: str, thread: int):
    async for post in _collect_posts(board, thread):
        if "tim" in post and "filename" in post and "ext" in post:
            url = _file_url(board, post.get("tim"), post.get("ext"))
            yield (post, url)
        for extra in post.get("extra_files", []):
            url = _file_url(board, extra.get("tim"), extra.get("ext"))
            new_post = post.copy()
            new_post["filename"] = extra.get("filename")
            yield (new_post, url)


async def _collect_files_board(board: str):
    async for thread in _collect_threads(board):
        yield await _collect_files_thread(board, thread)


async def _collect_posts(board: str, thread: str):
    uri = _thread_url(board, thread)
    async with aiohttp.ClientSession() as session:
        async with session.get(uri) as response:
            check_http_status(response.status, uri)
            json = await response.json()
            for post in json.get("posts", []):
                yield post


def collect_files(target: str):
    board, thread = target
    if thread is not None:
        return _collect_files_thread(board, thread)
    return _collect_files_board(board)


def collect_posts(target: str):
    board, thread = target
    return _collect_posts(board, thread)


def parse_target(target: str) -> tuple:
    target = quote(target, safe="/ ", errors="ignore").strip()

    match = re.search(r"(?<=\/)?[^\s\/]+(?=[\/ ])?", target)
    board = match.group() if match else None

    match = re.search(r"(?<=[^\s\/][\/ ])\d+(?=\/)?", target)
    thread = match.group() if match else None

    return (board, thread)
