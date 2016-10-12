# Tests assume that the CWD is writeable.

import os
import sqlite3
import unittest

from chandere2.write import (archive_sqlite, archive_plaintext,
                             insert_to_file, create_archive)


## TODO: Clean up. <jakob@memeware.net>
class InsertToFileTest(unittest.TestCase):
    def test_insert_at_end(self):
        with open("test_archive.txt", "w+") as test_archive:
            post = "Post: 1"
            insert_to_file(test_archive, post, None, 1)

        with open("test_archive.txt", "r+") as test_archive:
            self.assertEqual(test_archive.read(), "Post: 1\n\n\n")

    def test_insert_after_parent(self):
        with open("test_archive.txt", "w+") as test_archive:
            post = "Post: 2"
            test_archive.write("Post: 1" + "*" * 80 + "\n\n\n")
            insert_to_file(test_archive, post, 1, 2)

        with open("test_archive.txt", "r+") as test_archive:
            self.assertEqual(test_archive.read(),
                             "Post: 1" + "*" * 80 + "\nPost: 2\n\n")


class CreateArchiveTest(unittest.TestCase):
    def test_create_text_file(self):
        create_archive("ar", "plaintext", "archive.txt")
        self.assertTrue(os.path.exists("archive.txt"))
        os.remove("archive.txt")

    def test_create_database(self):
        create_archive("ar", "sqlite", "archive.db")
        self.assertTrue(os.path.exists("archive.db"))

        connection = sqlite3.connect("archive.db")
        cursor = connection.cursor()

        cursor.execute("SELECT name FROM sqlite_master")
        self.assertIn("posts", cursor.fetchone())

        os.remove("archive.db")

    def test_fail_on_fd_mode(self):
        create_archive("fd", "plaintext", "archive.txt")
        self.assertFalse(os.path.exists("archive.txt"))
