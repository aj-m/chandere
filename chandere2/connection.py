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


## TODO: Test 403 and 304 handling. <jakob@memeware.net>
async def enumerate_uris(target_uris: dict, use_ssl: bool, output):
    """Tries to fetch the content at the specified URI, yielding the
    JSON response if successful. If the server returns a status of 404
    or 403, the URI is removed from the target list. Also handles the
    last-modified client header to limit pointless network load.
    """
    failed_uris = []
    prefix = "https://" if use_ssl else "http://"

    async with aiohttp.ClientSession() as session:
        for uri in target_uris:
            last_modified = target_uris[uri][2]
            headers = dict({"last-modified": last_modified}, **HEADERS)

            async with session.get(prefix + uri, headers=headers) as response:
                if response.status == 200:
                    target_uris[uri][2] = response.headers.get("last-modified")
                    return await response.json()
                elif response.status == 404:
                    output.write_error("%s does not exist." % uri)
                    failed_uris.append(uri)
                elif response.status == 403:
                    output.write_error("Servers are blocking web scrapers.")
                    failed_uris.append(uri)
                elif response.status == 304:
                    output.write_debug("Page has not updated since last load.")

        for uri in failed_uris:
            del target_uris[uri]
