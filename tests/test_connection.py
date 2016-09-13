import unittest

import hypothesis
import hypothesis.strategies as st

from chandere2.connection import test_connection
from chandere2.output import Console

from tests.dummy_objects import FakeOutput


class TestConnectionTest(unittest.TestCase):
    def setUp(self):
        self.fake_stdout = FakeOutput()
        self.fake_stderr = FakeOutput()
        self.fake_output = Console(output=self.fake_stdout,
                                   error=self.fake_stderr)

    def test_successful_connection(self):
        uris = ["a.4cdn.org/f/threads.json", "a.4cdn.org/g/threads.json"]
        test_connection(uris, False, self.fake_output)
        self.assertIn(">", self.fake_stdout.last_received)

    def test_failed_connection(self):
        uris = [None, "a.4cdn.org/z/threads.json"]
        test_connection(uris, False, self.fake_output)
        self.assertIn("FAILED:", self.fake_stderr.last_received)
