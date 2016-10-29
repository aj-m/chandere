"""Module for handling connections with the imageboard."""

import os.path

import aiohttp

HEADERS = {"user-agent": "Chandere/2.1"}


async def try_connection(target_uris: dict, use_ssl: bool, output):
    """Attempts connections to each of the given URIs, writing the
    response headers or status code to the designated output.
    """
    prefix = "https://" if use_ssl else "http://"

    async with aiohttp.ClientSession() as session:
        for uri in target_uris:
            async with session.get(prefix + uri, headers=HEADERS) as response:
                if response.status == 200:
                    output.write("CONNECTED: %s" % uri)
                    for header in response.headers:
                        header_value = response.headers.get(header)
                        output.write("> %s: %s" % (header, header_value))
                else:
                    status = response.status
                    output.write_error("FAILED: %s with %d." % (uri, status))


async def fetch_uri(uri: str, last_load: str, use_ssl: bool) -> tuple:
    """Attempts to fetch the content at the specified URI, returning a
    tuple containing the parsed JSON response, the HTTP response code
    if it was anomalous, the last-modified response header, and the
    URI that this coroutine connected to.
    """
    prefix = "https://" if use_ssl else "http://"

    async with aiohttp.ClientSession() as session:
        headers = dict({"last-modified": last_load}, **HEADERS)
        async with session.get(prefix + uri, headers=headers) as response:
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


async def download_file(uri: str, path: str, name: str, use_ssl: bool):
    """Tries to get the binary data at the given URI, copying it into
    the given output path. If a file already exists at the given output
    path, "(Copy)" will be prepended to the filename.
    """
    prefix = "https://" if use_ssl else "http://"

    while os.path.exists(os.path.join(path, name)):
        name = "(Copy) " + name

    async with aiohttp.ClientSession() as session:
        async with session.get(prefix + uri, headers=HEADERS) as response:
            if response.status == 200:
                with open(os.path.join(path, name), "wb+") as output_file:
                    output_file.write(await response.read())


async def wrap_semaphore(coroutine, semaphore):
    """Wraps the execution of a given coroutine into a semaphore and
    returns the result of awaiting the coroutine.
    """
    async with semaphore:
        return await coroutine
