"""Module for working with posts and thread endpoints."""

import calendar
import re
import textwrap
import time

from chandere2.context import CONTEXTS
from chandere2.validate import generate_uri

SUBSTITUTIONS = ((r'<p class="body-line empty "><\/p>', "\n\n"),
                 (r'<\/p>(?=<p class="body-line ltr ">)', "\n"),
                 (r'<\/p>(?=<p class="body-line ltr quote ">)', "\n"),
                 (r"<\/?br\\?\/?>", "\n"), (r"&#0?39;?", "'"), (r"&gt;?", ">"),
                 (r"&#0?42;?", "*"), (r"&#0?45;?", "-"), (r"&lt;?", "<"),
                 (r"&#0?95;", "_"), (r"&quot;?", r"\\"), (r"&amp;?", "&"),
                 (r"<.+?>", ""), (r"\\/", "/"))


def get_threads_from_endpoint(content: list, board: str,
                              imageboard: str, ssl: bool):
    """Thread parsing function for imageboards that supply a normal
    threads.json endpoint.
    """
    context = CONTEXTS.get(imageboard)
    no, threads = context.get("thread_fields")
    for thread in sum([page.get(threads) for page in content], []):
        thread_no = str(thread.get(no))
        yield generate_uri(board, thread_no, imageboard, ssl)


def get_threads_from_catalog(content: list, board: str,
                             imageboard: str, ssl: bool):
    """Alternative thread parsing function for imageboards that do not
    offer a threads.json endpoint, but instead offer a catalog.json.
    """
    context = CONTEXTS.get(imageboard)
    no, _ = context.get("thread_fields")
    for thread in content:
        thread_no = str(thread.get(no))
        yield generate_uri(board, thread_no, imageboard, ssl)


def get_threads(content: list, board: str,
                imageboard: str, ssl: bool):
    """Generator that iterates through the content of a threads
    endpoint, creating and yielding a URI for every thread seen.
    Chooses the method that is appropriate for the given imageboard.
    """
    context = CONTEXTS.get(imageboard)
    endpoint = context.get("threads_endpoint")
    if endpoint == "threads.json":
        generator = get_threads_from_endpoint(content, board, imageboard, ssl)
    else:
        generator = get_threads_from_catalog(content, board, imageboard, ssl)
    return generator


def get_image_uri(filename: str, board: str, imageboard: str) -> str:
    """Produces a valid URI for the given filename, board and
    imageboard."""
    context = CONTEXTS.get(imageboard)
    uri = [context.get("image_uri")]
    if context.get("board_in_image_uri"):
        uri.append(board)
    if context.get("image_dir"):
        uri.append(context.get("image_dir"))
    uri.append(filename)
    return "/".join(uri)


def get_images_default(post: dict, imageboard: str):
    """Scrapes a post for images, yielding the user-provided filename
    and the filename as it's stored on the server for each image found.
    This uses the default method of finding filenames and extensions.
    """
    context = CONTEXTS.get(imageboard)
    filename, tim, ext, extra_files = context.get("image_fields")
    if post.get(tim) is not None:
        if post.get(filename) is False:
            original_filename = str(post.get(tim)) + post.get(ext)
        else:
            original_filename = post.get(filename) + post.get(ext)
        server_filename = str(post.get(tim)) + post.get(ext)
        yield (original_filename, server_filename)
        for image in post.get(extra_files, []):
            if image.get(filename) is False:
                original_filename = str(image.get(tim)) + image.get(ext)
            else:
                original_filename = image.get(filename) + image.get(ext)
            server_filename = str(image.get(tim)) + image.get(ext)
            yield (original_filename, server_filename)


def get_images_path_based(post: dict, imageboard: str):
    """Alternative method of getting images where an image path is
    provided by the imageboard's thread endpoint. Currently required for
    imageboards running Lynxchan.
    """
    context = CONTEXTS.get(imageboard)
    filename, path, _, files_field = context.get("image_fields")
    for image in post.get(files_field, []):
        yield (image.get(filename), image.get(path)[1:])


def get_images_id_based(post: dict, imageboard: str):
    """Alternative method of getting images where several identifiers
    provided by the imageboards' thread endpoint are used as part of
    the image URI. Currently required for imageboards running Infinity
    Next.
    """
    context = CONTEXTS.get(imageboard)
    filename, attachment_id, _, files_field = context.get("image_fields")
    for index, image in enumerate(post.get(files_field, [])):
        pivot = image.get(context.get("image_pivot"))
        original_filename = pivot.get(filename)
        extension = re.search(r"(?<=\.)\w+$", original_filename).group()
        gmtime = time.strptime(image.get("first_uploaded_at", ""),
                               "%Y-%m-%d %H:%M:%S")
        time_id = calendar.timegm(gmtime)
        server_filename = "%s/%d-%d.%s" % (pivot.get(attachment_id),
                                           time_id, index, extension)
        yield (original_filename, server_filename)


def iterate_posts(content: dict, imageboard: str):
    """Generator that simply iterates over every posts in a given thread
    listing. Used to form a more concrete data structure representing the
    thread.
    """
    context = CONTEXTS.get(imageboard)
    reply_field = context.get("reply_field")
    if reply_field:
        if reply_field in content:
            replies = content[reply_field]
            del content[reply_field]
        else:
            replies = []
        yield content
        for post in replies:
            yield post
    else:
        for post in content.get("posts"):
            yield post


## TODO: Make check more general. <jakob@memeware.net>
def find_files(posts: list, board: str, imageboard: str):
    """Generalized function to find every file in the given thread.
    Yields the URI as it is stored on the server, as well as the
    original filename.
    """
    if imageboard == "endchan":
        get_images = get_images_path_based
    elif imageboard == "nextchan":
        get_images = get_images_id_based
    else:
        get_images = get_images_default

    for post in posts:
        for original_filename, server_filename in get_images(post, imageboard):
            image_uri = get_image_uri(server_filename, board, imageboard)
            yield (image_uri, original_filename)


def filter_posts(posts: list, filters: list):
    """Removes any posts that are covered by a given list of filters
    from a given thread listing, and returns the new listing.
    """
    for field, pattern in filters:
        filtered = lambda post: not re.search(pattern, str(post.get(field, "")))
        posts = list(filter(filtered, posts))
    return list(posts)


def cache_posts(posts: list, cache: list, imageboard: str):
    """Removes any posts that are in a given cache and returns the new
    listing. Posts that have not already been seen are added to the
    cache.
    """
    context = CONTEXTS.get(imageboard)
    no = context.get("post_fields")[0]

    cached = lambda post: post.get(no) not in cache
    posts = list(filter(cached, posts))
    for post in posts:
        cache.append(post.get(no))
    return posts


def unescape(text: str) -> str:
    """Replaces escaped HTML in a given string with the respective,
    unescaped characters.
    """
    for pattern, substitution in SUBSTITUTIONS:
        text = re.sub(pattern, substitution, text)
    return text


def ascii_format_post(post: dict, imageboard: str):
    """Returns an ASCII-formtted version of the given post."""
    context = CONTEXTS.get(imageboard)
    post_id, date, name, tripcode, subject, _, _, _ = context.get("post_fields")
    _, _, _, _, _, comment, filename, extension = context.get("post_fields")
    alt_id, _ = context.get("thread_fields")
    _, timestamp, _, files_field = context.get("image_fields")
    formatted = ["=" * 80, "Post ID: %s" % post.get(post_id, post.get(alt_id))]

    # Some imageboard API's will supply date in epoch time,
    # while others will supply it as a string.
    if isinstance(post.get(date), int):
        date_value = time.ctime(post.get(date))
    else:
        date_value = post.get(date)

    tripcode_value = "!" + post.get(tripcode) if post.get(tripcode) else ""
    author = unescape(post.get(name)) or "Anonymous"
    formatted.append("%s%s on %s" % (author, tripcode_value, date_value))

    if post.get(subject):
        formatted.append("\"%s\"" % unescape(post.get(subject)))
    else:
        formatted.append("[No Subject]")

    if post.get(filename) is not None and post.get(extension) is not None:
        if post.get(filename) is False:
            filename_value = str(post.get(timestamp)) + post.get(extension)
        else:
            filename_value = post.get(filename) + post.get(extension)
    elif post.get(files_field):
        filename_value = post.get(files_field).get(filename)
    else:
        filename_value = "[No File]"
    formatted.append("File: " + filename_value)
    formatted.append("=" * 80)

    body = unescape(post.get(comment, "")).strip()
    wrap = lambda line: textwrap.wrap(line, width=80, replace_whitespace=False)
    for line in body.splitlines():
        formatted.append("\n".join(wrap(line)))
    formatted.append("=" * 80)
    return "\n".join(formatted)
