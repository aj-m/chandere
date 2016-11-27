"""Module for writing scrapad data to disk."""

import os.path
import re
import sqlite3

from chandere2.context import CONTEXTS
from chandere2.post import (ascii_format_post, unescape)


def archive_sqlite(posts: list, path: str, board: str, imageboard: str):
    """Connects to the Sqlite database located at the given path, and
    creates an entry for every post given.
    """
    connection = sqlite3.connect(path)
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS %s (no INTEGER " % board
                   + "PRIMARY KEY NOT NULL, time INTEGER NOT NULL, name TEXT "
                   "NOT NULL, trip TEXT, sub TEXT, com TEXT, filename TEXT);")


    context = CONTEXTS.get(imageboard)
    no, date, name, trip, sub, com, filename, ext = context.get("post_fields")

    for post in posts:
        if post.get(filename):
            if ext:
                filename = post.get(filename) + post.get(ext)
            else:
                filename = post.get(filename)
        else:
            filename = None

        cursor.execute("SELECT * FROM %s WHERE no = ?;" % board,
                       (post.get(no),))
        if cursor.fetchall():
            continue

        cursor.execute("INSERT INTO %s (no, time, name, trip, sub, " % board
                       + "com, filename) VALUES (?, ?, ?, ?, ?, ?, ?);",
                       (post.get(no), post.get(date),
                        unescape(post.get(name, "")), post.get(trip),
                        unescape(post.get(sub, "")),
                        unescape(post.get(com, "")),
                        filename))

    connection.commit()


def archive_plaintext(posts: list, path: str, imageboard: str):
    """Opens the text file located at the given path and inserts a
    formatted version of each post found in the content.
    """
    context = CONTEXTS.get(imageboard)
    no = context.get("post_fields")[0]
    parent = None

    resto = context.get("resto")
    alternative_no, _ = context.get("thread_fields")

    with open(path, "r+") as output_file:
        for post in posts:
            formatted = ascii_format_post(post, imageboard)
            insert_to_file(output_file, formatted, parent, post.get(no))

            if resto and post.get(resto) == 0 or post.get(resto) == None:
                parent = post.get(no)
            elif not resto and post.get(alternative_no):
                parent = post.get(alternative_no)


def insert_to_file(output_file, post: str, parent_id: str, post_id: str):
    """Finds the location of a given parent post in a text file, and
    inserts a post directly below it if a parent id is specified.
    Otherwise appends it to the bottom of the file.
    """
    output_file.seek(0)
    content = output_file.read()

    if re.search(r"Post ID: %s\n" % post_id, content):
        pass

    else:
        search = re.search(r"Post ID: %s\n.*?={80}(?=\n\n)" % parent_id,
                           content, re.DOTALL)

        if parent_id and search:
            split = search.end()
            content = content[:split + 1] + post.strip() + content[split + 1:]
            output_file.seek(0)
            output_file.write(content + "\n")
        else:
            output_file.seek(0, 2)
            output_file.write(post + "\n\n\n")


def create_archive(mode: str, output_format: str, path: str):
    """Creates the archive file if it doesn't already exist, provided
    that the mode and output_format would require the file to exist.
    """
    if mode == "ar" and not os.path.exists(path):
        if output_format == "plaintext":
            with open(path, "w"):
                pass
