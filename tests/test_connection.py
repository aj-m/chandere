# Tests assume that a connection to 4chan can be made.

import asyncio
import unittest

from chandere2.connection import (fetch_uri, test_connection)
from chandere2.output import Console

from tests.dummy_objects import FakeOutput


class TestConnectionTest(unittest.TestCase):
    def setUp(self):
        self.fake_stdout = FakeOutput()
        self.fake_stderr = FakeOutput()
        self.fake_output = Console(output=self.fake_stdout,
                                   error=self.fake_stderr)

        self.loop = asyncio.get_event_loop()

    def test_report_successful_connection(self):
        target_uris = ["a.4cdn.org/g/threads.json"]
        target_operation = test_connection(target_uris, False,
                                           self.fake_output)

        self.loop.run_until_complete(target_operation)

        self.assertIn(">", self.fake_stdout.last_received)

    def test_report_failed_connection(self):
        target_uris = ["a.4cdn.org/z/threads.json"]
        target_operation = test_connection(target_uris, False,
                                           self.fake_output)

        self.loop.run_until_complete(target_operation)

        self.assertIn("FAILED", self.fake_stderr.last_received)


class FetchUriTest(unittest.TestCase):
    def setUp(self):
        self.fake_stdout = FakeOutput()
        self.fake_stderr = FakeOutput()
        self.fake_output = Console(output=self.fake_stdout,
                                   error=self.fake_stderr)

        self.loop = asyncio.get_event_loop()

    def test_yield_successful_connection(self):
        target_operation = fetch_uri("a.4cdn.org/g/threads.json", "",
                                     False, self.fake_output)

        async def check_return_value():
            content, error, last_load = await target_operation
            self.assertIsNotNone(content)
            self.assertFalse(error)
            self.assertTrue(last_load)

        self.loop.run_until_complete(check_return_value())

    def test_error_on_failed_connection(self):
        target_operation = fetch_uri("a.4cdn.org/z/threads.json", "",
                                     False, self.fake_output)

        async def check_return_value():
            content, error, last_load = await target_operation
            self.assertIsNone(content)
            self.assertTrue(error)
            self.assertFalse(last_load)

        self.loop.run_until_complete(check_return_value())
        self.assertIn("not exist", self.fake_stderr.last_received)
