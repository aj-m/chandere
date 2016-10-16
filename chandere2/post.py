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


def find_files(content: dict, board: str, imageboard: str):
    """Generator to iterate over posts and yield a tuple containing the
    URI and filename for any files it happens to find.
    """
    for post in content.get("posts"):
        for original_filename, server_filename in get_images(post, imageboard):
            image_uri = get_image_uri(server_filename, board, imageboard)
            yield (image_uri, original_filename)


def check_filtered(text: str, pattern: str):
    """Returns whether or not a field of text is covered by a given
    4chan-regexp styled filtering pattern.
    """
    return pattern in text


def filter_posts(content: dict, filters: list):
    """Removes fields from the "posts" attribute of a dictionary
    according to a list of tuples, containing a field and a 4chan-regexp
    styled filtering pattern.
    """
    for index, post in enumerate(content.get("posts", [])):
        for field, pattern in filters:
            if check_filtered(str(post.get(field)), pattern):
                del content.get("posts")[index]


def ascii_format_post(post: dict, imageboard: str):
    """Returns an ASCII-formtted version of the given post."""
    context = CONTEXTS.get(imageboard)
    no, date, name, trip, sub, com, filename, ext = context.get("post_fields")

    body = post.get(com, "")
    for pattern, substitution in SUBSTITUTIONS:
        body = re.sub(pattern, substitution, body)

    if post.get(filename) and post.get(ext):
        filename = ".".join((post.get(filename), post.get(ext)))
    else:
        filename = "[No File]"

    date = time.ctime(post.get(date))
    subject = "\n\"%s\"" % post.get(sub) if post.get(sub) else ""
    tripcode = "!" + post.get(trip) if post.get(trip) else ""

    formatted = "*" * 80 + "\nPost: %s\n" % post.get(no)
    formatted += "%s%s on %s" % (post.get(name), tripcode, date)
    formatted += "%s\nFile: %s\n" % (subject, filename) + "*" * 80
    formatted += "\n"

    wrap = lambda line: textwrap.wrap(line, width=80, replace_whitespace=False)
    formatted += "\n".join("\n".join(wrap(line)) for line in body.splitlines())
    formatted += "\n" + "*" * 80

    return formatted
