import time
import unittest

import hypothesis
import hypothesis.strategies as st

from chandere2.post import (ascii_format_post, filter_posts, find_files,
                            get_images, get_image_uri, get_threads, unescape)
from chandere2.validate import generate_uri


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
    @hypothesis.given(st.text(), st.text(), st.integers())
    def test_get_images(self, filename, extension, tim):
        content = {"filename": filename, "ext": extension, "tim": str(tim)}
        parsed = [(filename + extension, str(tim) + extension)]

        # Hardcoded test for 4chan.
        self.assertEqual(get_images(content, "4chan"), parsed)

        # Hardcoded test for 8chan.
        self.assertEqual(get_images(content, "8chan"), parsed)

        # Hardcoded test for Lainchan.
        self.assertEqual(get_images(content, "lainchan"), parsed)

    @hypothesis.given(st.text(), st.text(), st.integers())
    def test_get_several_images(self, filename, extension, tim):
        content = {"filename": filename, "ext": extension, "tim": str(tim),
                   "extra_files": [{"filename": filename, "ext": extension,
                                    "tim": str(tim + 1)}]}
        parsed = [(filename + extension, str(tim) + extension),
                  (filename + extension, str(tim + 1) + extension)]

        # Hardcoded test for 4chan.
        self.assertEqual(get_images(content, "4chan"), parsed)

        # Hardcoded test for 8chan.
        self.assertEqual(get_images(content, "8chan"), parsed)

        # Hardcoded test for Lainchan.
        self.assertEqual(get_images(content, "lainchan"), parsed)


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


class FindFilesTest(unittest.TestCase):
    @hypothesis.given(st.text(), st.text(), st.text(), st.integers())
    def test_find_files(self, name, extension, board, tim):
        content = {"posts": [{"filename": name, "ext": extension, "tim": tim}]}

        # Hardcoded test for 4chan.
        found = list(get_images(content.get("posts")[0], "4chan"))
        if found:
            original_filename, server_filename = found[0]
            uri = get_image_uri(server_filename, board, "4chan")
            parsed = [(uri, original_filename)]
        else:
            parsed = []
        self.assertEqual(list(find_files(content, board, "4chan")), parsed)

        # Hardcoded test for 8chan.
        found = list(get_images(content.get("posts")[0], "4chan"))
        if found:
            original_filename, server_filename = found[0]
            uri = get_image_uri(server_filename, board, "8chan")
            parsed = [(uri, original_filename)]
        else:
            parsed = []
        self.assertEqual(list(find_files(content, board, "8chan")), parsed)

        # Hardcoded test for Lainchan.
        found = list(get_images(content.get("posts")[0], "4chan"))
        if found:
            original_filename, server_filename = found[0]
            uri = get_image_uri(server_filename, board, "lainchan")
            parsed = [(uri, original_filename)]
        else:
            parsed = []
        self.assertEqual(list(find_files(content, board, "lainchan")), parsed)


class FilterPostsTest(unittest.TestCase):
    @hypothesis.given(st.text(), st.text())
    def test_no_filters(self, field, value):
        content = {"posts": [{field: value}]}
        filter_posts(content, [])
        self.assertEqual(content, {"posts": [{field: value}]})

    # Regex characters are blacklisted to prevent false-negatives.
    @hypothesis.given(
        st.text(),
        st.characters(blacklist_characters="*+?()[]|")
    )
    def test_match_filter(self, field, value):
        content = {"posts": [{field: value}]}
        filter_posts(content, [(field, value)])
        self.assertEqual(content, {"posts": []})


## TODO: Join substitutions rather than cherrypick. <jakob@memeware.net>
class UnescapeTest(unittest.TestCase):
    def test_unescape_text(self):
        text = "<p class=\"body-line empty \"></p>&amp;"
        self.assertEqual(unescape(text), "\n\n&")


class AsciiFormatPostTest(unittest.TestCase):
    @hypothesis.given(
        st.integers(),
        st.integers(min_value=0, max_value=4294967295),
        st.text(),
        st.text(),
        st.text(),
        st.text(),
        st.text(),
        st.text()
    )
    def test_format_post(self, no, date, name, trip, sub, com, filename, ext):
        # Hardcoded test for Vichan styled-imageboards.
        post = {"no": no, "time": date, "name": name, "trip": trip, "sub": sub,
                "com": com, "filename": filename, "ext": ext}
        formatted = ascii_format_post(post, "4chan")

        self.assertEqual(formatted, ascii_format_post(post, "8chan"))
        self.assertEqual(formatted, ascii_format_post(post, "lainchan"))
        self.assertIn("Post ID: %s" % no, formatted)
        self.assertIn(time.ctime(date), formatted)

        if name:
            self.assertIn(name, formatted)
        if trip:
            self.assertIn("!%s" % trip, formatted)
        if sub:
            self.assertIn("\"%s\"" % sub, formatted)
        if filename and ext:
            self.assertIn(filename + ext, formatted)
