"""Base coroutines for scraping and writing to disk."""

import asyncio
import re

from chandere2.connection import (download_file, fetch_uri)
from chandere2.validate_input import generate_uri


async def scrape_target(target_uris: dict, use_ssl: bool, output, uri: str):
    """[Document me!]"""
    output.write("Fetching %s..." % uri)
    target_operation = fetch_uri(uri, targets[uri][2], use_ssl, output)
    content, error, last_load = await target_operation

    if not error:
        if target_uris[uri][1]:
            pass
        else:
            pass

        target_uris[uri][2] = last_load
    else:
        del target_uris[uri]
