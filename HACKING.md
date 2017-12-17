# Opening an Issue

If you are not a Github user, but would like to report a bug or request a
feature, you may get in contact with the [Project Maintainer][1].

Be sure to include specific details about the bug, such as relevant log output
and details about what you were trying to do. Please run Chandere with the
"verbose" flag, as this will give more detailed log output.

```
$ chandere2 --verbose ...
```


# Hacking on the Source Code

Please make an attempt to follow the [PEP 8 Guidelines][2] in your
contributions.

Chandere does not aim for any compatibility with Python <= 3.4, so Python 3.5
features such as type hinting and the async/await syntax can and should be used.

Tests can be run from the repository's root with "make test".

## Adding Support for a Website

Chandere is very modular, and adding support for a new website is as simple as
writing a new "Scraper" class. Examples can be found in the `chandere/websites/`
directory of the source tree, but here are a few methods that you may want to
define:

```
## Imageboards
# Returns all threads for a board's initials (e.g. "vr")
async def collect_threads(board: str) -> list

# Returns all posts in a thread.
async def collect_posts(board: str, thread: int) -> list

# Returns a list of (original_filename, url) for every image in a board or, if
# specified, thread.
async def collect_images(board: str, thread=None)
```

[1]: http://jakob.space/
[2]: https://www.python.org/dev/peps/pep-0008/
