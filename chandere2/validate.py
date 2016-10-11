"""Module for validating and parsing input from the command-line."""

import os
import re
import urllib.parse

from chandere2.context import CONTEXTS


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


def generate_uri(board: str, thread: str, imageboard="4chan") -> str:
    """Forms a valid URI for the given board, thread and imageboard.
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
            uri = "/".join((imageboard_uri, board, delimiter,
                            thread + ".json"))

    return uri


def get_targets(targets: list, imageboard: str, output) -> dict:
    """Strips the list of given target strings, creating and returning
    a dictionary where the URI for each target points to a list
    containing the board, whether or not the target refers to a thread,
    and a space to hold the HTTP Last-Modified header.
    """
    target_uris = {}

    for target in targets:
        board, thread = strip_target(target)
        if board is not None:
            uri = generate_uri(board, thread, imageboard)
            target_uris[uri] = [board, bool(thread), ""]
        else:
            output.write_error("Invalid target: %s" % target)

    return target_uris
