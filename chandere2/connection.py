"""Module for handling connections to the imageboard."""

import contextlib
import ssl
import sys
import re
import urllib.error
import urllib.request
import urllib.parse

USERAGENT = "Chandere/2.0"
KNOWN_IMAGEBOARDS = {"4chan": "a.4cdn.org",
                     "8chan": "8ch.net",
                     "lainchan": "lainchan.org"}


def test_connection(uris: list, use_ssl: bool, output) -> None:
    """Attempts connections to each of the given URIs, logging the
    response headers or status code to the designated output.
    """
    # create_default_context is used to make use of System-supplied SSL/TLS
    # certs. A default SSLContext constructor would not use certificates.
    context = ssl.create_default_context() if use_ssl else None
    prefix = "https://" if use_ssl else "http://"

    for index, uri in enumerate(uris):
        if uri is None:
            continue
        try:
            request = urllib.request.Request(prefix + uri)
            request.add_header("User-agent", USERAGENT)

            connection = urllib.request.urlopen(request, context=context)
            with contextlib.closing(connection) as result:
                headers = str(result.headers)[:-2]

        except urllib.error.HTTPError as status:
            output.write_error("FAILED: %s with %s." % (uri, status))

        else:
            output.write("CONNECTED: %s" % uri)
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
