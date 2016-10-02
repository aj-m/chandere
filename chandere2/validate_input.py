"""Module to validate and parse input from the command-line."""

import os
import re
import urllib.parse

from chandere2.context import CONTEXTS


def strip_target(target: str) -> tuple:
    """Strips the given target string for a board initial and, if found,
    a thread number. A tuple containing the two will be returned, with
    None as the thread if a thread number was not in the target string.
    """
    # The target should be quoted and stripped prior to further
    # handing, as Python has difficulty with some Unicode.
    target = urllib.parse.quote(target, safe="/ ", errors="ignore").strip()

    # The regular expression pattern matches a sequence of
    # characters not containing whitespace or a forward slash,
    # optionally preceded and succeeded by a forward slash.
    match = re.search(r"(?<=\/)?[^\s\/]+(?=[\/ ])?", target)
    board = match.group() if match else None

    # The regular expression pattern matches a sequence of digits
    # preceded by something that might look like a board and a
    # forward slash or space character, optionally succeeded by a
    # forward slash.
    match = re.search(r"(?<=[^\s\/][\/ ])\d+(?=\/)?", target)
    thread = match.group() if match else None

    return (board, thread)


def get_path(path: str, mode: str, output_format: str) -> str:
    """Validates the given output path, ensuring that the user has
    sufficient permissions to write there and appending a stock filename
    if necessary. The finalized path is returned.
    """
    parent_directory = os.path.dirname(os.path.abspath(path))

    if os.path.isdir(path):
        if not os.access(path, os.W_OK):
            path = None
        elif mode == "ar":
            if output_format == "sqlite3":
                filename = "archive.db"
            else:
                filename = "archive.txt"
            path = os.path.join(path, filename)

    else:
        if not os.access(parent_directory, os.W_OK) or mode == "fd":
            path = None

    return path


def generate_uri(board: str, thread: str, imageboard="4chan") -> str:
    """Forms a valid URN for the given board, thread and imageboard.
    None is returned if the imageboard does not have a known URI.
    """
    if imageboard in CONTEXTS:
        imageboard_uri = CONTEXTS.get(imageboard).get("uri")
        delimiter = CONTEXTS.get(imageboard).get("delimiter")
    else:
        imageboard_uri = None

    if imageboard_uri is None:
        uri = None
    else:
        if thread is None:
            uri = "/".join((imageboard_uri, board, "threads" + ".json"))
        else:
            uri = "/".join((imageboard_uri, board,
                            delimiter, thread + ".json"))

    return uri
