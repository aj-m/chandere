import re
import unittest
import urllib.parse

import hypothesis
import hypothesis.strategies as st

from chandere2.uri import (generate_uri, strip_target)


class GenerateUriTest(unittest.TestCase):
    @hypothesis.given(st.characters())
    def test_create_url_with_board(self, board):
        uri = generate_uri(board, "threads")
        self.assertIn(board, uri)
        self.assertIn("threads.json", uri)

    @hypothesis.given(st.characters(), st.integers(min_value=0))
    def test_create_url_with_thread(self, board, thread):
        uri = generate_uri(board, str(thread))
        self.assertIn(board + "/" + str(thread), uri)
        self.assertNotIn("threads.json", uri)

    def test_fail_on_unknown_imageboard(self):
        self.assertIs(generate_uri("/g/", "", imageboard="krautchan"), None)


class StripTargetTest(unittest.TestCase):
    @hypothesis.given(st.characters(blacklist_characters="/"))
    def test_strip_bare_board(self, target):
        expected_board = urllib.parse.quote(target.strip("/"), safe="/ ",
                                            errors="ignore")

        if not re.search(r"[^\s\/]", expected_board):
            expected_board = None

        self.assertEqual(strip_target(target), (expected_board, "threads"))

    @hypothesis.given(st.characters(blacklist_characters="/"),
                      st.integers(min_value=0))
    def test_strip_board_with_thread(self, target_board, target_thread):
        expected_thread = str(target_thread)
        expected_board = urllib.parse.quote(target_board.strip("/"),
                                            safe="/ ", errors="ignore")

        # If the given target lacks a valid board initial but a thread
        # is given, the subroutine will interpret the thread as a board.
        if not re.search(r"[^\s\/]", expected_board):
            expected_board = str(target_thread)
            expected_thread = "threads"

        target = "/".join((target_board, str(target_thread)))
        self.assertEqual(strip_target(target),
                         (expected_board, expected_thread))
