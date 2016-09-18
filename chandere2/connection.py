"""Module for handling connections with the imageboard."""

import asyncio

import aiohttp

DEFAULT_HEADERS = {"user-agent": "Chandere/2.1"}


async def test_connection(target_uris: list, use_ssl: bool, output) -> None:
    """Attempts connections to each of the given URIs, logging the
    response headers or status code to the designated output.
    """
    connector = aiohttp.TCPConnector(verify_ssl=use_ssl)
    prefix = "https://" if use_ssl else "http://"

    async with aiohttp.ClientSession(connector=connector) as session:
        for index, uri in enumerate(target_uris):
            headers = DEFAULT_HEADERS
            async with session.get(prefix + uri, headers=headers) as response:
                if response.status == 200:
                    output.write("CONNECTED: %s" % uri)
                    for header in response.headers:
                        ## TODO: Clean up. <jakob@memware.net>
                        output.write("> %s: %s" % (header, response.headers.get(header)))
                    if index != len(target_uris) - 1:
                        output.write()
                else:
                    output.write_error("FAILED: %s with %s." % (uri, response.status))


async def enumerate_targets(target_uris: list, use_ssl: bool, output) -> None:
    """Tries to fetch the content at the specified URI, returning the
    content if successful. If the server returns a status of 404 or 403,
    the URI is removed from the target list and None is returned.
    """
    # The prefix is actually required for use with Aiohttp.
    connector = aiohttp.TCPConnector(verify_ssl=use_ssl)
    prefix = "https://" if use_ssl else "http://"

    async with aiohttp.ClientSession(connector=connector) as session:
        for uri in target_uris:
            headers = DEFAULT_HEADERS + {"last-modified": target_uris[uri][2]}
            async with session.get(prefix + uri, headers=headers) as response:
                if response.status == 200:
                    target_uris[uri][2] = response.headers.get("last-modified")
                    await response.text()
                elif response.status == 404:
                    output.write_error("%s does not exist." % uri)
                    del target_uris[uri]
                elif response.status == 403:
                    output.write_error("Servers are blocking web scrapers.")
                    del target_uris[uri]
                elif response.status == 304:
                    output.write_debug("Page has not updated since last load.")
