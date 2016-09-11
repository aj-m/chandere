"""Module for handling connections to the imageboard."""

import sys
import re
import urllib.parse

KNOWN_IMAGEBOARDS = {"4chan": "a.4cdn.org",
                     "8chan": "8ch.net",
                     "lainchan": "lainchan.org"}


def generate_uri(target, imageboard="4chan"):
    """Strips the board and thread number from the given target string,
    and forms them into a valid URN for the given imageboard.
    """
    if imageboard in KNOWN_IMAGEBOARDS:
        # The target should be quoted and stripped prior to further
        # handing, in the case that stranger unicode characters are
        # given.
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
        thread = match.group() if match else "threads"

        uri = "/".join((KNOWN_IMAGEBOARDS[imageboard], board,
                        thread + ".json")) if board is not None else None
    else:
        uri = None

    return uri
