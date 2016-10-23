## Tests assume that a connection to 4chan can be made.

import asyncio
import os
import unittest

from chandere2.connection import (download_file, fetch_uri,
                                  test_connection, wrap_semaphore)
from chandere2.output import Console

from tests.dummy_output import FakeOutput


class TestConnectionTest(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

        self.fake_stdout = FakeOutput()
        self.fake_stderr = FakeOutput()
        self.fake_output = Console(output=self.fake_stdout,
                                   error=self.fake_stderr)

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


## TODO: Write a test for HTTP/304 handling. <jakob@memeware.net>
class FetchUriTest(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_yield_successful_connection(self):
        target_operation = fetch_uri("a.4cdn.org/g/threads.json", "", False)

        async def check_return_value():
            content, error, last_load, uri = await target_operation
            self.assertIsNotNone(content)
            self.assertFalse(error)
            self.assertTrue(last_load)
            self.assertEqual(uri, "a.4cdn.org/g/threads.json")

        self.loop.run_until_complete(check_return_value())

    def test_error_on_failed_connection(self):
        target_operation = fetch_uri("a.4cdn.org/z/threads.json", "", False)

        async def check_return_value():
            content, error, last_load, uri = await target_operation
            self.assertIsNone(content)
            self.assertEqual(error, 404)
            self.assertFalse(last_load)
            self.assertEqual(uri, "a.4cdn.org/z/threads.json")

        self.loop.run_until_complete(check_return_value())


class DownloadFileTest(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_successful_image_download(self):
        target_uri = "wiki.installgentoo.com/images/a/a8/GNU.png"
        target_operation = download_file(target_uri, ".", "gnu.png", False)
        self.loop.run_until_complete(target_operation)

        self.assertTrue(os.path.exists(os.path.join(".", "gnu.png")))

        os.remove(os.path.join(".", "gnu.png"))

    def test_failed_image_download(self):
        target_uri = "wiki.installgentoo.com/images/a/a8/GNU.gif"
        target_operation = download_file(target_uri, ".", "gnu.gif", False)
        self.loop.run_until_complete(target_operation)

        self.assertFalse(os.path.exists(os.path.join(".", "gnu.gif")))

    def test_prepend_copy(self):
        target_uri = "wiki.installgentoo.com/images/a/a8/GNU.png"
        target_operation = download_file(target_uri, ".", "gnu.png", False)
        self.loop.run_until_complete(target_operation)

        target_operation = download_file(target_uri, ".", "gnu.png", False)
        self.loop.run_until_complete(target_operation)

        self.assertTrue(os.path.exists(os.path.join(".", "gnu.png")))
        self.assertTrue(os.path.exists(os.path.join(".", "(Copy) gnu.png")))

        os.remove(os.path.join(".", "gnu.png"))
        os.remove(os.path.join(".", "(Copy) gnu.png"))


## FIXME: Doesn't test for semaphore's presence. <jakob@memeware.net>
class WrapSemaphoreTest(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_wrap_semaphore(self):
        async def dummy_coroutine():
            return True

        semaphore = asyncio.Semaphore(1)
        coroutine = wrap_semaphore(dummy_coroutine(), semaphore)
        self.assertTrue(self.loop.run_until_complete(coroutine))
