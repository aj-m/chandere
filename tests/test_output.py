import hypothesis
import hypothesis.strategies as st

from chandere2.output import Console

from dummy_output import FakeOutput


class TestOutput:
    # Asserts that the text is successfully joined and written.
    @hypothesis.given(st.lists(st.text()))
    def test_write(self, text):
        fake_stderr = FakeOutput()
        fake_stdout = FakeOutput()
        output = Console(output=fake_stdout, error=fake_stderr)

        output.write(*text)
        assert fake_stdout.last_received == " ".join(text) + "\n"

    # Asserts that write_debug only writes when output.debug is True.
    @hypothesis.given(st.text(), st.text())
    def test_write_if_debug(self, info, debug):
        fake_stderr = FakeOutput()
        fake_stdout = FakeOutput()
        output = Console(output=fake_stdout, error=fake_stderr)

        output.write(info)
        output.write_debug(debug)
        assert fake_stdout.last_received == info + "\n"

        output.debug = True
        output.write(info)
        output.write_debug(debug)
        assert fake_stdout.last_received == "DEBUG: %s\n" % debug

    # Asserts that the text is written to stderr with "ERROR: ".
    @hypothesis.given(st.lists(st.text()))
    def test_write_stderr(self, text):
        fake_stderr = FakeOutput()
        fake_stdout = FakeOutput()
        output = Console(output=fake_stdout, error=fake_stderr)

        output.write_error(*text)
        assert fake_stderr.last_received == "ERROR: %s\n" % " ".join(text)

    # Asserts that an end is properly appended to all written text.
    @hypothesis.given(st.text(), st.text())
    def test_supply_end(self, text, end):
        fake_stderr = FakeOutput()
        fake_stdout = FakeOutput()
        output = Console(output=fake_stdout, error=fake_stderr)

        output.debug = True
        output.write(text, end=end)
        assert fake_stdout.last_received == text + end

        output.write_debug(text, end=end)
        assert fake_stdout.last_received == "DEBUG: " + text + end

        output.write_error(text, end=end)
        assert fake_stderr.last_received == "ERROR: " + text + end
