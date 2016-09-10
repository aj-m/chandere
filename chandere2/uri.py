"""Functions for handling imageboard URI's."""

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
    target = urllib.parse.quote_plus(target, safe="/").strip()

    match = re.search(r"(?<=\/)?[^\s\/]+(?=[\/ ])?", target)
    board = match.group() if match else None

    match = re.search(r"(?<=[\/ ])\d+(?=\/)?", target)
    thread = match.group() if match else "threads"

    if imageboard in KNOWN_IMAGEBOARDS and board is not None:
        uri = "/".join((KNOWN_IMAGEBOARDS[imageboard],
                        board, thread + ".json"))
    else:
        uri = None

    return uri
