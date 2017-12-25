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

"""Scraper for dangeru.us"""

__author__ = "Jakob L. Kreuze <jakob@memeware.net>"
__licence__ = "GPLv3"
__version__ = "0.1.0"

import itertools

import aiohttp

from chandere.errors import ChandereError, check_http_status
from chandere.websites._common import contains_uri_scheme, parse_crosslink
from chandere.websites._common import parse_imageboard_uri_factory

FIELD_NAMES = ["no", "time", "hash", "com", "filename"]

API_BASE = "https://dangeru.us/api/v2"

parse_uri = parse_imageboard_uri_factory("us", "thread")


def _catalog_url(board: str) -> str:
    return API_BASE + "/board/{}".format(board)


def _thread_url(thread: str) -> str:
    return API_BASE + "/thread/{}/replies".format(thread)


def _tidy_post_fields(post: dict):
    post["no"] = post.get("post_id")
    post["com"] = post.get("comment")
    post["time"] = post.get("date_posted")


async def _collect_posts_thread(board: str, thread: str):
    async with aiohttp.ClientSession() as session:
        uri = _thread_url(thread)
        async with session.get(uri) as response:
            check_http_status(response.status, uri)
            for post in await response.json():
                _tidy_post_fields(post)
                yield post


async def _collect_posts_board(board: str):
    async with aiohttp.ClientSession() as session:
        for i in itertools.count():
            params = {"page": i}
            async with session.get(uri, params=params) as response:
                threads = response.json()

                # Empty page - stop searching.
                if len(threads) == 0:
                    break

                async for post in _thread_foreach(threads):
                    yield post


async def _thread_foreach(threads: list):
    for thread in threads:
        async for post in _collect_posts_thread(board, thread.get("post_id")):
            yield post


def collect_posts(target: tuple):
    board, thread = target
    if thread is None:
        return _collect_posts_board(board)
    return _collect_posts_thread(board, thread)


def parse_target(target: str) -> tuple:
    parse = parse_uri if contains_uri_scheme(target) else parse_crosslink
    board, thread = parse(target)
    if board is None:
        raise ChandereError("Invalid target '{}'".format(target))
    return (board, thread)
