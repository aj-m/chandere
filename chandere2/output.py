"""A more versatile wrapper for program output."""

import sys


class Console(object):
    """Versatile output wrapper. Writes to sys.stdout and sys.stderr by
    default, but this can be changed via parameters to the constructor.
    """
    def __init__(self, debug=False, output=sys.stdout, error=sys.stderr):
        self.debug = debug
        self.error = error
        self.output = output

    def write(self, *args, end="\n"):
        """Joins and writes the given arguments to the Console's
        assigned output, which in most cases will be sys.stdout.
        """
        self.output.write(" ".join(map(str, args)) + end)

    def write_debug(self, *args, end="\n"):
        """Wrapper for Console.write, which will prefix the given
        arguments with "DEBUG:" and only write them if Console.debug is
        enabled.
        """
        if self.debug: self.write("DEBUG:", *args, end=end)

    def write_error(self, *args, end="\n"):
        """Joins and writes the given arguments prefixed with "ERROR: "
        to the Console's designated error output, which will typically
        be sys.stderr.
        """
        self.error.write("ERROR: " + " ".join(map(str, args)) + end)
