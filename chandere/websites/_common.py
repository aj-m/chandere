# Copyright (C) 2017 Jakob Kreuze, All Rights Reserved.
#
# This file is part of Chandere.
#
# Chandere is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Chandere is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with Chandere. If not, see <http://www.gnu.org/licenses/>.

"""Common functionality for writing scraper modules."""

from urllib.parse import quote
import re


def contains_uri_scheme(target: str) -> bool:
    """Returns whether or not a target contains a URI scheme. RFC 1738
    states that two forward slashes following the colon are not required
    for all schemes, but this function does indeed check for them.
    """
    return re.search(r":\/\/", target) is not None


def parse_crosslink(target: str) -> tuple:
    """Parses a target of a format loosely based on the "crosslink"
    feature of imageboards, which is when users reference a post from
    another board like ">>>/g/51971506" or just ">>>/g/". This function
    allows the forward slashes to be omited.

    Args:
        target: The raw target string.

    Returns:
        Tuple containing the board's initial, followed by a thread
        number. If either field is not present in the target string, it
        will have a value of None in the returned tuple.
    """
    target = quote(target, safe="/ ", errors="ignore").strip()

    match = re.search(r"(?<=\/)?[^\s\/]+(?=[\/ ])?", target)
    board = match.group() if match else None

    match = re.search(r"(?<=[^\s][\/ ])\d+(?=\/)?", target)
    thread = match.group() if match else None

    return (board, thread)


def parse_imageboard_uri_factory(ext: str, thread_dir: str) -> tuple:
    """Returns an anonymous function for stripping the board initial and
    thread number from some URI pointing to an imageboard.

    Args:
        ext: The TLD extension of the imageboard. 4chan.org, for
            example, would be "org".
        thread_dir: The directory which precedes the thread number in
            the URI. 4chan.org, for example, would be "thread".

    Returns:
        An anonymous function taking a raw target string as a parameter,
        and returning a tuple containing the board's initial, followed
        by a thread number. If either field is not present in the target
        string, it will have a value of None in the returned tuple.
    """
    board_regex = r"(?<={}\/)[^\s\/]+(?=[\/ ])?".format(ext)
    thread_regex = r"(?<={}\/)\d+(?=\/)?".format(thread_dir)

    def parse_uri(target: str) -> tuple:
        target = quote(target, safe="/ ", errors="ignore").strip()

        match = re.search(board_regex, target)
        board = match.group() if match else None

        match = re.search(thread_regex, target)
        thread = match.group() if match else None

        return (board, thread)

    return parse_uri
