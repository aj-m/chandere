"""Command-line argument definitions."""

import argparse
import textwrap

from chandere2 import (__doc__, __version__)
from chandere2.context import CONTEXTS


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


PARSER = argparse.ArgumentParser(
    add_help=False,
    formatter_class=CustomHelp,
    usage="%(prog)s (TARGETS) [-i ALIAS] [OPTIONS]",
    description=textwrap.fill(__doc__.strip(), width=80)
)


DOCS = PARSER.add_argument_group("Documentation")
DOCS.add_argument(
    "-h",
    "--help",
    action="help",
    help="Display this help page and exit."
)
DOCS.add_argument(
    "-v",
    "--version",
    action="version",
    version="Chandere2 Version %s\n" % __version__ + "Developed by Jakob, "
    "released under the GNU GPLv3.\n",
    help="Display the currently installed version and exit."
)
DOCS.add_argument(
    "--list-imageboards",
    action="version",
    version="Available Imageboard Aliases: %s" % ", ".join(CONTEXTS),
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
    "--continuous",
    action="store_false",
    dest="run_once",
    help="Rather than exiting as soon as the scraping task has\ncompleted, "
    "continue to refresh for new posts until a\nSIGINT is received.\n\n"
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
    help="Indicates the path in which downloaded filess or\narchives should "
    "be placed. Defaults to \"./\".\n\n"
)
OUTPUT_OPTIONS.add_argument(
    "--output-format",
    metavar="FMT",
    default="ascii",
    help="Specify the format that output should be put into. Can\nbe either "
    "\"ascii\" or \"sqlite3\"."
)
