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

"""Functions for displaying output to the console. Should be used
instead of the print builtin as it takes verbosity into account.
"""

import sys

# See <https://stackoverflow.com/questions/4842424/>
ANSI_ESCAPE = "\033[{}m"
ANSI_RESET = "0"

verbose = False


def _ansi_escape(escape: str) -> str:
    """Wraps the given escape into an ANSI escape sequence."""
    return ANSI_ESCAPE.format(escape)


def _ansi_wrap(escape: str, line: str) -> str:
    """Applies an ANSI escape to the provided text, appending an ANSI
    reset to the end such that the escape does not affect anything
    printed following the line.
    """
    return _ansi_escape(escape) + line + _ansi_escape(ANSI_RESET)


def info(msg: str):
    """Displays a message to the console, if running in verbose mode."""
    if verbose:
        sys.stdout.write(msg + "\n")


def put(msg: str):
    """Displays a message to the console unconditionally."""
    sys.stdout.write(msg + "\n")


def error(msg: str):
    """Displays a message to the console unconditionally with scary red
    text to emphasize that a critical error has occurred.
    """
    sys.stdout.write(_ansi_wrap("38;5;9", "Critical Error: "))
    sys.stdout.write(msg + "\n")
