"""Command-line argument definitions."""

import argparse
import textwrap

from chandere import (__doc__, __version__)


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
    usage="%(prog)s (TARGETS) [-s ALIAS] [OPTIONS]",
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
    "-V",
    "--version",
    action="version",
    version=__version__,
    help="Display the currently installed version and exit."
)


SCRAPER_OPTIONS = PARSER.add_argument_group("Scraping Options")
SCRAPER_OPTIONS.add_argument(
    "targets",
    metavar="TARGETS",
    nargs="+",
    help="Targets to download from.\n\n"
)
SCRAPER_OPTIONS.add_argument(
    "-s",
    "--source",
    metavar="X",
    default="4chan",
    help="The website to be scraped from.\n\n"
)


OUTPUT_OPTIONS = PARSER.add_argument_group("Output Options")
OUTPUT_OPTIONS.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="Provides more verbose runtime information.\n\n"
)
OUTPUT_OPTIONS.add_argument(
    "-o",
    "--output",
    metavar="DIR",
    default=".",
    help="The path in which downloaded resources or archives should be "
    "placed. Defaults to the current working directory.\n\n"
)
