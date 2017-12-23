# Copyright (C) 2017 Jakob Kreuze, All Rights Reserved.
#
# This file is part of Chandere.
#
# Chandere is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Chandere is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with Chandere. If not, see <http://www.gnu.org/licenses/>.

"""Tasks related to self-documentation and definitions for the
command-line arguments recognized by Chandere.
"""

import argparse
import sys
import textwrap

from chandere import __doc__, __version__, output
from chandere.loader import list_actions, list_scrapers
from chandere.loader import load_action, load_scraper

HELP_INDENT_WIDTH = 24


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


class ActionsAction(argparse.Action):
    """Lists all action modules."""
    def __call__(self, parser, namespace, values, option_string=None):
        for action in list_actions():
            module = load_action(action)

            if hasattr(module, "__doc__"):
                description = module.__doc__
            else:
                description = "[No description provided]"

            if hasattr(module, "__author__"):
                author = module.__author__
            else:
                author = "[Unknown]"

            if hasattr(module, "__version__"):
                version = module.__version__
            else:
                version = "[Unknown]"

            output.put("{} - '{}'".format(action, description))
            output.info("By {}, version {}".format(
                author,
                version
            ))
            output.info("")
        sys.exit(0)


class ScrapersAction(argparse.Action):
    """Lists all scraping modules."""
    def __call__(self, parser, namespace, values, option_string=None):
        for website in list_scrapers():
            module = load_scraper(website)

            if hasattr(module, "__doc__"):
                description = module.__doc__
            else:
                description = "[No description provided]"

            if hasattr(module, "__author__"):
                author = module.__author__
            else:
                author = "[Unknown]"

            if hasattr(module, "__version__"):
                version = module.__version__
            else:
                version = "[Unknown]"

            output.put("{} - '{}'".format(website, description))
            output.info("By {}, version {}".format(
                author,
                version
            ))
            output.info("")
        sys.exit(0)


# Implemented as an action, so that verbosity can be checked by both
# ActionsAction and ScrapersAction.
class VerbosifyAction(argparse.Action):
    """Updates the verbose property of the output module."""
    def __call__(self, parser, namespace, values, option_string=None):
        output.verbose = True


# Touching private data members like this is probably going to break
# some time in the future, lmfao. Maybe at this point I should have just
# written my own argument parser.
class CustomHelpAction(argparse._HelpAction):
    """A context-aware help action, which displays help related to the
    specified website and action in addition to a description of the
    arguments not related to any modules.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        action = load_action(namespace.action)
        scraper = load_scraper(namespace.website)
        formatter = parser._get_formatter()

        formatter.add_usage(
            parser.usage,
            parser._actions,
            parser._mutually_exclusive_groups
        )

        formatter.add_text(parser.description)
        for action_group in parser._action_groups:
            formatter.start_section(action_group.title)
            formatter.add_text(action_group.description)
            formatter.add_arguments(action_group._group_actions)
            formatter.end_section()
        formatter.add_text(parser.epilog)

        if hasattr(action, "PARSER"):
            formatter.start_section("'{}' Options".format(namespace.action))
            for action_group in action.PARSER._action_groups:
                formatter.add_arguments(action_group._group_actions)
            formatter.end_section()

        if hasattr(scraper, "PARSER"):
            formatter.start_section("'{}' Options".format(namespace.website))
            for action_group in scraper.PARSER._action_groups:
                formatter.add_arguments(action_group._group_actions)
            formatter.end_section()

        sys.stdout.write(formatter.format_help())
        sys.exit(0)


def reorder_args(args: list) -> list:
    """Reorders all arguments such that anything found in ACTION_ARGS is
    pushed back to the end of the argument vector.
    """
    rest = list(filter(lambda x: x not in ACTION_ARGS, args))
    deferred = list(filter(lambda x: x in ACTION_ARGS, args))
    return rest + deferred


def wrap(line: str, end="\n"):
    """Wraps the line such that, when included in the help page
    generated by argparse, the entire help line fits within a standard
    80 columns.
    """
    return textwrap.fill(line.strip(), width=80 - HELP_INDENT_WIDTH) + end


# This is a fragile way of dealing with action deferral. Because
# arguments such as -w and -v can affect how certain actions are
# performed, they are pushed to the end of the argument vector. Every
# time an argument that invokes an action is added PARSER, it is also
# added to ACTION_ARGS, which gets used by reorder_args.
ACTION_ARGS = []


PARSER = argparse.ArgumentParser(
    add_help=False,
    formatter_class=CustomHelp,
    usage="%(prog)s TARGETS [OPTIONS]",
    description=wrap(__doc__)
)
PARSER.register("action", "actions", ActionsAction)
PARSER.register("action", "scrapers", ScrapersAction)
PARSER.register("action", "verbosify", VerbosifyAction)
PARSER.register("action", "help", CustomHelpAction)


DOCUMENTATION = PARSER.add_argument_group("Documentation")
DOCUMENTATION.add_argument(
    "-h",
    "--help",
    action="help",
    help=wrap(
        "Display this help page and exit."
    )
)
ACTION_ARGS.append("-h")
ACTION_ARGS.append("--help")
DOCUMENTATION.add_argument(
    "-V",
    "--version",
    action="version",
    version=__version__,
    help=wrap(
        "Display the current version and exit."
    )
)
ACTION_ARGS.append("-V")
ACTION_ARGS.append("--version")
DOCUMENTATION.add_argument(
    "--list-actions",
    action="actions",
    nargs=0,
    help=wrap(
        "Display all actions that can be specified with -a."
    )
)
ACTION_ARGS.append("--list-actions")
DOCUMENTATION.add_argument(
    "--list-websites",
    action="scrapers",
    nargs=0,
    help=wrap(
        "Display all websites that can be specified with -w."
    )
)
ACTION_ARGS.append("--list-websites")


SCRAPER_OPTIONS = PARSER.add_argument_group("Scraping Options")
SCRAPER_OPTIONS.add_argument(
    "targets",
    metavar="TARGETS",
    nargs="+",
    help=wrap(
        "The targets to download from."
    )
)
SCRAPER_OPTIONS.add_argument(
    "-a",
    "--action",
    metavar="X",
    default="download",
    help=wrap(
        "The action to be performed on all collected posts. Defaults to "
        "'download', which will download every file in the provided targets."
    )
)
SCRAPER_OPTIONS.add_argument(
    "-w",
    "--website",
    metavar="X",
    default="4chan",
    help=wrap(
        "The website to scrape from. Defaults to '4chan'."
    )
)
SCRAPER_OPTIONS.add_argument(
    "--custom-action",
    metavar="X",
    help=wrap(
        "Path to a python script exposing the action API to be used."
    )
)
SCRAPER_OPTIONS.add_argument(
    "--custom-scraper",
    metavar="X",
    help=wrap(
        "Path to a python script exposing the scraping API to be used."
    )
)


OUTPUT_OPTIONS = PARSER.add_argument_group("Output Options")
OUTPUT_OPTIONS.add_argument(
    "-v",
    "--verbose",
    action="verbosify",
    nargs=0,
    help=wrap(
        "Provides more verbose runtime information."
    )
)
ACTION_ARGS.append("-v")
ACTION_ARGS.append("--verbose")
