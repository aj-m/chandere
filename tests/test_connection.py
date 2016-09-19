import asyncio
import unittest

import hypothesis
import hypothesis.strategies as st

from chandere2.connection import (enumerate_targets, test_connection)
from chandere2.output import Console

from tests.dummy_objects import FakeOutput


class ConnectionTrialTest(unittest.TestCase):
    def setUp(self):
        self.fake_stdout = FakeOutput()
        self.fake_stderr = FakeOutput()
        self.fake_output = Console(output=self.fake_stdout,
                                   error=self.fake_stderr)

        self.loop = asyncio.get_event_loop()

    def test_successful_connection(self):
        uris = ["a.4cdn.org/f/threads.json", "a.4cdn.org/g/threads.json"]
        target_operation = test_connection(uris, False, self.fake_output)
        self.loop.run_until_complete(target_operation)

        self.assertIn(">", self.fake_stdout.last_received)

    def test_failed_connection(self):
        uris = ["a.4cdn.org/z/threads.json"]
        target_operation = test_connection(uris, False, self.fake_output)
        self.loop.run_until_complete(target_operation)

        self.assertIn("FAILED:", self.fake_stderr.last_received)


class EnumerateUrisTest(unittest.TestCase):
    def setUp(self):
        self.fake_stderr = FakeOutput()
        self.fake_output = Console(output=FakeOutput(), error=self.fake_stderr)

        self.loop = asyncio.get_event_loop()

    def test_successful_content_fetch(self):
        target_uris = {"a.4cdn.org/g/threads.json": [None, None, ""]}
        target_operation = enumerate_targets(target_uris, False,
                                             self.fake_output)

        self.loop.run_until_complete(target_operation)
        self.assertFalse(hasattr(self.fake_stderr, "last_received"))
        self.assertIn("a.4cdn.org/g/threads.json", target_uris)
    
    def test_fetch_fail_on_nonexistent(self):
        target_uris = {"a.4cdn.org/z/threads.json": [None, None, ""]}
        target_operation = enumerate_targets(target_uris, False,
                                             self.fake_output)

        self.loop.run_until_complete(target_operation)
        self.assertIn("does not exist.", self.fake_stderr.last_received)
        self.assertNotIn("a.4cdn.org/z/threads.json", target_uris)

    ## No way to test thus far.
    # def test_fetch_fail_on_blocked(self):
    #     self.assertIs(get_content("a.4cdn.org/g/threads.json",
    #                               {"a.4cdn.org/g/threads.json": ()},
    #                               False, self.fake_output), None)
    #     self.assertIn("blocking web scrapers.", self.fake_stderr.last_received)

    ## No way to test thus far.
    # def test_fetch_fail_on_not_updated(self):
    #     self.assertTrue(get_content("a.4cdn.org/3/threads.json", {},
    #                                 False, self.fake_output))
    #     self.assertIs(get_content("a.4cdn.org/3/threads.json",
    #                               {"a.4cdn.org/z/threads.json": ()},
    #                               False, self.fake_output), None)
    #     self.assertIn("Page has not updated", self.fake_stderr.last_received)
