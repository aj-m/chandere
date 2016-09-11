"""Module for handling connections to the imageboard."""

from contextlib import closing
import sys
import re
import urllib.error
import urllib.request
import urllib.parse

USERAGENT = "Chandere/2.0"
KNOWN_IMAGEBOARDS = {"4chan": "a.4cdn.org",
                     "8chan": "8ch.net",
                     "lainchan": "lainchan.org"}


## TODO: Clean up function. <jakob@memeware.net>
def test_connection(uris: list, ssl: bool, output) -> None:
    """Attempts connections to each of the given URIs, logging the
    response headers or status code to the designated output.
    """
    for index, uri in enumerate(uris):
        try:
            if uri is None: continue
            request = urllib.request.Request("http://" + uri)
            request.add_header("User-agent", USERAGENT)
            with closing(urllib.request.urlopen(request)) as connection:
                headers = str(connection.headers)[:-2]
        except urllib.error.HTTPError as status:
            output.write_error("FAILED: %s with %s." % (uri, status))
        else:
            output.write("OKAY: %s" % uri)
            for line in headers.split("\n"):
                output.write(">", line)
            if index != len(uris) - 1:
                output.write()


def generate_uri(target: str, imageboard="4chan") -> str:
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
        uri = thread = None

    return uri


def thread_in_uri(uri: str) -> bool:
    """Returns True if the given URI refers to a thread."""
    return not bool(re.search(r"\/threads.json", uri))
