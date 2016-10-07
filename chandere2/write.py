"""Module for formatting and writing information to disk."""

import re
import textwrap
import time

from chandere2.context import CONTEXTS

SUBSTITUTIONS = ((r'<p class="body-line empty "><\/p>', "\n\n"),
                 (r'<\/p>(?=<p class="body-line ltr ">)', "\n"),
                 (r"<\/?br\\?\/?>", "\n"), (r"&#039;", "'"), (r"&gt;", ">"),
                 (r"&quot;", r"\\"), (r"&amp;", "&"), (r"<.+?>", ""),
                 (r"\\/", "/"))


def ascii_format_post(post: dict, imageboard: str):
    """Returns an ASCII-formtted version of the given post."""
    context = CONTEXTS.get(imageboard)
    no, date, name, trip, sub, com, filename, ext = context.get("post_fields")

    body = post.get(com)
    for pattern, substitution in SUBSTITUTIONS:
        body = re.sub(pattern, substitution, body)

    if post.get(filename) and post.get(ext):
        filename = ".".join((post.get(filename), post.get(ext)))

    date = time.ctime(post.get(date))
    subject = "\n\"%s\"" % post.get(sub) if post.get(sub) else ""
    tripcode = "!" + post.get(trip) if post.get(trip) else ""
    
    formatted = "*" * 80 + "\nPost: %s\n" % post.get(no)
    formatted += "\n%s%s on %s" % (post.get(name), tripcode, date)
    formatted += "%s\nFile: %s\n" % (subject, filename) + "*" * 80
    formatted += "\n"

    wrap = lambda line: textwrap.wrap(line, width=80, replace_whitespace=False)
    formatted += "\n".join("\n".join(wrap(line)) for line in body.splitlines())
    formatted += "\n" + "*" * 80

    return formatted
