import re
import unittest
import urllib.parse

import hypothesis
import hypothesis.strategies as st

from chandere2.uri import generate_uri

FAILING_BOARDS = ("", " ", "/")


class UrlGenerationTest(unittest.TestCase):
    ## TODO: Clean up. <jakob@memeware.net>
    @hypothesis.given(st.text())
    def test_bare_board(self, board):
        if board in FAILING_BOARDS:
            result = None
        elif "/" in board:
            return
        else:
            url = "a.4cdn.org/" + board.strip("/") + "/threads.json"
            result = urllib.parse.quote_plus(url, safe="/")
        self.assertEqual(generate_uri(board), result)

    ## TODO: Clean up. <jakob@memeware.net>
    @hypothesis.given(st.text(), st.integers(min_value=0))
    def test_thread_url(self, board, thread):
        if board == "" or "/" in board:
            return
        elif board in FAILING_BOARDS:
            result = None
        else:
            url = "a.4cdn.org/" + board.strip("/") + "/" + str(thread) + ".json"
            result = urllib.parse.quote_plus(url, safe="/")
        self.assertEqual(generate_uri(board + "/" + str(thread)), result)
