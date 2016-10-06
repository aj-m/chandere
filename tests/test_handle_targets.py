import asyncio
import unittest

import hypothesis
import hypothesis.strategies as st

from chandere2.handle_targets import (get_images, get_image_uri,
                                      get_threads, wrap_semaphore)


class GetImageURITest(unittest.TestCase):
    @hypothesis.given(st.characters(), st.characters(), st.characters())
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


## TODO: Does not test for the existence of a semaphore.
class WrapSemaphoreTest(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_wrap_semaphore(self):
        async def dummy_coroutine():
            return True

        semaphore = asyncio.Semaphore(1)
        coroutine = wrap_semaphore(dummy_coroutine(), semaphore)
        self.assertTrue(self.loop.run_until_complete(coroutine))
