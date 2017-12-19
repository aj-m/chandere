import hypothesis
import hypothesis.strategies as st

from chandere.cli import _wrap

@hypothesis.given(st.text())
def test_wrap(text: str):
    for line in _wrap(text):
        assert len(line) < 80
