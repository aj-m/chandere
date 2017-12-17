import importlib
from urllib.parse import unquote

import hypothesis
import hypothesis.strategies as st

Scraper = importlib.import_module("chandere.websites.4chan").Scraper


class Test4chan:
    @hypothesis.given(st.text())
    def test_catalog_url(self, board: str):
        assert board in unquote(Scraper._catalog_url(board))
