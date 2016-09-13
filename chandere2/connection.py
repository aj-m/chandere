"""Module for handling connections with the imageboard."""

import contextlib
import ssl
import urllib.error
import urllib.request

USERAGENT = "Chandere/2.0"


def test_connection(target_uris: list, use_ssl: bool, output) -> None:
    """Attempts connections to each of the given URIs, logging the
    response headers or status code to the designated output.
    """
    # create_default_context is used to make use of System-supplied SSL/TLS
    # certs. A default SSLContext constructor would not use certificates.
    context = ssl.create_default_context() if use_ssl else None
    prefix = "https://" if use_ssl else "http://"

    for index, uri in enumerate(target_uris):
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
            if index != len(target_uris) - 1:
                output.write()
