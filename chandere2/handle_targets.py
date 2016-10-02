"""[Document me!]"""

import asyncio
import re
import signal

from chandere2.connection import (download_file, fetch_uri)
from chandere2.validate_input import generate_uri


async def wrap_semaphore(coroutine, semaphore):
    """[Document me!]"""
    async with semaphore:
        return await coroutine


async def main_loop(target_uris: dict, args, output):
    """[Document me!]"""
    while True:
        operations = []
        if args.nocap:
            for uri in target_uris:
                last_load = target_uris[uri][2]
                operations.append(fetch_uri(uri, last_load, args.ssl, output))
        else:
            connection_cap = asyncio.Semaphore(16)
            for uri in target_uris:
                last_load = target_uris[uri][2]
                target_operation = fetch_uri(uri, last_load, args.ssl, output)
                wrapped = wrap_semaphore(target_operation, connection_cap)
                operations.append(wrapped)

        for future in asyncio.as_completed(operations):
            content, error, last_load, uri = await future
            if not error:
                if target_uris[uri][1]:
                    pass
                else:
                    board = target_uris[uri][0]
                    for uri in get_threads(content, board, args.imageboard):
                        target_uris[uri] = [board, True, ""]
                
                target_uris[uri][2] = last_load
            else:
                del target_uris[uri]


def get_threads(content: list, board: str, imageboard: str):
    """Generator that iterates through the content of a threads.json
    output, creating and yielding a URI for every thread seen.
    """
    for thread in sum([page.get("threads") for page in content], []):
        thread_no = str(thread.get("no"))
        yield generate_uri(board, thread_no, imageboard)
