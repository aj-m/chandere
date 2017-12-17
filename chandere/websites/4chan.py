"""Scraper for 4chan.org"""

import async_timeout
from urllib.parse import quote

import aiohttp

from chandere.errors import handle_anomalous_http_status

API_BASE = "https://a.4cdn.org"
RES_BASE = "https://i.4cdn.org"


class Scraper:
    @staticmethod
    def _catalog_url(board: str) -> str:
        return API_BASE + "/{}/catalog.json".format(quote(board))

    @staticmethod
    def _thread_url(board: str, thread: str) -> str:
        return API_BASE + "/{}/thread/{}.json".format(board, thread)

    @staticmethod
    def _file_url(board: str, tim: str, ext: str) -> str:
        return RES_BASE + "/{}/{}{}".format(board, tim, ext)

    @staticmethod
    def _threads_from_page(page: dict) -> list:
        return [int(thread.get("no")) for thread in page.get("threads")]

    @staticmethod
    def tidy_post_fields(post: dict):
        if "ext" in post:
            post["ext"] = post["ext"][1:]

    @staticmethod
    async def collect_threads(board: str) -> list:
        uri = Scraper._catalog_url(board)
        threads = []
        async with aiohttp.ClientSession() as session:
            async with session.get(uri) as response:
                handle_anomalous_http_status(response.status, uri)
                for page in await response.json():
                    if "threads" not in page:
                        continue
                    threads += Scraper._threads_from_page(board, page)
                return threads

    @staticmethod
    async def collect_posts(board: str, thread: int) -> list:
        uri = Scraper._thread_url(board, thread)
        async with aiohttp.ClientSession() as session:
            async with session.get(uri) as response:
                handle_anomalous_http_status(response.status, uri)
                json = await response.json()
                return json.get("posts", [])

    @staticmethod
    async def _collect_files_thread(board: str, thread: int):
        files = []
        for post in await Scraper.collect_posts(board, thread):
            if "tim" in post and "filename" in post and "ext" in post:
                url = Scraper._file_url(board, post.get("tim"), post.get("ext"))
                files.append((post, url))
        return files

    @staticmethod
    async def _collect_files_board(board: str):
        files = []
        for thread in await Scraper.collect_threads(board):
            files += await Scraper._collect_files_thread(board, thread)
        return files

    @staticmethod
    async def collect_files(board: str, thread=None) -> list:
        if thread is not None:
            return await Scraper._collect_files_thread(board, thread)
        return await Scraper._collect_files_board(board)
