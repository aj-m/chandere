## Tests assume that an internet connection is available.

import asyncio
import os

from chandere2.connection import (download_file, fetch_uri, try_connection, wrap_semaphore)
from chandere2.output import Console

from dummy_output import FakeOutput


class TestTryConnection:
    # Test asserts that HTTP headers are written to stdout.
    def test_report_successful_connection(self):
        fake_stdout = FakeOutput()
        fake_stderr = FakeOutput()
        fake_output = Console(output=fake_stdout, error=fake_stderr)

        loop = asyncio.get_event_loop()

        target_uris = ["a.4cdn.org/g/threads.json"]
        target_operation = try_connection(target_uris, False, fake_output)

        loop.run_until_complete(target_operation)
        assert ">" in fake_stdout.last_received

    # Test asserts that "FAILED" is written to stderr.
    def test_report_failed_connection(self):
        fake_stdout = FakeOutput()
        fake_stderr = FakeOutput()
        fake_output = Console(output=fake_stdout, error=fake_stderr)

        loop = asyncio.get_event_loop()

        target_uris = ["a.4cdn.org/z/threads.json"]
        target_operation = try_connection(target_uris, False, fake_output)

        loop.run_until_complete(target_operation)
        assert "FAILED" in fake_stderr.last_received


class TestFetchUri:
    # Asserts that a proper connection was made and returned.
    def test_fetch_uri_successfully(self):
        loop = asyncio.get_event_loop()
        target_operation = fetch_uri("a.4cdn.org/g/threads.json", "", False)

        async def check_return_value():
            content, error, last_load, uri = await target_operation
            assert content is not None
            assert not error
            assert last_load
            assert uri == "a.4cdn.org/g/threads.json"

        loop.run_until_complete(check_return_value())

    # Asserts that a connection wasn't made and was properly handled.
    def test_error_on_failed_connection(self):
        loop = asyncio.get_event_loop()
        target_operation = fetch_uri("a.4cdn.org/z/threads.json", "", False)

        async def check_return_value():
            content, error, last_load, uri = await target_operation
            assert content is None
            assert error == 404
            assert not last_load
            assert uri == "a.4cdn.org/z/threads.json"

        loop.run_until_complete(check_return_value())


class TestDownloadFile:
    # Asserts that a file was created, implying successful connection.
    def test_successful_image_download(self):
        loop = asyncio.get_event_loop()
        target_uri = "wiki.installgentoo.com/images/a/a8/GNU.png"
        target_operation = download_file(target_uri, ".", "gnu.png", False)

        assert loop.run_until_complete(target_operation)
        assert os.path.exists("gnu.png")

        os.remove("gnu.png")

    # Asserts that the file does not exist, implying a failed connection.
    def test_failed_image_download(self):
        loop = asyncio.get_event_loop()
        target_uri = "wiki.installgentoo.com/images/a/a8/GNU.gif"
        target_operation = download_file(target_uri, ".", "gnu.gif", False)

        assert not loop.run_until_complete(target_operation)

        assert not os.path.exists("gnu.gif")

    # Asserts that each time a file is downloaded,
    # "(Copy) " is prepended to the filename
    def test_prepend_copy(self):
        loop = asyncio.get_event_loop()
        target_uri = "wiki.installgentoo.com/images/a/a8/GNU.png"

        for _ in range(3):
            target_operation = download_file(target_uri, ".", "gnu.png", False)
            assert loop.run_until_complete(target_operation)

        assert os.path.exists("gnu.png")
        assert os.path.exists("(Copy) gnu.png")
        assert os.path.exists("(Copy) (Copy) gnu.png")

        os.remove("gnu.png")
        os.remove("(Copy) gnu.png")
        os.remove("(Copy) (Copy) gnu.png")


## FIXME: Doesn't test for semaphore's presence. <jakob@memeware.net>
class TestWrapSemaphore:
    # Asserts that the coroutine returned runs normally.
    def test_wrap_semaphore(self):
        loop = asyncio.get_event_loop()

        async def dummy_coroutine():
            return True

        semaphore = asyncio.Semaphore(1)
        coroutine = wrap_semaphore(dummy_coroutine(), semaphore)
        assert loop.run_until_complete(coroutine)
