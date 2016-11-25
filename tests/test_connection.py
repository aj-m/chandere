## Tests will fail if an internet connection is not present.

import asyncio
import os

from chandere2.connection import (download_file, fetch_uri, try_connection, wrap_semaphore)
from chandere2.output import Console

from dummy_output import FakeOutput


class TestTryConnection:
    # Asserts that connection headers are written to stdout.
    def test_successful_connection(self):
        fake_stdout = FakeOutput()
        fake_stderr = FakeOutput()
        fake_output = Console(output=fake_stdout, error=fake_stderr)

        loop = asyncio.get_event_loop()

        target_uris = ["a.4cdn.org/g/threads.json"]
        target_operation = try_connection(target_uris, False, fake_output)

        loop.run_until_complete(target_operation)
        assert ">" in fake_stdout.last_received

    # Asserts that "FAILED" is written to stderr.
    def test_failed_connection(self):
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
    def test_successful_fetch(self):
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
    def test_failed_fetch(self):
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
    # Asserts that the file was created.
    def test_successful_download(self):
        loop = asyncio.get_event_loop()
        target_uri = "wiki.installgentoo.com/images/a/a8/GNU.png"
        target_operation = download_file(target_uri, ".", "gnu.png", False)

        assert loop.run_until_complete(target_operation)
        assert os.path.exists("gnu.png")

        os.remove("gnu.png")

    # Asserts that the file does not exist.
    def test_failed_download(self):
        loop = asyncio.get_event_loop()
        target_uri = "wiki.installgentoo.com/images/a/a8/GNU.gif"
        target_operation = download_file(target_uri, ".", "gnu.gif", False)

        assert not loop.run_until_complete(target_operation)

        assert not os.path.exists("gnu.gif")

    # Asserts that "(Copy)" is successfully prepended to the filename.
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


# Asserts that the coroutine returned runs normally.
def test_wrap_semaphore():
    loop = asyncio.get_event_loop()

    async def dummy_coroutine():
        return True

    semaphore = asyncio.Semaphore(1)
    coroutine = wrap_semaphore(dummy_coroutine(), semaphore)
    assert loop.run_until_complete(coroutine)
