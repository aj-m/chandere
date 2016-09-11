import re
import unittest
import urllib.parse

import hypothesis
import hypothesis.strategies as st

from chandere2.connection import (generate_uri, test_connection, thread_in_uri)
from chandere2.output import Console

from tests.dummy_objects import FakeOutput


## TODO: Clean up test. <jakob@memeware.net>
class TestConnectionTest(unittest.TestCase):
    def setUp(self):
        self.fake_stdout = FakeOutput()
        self.fake_stderr = FakeOutput()
        self.fake_output = Console(output=self.fake_stdout,
                                   error=self.fake_stderr)
    
    def test_successful_connection(self):
        test_connection(["a.4cdn.org/g/threads.json"], False, self.fake_output)
        self.assertEqual(self.fake_stdout.last_received[0][0], ">")

    def test_failed_connection(self):
        test_connection(["a.4cdn.org/z/threads.json"], False, self.fake_output)
        self.assertEqual(self.fake_stderr.last_received[0][7:14], "FAILED:")


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
        if expected_board.strip() == "":
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


class ThreadCheckingTest(unittest.TestCase):
    def test_thread_in_uri(self):
        self.assertTrue(thread_in_uri("a.4cdn.org/b/12345678.json"))
        self.assertFalse(thread_in_uri("a.4cdn.org/b/threads.json"))
