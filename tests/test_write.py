## Tests assume that the CWD is writeable

import os
import sqlite3

import hypothesis
import hypothesis.strategies as st

from chandere2.post import unescape
from chandere2.write import (archive_sqlite, create_archive, insert_to_file)


class TestInsertToFile:
    # Asserts that the post is inserted at the end if it is not a child.
    def test_insert_at_end(self):
        with open("test_archive.txt", "w+") as test_archive:
            post = "Post ID: 1"
            insert_to_file(test_archive, post, None, 1)

        with open("test_archive.txt", "r+") as test_archive:
            assert test_archive.read() == "Post ID: 1\n\n\n"

        os.remove("test_archive.txt")

    # Asserts that children are inserted immediately after the parent.
    def test_insert_after_parent(self):
        with open("test_archive.txt", "w+") as test_archive:
            post = "Post ID: 2"
            test_archive.write("Post ID: 1\n" + "=" * 80 + "\n\n\n")
            insert_to_file(test_archive, post, 1, 2)

        written = "Post ID: 1\n" + "=" * 80 + "\nPost ID: 2\n\n\n"

        with open("test_archive.txt", "r+") as test_archive:
            assert test_archive.read() == written

        os.remove("test_archive.txt")


class TestCreateArchive:
    # Asserts that a text file is created.
    def test_create_text_file(self):
        create_archive("ar", "plaintext", "archive.txt")
        assert os.path.exists("archive.txt")
        os.remove("archive.txt")

    # Asserts that nothing is done in file download mode.
    def test_fail_on_fd_mode(self):
        create_archive("fd", "plaintext", "archive.txt")
        assert not os.path.exists("archive.txt")
