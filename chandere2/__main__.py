#!/usr/bin/env python

"""Main entry point to Chandere2. Run when the package is invoked as
"chandere2" or "python -m chandere2"
"""

import sys

from chandere2.core import main


if __name__ == "__main__":
    sys.exit(main())
