import asyncio
import os

from chandere2.connection import (download_file, fetch_uri, try_connection, wrap_semaphore)
from chandere2.output import Console

from dummy_output import FakeOutput


# Fake response object that can be awaited.
class DummyResponse:
    def __init__(self, status: int, headers: dict, content: bytes):
        self.status = status
        self.headers = headers
        self.content = content

    async def json(self):
        return {}

    async def read(self):
        return self.content

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass


class TestTryConnection:
    # Asserts that a connection header is written to stdout.
    def test_successful_connection(self, monkeypatch):
        fake_stdout = FakeOutput()
        fake_stderr = FakeOutput()
        fake_output = Console(output=fake_stdout, error=fake_stderr)

        fake_response = DummyResponse(200, {"X-Served": "Nginx"}, b"")
        fake_get = lambda *args, **kwargs: fake_response
        monkeypatch.setattr("aiohttp.ClientSession.get", fake_get)

        loop = asyncio.get_event_loop()

        target_uris = ["http://a.4cdn.org/g/threads.json"]
        target_operation = try_connection(target_uris, fake_output)

        loop.run_until_complete(target_operation)
        assert ">" in fake_stdout.last_received

    # Asserts that "FAILED" is written to stderr.
    def test_failed_connection(self, monkeypatch):
        fake_stdout = FakeOutput()
        fake_stderr = FakeOutput()
        fake_output = Console(output=fake_stdout, error=fake_stderr)

        fake_response = DummyResponse(404, {}, b"")
        fake_get = lambda *args, **kwargs: fake_response
        monkeypatch.setattr("aiohttp.ClientSession.get", fake_get)

        loop = asyncio.get_event_loop()

        target_uris = ["http://a.4cdn.org/z/threads.json"]
        target_operation = try_connection(target_uris, fake_output)

        loop.run_until_complete(target_operation)
        assert "FAILED" in fake_stderr.last_received


class TestFetchUri:
    # Asserts that a connection could be made.
    def test_successful_fetch(self, monkeypatch):
        fake_response = DummyResponse(200, {"last-modified": "fake_info"}, b"")
        fake_get = lambda *args, **kwargs: fake_response
        monkeypatch.setattr("aiohttp.ClientSession.get", fake_get)

        loop = asyncio.get_event_loop()
        target_operation = fetch_uri("http://a.4cdn.org/g/threads.json", "")

        async def check_return_value():
            content, error, last_load, uri = await target_operation
            assert content is not None
            assert not error
            assert last_load
            assert uri == "http://a.4cdn.org/g/threads.json"

        loop.run_until_complete(check_return_value())

    # Asserts that a connection wasn't made and was properly handled.
    def test_failed_fetch(self, monkeypatch):
        fake_response = DummyResponse(404, {"X-Served": "Nginx"}, b"")
        fake_get = lambda *args, **kwargs: fake_response
        monkeypatch.setattr("aiohttp.ClientSession.get", fake_get)

        loop = asyncio.get_event_loop()
        target_operation = fetch_uri("http://a.4cdn.org/z/threads.json", "")

        async def check_return_value():
            content, error, last_load, uri = await target_operation
            assert content is None
            assert error == 404
            assert not last_load
            assert uri == "http://a.4cdn.org/z/threads.json"

        loop.run_until_complete(check_return_value())

    # Asserts that a connection has not been updated was handled.
    def test_already_fetched(self, monkeypatch):
        fake_response = DummyResponse(304, {"X-Served": "Nginx"}, b"")
        fake_get = lambda *args, **kwargs: fake_response
        monkeypatch.setattr("aiohttp.ClientSession.get", fake_get)

        loop = asyncio.get_event_loop()
        target_operation = fetch_uri("http://a.4cdn.org/3/threads.json", "")

        async def check_return_value():
            content, error, last_load, uri = await target_operation
            assert content is None
            assert not error
            assert not last_load
            assert uri == "http://a.4cdn.org/3/threads.json"

        loop.run_until_complete(check_return_value())


class TestDownloadFile:
    # Asserts that a file was created.
    def test_successful_download(self, monkeypatch):
        fake_response = DummyResponse(200, {"X-Served": "Nginx"}, b"\x00")
        fake_get = lambda *args, **kwargs: fake_response
        monkeypatch.setattr("aiohttp.ClientSession.get", fake_get)

        loop = asyncio.get_event_loop()
        target_uri = "http://wiki.installgentoo.com/images/a/a8/GNU.png"
        target_operation = download_file(target_uri, ".", "gnu.png")

        assert loop.run_until_complete(target_operation)
        assert os.path.exists("gnu.png")

        os.remove("gnu.png")

    # Asserts that the file was not created.
    def test_failed_download(self, monkeypatch):
        fake_response = DummyResponse(404, {"X-Served": "Nginx"}, b"")
        fake_get = lambda *args, **kwargs: fake_response
        monkeypatch.setattr("aiohttp.ClientSession.get", fake_get)

        loop = asyncio.get_event_loop()
        target_uri = "http://wiki.installgentoo.com/images/a/a8/GNU.gif"
        target_operation = download_file(target_uri, ".", "gnu.gif")

        assert not loop.run_until_complete(target_operation)
        assert not os.path.exists("gnu.gif")

    # Asserts that "(Copy)" is prepended to the filename.
    def test_prepend_copy(self, monkeypatch):
        fake_response = DummyResponse(200, {"X-Served": "Nginx"}, b"\x00")
        fake_get = lambda *args, **kwargs: fake_response
        monkeypatch.setattr("aiohttp.ClientSession.get", fake_get)

        loop = asyncio.get_event_loop()
        target_uri = "http://wiki.installgentoo.com/images/a/a8/GNU.png"

        for _ in range(3):
            target_operation = download_file(target_uri, ".", "gnu.png")
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
