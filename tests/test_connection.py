import asyncio
import unittest
import unittest.mock

import hypothesis
import hypothesis.strategies as st

from chandere2.connection import test_connection
from chandere2.output import Console

from tests.dummy_objects import FakeOutput


class GetConnectionHeadersTest(unittest.TestCase):
    def setUp(self):
        self.event_loop = asyncio.get_event_loop()
        self.fake_stdout = FakeOutput()
        self.fake_stderr = FakeOutput()
        self.fake_output = Console(output=self.fake_stdout,
                                   error=self.fake_stderr)

    def test_successful_connection(self):
        uris = ["a.4cdn.org/f/threads.json", "a.4cdn.org/g/threads.json"]
        self.event_loop.run_until_complete(
            test_connection(uris, False, self.fake_output)
        )
        self.assertIn(">", self.fake_stdout.last_received)

    def test_failed_connection(self):
        uris = ["a.4cdn.org/z/threads.json"]
        self.event_loop.run_until_complete(
            test_connection(uris, False, self.fake_output)
        )
        self.assertIn("FAILED:", self.fake_stderr.last_received)


## TODO: Clean up and improve test, change test names. <jakob@memeware.net>
# class GetContentTest(unittest.TestCase):
#     def setUp(self):
#         self.fake_stderr = FakeOutput()
#         self.fake_output = Console(output=FakeOutput(), error=self.fake_stderr)

#     def test_successful_content_fetch(self):
#         self.assertTrue(get_content("a.4cdn.org/g/threads.json", {},
#                                     False, self.fake_output))
    
#     def test_fetch_fail_on_nonexistent(self):
#         self.assertIs(get_content("a.4cdn.org/z/threads.json",
#                                   {"a.4cdn.org/z/threads.json": ()},
#                                   False, self.fake_output), None)
#         self.assertIn("does not exist.", self.fake_stderr.last_received)
        ## TEST THIS, REPLACE DICTIONARY WITH A REFERENCEABLE VARIABLE
        # self.assertNotIn("a.4cdn.org/z/threads.json")

    ## NO WORKING TEST THUS FAR
    # def test_fetch_fail_on_blocked(self):
    #     self.assertIs(get_content("a.4cdn.org/g/threads.json",
    #                               {"a.4cdn.org/g/threads.json": ()},
    #                               False, self.fake_output), None)
    #     self.assertIn("blocking web scrapers.", self.fake_stderr.last_received)

    ## NOT IMPLEMENTED, REQUIRES ARCHITECTURAL CHANGE.
    # # This is quite possibly the worst way to test this.
    # def test_fetch_fail_on_not_updated(self):
    #     self.assertTrue(get_content("a.4cdn.org/3/threads.json", {},
    #                                 False, self.fake_output))
    #     self.assertIs(get_content("a.4cdn.org/3/threads.json",
    #                               {"a.4cdn.org/z/threads.json": ()},
    #                               False, self.fake_output), None)
    #     self.assertIn("Page has not updated", self.fake_stderr.last_received)
