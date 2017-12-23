from urllib.parse import unquote

import hypothesis
import hypothesis.strategies as st

from chandere.loader import load_scraper


@hypothesis.given(st.text())
def test_catalog_url(board: str):
    scraper = load_scraper("4chan")
    assert board in unquote(scraper._catalog_url(board))
