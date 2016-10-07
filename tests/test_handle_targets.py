import asyncio
import unittest

import hypothesis
import hypothesis.strategies as st

from chandere2.handle_targets import (get_images, get_image_uri,
                                      get_threads, wrap_semaphore)
from chandere2.validate_input import generate_uri


class GetImageURITest(unittest.TestCase):
    @hypothesis.given(st.text(), st.text(), st.text())
    def test_get_image_uri(self, name, extension, board):
        filename = ".".join((name, extension))

        # Hardcoded test for 4chan.
        self.assertEqual(get_image_uri(filename, board, "4chan"),
                         "/".join(("i.4cdn.org", board, filename)))

        # Hardcoded test for 8chan.
        self.assertEqual(get_image_uri(filename, board, "8chan"),
                         "/".join(("media.8ch.net/file_store", filename)))

        # Hardcoded test for Lainchan.
        self.assertEqual(get_image_uri(filename, board, "lainchan"),
                         "/".join(("lainchan.org", board, "src", filename)))


## TODO: Does not test for the existence of a semaphore. <jakob@memeware.net>
class WrapSemaphoreTest(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_wrap_semaphore(self):
        async def dummy_coroutine():
            return True

        semaphore = asyncio.Semaphore(1)
        coroutine = wrap_semaphore(dummy_coroutine(), semaphore)
        self.assertTrue(self.loop.run_until_complete(coroutine))


## TODO: Test for contextual scraping. <jakob@memeware.net>
class GetThreadsTest(unittest.TestCase):
    @hypothesis.given(st.integers(min_value=0), st.text())
    def test_get_threads(self, thread, board):
        content = [{"page": 1, "threads": [{"no": thread}]}]

        # Hardcoded test for 4chan.
        self.assertEqual(list(get_threads(content, board, "4chan")),
                         [generate_uri(board, str(thread), "4chan")])

        # Hardcoded test for 8chan.
        self.assertEqual(list(get_threads(content, board, "8chan")),
                         [generate_uri(board, str(thread), "8chan")])

        # Hardcoded test for Lainchan.
        self.assertEqual(list(get_threads(content, board, "lainchan")),
                         [generate_uri(board, str(thread), "lainchan")])


## TODO: Test for contextual scraping. <jakob@memeware.net>
class GetImagesTest(unittest.TestCase):
    def test_get_images(self):
        # Hardcoded test for 4chan.
        content = {"filename": "RMS", "ext": ".png", "tim": "1462739442146"}
        self.assertEqual(get_images(content, "4chan"),
                         [("RMS.png", "1462739442146.png")])
        
        # Hardcoded test for 8chan.
        content = {"filename": "RMS", "ext": ".png", "tim": "1462739442146"}
        self.assertEqual(get_images(content, "8chan"),
                         [("RMS.png", "1462739442146.png")])

        # Hardcoded test for Lainchan.
        content = {"filename": "RMS", "ext": ".png", "tim": "1462739442146"}
        self.assertEqual(get_images(content, "lainchan"),
                         [("RMS.png", "1462739442146.png")])
