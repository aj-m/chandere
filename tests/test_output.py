import unittest

import hypothesis
import hypothesis.strategies as st

from chandere2.output import Console

from tests.dummy_output import FakeOutput


class OutputTest(unittest.TestCase):
    def setUp(self):
        self.fake_stderr = FakeOutput()
        self.fake_stdout = FakeOutput()
        self.output = Console(output=self.fake_stdout,
                              error=self.fake_stderr)

    @hypothesis.given(st.lists(st.text()))
    def test_write(self, text):
        self.output.write(*text)
        self.assertEqual(self.fake_stdout.last_received,
                         " ".join(text) + "\n")

    @hypothesis.given(st.text(), st.text())
    def test_write_if_debug(self, info, debug):
        self.output.debug = False
        self.output.write(info)
        self.output.write_debug(debug)
        self.assertEqual(self.fake_stdout.last_received,
                         info + "\n")

        self.output.debug = True
        self.output.write_debug(debug)
        self.assertEqual(self.fake_stdout.last_received,
                         "DEBUG: %s\n" % debug)

    @hypothesis.given(st.lists(st.text()))
    def test_write_stderr(self, text):
        self.output.write_error(*text)
        self.assertEqual(self.fake_stderr.last_received,
                         "ERROR: %s\n" % " ".join(text))

    @hypothesis.given(st.text(), st.text())
    def test_supply_end(self, text, end):
        self.output.debug = True
        self.output.write(text, end=end)
        self.assertEqual(self.fake_stdout.last_received,
                         text + end)
        self.output.write_debug(text, end=end)
        self.assertEqual(self.fake_stdout.last_received,
                         "DEBUG: " + text + end)
        self.output.write_error(text, end=end)
        self.assertEqual(self.fake_stderr.last_received,
                         "ERROR: " + text + end)
