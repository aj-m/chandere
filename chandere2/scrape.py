## TODO: Redocument this module. <jakob@memeware.net>

"""Coroutines for carrying out the actual scraping procedure."""

import asyncio

from chandere2.connection import (download_file, fetch_uri)


# Use None in the queue as a sentinel value to signal that this is done.
async def poll_targets(targets: dict, use_ssl: bool, posts, output):
    """Enumerates targets in the given hashmap, removing and adding
    targets as they are polled. Content is put into the given queue for
    as long as the task is not completed.
    """
    while True:
        failed_targets = []

        for uri in targets:
            target_operation = fetch_uri(uri, targets[uri][2], use_ssl, output)
            content, error, last_load = await target_operation

            if not error:
                await posts.put(content)
                targets[uri][2] = last_load

        for uri in failed_targets:
            del targets[uri]

        await posts.put(None)
        return


async def scrape_posts(uris: dict, mode: str, posts, write, output):
    """Collects page content from a given queue and scrapes for
    information relevant to the given mode of operation.
    """
    while True:
        content = await posts.get()

        if content is None:
            return

        print(content)
