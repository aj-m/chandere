"""Module for getting content from an imageboards's JSON models."""

import asyncio
import json

from chandere2.uri import generate_uri


# def get_current_threads(listing: str, info: tuple) -> list:
#     """[Document me!]"""
#     for page in (page.get("threads") for page in json.loads(listing)):
#         for thread_no in (thread.get("no") for thread in page):
#             yield generate_uri(info.get(""))
