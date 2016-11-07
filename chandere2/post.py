"""Module for working with posts and thread listings."""

import re
import textwrap
import time

from chandere2.context import CONTEXTS
from chandere2.validate import generate_uri

SUBSTITUTIONS = ((r'<p class="body-line empty "><\/p>', "\n\n"),
                 (r'<\/p>(?=<p class="body-line ltr ">)', "\n"),
                 (r"<\/?br\\?\/?>", "\n"), (r"&#039;", "'"), (r"&gt;", ">"),
                 (r"&quot;", r"\\"), (r"&amp;", "&"), (r"<.+?>", ""),
                 (r"\\/", "/"))


def get_threads_from_endpoint(content: list, board: str, imageboard: str):
    """Typical thread parsing function for imageboards that supply a
    plain threads.json endpoint.
    """
    for thread in sum([page.get("threads") for page in content], []):
        thread_no = str(thread.get("no"))
        yield generate_uri(board, thread_no, imageboard)


def get_threads_from_catalog(content: list, board: str, imageboard: str):
    """Alternative thread parsing function for imageboards that do not
    offer a threads.json endpoint.
    """
    context = CONTEXTS.get(imageboard)
    no = context.get("post_fields")[0]
    for thread in content:
        thread_no = str(thread.get(no))
        yield generate_uri(board, thread_no, imageboard)


def get_threads(content: list, board: str, imageboard: str):
    """Generator that iterates through the content of a threads
    endpoint, creating and yielding a URI for every thread seen.
    Chooses the method that is appropriate for the given imageboard.
    """
    context = CONTEXTS.get(imageboard)
    endpoint = context.get("threads_endpoint")
    if endpoint == "threads.json":
        generator = get_threads_from_endpoint(content, board, imageboard)
    else:
        generator = get_threads_from_catalog(content, board, imageboard)
    return generator


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


def get_images_default(post: dict, imageboard: str):
    """Scrapes a post for images, yielding the user-provided filename
    and the filename as it's stored on the server for each image found.
    This uses the default method of finding filenames and extensions.
    """
    context = CONTEXTS.get(imageboard)
    filename, tim, ext, extra_files = context.get("image_fields")

    if post.get(tim):
        original_filename = post.get(filename) + post.get(ext)
        server_filename = str(post.get(tim)) + post.get(ext)
        yield (original_filename, server_filename)
        for image in post.get(extra_files, []):
            original_filename = image.get(filename) + image.get(ext)
            server_filename = str(image.get(tim)) + image.get(ext)
            yield (original_filename, server_filename)


def get_images_path_based(post: dict, imageboard: str):
    """Alternative method of getting images. Uses the path supplied by
    the API endpoint.
    """
    context = CONTEXTS.get(imageboard)
    filename, path, _, files_field = context.get("image_fields")

    for image in post.get(files_field, []):
        yield (image.get(filename), image.get(path)[1:])


def get_images_id_based(post: dict, imageboard: str):
    """Alternative method of getting images. Uses the post and file ID's
    supplied by the API endpoint.
    """
    context = CONTEXTS.get(imageboard)
    no = context.get("post_fields")[0]
    filename, file_id, _, files_field = context.get("image_fields")

    for index, image in enumerate(post.get(files_field, [])):
        pivot = image.get(context.get("image_pivot"))
        extension = re.search("(?<=\\\\\/).+", image.get("mime")).group()
        original_filename = ".".join((pivot.get(filename), extension))
        server_filename = "%s/%d-%d.%s" % (pivot.get(file_id), post.get(no),
                                           index, extension)
        yield (original_filename, server_filename)


def iterate_posts(content: dict, imageboard: str):
    """Contextual subroutine for iterating over all of the posts in a
    thread's JSON representation.
    """
    context = CONTEXTS.get(imageboard)

    if context.get("reply_field"):
        yield content
        for post in content.get(context.get("reply_field"), []):
            yield post
    else:
        for post in content.get("posts"):
            yield post


def find_files(content: dict, board: str, imageboard: str):
    """Generator to iterate over posts and yield a tuple containing the
    URI and filename for any files it happens to find.
    """
    ## TODO: Make check more general. <jakob@memeware.net>
    if imageboard == "endchan":
        get_images = get_images_path_based
    elif imageboard == "nextchan":
        get_images = get_images_id_based
    else:
        get_images = get_images_default

    for post in iterate_posts(content, imageboard):
        for original_filename, server_filename in get_images(post, imageboard):
            image_uri = get_image_uri(server_filename, board, imageboard)
            yield (image_uri, original_filename)


## FIXME: No method of filtering posts with a reply field. <jakob@memeware.net>
def filter_posts(content: dict, filters: list, imageboard: str):
    """Removes values of the "posts" attribute of a dictionary according
    to a given list of filters.
    """
    check_filtered = lambda post: re.search(pattern, str(post.get(field, "")))
    for field, pattern in filters:
        content = filter(check_filtered, iterate_posts(content, imageboard))
    return list(content)


## FIXME: No method of filtering posts with a reply field. <jakob@memeware.net>
def cache_posts(content: dict, cache: list, imageboard: str):
    """Removes values of the "posts" attribute of a dictionary if they
    are in the cache. Any values still remaining will be added to the
    cache.
    """
    context = CONTEXTS.get(imageboard)
    no = context.get("post_fields")[0]

    check_cached = lambda post: not post.get(no) in cache
    content["posts"] = list(filter(check_cached, content.get("posts")))

    for post in content.get("posts"):
        cache.append(post.get(no))


def unescape(text: str) -> str:
    """Replaces escaped HTML in some text with escape sequences."""
    for pattern, substitution in SUBSTITUTIONS:
        text = re.sub(pattern, substitution, text)
    return text


def ascii_format_post(post: dict, imageboard: str):
    """Returns an ASCII-formtted version of the given post."""
    context = CONTEXTS.get(imageboard)
    no, date, name, trip, sub, com, filename, ext = context.get("post_fields")
    string = ["=" * 80, "Post ID: %s" % post.get(no)]

    date = time.ctime(post.get(date))
    tripcode = "!" + post.get(trip) if post.get(trip) else ""
    author = unescape(post.get(name)) or "Anonymous"
    string.append("%s%s on %s" % (author, tripcode, date))

    if post.get(sub):
        string.append("\"%s\"" % unescape(post.get(sub)))
    else:
        string.append("[No Subject]")

    if post.get(filename) and post.get(ext):
        string.append("File: " + post.get(filename) + post.get(ext))
        ## TODO: Check should be more reasonable. <jakob@memeware.net>
        # if ext is None:
        #     files_field = context.get("image_fields")[3]
        #     string.append("File: " + post.get(files_field).get(filename))
        # else:
        #     string.append("File: " + post.get(filename) + post.get(ext))
    else:
        string.append("File: [No File]")

    string.append("=" * 80)

    body = unescape(post.get(com, ""))
    wrap = lambda line: textwrap.wrap(line, width=80, replace_whitespace=False)

    for line in body.splitlines():
        string.append("\n".join(wrap(line)))

    string.append("=" * 80)

    return "\n".join(string)
