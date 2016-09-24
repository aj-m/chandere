"""Module for handling connections with the imageboard."""

import asyncio

import aiohttp

HEADERS = {"user-agent": "Chandere/2.1"}


async def test_connection(target_uris: dict, use_ssl: bool, output):
    """Attempts connections to each of the given URIs, writing the
    response headers or status code to the designated output.
    """
    prefix = "https://" if use_ssl else "http://"

    async with aiohttp.ClientSession() as session:
        for index, uri in enumerate(target_uris):
            async with session.get(prefix + uri, headers=HEADERS) as response:
                if response.status == 200:
                    output.write("CONNECTED: %s" % uri)
                    for header in response.headers:
                        header_value = response.headers.get(header)
                        output.write("> %s: %s" % (header, header_value))
                else:
                    status = response.status
                    output.write_error("FAILED: %s with %d." % (uri, status))


## TODO: Rewrite tests. <jakob@memeware.net>
async def fetch_uri(uri: str, last_load: str, use_ssl: bool, output) -> tuple:
    """Attempts to fetch the content at the specified URI, returning a
    tuple containing the parsed JSON response, a boolean representing
    whether or not an anomalous HTTP response code was received, and the
    last-modified response header.
    """
    prefix = "https://" if use_ssl else "http://"

    async with aiohttp.ClientSession() as session:
        headers = dict({"last-modified": last_load}, **HEADERS)

        async with session.get(prefix + uri, headers=headers) as response:
            if response.status == 200:
                content = await response.json()
                error = False
                last_load = response.headers.get("last-modified")
            elif response.status == 404:
                output.write_error("%s does not exist." % uri)
                content = None
                error = True
            elif response.status == 403:
                output.write_error("Servers are blocking web scrapers.")
                content = None
                error = True
            elif response.status == 304:
                output.write_debug("Page has not updated since last load.")
                content = None
                error = False

        return (content, error, last_load)
