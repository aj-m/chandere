#!/usr/bin/env python

"""JABS, or Jakob's Awesome Build Script is a tool for collecting
multiple Python source files and compiling them into a single,
portable Python script.
"""

import os.path
import re
import sys

__author__ = "Jakob Tsar-Fox <jakob@memeware.net>"
__licence__ = "GPLv3"
__version__ = "1.0.0.dev1"

COLORS = {"okay": "\033[m",
          "error": "\033[91m",
          "warning": "\033[93m",
          "good": "\033[92m"}

EOL = "\n"

PACKAGE_NAME = "chandere2"
ENTRY_POINT = "__main__.py"
METADATA = "__init__.py"
SOURCES = ("cli.py", "connection.py", "context.py", "core.py",
           "output.py", "post.py", "validate.py", "write.py")


def write_message(text: str, level="okay") -> None:
    """Writes the given text with the given loglevel."""
    text = "[%s*%s] " % (COLORS.get(level, "okay"), COLORS["okay"]) + text
    output = sys.stderr if level == "error" else sys.stdout
    output.write(text + "\n")


def get_package_metadata(source) -> tuple:
    """Finds the package description, and a list containing any other
    metadata embedded in the given source file.
    """
    source_content = source.read()
    metadata = []
    description_match = re.search(r"\"\"\".*?\"\"\"", source_content, re.S)
    if description_match:
        package_description = description_match.group()
    else:
        package_description = "\"\"\"[No Script Docstring]\"\"\""
    for variable in re.findall(r"__.+?__ = .+", source_content):
        metadata.append(variable)
    return (package_description, metadata)


def get_package_entry_point(source) -> str:
    """Finds the package's entry point."""
    entry_point_match = re.search(r"if __name__ == \"__main__\":.*", source.read(), re.S)
    return entry_point_match.group() if entry_point_match else None


def find_import_statements(source) -> list:
    """Given a readable source file, extracts every import statements
    and returns a list containing them. Import statements containing
    the PACKAGE_NAME are discarded.
    """
    import_statements = []
    lines = source.read().split(EOL)
    text = ""
    for index, line in enumerate(lines):
        statement = re.search(r"(from .*)?import .*", line)
        if statement:
            text = statement.group().strip()
            if PACKAGE_NAME in text:
                text = ""
                continue

            # Unpaired parentheses in an if statement imply that there's
            # more to it, but is continued on a separate line. Text is a
            # variable in the local scope that only gets cleared out
            # when the import statement has been accounted for.
            elif text.count("(") > text.count(")"):
                pass

            else:
                import_statements.append(text)
                text = ""
        elif text:
            text += " " + line.strip()
            if ")" in text:
                import_statements.append(text)
    return import_statements


def write_metadata(destination, metadata: tuple) -> None:
    """Writes package metadata to the given destination file."""
    description, metadata_variables = metadata
    metadata_text = "\n".join((description, "\n".join(metadata_variables)))
    destination.write(metadata_text + "\n\n")


def write_import_statements(destination, import_statements: list) -> None:
    """Writes the import statements to the given destination."""
    destination.write("\n".join(sorted(set(import_statements))) + "\n\n")


def write_entry_point(destination, entry_point: str) -> None:
    """Writes the entry point to the given destination."""
    destination.write(entry_point + "\n")


def parse_arguments(argv: list) -> None:
    """Handles improper usage of the script, as well as writing help and
    versioning info if requested.
    """
    if len(argv) != 2:
        write_message("USAGE: %s (OUTPUT)" % argv[0], "error")
        sys.exit(1)
    elif argv[1] == "-h" or argv[1] == "--help":
        write_message("JABS - Jakob's Awesome Build Script", "good")
        write_message("USAGE: %s (OUTPUT)" % argv[0])
        write_message("Options:")
        write_message("-h, --help\t\tPrint this help page and exit.")
        write_message("-v, --version\tPrint the version of JABS and exit.")
        sys.exit(0)
    elif argv[1] == "-v" or argv[1] == "--version":
        write_message("JABS Version %s" % __version__, "good")
        sys.exit(0)


def main(argv: list) -> None:
    """Entry point to the compilation script."""

    write_message("Welcome to JABS - Jakob's Awesome Build Script", "good")

    with open("/".join((PACKAGE_NAME, METADATA))) as source:
        metadata = get_package_metadata(source)

    import_statements = []
    for source_file in SOURCES:
        with open("/".join((PACKAGE_NAME, source_file))) as source:
            import_statements += find_import_statements(source)

    with open("/".join((PACKAGE_NAME, ENTRY_POINT))) as source:
        import_statements += find_import_statements(source)
        source.seek(0)
        entry_point = get_package_entry_point(source)
    print(metadata, import_statements, entry_point)

    with open(argv[1], "w+") as output_script:
        write_metadata(output_script, metadata)
        write_import_statements(output_script, import_statements)
        write_entry_point(output_script, entry_point)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
