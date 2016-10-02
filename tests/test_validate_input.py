import os
import re
import unittest
import urllib.parse

import hypothesis
import hypothesis.strategies as st

from chandere2.validate_input import (generate_uri, get_path, strip_target)


class GenerateUriTest(unittest.TestCase):
    @hypothesis.given(st.characters())
    def test_create_url_with_board(self, board):
        uri = generate_uri(board, None)
        self.assertIn(board, uri)
        self.assertIn("threads.json", uri)

    @hypothesis.given(st.characters(), st.integers(min_value=0))
    def test_create_url_with_thread(self, board, thread):
        uri = generate_uri(board, str(thread))
        self.assertIn("/".join((board, "thread", str(thread))), uri)
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

        self.assertEqual(strip_target(target), (expected_board, None))

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
            expected_thread = None

        target = "/".join((target_board, str(target_thread)))
        self.assertEqual(strip_target(target),
                         (expected_board, expected_thread))


class GetPathTest(unittest.TestCase):
    # Expected permissions for the root directory and the CWD are not
    # hardcoded, as the permissions may vary on other machines.
    def test_check_output_permissions(self):
        self.assertEqual(os.access("/", os.W_OK), bool(get_path("/", "", "")))
        self.assertEqual(os.access(".", os.W_OK), bool(get_path(".", "", "")))
        self.assertEqual(os.access("/etc/hosts", os.W_OK),
                         bool(get_path("/etc/hosts", "", "")))

    # The following tests, however, assume that the CWD is writeable.
    def test_directory_for_file_downloading(self):
        self.assertEqual(get_path(".", "fd", ""), ".")
        self.assertIs(get_path("./a_file.txt", "fd", ""), None)

    def test_file_for_thread_archiving(self):
        self.assertEqual(get_path(".", "ar", "sqlite3"), "./archive.db")
        self.assertEqual(get_path("./file.txt", "ar", ""), "./file.txt")
        self.assertEqual(get_path(".", "ar", ""), "./archive.txt")
