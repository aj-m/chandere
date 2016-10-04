## TODO: Improve tests. <jakob@memeware.net>

import asyncio
import unittest

import hypothesis
import hypothesis.strategies as st

from chandere2.handle_targets import (get_image_uri, get_images,
                                      get_threads, wrap_semaphore)


class GetImageURITest(unittest.TestCase):
    @hypothesis.given(st.characters(), st.characters(), st.characters())
    def test_get_image_uri(self, name, extension, board):
        filename = ".".join((name, extension))
        self.assertEqual(get_image_uri(filename, board, "4chan"),
                         "/".join(("i.4cdn.org", board, filename)))
        self.assertEqual(get_image_uri(filename, board, "8chan"),
                         "/".join(("media.8ch.net/file_store", filename)))
        self.assertEqual(get_image_uri(filename, board, "lainchan"),
                         "/".join(("lainchan.org", board, "src", filename)))


## TODO: Test contextual image fields. <jakob@memeware.net>
## TODO: Make the example posts less messy. There should be spaces
## following colons. <jakob@memeware.net>
class GetImagesTest(unittest.TestCase):
    def test_get_images(self):
        post = {"no":1392415, "filename":"triforce",
                "ext":".gif", "tim":1391831618569}
        images = [("triforce.gif", "1391831618569.gif")]

        self.assertEqual(get_images(post, "4chan"), images)

    def test_pass_on_no_images(self):
        post = {"no": 3537167}
        self.assertEqual(get_images(post, "4chan"), [])

    def test_get_multiple_images(self):
        post = {"filename":"example", "ext":".png", "tim":"1391831618569",
                "extra_files":[{"filename":"12826430", "ext":".png",
                                "tim":"1391831618570"}]}
        images = [("example.png", "1391831618569.png"),
                  ("12826430.png", "1391831618570.png")]

        self.assertEqual(get_images(post, "8chan"), images)


## TODO: Test contextual post fields. <jakob@memeware.net>
## TODO: Make the example posts less messy. There should be spaces
## following colons. <jakob@memeware.net>
## FIXME: Test does not accurately reflect behavior of subroutine.
## Fix this as more is developed. <jakob@memeware.net>
class ScrapePostTest(unittest.TestCase):
    def test_scrape_post(self):
        post = {"no":1392415, "time":1, "name":"Anonymous", "trip":"",
                "sub": "", "com": "", "filename": "", "ext": ""}
        scraped = (1392415, 1, "Anonymous", "", "", "", "", "")



class GetThreadsTest(unittest.TestCase):
    def test_get_threads(self):
        content = [{"threads":[{"no":589254,"last_modified":1473600302}]}]
        self.assertEqual(list(get_threads(content, "g", "4chan")),
                         ["a.4cdn.org/g/thread/589254.json"])


class WrapSemaphoreTest(unittest.TestCase):
    def test_wrap_semaphore(self):
        async def dummy_coroutine():
            pass

        semaphore = asyncio.Semaphore(1)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(wrap_semaphore(dummy_coroutine(), semaphore))
