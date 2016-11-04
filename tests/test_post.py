import time
import types

import hypothesis
import hypothesis.strategies as st

from chandere2.context import CONTEXTS
from chandere2.post import (ascii_format_post, cache_posts, filter_posts,
                            find_files, get_images_default,
                            get_images_id_based, get_images_path_based,
                            get_image_uri, get_threads,
                            get_threads_from_catalog,
                            get_threads_from_endpoint, unescape)
from chandere2.validate import generate_uri


# Asserts that a list of thread URIs is returned.
@hypothesis.given(st.integers(min_value=0), st.text())
def test_get_threads_from_endpoint(thread, board):
    content = [{"page": 1, "threads": [{"no": thread}]}]

    # Hardcoded test for 4chan.
    threads = list(get_threads_from_endpoint(content, board, "4chan"))
    expected = [generate_uri(board, str(thread), "4chan")]
    assert threads == expected

    # Hardcoded test for 8chan.
    threads = list(get_threads_from_endpoint(content, board, "8chan"))
    expected = [generate_uri(board, str(thread), "8chan")]
    assert threads == expected

    # Hardcoded test for Lainchan.
    threads = list(get_threads_from_endpoint(content, board, "lainchan"))
    expected = [generate_uri(board, str(thread), "lainchan")]
    assert threads == expected


# Asserts that a list of thread URIs is returned.
@hypothesis.given(st.integers(min_value=0), st.text())
def test_get_threads_from_catalog(thread, board):
    content = [{"threadId": thread}]

    # Hardcoded test for Endchan.
    threads = list(get_threads_from_catalog(content, board, "endchan"))
    expected = [generate_uri(board, str(thread), "endchan")]
    assert threads == expected

    # Hardcoded test for Nextchan.
    content = [{"post_id": thread}]

    threads = list(get_threads_from_catalog(content, board, "nextchan"))
    expected = [generate_uri(board, str(thread), "nextchan")]
    assert threads == expected


# Asserts that a valid generator is returned.
@hypothesis.given(st.text())
def test_get_threads(board):
    for imageboard in CONTEXTS:
        generator = get_threads([], board, imageboard)
        assert isinstance(generator, types.GeneratorType)


class TestGetImagesDefault:
    # Asserts that images are properly parsed
    @hypothesis.given(st.text(), st.text(), st.integers())
    def test_get_images(self, filename, extension, tim):
        content = {"filename": filename, "ext": extension, "tim": str(tim)}
        parsed = [(filename + extension, str(tim) + extension)]

        # Hardcoded test for 4chan.
        assert list(get_images_default(content, "4chan")) == parsed

        # Hardcoded test for 8chan.
        assert list(get_images_default(content, "8chan")) == parsed

        # Hardcoded test for Lainchan.
        assert list(get_images_default(content, "lainchan")) == parsed

    # Asserts that multiple images can be parsed out of one post.
    @hypothesis.given(st.text(), st.text(), st.integers())
    def test_get_several_images(self, filename, extension, tim):
        content = {"filename": filename, "ext": extension, "tim": str(tim),
                   "extra_files": [{"filename": filename, "ext": extension,
                                    "tim": str(tim + 1)}]}
        parsed = [(filename + extension, str(tim) + extension),
                  (filename + extension, str(tim + 1) + extension)]

        # Hardcoded test for 4chan.
        assert list(get_images_default(content, "4chan")) == parsed

        # Hardcoded test for 8chan.
        assert list(get_images_default(content, "8chan")) == parsed

        # Hardcoded test for Lainchan.
        assert list(get_images_default(content, "lainchan")) == parsed


class TestGetImagesPathBased:
    # Asserts that images are properly parsed
    @hypothesis.given(st.text(), st.text())
    def test_get_images(self, filename, path):
        content = {"files": [{"originalName": filename, "path": path}]}
        parsed = [(filename, path[1:])]

        # Hardcoded test for Endchan.
        assert list(get_images_path_based(content, "endchan")) == parsed

    # Asserts that multiple images can be parsed out of one post.
    @hypothesis.given(st.text(), st.text())
    def test_get_several_images(self, filename, path):
        content = {"files": [{"originalName": filename, "path": path},
                             {"originalName": filename, "path": path}]}
        parsed = [(filename, path[1:]), (filename, path[1:])]

        # Hardcoded test for Endchan.
        assert list(get_images_path_based(content, "endchan")) == parsed


## TODO: Clean up. <jakob@memeware.net>
class TestGetImagesIdBased:
    # Asserts that images are properly parsed
    @hypothesis.given(st.text(), st.integers(), st.integers())
    def test_get_images(self, filename, file_id, post_id):
        content = {
            "post_id": post_id,
            "attachments": [
                {
                    "mime": "img\\/png",
                    "pivot": {
                        "filename": filename,
                        "file_id": file_id
                    }
                }
            ]
        }
        parsed = [(filename + ".png",
                   "%s/%d-%d.%s" % (file_id, post_id, 0, "png"))]

        # Hardcoded test for Nextchan.
        assert list(get_images_id_based(content, "nextchan")) == parsed


    # Asserts that multiple images can be parsed out of one post.
    @hypothesis.given(st.text(), st.integers(), st.integers())
    def test_get_several_images(self, filename, file_id, post_id):
        content = {
            "post_id": post_id,
            "attachments": [
                {
                    "mime": "img\\/png",
                    "pivot": {
                        "filename": filename,
                        "file_id": file_id
                    }
                },
                {
                    "mime": "img\\/png",
                    "pivot": {
                        "filename": filename,
                        "file_id": file_id
                    }
                }
            ]
        }

        parsed = [(filename + ".png",
                   "%s/%d-%d.%s" % (file_id, post_id, 0, "png")),
                  (filename + ".png",
                   "%s/%d-%d.%s" % (file_id, post_id, 1, "png"))]

        # Hardcoded test for Nextchan.
        assert list(get_images_id_based(content, "nextchan")) == parsed


# Asserts that a proper image URI is returned.
@hypothesis.given(st.text(), st.text(), st.text())
def test_get_image_uri(name, extension, board):
    filename = ".".join((name, extension))

    # Hardcoded test for 4chan.
    uri = get_image_uri(filename, board, "4chan")
    parsed = "/".join(("i.4cdn.org", board, filename))
    assert uri == parsed

    # Hardcoded test for 8chan.
    uri = get_image_uri(filename, board, "8chan")
    parsed = "/".join(("media.8ch.net/file_store", filename))
    assert uri == parsed

    # Hardcoded test for Lainchan.
    uri = get_image_uri(filename, board, "lainchan")
    parsed = "/".join(("lainchan.org", board, "src", filename))
    assert uri == parsed


# Asserts that files are properly extracted from a post.
@hypothesis.given(st.text(), st.text(), st.text(), st.integers())
def test_find_files(name, extension, board, tim):
    # Hardcoded example post for Vichan-styled imageboards.
    content = {"posts": [{"filename": name, "ext": extension, "tim": tim}]}

    # Hardcoded test for 4chan.
    found = list(get_images_default(content.get("posts")[0], "4chan"))
    if found:
        original_filename, server_filename = found[0]
        uri = get_image_uri(server_filename, board, "4chan")
        parsed = [(uri, original_filename)]
    else:
        parsed = []

    assert list(find_files(content, board, "4chan")) == parsed

    # Hardcoded test for 8chan.
    found = list(get_images_default(content.get("posts")[0], "8chan"))
    if found:
        original_filename, server_filename = found[0]
        uri = get_image_uri(server_filename, board, "8chan")
        parsed = [(uri, original_filename)]
    else:
        parsed = []

    assert list(find_files(content, board, "8chan")) == parsed

    # Hardcoded test for Lainchan.
    found = list(get_images_default(content.get("posts")[0], "lainchan"))
    if found:
        original_filename, server_filename = found[0]
        uri = get_image_uri(server_filename, board, "lainchan")
        parsed = [(uri, original_filename)]
    else:
        parsed = []

    assert list(find_files(content, board, "lainchan")) == parsed

    # Hardcoded example post for Lynxchan-styled imageboards.
    content = {"files": [{"originalName": name, "path": name}]}

    # Hardcoded test for Endchan.
    found = list(get_images_path_based(content, "endchan"))
    if found:
        original_filename, server_filename = found[0]
        uri = get_image_uri(server_filename, board, "endchan")
        parsed = [(uri, original_filename)]
    else:
        parsed = []

    assert list(find_files(content, board, "endchan")) == parsed

    # Hardcoded example post for Infinity Next styled imageboards.
    content = {
        "post_id": tim,
        "attachments": [
            {
                "mime": "img\\/png",
                "pivot": {
                    "filename": name,
                    "file_id": tim
                }
            }
        ]
    }

    # Hardcoded test for Nextchan.
    found = list(get_images_id_based(content, "nextchan"))
    if found:
        original_filename, server_filename = found[0]
        uri = get_image_uri(server_filename, board, "nextchan")
        parsed = [(uri, original_filename)]
    else:
        parsed = []

    assert list(find_files(content, board, "nextchan")) == parsed


class TestFilterPosts:
    # Asserts that the dictionary is untouched.
    @hypothesis.given(st.text(), st.text())
    def test_no_filters(self, field, value):
        content = {"posts": [{field: value}]}
        filter_posts(content, [])
        assert content == {"posts": [{field: value}]}

    # Asserts that the post is properly filtered.
    # Regex characters are blacklisted to prevent false negatives.
    @hypothesis.given(st.text(),
                      st.characters(blacklist_characters="*+?()[]|\\"))
    def test_match_filter(self, field, value):
        content = {"posts": [{field: value}]}
        filter_posts(content, [(field, value)])
        assert content == {"posts": []}


class TestCachePosts:
    # Asserts that the post ID is properly added to the cache.
    @hypothesis.given(st.integers())
    def test_cache_posts(self, first_id):
        # Hardcoded test for 4chan.
        cache = []
        content = {"posts": [{"no": first_id}]}

        cache_posts(content, cache, "4chan")
        assert content == {"posts": [{"no": first_id}]}
        assert cache == [first_id]

        # Hardcoded test for 8chan.
        cache = []
        content = {"posts": [{"no": first_id}]}

        cache_posts(content, cache, "8chan")
        assert content == {"posts": [{"no": first_id}]}
        assert cache == [first_id]

        # Hardcoded test for Lainchan.
        cache = []
        content = {"posts": [{"no": first_id}]}

        cache_posts(content, cache, "lainchan")
        assert content == {"posts": [{"no": first_id}]}
        assert cache == [first_id]

    @hypothesis.given(st.integers(), st.integers())
    def test_remove_cached_posts(self, first_id, second_id):
        if first_id == second_id:
            return

        # Hardcoded test for 4chan.
        cache = [first_id]
        content = {"posts": [{"no": first_id}, {"no": second_id}]}

        cache_posts(content, cache, "4chan")
        assert content == {"posts": [{"no": second_id}]}
        assert cache == [first_id, second_id]

        # Hardcoded test for 8chan.
        cache = [first_id]
        content = {"posts": [{"no": first_id}, {"no": second_id}]}

        cache_posts(content, cache, "8chan")
        assert content == {"posts": [{"no": second_id}]}
        assert cache == [first_id, second_id]

        # Hardcoded test for Lainchan.
        cache = [first_id]
        content = {"posts": [{"no": first_id}, {"no": second_id}]}

        cache_posts(content, cache, "lainchan")
        assert content == {"posts": [{"no": second_id}]}
        assert cache == [first_id, second_id]


## TODO: Write a test to cover all patterns. <jakob@memeware.net>
def test_unescape_text():
    text = "<p class=\"body-line empty \"></p>&amp;"
    assert unescape(text) == "\n\n&"


@hypothesis.given(st.integers(), st.text(), st.text(), st.text(), st.text(),
                  st.text(), st.text(),
                  st.integers(min_value=0, max_value=4294967295))
def test_format_post(no, name, trip, sub, com, filename, ext, date):
    # Hardcoded tests for vichan-styled imageboards.
    post = {"no": no, "time": date, "name": name, "trip": trip, "sub": sub,
            "com": com, "filename": filename, "ext": ext}
    formatted = ascii_format_post(post, "4chan")

    assert formatted == ascii_format_post(post, "8chan")
    assert formatted == ascii_format_post(post, "lainchan")
    assert "Post ID: %s" % no in formatted
    assert time.ctime(date) in formatted

    if name:
        assert unescape(name) in formatted or "Anonymous" in formatted
    if trip:
        assert "!%s" % trip in formatted
    if sub:
        assert unescape("\"%s\"" % sub) in formatted
    if filename and ext:
        assert filename + ext in formatted
