"""Definitions for command-line arguments."""

import argparse
import textwrap

from chandere2 import (__doc__, __version__)


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
    usage="%(prog)s (TARGETS) [-c CHAN] [OPTIONS]",
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


connection_opts = parser.add_argument_group("Connection Options")
connection_opts.add_argument(
    "targets",
    metavar="TARGETS",
    nargs="+",
    help="Combination of a board and optionally a thread to scrape\nfrom. (E.g"
    ".\"/g/51971506\"). If a thread is not given,\nChandere will attempt to "
    "scrape the entire board.\nMultiple board/thread combinations can be "
    "given.\n\n"
)


output_opts = parser.add_argument_group("Output Options")
output_opts.add_argument(
    "--debug",
    action="store_true",
    help="Provides more detailed runtime information.\n\n"
)
