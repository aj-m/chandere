"""Command-line argument definitions."""

import argparse
import textwrap

from chandere2 import (__doc__, __version__)
from chandere2.uri import KNOWN_IMAGEBOARDS


class CustomHelp(argparse.HelpFormatter):
    """Formatting modifications to argparse's default HelpFormatter."""
    def _fill_text(self, text, width, indent):
        return "".join(indent + line
                       for line in text.splitlines(keepends=True))

    def _split_lines(self, text, width):
        return text.splitlines()

    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = "Usage: "
        return super(CustomHelp, self).add_usage(usage, actions, groups,
                                                 prefix)


parser = argparse.ArgumentParser(
    add_help=False,
    formatter_class=CustomHelp,
    usage="%(prog)s (TARGETS) [-i CHAN] [OPTIONS]",
    description=textwrap.fill(__doc__.strip(), width=80)
)


docs = parser.add_argument_group("Documentation")
docs.add_argument(
    "-h",
    "--help",
    action="help",
    help="Display this help page and exit."
)
docs.add_argument(
    "-v",
    "--version",
    action="version",
    version="Chandere2, version %s" % __version__,
    help="Display the currently installed version and exit."
)
docs.add_argument(
    "--list-imageboards",
    action="version",
    version="Available Imageboard Aliases: %s" % ", ".join(KNOWN_IMAGEBOARDS),
    help="List known imageboard aliases and exit."
)


scraper_opts = parser.add_argument_group("Scraper Options")
modal_opts = scraper_opts.add_mutually_exclusive_group()
modal_opts.add_argument(
    "-d",
    "--download",
    action="store_const",
    const="fd",
    dest="mode",
    help="Download every file in a thread, or crawl for every\nfile on "
    "a board if a thread is not specified.\n\n"
)
modal_opts.add_argument(
    "-a",
    "--archive",
    action="store_const",
    const="ar",
    dest="mode",
    help="Archive every post in a thread to plaintext, or crawl\nfor "
    "every post on a board if a thread is not specified.\n\n"
)
scraper_opts.add_argument(
    "targets",
    metavar="TARGETS",
    nargs="+",
    help="Combination of a board and optionally a thread to scrape\nfrom. (E.g"
    ".\"/g/51971506\"). If a thread is not given,\nChandere2 will attempt to "
    "scrape the entire board.\nMultiple board/thread combinations can be "
    "given.\n\n"
)
scraper_opts.add_argument(
    "-i",
    "--imageboard",
    default="4chan",
    help="Used to designate the imageboard to be scraped from.\nAvailable "
    "aliases can be listed with --list-imageboards.\n\n"
)
scraper_opts.add_argument(
    "--continuous",
    action="store_false",
    dest="run_once",
    help="Rather than exiting as soon as the scraping task has\ncompleted, "
    "continue to refresh for new posts until a\nSIGINT is received.\n\n"
)
scraper_opts.add_argument(
    "--ssl",
    action="store_true",
    help="Uses HTTPS if it is available.\n\n"
    # Redoc this
)


output_opts = parser.add_argument_group("Output Options")
output_opts.add_argument(
    "--debug",
    action="store_true",
    help="Provides more detailed runtime information.\n\n"
)
output_opts.add_argument(
    "-o",
    "--output",
    metavar="DIR",
    default=".",
    help="Indicates the path in which downloaded filess or\narchives should "
    "be placed. Defaults to \"./\".\n\n"
)
# output_opts.add_argument(
#     "--output-format",
#     metavar="FMT",
#     default="ascii",
#     help="Specify the format that output should be put into."
#     # Redoc this.
# )