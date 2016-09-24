"""Module for writing scraped information to disk."""

import os


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
