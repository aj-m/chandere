"""Module containing the processing loop and related subroutines."""

import asyncio

from chandere2.connection import (download_file, fetch_uri)
from chandere2.context import CONTEXTS
from chandere2.validate_input import generate_uri

MAX_CONNECTIONS = 8


async def wrap_semaphore(coroutine, semaphore):
    """Wraps the execution of a given coroutine into the given
    semaphore, returning whatever the coroutine returns.
    """
    async with semaphore:
        return await coroutine


def get_threads(content: list, board: str, imageboard: str):
    """Generator that iterates through the content of a threads.json
    output, creating and yielding a URI for every thread seen.
    """
    for thread in sum([page.get("threads") for page in content], []):
        thread_no = str(thread.get("no"))
        yield generate_uri(board, thread_no, imageboard)


def get_images(post: dict, imageboard: str) -> list:
    """Scrapes a post for images, returning a list of tuples containing
    the original filename and the filename as it's stored on the server.
    """
    context = CONTEXTS.get(imageboard)
    filename, tim, ext, extra_files = context.get("image_fields")
    images = []

    if post.get(tim):
        original_filename = post.get(filename) + post.get(ext)
        server_filename = str(post.get(tim)) + post.get(ext)
        images = [(original_filename, server_filename)]
        for image in post.get(extra_files, []):
            original_filename = image.get(filename) + image.get(ext)
            server_filename = str(image.get(tim)) + image.get(ext)
            images += [(original_filename, server_filename)]
    return images


def get_image_uri(filename: str, board: str, imageboard: str) -> str:
    """Given a filename, a board, and an imageboard, returns a URI
    pointing to the image specified by the parameters.
    """
    context = CONTEXTS.get(imageboard)

    uri = context.get("image_uri")
    if context.get("board_in_image_uri"):
        uri += "/" + board
    if context.get("image_dir"):
        uri += "/" + context.get("image_dir")
    return uri + "/" + filename


async def main_loop(target_uris: dict, path: str, args, output):
    """Main scraping loop."""
    while True:
        imageboard = args.imageboard
        operations = []

        if args.nocap:
            for uri in target_uris:
                last_load = target_uris[uri][2]
                operations.append(fetch_uri(uri, last_load, args.ssl, output))
        else:
            connection_cap = asyncio.Semaphore(MAX_CONNECTIONS)
            for uri in target_uris:
                last_load = target_uris[uri][2]
                target_operation = fetch_uri(uri, last_load, args.ssl, output)
                wrapped = wrap_semaphore(target_operation, connection_cap)
                operations.append(wrapped)


        for future in asyncio.as_completed(operations):
            board, thread, _ = target_uris[uri]
            content, error, last_load, uri = await future

            if error:
                del target_uris[uri]
                continue

            ## TODO: Separate into subroutines? <jakob@memeware.net>
            if thread and args.mode == "fd":
                ## TODO: Add support for contexts. <jakob@memeware.net>
                for post in content.get("posts"):
                    images = get_images(post, imageboard)
                    for original_filename, server_filename in images:
                        ## TODO: Clean up. <jakob@memeware.net>
                        image_uri = get_image_uri(server_filename, board,
                                                  imageboard)
                        output.write("Downloading %s..." % original_filename)

                        ## TODO: Clean up. <jakob@memeware.net>
                        await download_file(image_uri, path, original_filename,
                                            args.ssl)
            elif thread and args.mode == "ar":
                ## TODO: Add support for contexts. <jakob@memeware.net>
                for post in content.get("posts"):
                    pass
            else:
                for uri in get_threads(content, board, args.imageboard):
                    target_uris[uri] = [board, True, ""]

            target_uris[uri][2] = last_load

        break ##
