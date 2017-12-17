class ChandereCriticalException(Exception):
    def __init__(self, *args, **kwargs):
        super.__init__(self, *args, **kwargs)


def handle_anomalous_http_status(code: int, url=None):
    if code != 200:
        error = "Encountered HTTP/1.1 {}".format(code)
        if url is not None:
            error += " while fetching '{}'.".format(url)
        raise ChandereCriticalException(error)
