import os
import unittest

from chandere2.write import get_path


class GetPathTest(unittest.TestCase):
    # Expected permissions for the root directory and the CWD are not
    # hardcoded, as these tests will likely be ran elsewhere.
    def test_check_output_permissions(self):
        self.assertEqual(os.access("/", os.W_OK), bool(get_path("/", "", "")))
        self.assertEqual(os.access(".", os.W_OK), bool(get_path(".", "", "")))

    def test_directory_for_file_downloading(self):
        self.assertEqual(get_path(".", "fd", ""), ".")
        self.assertIs(get_path("./a_file.txt", "fd", ""), None)

    def test_file_for_thread_archiving(self):
        self.assertEqual(get_path(".", "ar", "sqlite3"), "./archive.db")
        self.assertEqual(get_path("./file.txt", "ar", ""), "./file.txt")
        self.assertEqual(get_path(".", "ar", ""), "./archive.txt")
