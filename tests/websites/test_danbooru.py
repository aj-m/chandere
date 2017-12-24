import pytest

from chandere.errors import ChandereError
from chandere.loader import load_scraper

scraper = load_scraper("danbooru")

VALID_TARGETS = [
    ("touhou yuri", "touhou+yuri"),
    ("rating:q", "rating%3Aq")
]


def test_parse_valid_targets():
    for target, expected in VALID_TARGETS:
        assert scraper.parse_target(target) == expected
