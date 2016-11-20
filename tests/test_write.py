## Tests assume that the CWD is writeable

import os
import sqlite3

import hypothesis
import hypothesis.strategies as st

from chandere2.post import unescape
from chandere2.write import (archive_sqlite, create_archive, insert_to_file)


# class TestArchiveSqlite:
#     @hypothesis.given(st.integers(), st.text(), st.text(), st.text(),
#                       st.text(), st.text(), st.text(),
#                       st.integers(min_value=0, max_value=4294967295))
#     def test_archive_post(self, no, name, trip, sub, com, filename, ext, date):
#         # Hardcoded test for 4chan.
#         create_archive("ar", "sqlite", "archive.db")
#         posts = [{"no": no, "name": name, "trip": trip, "sub": sub, "com": com,
#                   "filename": filename, "ext": ext, "time": date}]
#         archive_sqlite(posts, "archive.db", "4chan")
#         connection = sqlite3.connect("archive.db")
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM posts WHERE no = %d;" % no)
#         assert cursor.fetchall() == [(no, date, unescape(name), trip,
#                                       unescape(sub), unescape(com),
#                                       filename + ext if filename else None)]
#         cursor.execute("DELETE FROM posts WHERE no = %d;" % no)
#         connection.commit()

#         # Hardcoded test for Endchan.
#         posts = [{"threadId": no, "name": name, "id": trip, "subject": sub,
#                   "markdown": com, "filename": filename, "creation": date}]
#         archive_sqlite(posts, "archive.db", "endchan")
#         cursor.execute("SELECT * FROM posts WHERE no = %d;" % no)
#         assert cursor.fetchall() == [(no, date, unescape(name), trip,
#                                       unescape(sub), unescape(com),
#                                       filename or None)]
#         cursor.execute("DELETE FROM posts WHERE no = %d;" % no)
#         connection.commit()

#         # Hardcoded test for Nextchan.
#         # posts = [{"board_id": no, "author": name, "author_id": trip,
#         #           "subject": sub, "content_html": com, "filename": filename,
#         #           "created_at": date}]
#         # archive_sqlite(posts, "archive.db", "nextchan")
#         # cursor.execute("SELECT * FROM posts WHERE no = %d;" % no)
#         # results = list(cursor.fetchall())
#         # assert cursor.fetchall() == [(no, date, unescape(name), trip,
#         #                               unescape(sub), unescape(com),
#         #                               filename or None)]
#         cursor.close()
#         connection.close()
#         os.remove("archive.db")


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
