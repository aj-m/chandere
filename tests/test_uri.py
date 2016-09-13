import re
import unittest
import urllib.parse

import hypothesis
import hypothesis.strategies as st

from chandere2.uri import (generate_uri, strip_target)


class UriGenerationTest(unittest.TestCase):
    @hypothesis.given(st.characters())
    def test_bare_board(self, board, thread):
        uri = generate_uri(board, str(thread))
        self.assertIn("%s" % board, uri)
        self.assertIn("threads.json", uri)

    @hypothesis.given(st.characters(), st.integers(min_value=0))
    def test_bare_board(self, board, thread):
        uri = generate_uri(board, str(thread))
        self.assertIn("%s/%d" % (board, thread), uri)
        self.assertNotIn("threads.json", uri)

    def test_fail_unknown_imageboard(self):
        self.assertIs(generate_uri("/g/", "", imageboard="krautchan"), None)


class TargetStrippingTest(unittest.TestCase):
    @hypothesis.given(st.characters(blacklist_characters="/"))
    def test_bare_board(self, target):
        # Certain unicode characters, when encoded and decoded will
        # become an empty string. The following is done to handle that.
        expected_board = target.encode(errors="ignore").decode()
        expected_board = urllib.parse.quote(target.strip("/"), safe="/ ",
                                            errors="ignore")
        if not re.search(r"[^\s\/]", expected_board):
            expected_board = None

        self.assertEqual(strip_target(target), (expected_board, "threads"))

    ## TODO: Clean up. <jakob@memeware.net>
    @hypothesis.given(st.characters(blacklist_characters="/"),
                      st.integers(min_value=0))
    def test_board_with_thread(self, target_board, target_thread):
        # Certain unicode characters, when encoded and decoded will
        # become an empty string. The following is done to handle that.
        expected_thread = str(target_thread)
        expected_board = target_board.encode(errors="ignore").decode()
        expected_board = urllib.parse.quote(target_board.strip("/"), safe="/ ",
                                            errors="ignore")
        if not re.search(r"[^\s\/]", expected_board):
            expected_board = None
            expected_thread = "threads"

        target = "/".join((target_board, str(target_thread)))
        self.assertEqual(strip_target(target),
                         (expected_board, expected_thread))
