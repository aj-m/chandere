import re
import unittest
import urllib.parse

import hypothesis
import hypothesis.strategies as st

from chandere2.connection import generate_uri


class UrlGenerationTest(unittest.TestCase):
    @hypothesis.given(st.characters(blacklist_characters="0123456789/"))
    def test_bare_board(self, board):
        # Certain unicode characters, when encoded and decoded will
        # become an empty string. The following is done to handle that.
        expected_board = board.encode(errors="ignore").decode()
        expected_board = urllib.parse.quote(board.strip("/"), safe="/ ",
                                            errors="ignore")
        if not re.search(r"[^\s\/]", expected_board):
            expected_result = None
        else:
            expected_result = "a.4cdn.org/%s/threads.json" % expected_board

        self.assertEqual(generate_uri(board), expected_result)

    @hypothesis.given(st.characters(blacklist_characters="0123456789/"),
                      st.integers(min_value=0))
    def test_thread_url(self, board, thread):
        expected_board = board.encode(errors="ignore").decode()
        expected_board = urllib.parse.quote(board.strip("/"), safe="/ ",
                                            errors="ignore")

        # When an empty string and thread number are combined and separated
        # by a forward slash, the function will interpret that as just a
        # board, rather than a board and a thread.
        if expected_board == "":
            expected_result = "a.4cdn.org/%d/threads.json" % thread
        elif not re.search(r"[^\s\/]", expected_board):
            expected_result = None
        else:
            expected_result = "a.4cdn.org/%s/%d.json" % (expected_board,
                                                         thread)

        self.assertEqual(generate_uri("%s/%d" % (board, thread)),
                         expected_result)

    def test_fail_unknown_imageboard(self):
        self.assertIs(generate_uri("/g/", imageboard="krautchan"), None)
