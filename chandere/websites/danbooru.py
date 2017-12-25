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

"""Scraper for danbooru.donmai.us"""

__author__ = "Jakob L. Kreuze <jakob@memeware.net>"
__licence__ = "GPLv3"
__version__ = "0.1.0"

from dateutil.parser import parse
import itertools

import aiohttp

from chandere.errors import check_http_status

FIELD_NAMES = ["id", "time_posted", "name", "filename"]

API_BASE = "https://danbooru.donmai.us"


def _tidy_post_fields(post: dict):
    post["name"] = post.get("uploader_name")
    post["time_posted"] = int(parse(post.get("created_at")).timestamp())
    if "large_file_url" in post:
        url = post.get("large_file_url")
        post["filename"] = url[url.rindex("/") + 1:-4]
    if "file_ext" in post:
        post["ext"] = post.get("file_ext")

    del post["uploader_name"]


async def collect_files(target: str):
    async for post in collect_posts(target):
        if "large_file_url" in post:
            yield (post, API_BASE + post.get("large_file_url"))


async def collect_posts(target: str):
    uri = API_BASE + "/posts.json"
    params = {"tags": target}
    async with aiohttp.ClientSession() as session:
        for i in itertools.count():
            params["page"] = i
            async with session.get(uri, params=params) as response:
                check_http_status(response.status, uri)
                posts = await response.json()

                # Empty page - stop searching.
                if len(posts) == 0:
                    break

                for post in posts:
                    _tidy_post_fields(post)
                    yield post


def parse_target(target: str) -> str:
    return target.strip()
