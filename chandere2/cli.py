"""Definitions for command-line arguments."""

import argparse
import textwrap

from chandere2 import (__doc__, __version__)
from chandere2.context import CONTEXTS


class CustomHelp(argparse.HelpFormatter):
    """Modifications to argparse's default HelpFormatter."""
    def _fill_text(self, text, width, indent):
        filled = []
        for line in text.splitlines(keepends=True):
            filled.append(indent + line)
        return "".join(filled)

    def _split_lines(self, text, width):
        return text.splitlines()

    def add_usage(self, usage, actions, groups, prefix=None):
        prefix = prefix or "Usage: "
        both = super(CustomHelp, self)
        return both.add_usage(usage, actions, groups, prefix)


PARSER = argparse.ArgumentParser(
    add_help=False,
    formatter_class=CustomHelp,
    usage="%(prog)s (TARGETS) [-i ALIAS] [OPTIONS]",
    description=textwrap.fill(__doc__.strip(), width=80)
)


META = PARSER.add_argument_group("Meta")
META.add_argument(
    "-h",
    "--help",
    action="help",
    help="Display this help page and exit."
)
META.add_argument(
    "-v",
    "--version",
    action="version",
    version="Chandere2 Version %s\n" % __version__ + "Developed by Jakob, "
    "released under the GNU GPLv3.\n",
    help="Display the currently installed version and exit."
)
META.add_argument(
    "--list-imageboards",
    action="version",
    version="Available Imageboard Aliases:\n * %s" % "\n * ".join(CONTEXTS),
    help="List known imageboard aliases and exit."
)


SCRAPER_OPTIONS = PARSER.add_argument_group("Scraping Options")
SCRAPER_OPTIONS.add_argument(
    "targets",
    metavar="TARGETS",
    nargs="+",
    help="Combination of a board and optionally a thread to scrape\nfrom. (E.g"
    ".\"/g/51971506\"). If a thread is not supplied,\nChandere2 will attempt "
    "to scrape the entire board.\nMultiple board/thread combinations can be "
    "given.\n\n"
)
SCRAPER_OPTIONS.add_argument(
    "-i",
    "--imageboard",
    metavar="X",
    default="4chan",
    help="Used to designate the imageboard to be scraped from.\nAvailable "
    "aliases can be listed with --list-imageboards.\n\n"
)
MODAL_OPTIONS = SCRAPER_OPTIONS.add_mutually_exclusive_group()
MODAL_OPTIONS.add_argument(
    "-d",
    "--download",
    action="store_const",
    const="fd",
    dest="mode",
    help="Crawl for and download every file in the given targets.\n\n"
)
MODAL_OPTIONS.add_argument(
    "-a",
    "--archive",
    action="store_const",
    const="ar",
    dest="mode",
    help="Archive every post in the given targets.\n\n"
)
SCRAPER_OPTIONS.add_argument(
    "--filter",
    metavar="x",
    default=[],
    nargs="*",
    dest="filters",
    help="A list of filters to check posts against. Filters should\nfollow "
    "the pattern of [field]:[pattern], where [field] is\nthe post field and "
    "[pattern] is a filtering pattern\nfollowing 4chan's \"Comment, Subject "
    "and E-mail\" filter\nformat. Patterns are case insensitive, and "
    "multiple\nfilters can be given.\n\n"
)
SCRAPER_OPTIONS.add_argument(
    "--continuous",
    action="store_true",
    help="Rather than exiting as soon as the task has completed,\ncontinue to "
    "refresh for new posts until a SIGINT is\nreceived.\n\n"
)
SCRAPER_OPTIONS.add_argument(
    "--ssl",
    action="store_true",
    help="Uses TLS/SSL encryption when making connections with "
    "the\nimageboard.\n\n"
)
SCRAPER_OPTIONS.add_argument(
    "--nocap",
    action="store_true",
    help="Will not attempt to limit the number of concurrent\nconnections. "
    "This can generate unreasonable amounts of\ntraffic and should only be "
    "used if you know what you're\ndoing."
)

OUTPUT_OPTIONS = PARSER.add_argument_group("Output Options")
OUTPUT_OPTIONS.add_argument(
    "--debug",
    action="store_true",
    help="Provides more detailed runtime information.\n\n"
)
OUTPUT_OPTIONS.add_argument(
    "-o",
    "--output",
    metavar="DIR",
    default=".",
    help="Indicates the path in which downloaded files or\narchives should "
    "be placed. Defaults to the current\nworking directory.\n\n"
)
OUTPUT_OPTIONS.add_argument(
    "--output-format",
    metavar="FMT",
    default="ascii",
    help="Specify the format that archives should be saved to. Can\nbe either "
    "\"plaintext\" or \"sqlite\"."
)
