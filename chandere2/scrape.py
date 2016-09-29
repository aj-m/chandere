"""Base coroutines for scraping and writing to disk."""

import asyncio
import re

from chandere2.connection import (download_file, fetch_uri)
from chandere2.uri import generate_uri


async def poll_targets(targets: list, use_ssl: bool, posts: asyncio.Queue,
                       threads: asyncio.Queue, run_once: bool, output):
    """Enumerates targets in the given dictionary either forever if
    run_once is false, or until no new targets are found. Content is put
    into the given queue, 
    """
    while True:
        # A runtime error is raised if a dictionary's size
        # changes during iteration, so dict.keys() is used.
        for uri in set(targets.keys()):
            target_operation = fetch_uri(uri, targets[uri][2], use_ssl, output)
            content, error, last_load = await target_operation

            if not error:
                if targets[uri][1]:
                    pass
                else:
                    await threads.put((content, uri))
                targets[uri][2] = last_load
            else:
                del targets[uri]

        break ##

    # None is a Sentinel value to tell any coroutines
    # watching these queues that the task is done.
    await threads.put((None, None))
    await posts.put((None, None, None))


async def get_threads(targets, threads, imageboard, output):
    """[Document me!]"""
    while True:
        content, uri = await threads.get()
        
        for thread in sum((page.get("threads") for page in content), []):
            board = targets[uri][0]
            uri = generate_uri(board, str(thread.get("no")), imageboard)
            targets[uri] = [board, True, ""]
            print(targets)


## TODO: Refactor and finish. <jakob@memeware.net>
async def filter_posts(filters, posts, filtered, output):
    """[Document me!]"""
    def check_filtered(post):
        """[Document me]"""
        for kind, pattern in filters:
            field_value = str(kwargs.get(kind, ""))
            for regex in re.findall(r"(?<!//)(?<=\/).*(?!//)(?=\/)", pattern):
                filtered = bool(re.search(regex, field_value))
                pattern = re.sub(r"\/%s\/" % re.escape(regex), "", pattern)
            for exact in re.findall(r"(?<!//)(?<=\[).*(?!//)(?=\])", pattern):
                filtered = exact in field_value
                pattern = re.sub(r"\[%s\]" % exact, "", pattern)
            for subpattern in pattern.split():
                subpattern = re.escape(subpattern)
                subpattern = r".+" if subpattern == "\*" else subpattern
                subpattern = re.sub(r"\\\*\b", r".*\b", subpattern)
                subpattern = re.sub(r"\\\*", r".*?", subpattern)
            filtered = bool(re.search(subpattern, str(field_value)))
            if filtered:
                break
        return filtered
    
    content, board, thread = await posts.get()
    filtered = False

    if thread:
        for post in content.get("posts"):
            if not check_filtered(post):
                await filtered.put((post, board, thread))
    else:
        await filtered.put((content, board, thread))


async def scrape_posts(targets, mode, chan, posts, write, output):
    """[Document me!]"""
    while True:
        content, board, thread = await posts.get()

