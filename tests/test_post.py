import asyncio
import time
import unittest

import hypothesis
import hypothesis.strategies as st

from chandere2.post import (ascii_format_post, get_images,
                            get_image_uri, get_threads)
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

    ## TODO: Write this. <jakob@memeware.net>
    def test_get_multiple_images(self):
        pass


class AsciiFormatPostTest(unittest.TestCase):
    ## TODO: Clean up. <jakob@memeware.net>
    @hypothesis.given(st.integers(),
                      st.integers(min_value=0, max_value=4294967295),
                      st.text(), st.text(), st.text(), st.text(), st.text(),
                      st.text())
    def test_format_post(self, no, date, name, trip, sub, com, filename, ext):
        # Hardcoded test for 4chan, 8chan, and Lainchan.
        post = {"no": no, "time": date, "name": name, "trip": trip, "sub": sub,
                "com": com, "filename": filename, "ext": ext}
        formatted = ascii_format_post(post, "4chan")
        self.assertIn("Post: %s" % no, formatted)
        self.assertIn(time.ctime(date), formatted)
        if name:
            self.assertIn(name, formatted)
        if trip:
            self.assertIn("!%s" % trip, formatted)
        if sub:
            self.assertIn("\"%s\"" % sub, formatted)
        if filename and ext:
            self.assertIn(".".join((filename, ext)), formatted)
