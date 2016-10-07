import time
import unittest

import hypothesis
import hypothesis.strategies as st

from chandere2.write import ascii_format_post


class AsciiFormatPostTest(unittest.TestCase):
    ## TODO: Clean up. <jakob@memeware.net>
    @hypothesis.given(st.integers(),
                      st.integers(min_value=0, max_value=4294967295),
                      st.text(), st.text(), st.text(), st.text(), st.text(),
                      st.text())
    def test_format_post(self, no, date, name, trip, sub, com, filename, ext):
        # Hardcoded test for 4chan, 8chan, and Lainchan.
        post = {"no": no, "time": date, "name": name, "trip": trip, "sub": sub,
                "com": com, "filename": filename, "ext": ext}
        formatted = ascii_format_post(post, "4chan")
        self.assertIn("Post: %s" % no, formatted)
        self.assertIn(time.ctime(date), formatted)
        if name:
            self.assertIn(name, formatted)
        if trip:
            self.assertIn("!%s" % trip, formatted)
        if sub:
            self.assertIn("\"%s\"" % sub, formatted)
        if filename and ext:
            self.assertIn(".".join((filename, ext)), formatted)
