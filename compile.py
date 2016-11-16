#!/usr/bin/env python

"""Script to collect the Chandere2 source files and compile them into a
single, portable Python script.
"""

import os.path
import re

EOF = "\n"

PACKAGE_NAME = "chandere2"
ENTRY_POINT = "__main__.py"
METADATA = "__init__.py"
SOURCES = ("cli.py", "connection.py", "context.py", "core.py",
           "output.py", "post.py", "validate.py", "write.py")


def get_package_metadata(source):
    """Finds the package description, and a list containing any other
    metadata embedded in the given source file.
    """
    source_content = source.read()
    metadata = []
    package_description = ""
    description_match = re.search(r"\"\"\".*?\"\"\"", source_content, re.S)
    if description_match:
        package_description = " ".join(description_match.group().split("\n"))
    for variable in re.findall(r"__.+?__ = .+", source_content):
        metadata.append(variable)
    return (package_description, metadata)


def find_import_statements(source):
    """Given a readable source file, extracts every import statements
    and returns a list containing them. Import statements containing
    the PACKAGE_NAME are discarded.
    """
    import_statements = []
    lines = source.read().split(EOF)
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


def main():
    """Entry point to the compilation script. """
    with open("chandere2/__init__.py") as source:
        print(get_package_metadata(source))


if __name__ == "__main__":
    main()
