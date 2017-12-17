"""[Document me!]"""

import async_timeout
from urllib.parse import quote

import aiohttp

from chandere.errors import handle_anomalous_http_status

URI_BASE = "https://a.4cdn.org"


class Scraper:
    @staticmethod
    def _catalog_url(board: str) -> str:
        return URI_BASE + "/{}/catalog.json".format(quote(board))

    @staticmethod
    def _thread_url(board: str, thread: str) -> str:
        return URI_BASE + "/{}/thread/{}.json".format(board, thread)

    @staticmethod
    def _image_url(board: str, tim: str, ext: str) -> str:
        return URI_BASE + "/{}/{}{}".format(board, tim, ext)

    @staticmethod
    def _get_threads_from_page(page: dict) -> list:
        return [int(thread.get("no")) for thread in page.get("threads")]

    @staticmethod
    async def collect_threads(board: str):
        uri = Scraper._catalog_url(board)
        threads = []
        async with aiohttp.ClientSession() as session:
            async with session.get(uri) as response:
                handle_anomalous_http_status(response.status)
                for page in await response.json():
                    if "threads" not in page:
                        continue
                    threads += Scraper._get_threads_from_page(board, page)
                return threads

    @staticmethod
    async def collect_posts(board: str, thread: int):
        uri = Scraper._thread_url(board, thread)
        async with aiohttp.ClientSession() as session:
            async with session.get(uri) as response:
                handle_anomalous_http_status(response.status)
                json = await response.json()
                return json.get("posts", [])

    @staticmethod
    async def _collect_images_thread(board: str, thread: int):
        images = []
        for post in await Scraper.collect_posts(board, thread):
            if "tim" in post and "filename" in post and "ext" in post:
                filename = post.get("filename") + post.get("ext")
                url = Scraper._image_url(board, post.get("tim"), post.get("ext"))
                images.append((filename, url))
        return images

    @staticmethod
    async def _collect_images_board(board: str):
        images = []
        for thread in await Scraper.collect_threads(board):
            images += await Scraper._collect_images_thread(board, thread)
        return images

    @staticmethod
    async def collect_images(board: str, thread=None):
        if thread is not None:
            return await Scraper._collect_images_thread(board, thread)
        return await Scraper._collect_images_board(board)
