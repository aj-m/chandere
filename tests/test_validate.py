import os
import re
import unittest
import urllib.parse

import hypothesis
import hypothesis.strategies as st

from chandere2.validate import (convert_to_regexp, generate_uri,
                                get_filters, get_path, get_targets,
                                split_pattern, strip_target)


class GetPathTest(unittest.TestCase):
    # Expected permissions for the root directory and the CWD are not
    # hardcoded, as the permissions may vary on other machines.
    def test_check_output_permissions(self):
        self.assertEqual(os.access("/", os.W_OK), bool(get_path("/", "", "")))
        self.assertEqual(os.access(".", os.W_OK), bool(get_path(".", "", "")))
        self.assertEqual(os.access("/etc/hosts", os.W_OK),
                         bool(get_path("/etc/hosts", "", "")))

    # The following tests, however, assume that the CWD is writeable.
    def test_directory_for_file_downloading(self):
        self.assertEqual(get_path(".", "fd", ""), ".")
        self.assertIs(get_path("./a_file.txt", "fd", ""), None)

    def test_file_for_thread_archiving(self):
        self.assertEqual(get_path(".", "ar", "sqlite"), "./archive.db")
        self.assertEqual(get_path("./file.txt", "ar", ""), "./file.txt")
        self.assertEqual(get_path(".", "ar", ""), "./archive.txt")


class GenerateUriTest(unittest.TestCase):
    @hypothesis.given(st.text())
    def test_create_url_with_board(self, board):
        uri = generate_uri(board, None)
        self.assertIn(board, uri)
        self.assertIn("threads.json", uri)

    @hypothesis.given(st.text(), st.integers(min_value=0))
    def test_create_url_with_thread(self, board, thread):
        uri = generate_uri(board, str(thread))
        self.assertIn("/".join((board, "thread", str(thread))), uri)
        self.assertNotIn("threads.json", uri)

    def test_fail_on_unknown_imageboard(self):
        self.assertIs(generate_uri("g", "", imageboard="krautchan"), None)


class StripTargetTest(unittest.TestCase):
    @hypothesis.given(st.characters(blacklist_characters="/"))
    def test_strip_bare_board(self, target):
        expected_board = urllib.parse.quote(target.strip("/"), safe="/ ",
                                            errors="ignore")

        if not re.search(r"[^\s\/]", expected_board):
            expected_board = None

        self.assertEqual(strip_target(target), (expected_board, None))
        self.assertEqual(strip_target("/%s" % target), (expected_board, None))
        self.assertEqual(strip_target("%s/" % target), (expected_board, None))
        self.assertEqual(strip_target("/%s/" % target), (expected_board, None))

    @hypothesis.given(st.characters(blacklist_characters="/"),
                      st.integers(min_value=0))
    def test_strip_board_with_thread(self, target_board, target_thread):
        expected_thread = str(target_thread)
        expected_board = urllib.parse.quote(target_board.strip("/"),
                                            safe="/ ", errors="ignore")

        # If the given target lacks a valid board initial but a thread
        # is given, the subroutine will interpret the thread as a board.
        if not re.search(r"[^\s\/]", expected_board):
            expected_board = str(target_thread)
            expected_thread = None

        target = "/".join((target_board, str(target_thread)))
        self.assertEqual(strip_target(target),
                         (expected_board, expected_thread))


class GetTargetsTest(unittest.TestCase):
    @hypothesis.given(st.characters(blacklist_characters="/ "))
    def test_get_single_board(self, board):
        escaped = urllib.parse.quote(board, safe="/ ", errors="ignore").strip()
        # Hardcoded test for 4chan.
        if not escaped and not re.search(r"[^\s\/]", escaped):
            expected_result = {}
            expected_failed = [board]
        else:
            expected_uri = "a.4cdn.org/%s/threads.json" % escaped
            expected_result = {expected_uri: [escaped, False, ""]}
            expected_failed = []

        parsed, failed = get_targets([board], "4chan")
        self.assertEqual(parsed, expected_result)
        self.assertEqual(failed, expected_failed)

        # Hardcoded test for 8chan.
        if expected_result:
            expected_uri = "8ch.net/%s/threads.json" % escaped
            expected_result = {expected_uri: [escaped, False, ""]}

        parsed, failed = get_targets([board], "8chan")
        self.assertEqual(parsed, expected_result)
        self.assertEqual(failed, expected_failed)

        # Hardcoded test for Lainchan.
        if expected_result:
            expected_uri = "lainchan.org/%s/threads.json" % escaped
            expected_result = {expected_uri: [escaped, False, ""]}

        parsed, failed = get_targets([board], "lainchan")
        self.assertEqual(parsed, expected_result)
        self.assertEqual(failed, expected_failed)


    @hypothesis.given(st.characters(blacklist_characters="/"),
                      st.integers(min_value=0))
    def test_get_board_and_thread(self, board, thread):
        # Hardcoded tests for 4chan.
        target = "/".join((board, str(thread)))
        escaped = urllib.parse.quote(board, safe="/ ", errors="ignore").strip()

        if not re.search(r"[^\s\/]", escaped):
            expected_uri = "a.4cdn.org/%d/threads.json" % thread
            expected_result = {expected_uri: [str(thread), False, ""]}
        else:
            expected_uri = "a.4cdn.org/%s/thread/%s.json" % (escaped, thread)
            expected_result = {expected_uri: [escaped, True, ""]}

        parsed, failed = get_targets([target], "4chan")
        self.assertEqual(parsed, expected_result)
        self.assertFalse(failed)

        # Hardcoded tests for 8chan.
        target = "/".join((board, str(thread)))
        escaped = urllib.parse.quote(board, safe="/ ", errors="ignore").strip()

        if not re.search(r"[^\s\/]", escaped):
            expected_uri = "8ch.net/%d/threads.json" % thread
            expected_result = {expected_uri: [str(thread), False, ""]}
        else:
            expected_uri = "8ch.net/%s/res/%s.json" % (escaped, thread)
            expected_result = {expected_uri: [escaped, True, ""]}

        parsed, failed = get_targets([target], "8chan")
        self.assertEqual(parsed, expected_result)
        self.assertFalse(failed)

        # Hardcoded tests for Lainchan.
        target = "/".join((board, str(thread)))
        escaped = urllib.parse.quote(board, safe="/ ", errors="ignore").strip()

        if not re.search(r"[^\s\/]", escaped):
            expected_uri = "lainchan.org/%d/threads.json" % thread
            expected_result = {expected_uri: [str(thread), False, ""]}
        else:
            expected_uri = "lainchan.org/%s/res/%s.json" % (escaped, thread)
            expected_result = {expected_uri: [escaped, True, ""]}

        parsed, failed = get_targets([target], "lainchan")
        self.assertEqual(parsed, expected_result)
        self.assertFalse(failed)

    def test_fail_invalid_target(self):
        # Hardcoded test for 4chan.
        parsed, failed = get_targets(["/"], "4chan")
        self.assertFalse(parsed)
        self.assertIn("/", failed)

        # Hardcoded test for 8chan.
        parsed, failed = get_targets(["/"], "8chan")
        self.assertFalse(parsed)
        self.assertIn("/", failed)

        # Hardcoded test for Lainchan.
        parsed, failed = get_targets(["/"], "lainchan")
        self.assertFalse(parsed)
        self.assertIn("/", failed)


class ConvertToRegexpTest(unittest.TestCase):
    @hypothesis.given(st.characters(blacklist_characters="\n.?*+()[]\\/"))
    def test_ignore_expicit_regex(self, pattern):
        self.assertEqual(convert_to_regexp("/%s/" % pattern), pattern)
        self.assertEqual(convert_to_regexp("%s/%s/" % (pattern, pattern)),
                                           "%s%s" % (pattern, pattern))
        self.assertEqual(convert_to_regexp("/%s/%s" % (pattern, pattern)),
                                           "%s%s" % (pattern, pattern))

    @hypothesis.given(st.characters(blacklist_characters="\n*"))
    def test_escape_patterns(self, pattern):
        expected = pattern
        for character in ".?+()[]/\\":
            expected = expected.replace(character, "\\" + character)

        self.assertEqual(convert_to_regexp(pattern), expected)

    @hypothesis.given(st.characters(blacklist_characters="\n.?+()[]\\/"))
    def test_escape_patterns(self, pattern):
        expected = re.sub(r"\*(\s|$)", ".*", pattern)
        expected = re.sub(r"\*(?=\w)", ".", expected)

        self.assertEqual(convert_to_regexp(pattern), expected)


## TODO: Write a test for yielding final part. <jakob@memeware.net>
class SplitPatternTest(unittest.TestCase):
    @hypothesis.given(
        st.lists(
            elements=st.characters(blacklist_characters="\"")
        )
    )
    def test_use_and_operator(self, pattern):
        expected = list(filter(lambda x: x.strip(), pattern))
        self.assertEqual(list(split_pattern(" ".join(pattern))), expected)

    ## TODO: Clean up. <jakob@memeware.net>
    @hypothesis.given(
        st.lists(
            elements=st.characters(blacklist_characters="\"\n")
        ),
        st.lists(
            elements=st.characters(blacklist_characters="\"\n")
        ),
        st.lists(
            elements=st.characters(blacklist_characters="\"\n")
        )
    )
    def test_use_exact_match(self, prefix, exact, postfix):
        pattern = " \" ".join(map(" ".join, (prefix, exact, postfix)))

        expected = prefix if prefix else []
        if exact and "".join(exact).strip():
            expected.append(" ".join(exact).strip())
        if postfix:
            expected += postfix

        expected = filter(lambda x: not re.search(r"^\s*$", x), expected)

        self.assertEqual(sorted(list(split_pattern(pattern))), sorted(expected))


class GetFiltersTest(unittest.TestCase):
    @hypothesis.given(st.characters(blacklist_characters=":"),
                      st.characters(blacklist_characters=":"))
    def test_evaluate_filters(self, field, pattern):
        if not re.search(r"[^\s]", pattern.strip()):
            return

        # Imageboard is unimportant to the subroutine at this point.
        evaluated, failed = get_filters([":".join((field, pattern))], "4chan")
        evaluated_field, evaluated_pattern = evaluated[0]
        self.assertEqual(evaluated_field, field)
        self.assertEqual(evaluated_pattern, convert_to_regexp(pattern))
        self.assertFalse(failed)

    @hypothesis.given(st.characters(blacklist_characters=":"))
    def test_evaluate_failed(self, pattern):
        # Imageboard is unimportant to the subroutine at this point.
        evaluated, failed = get_filters([pattern], "4chan")
        self.assertFalse(evaluated)
        self.assertEqual(failed, [pattern])
