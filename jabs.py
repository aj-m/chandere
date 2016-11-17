#!/usr/bin/env python

"""JABS, or Jakob's Awesome Build Script is a tool for collecting
multiple Python source files and compiling them into a single,
portable Python script.
"""

import imp
import os.path
import re
import sys

__author__ = "Jakob Tsar-Fox <jakob@memeware.net>"
__licence__ = "GPLv3"
__version__ = "1.0.0.dev1"

COLORS = {"good": "\033[92m",
          "okay": "\033[m",
          "warning": "\033[93m",
          "error": "\033[91m"}

EOL = "\n"

PACKAGE_NAME = "chandere2"
ENTRY_POINT = "__main__.py"
METADATA = "__init__.py"
SOURCES = ("cli.py", "connection.py", "context.py", "core.py",
           "output.py", "post.py", "validate.py", "write.py")


def write_message(text: str, level="okay") -> None:
    """Writes the text to either stdout or stderr depending upon whether
    or not the loglevel is "error", with a short colored prefix.
    """
    text = "[%s*%s] " % (COLORS.get(level, "okay"), COLORS["okay"]) + text
    output = sys.stderr if level == "error" else sys.stdout
    output.write(text + "\n")


def get_package_metadata(source: str) -> tuple:
    """Finds the package description, and a list containing any other
    metadata embedded in the given source file.
    """
    metadata = []
    description_match = re.search(r"\"\"\".*?\"\"\"", source, re.S)
    if description_match:
        package_description = description_match.group()
    else:
        package_description = "\"\"\"[No Script Docstring]\"\"\""
    for variable in re.findall(r"__.+?__ = .+", source):
        metadata.append(variable)
    return (package_description, metadata)


def get_package_entry_point(source: str) -> str:
    """Finds the package's entry point."""
    entry_point_match = re.search(r"if __name__ == \"__main__\":.*", source, re.S)
    return entry_point_match.group() if entry_point_match else None


def get_class_definitions(source: str) -> list:
    """Finds all class definitions in the package."""
    definitions = []
    for header_match in re.finditer(r"class .+?\n", source):
        definition = header_match.group()
        for line in source[header_match.end():].split("\n"):
            if line == "" or line.startswith("    "):
                definition += "\n" + line
            else:
                break
    return definitions


def get_import_statements(source: str) -> list:
    """Finds all import statements in the package that do not contain
    the PACKAGE_NAME, as those dependencies will be resolved by the
    compilation process.
    """
    import_statements = []
    lines = source.split(EOL)
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


def check_dependencies(import_statements: list) -> list:
    """Checks each import statement to see if the package is installed
    and importable on the system. Any failed dependencies are returned.
    """
    failed = []
    for dependency in import_statements:
        dependency = re.search(r"(?<=import )[^.]*", dependency).group()
        try:
            imp.find_module(dependency)
        except ImportError:
            failed.append(dependency)
    return failed


def write_metadata(destination, metadata: tuple) -> None:
    """Writes package metadata to the given destination file."""
    description, metadata_variables = metadata
    metadata_text = "\n".join((description, "\n".join(metadata_variables)))
    destination.write(metadata_text + "\n\n")


def write_import_statements(destination, import_statements: list) -> None:
    """Writes all import statements into the given destination file."""
    destination.write("\n".join(sorted(set(import_statements))) + "\n\n")


def write_entry_point(destination, entry_point: str) -> None:
    """Writes the entry point into the given destination file."""
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

    import_statements = []
    write_message("Collecting dependencies...")
    for source_file in SOURCES + (ENTRY_POINT,):
        with open(os.path.join(PACKAGE_NAME, source_file)) as source:
            code = source.read()
            import_statements += get_import_statements(code)

    ## TODO: -f, --force option.
    failed_dependencies = check_dependencies(import_statements)
    for dependency in failed_dependencies:
        write_message("Could not import %s!" % dependency, "error")
    if failed_dependencies:
        write_message("Build failed.", "error")
        sys.exit(1)
    write_message("All dependencies resolved!", "good")

    write_message("Collecting package metadata...", "okay")
    with open("/".join((PACKAGE_NAME, METADATA))) as source:
        metadata = get_package_metadata(source.read())

    write_message("Finding code...", "okay")
    class_definitions = []
    for source_file in SOURCES + (ENTRY_POINT,):
        with open(os.path.join(PACKAGE_NAME, source_file)) as source:
            code = source.read()
            class_definitions += get_class_definitions(code)

    with open(os.path.join(PACKAGE_NAME, ENTRY_POINT)) as source:
        code = source.read()
        import_statements += get_import_statements(code)
        entry_point = get_package_entry_point(code)

    print(class_definitions)

    with open(argv[1], "w+") as output_script:
        write_metadata(output_script, metadata)
        write_import_statements(output_script, import_statements)
        write_entry_point(output_script, entry_point)
    write_message("All done!", "good")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
