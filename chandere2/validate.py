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
            if output_format == "sqlite":
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
    context = CONTEXTS.get(imageboard)

    if context is None:
        uri = None
    else:
        imageboard_uri = context.get("uri")
        delimiter = context.get("delimiter")
        threads_endpoint = context.get("threads_endpoint")

        if thread is None:
            uri = "/".join((imageboard_uri, board, threads_endpoint))
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


def convert_to_regexp(pattern: str) -> str:
    """Converts a given filter pattern to regular expression syntax."""
    # Separate subpatterns encapsulated in forward slashes from the
    # rest, so that wildcard substitutions don't affect anything meant
    # to use regular expression syntax.
    if re.search(r"\/.+\/", pattern):
        subpatterns = []
        while True:
            regexp = re.search(r"\/.+\/", pattern)
            if not regexp:
                break
            subpatterns.append(pattern[:regexp.start()])
            subpatterns.append(pattern[regexp.start():regexp.end()])
            pattern = pattern[regexp.end():]
        subpatterns.append(pattern)
    else:
        subpatterns = [pattern]


    # Clear out the pattern variable, since it will be used to store the
    # regular expression as each subexpression is evaluated.
    pattern = ""

    # Turn wildcards into an appropriate regex substitution if and only
    # if the subpattern is not already a regular expression.
    for subpattern in subpatterns:
        if subpattern.startswith("/") and subpattern.endswith("/"):
            pattern += subpattern[1:-1]

        else:
            subpattern = re.sub(r"\*(\s|$)", ".*", subpattern)
            subpattern = re.sub(r"\*(?=\w)", ".", subpattern)
            pattern += subpattern

    return pattern


def split_pattern(pattern: str) -> iter:
    """Generator that splits a given filter pattern with respect to
    4chan's "and operator" and "exact match" syntax.
    """
    while True:
        regexp = re.search(r"\".+\"", pattern)
        if not regexp:
            break

        yield pattern[:regexp.start()]
        yield pattern[regexp.start():regexp.end()][1:-1]
        pattern = pattern[regexp.end():]

    yield pattern


def get_filters(filters: list, imageboard: str, output) -> list:
    """Returns a list of tuples containing a post field and a filter
    pattern according to a list of colon-separated arguments.
    """
    evaluated = []
    for argument in filters:
        if argument.count(":") == 1:
            field, pattern = argument.split(":")
            for subexpression in split_pattern(pattern):
                evaluated.append((field, convert_to_regexp(subexpression)))
        else:
            output.write("Invalid filter pattern: %s." % argument)
    return filters
