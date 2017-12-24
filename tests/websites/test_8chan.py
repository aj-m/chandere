import pytest

from chandere.errors import ChandereError
from chandere.loader import load_scraper

scraper = load_scraper("8chan")

VALID_CROSSLINK_TARGETS = [
    ("/tech/589254", ("tech", "589254")),
    ("/tech/ 589254", ("tech", "589254")),
    ("tech/589254", ("tech", "589254")),
    ("/tech 589254", ("tech", "589254")),
    ("tech 589254", ("tech", "589254")),
    ("/tech/", ("tech", None)),
    ("/tech", ("tech", None)),
    ("tech/", ("tech", None)),
    ("tech", ("tech", None)),
]

INVALID_CROSSLINK_TARGETS = [
    "/"
]

VALID_URI_TARGETS = [
    ("https://8ch.net/tech/res/589254.html", ("tech", "589254")),
    ("http://8ch.net/tech/res/589254.html", ("tech", "589254")),
    ("https://8ch.net/tech/res/589254.json", ("tech", "589254")),
    ("http://8ch.net/tech/res/589254.json", ("tech", "589254")),
    ("https://8ch.net/tech/", ("tech", None)),
    ("http://8ch.net/tech/", ("tech", None)),
]

INVALID_URI_TARGETS = [
    "https://8ch.net/",
    "http://8ch.net/",
    "https://google.com/",
    "http://google.com/",
]


def test_parse_valid_uri_target():
    for target, expected in VALID_URI_TARGETS:
        assert scraper.parse_target(target) == expected


def test_parse_invalid_uri_target():
    for target in INVALID_URI_TARGETS:
        with pytest.raises(ChandereError):
            scraper.parse_target(target)


def test_parse_valid_crosslink_target():
    for target, expected in VALID_CROSSLINK_TARGETS:
        assert scraper.parse_target(target) == expected


def test_parse_invalid_crosslink_target():
    for target in INVALID_CROSSLINK_TARGETS:
        with pytest.raises(ChandereError):
            scraper.parse_target(target)
