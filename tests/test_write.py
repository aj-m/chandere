## Tests assume that the CWD is writeable

import os
import sqlite3

import hypothesis
import hypothesis.strategies as st

from chandere2.post import ascii_format_post
from chandere2.write import (create_archive, insert_to_file)


class TestInsertToFile:
    # Asserts that the post is inserted at the end if it is not a child.
    def test_insert_at_end(self):
        with open("test_archive.txt", "w+") as test_archive:
            post = "Post: 1"
            insert_to_file(test_archive, post, None, 1)

        with open("test_archive.txt", "r+") as test_archive:
            assert test_archive.read() == "Post: 1\n\n\n"

        os.remove("test_archive.txt")

    # Asserts that children are inserted immediately after the parent.
    def test_insert_after_parent(self):
        with open("test_archive.txt", "w+") as test_archive:
            post = "Post: 2"
            test_archive.write("Post: 1" + "*" * 80 + "\n\n\n")
            insert_to_file(test_archive, post, 1, 2)

        written = "Post: 1" + "*" * 80 + "\nPost: 2\n\n"

        with open("test_archive.txt", "r+") as test_archive:
            assert test_archive.read() == written

        os.remove("test_archive.txt")


class TestCreateArchive:
    # Asserts that a text file is created.
    def test_create_text_file(self):
        create_archive("ar", "plaintext", "archive.txt")
        assert os.path.exists("archive.txt")
        os.remove("archive.txt")

    # Asserts that a database is properly created.
    def test_create_database(self):
        create_archive("ar", "sqlite", "archive.db")
        assert os.path.exists("archive.db")

        connection = sqlite3.connect("archive.db")
        cursor = connection.cursor()

        cursor.execute("SELECT name FROM sqlite_master")
        assert "posts" in cursor.fetchone()

        os.remove("archive.db")

    # Asserts that nothing is done in file download mode.
    def test_fail_on_fd_mode(self):
        create_archive("fd", "plaintext", "archive.txt")
        assert not os.path.exists("archive.txt")
