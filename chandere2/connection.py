"""Module for handling connections with the imageboard."""

import os.path

import aiohttp

HEADERS = {"user-agent": "Chandere/2.4"}


async def try_connection(target_uris: dict, output):
    """Attempts connections to each of the given targets, writing either
    the response headers or status code to output.
    """
    async with aiohttp.ClientSession() as session:
        for uri in target_uris:
            async with session.get(uri, headers=HEADERS) as response:
                if response.status == 200:
                    output.write("CONNECTED: %s" % uri)
                    for header in response.headers:
                        header_value = response.headers.get(header)
                        output.write("> %s: %s" % (header, header_value))
                else:
                    status = response.status
                    output.write_error("FAILED: %s with %d." % (uri, status))


async def fetch_uri(uri: str, last_load: str) -> tuple:
    """Attempts to fetch the content at the specified URI, returning the
    parsed JSON response, the HTTP response code if it indicated an
    error, the last-modified response header, and the URI that this
    coroutine connected to.
    """
    async with aiohttp.ClientSession() as session:
        # Join the headers into a single dictionary.
        headers = dict({"last-modified": last_load}, **HEADERS)
        async with session.get(uri, headers=headers) as response:
            if response.status == 200:
                content = await response.json()
                error = False
                last_load = response.headers.get("last-modified")
            elif response.status == 304:
                content = None
                error = False
            else:
                content = last_load = None
                error = response.status
    return (content, error, last_load, uri)


async def download_file(uri: str, path: str, name: str) -> bool:
    """Tries to get the binary data at the given URI and save it into a
    file at the output path. If a file is found with the same name,
    "(Copy)" will be prepended. A boolean representing whether or not
    the operation was successful is returned.
    """
    while os.path.exists(os.path.join(path, name)):
        name = "(Copy) " + name

    async with aiohttp.ClientSession() as session:
        async with session.get(uri, headers=HEADERS) as response:
            if response.status == 200:
                with open(os.path.join(path, name), "wb+") as output_file:
                    output_file.write(await response.read())
            return response.status == 200


async def wrap_semaphore(coroutine, semaphore):
    """Wraps the execution of a coroutine into a semaphore."""
    async with semaphore:
        return await coroutine
