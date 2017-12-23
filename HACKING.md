# Opening an Issue

If you are not a Github user, but would like to report a bug or request a
feature, you can get in contact with the [Project Maintainer][1].

Be sure to include specific details about the bug, such as relevant log output
and details about what you were trying to do. Please run Chandere with the
"verbose" flag, as this will give more detailed log output.

```
$ chandere --verbose ...
```


# Hacking on the Source Code

Thank you for your interest in improving Chandere! The following are standards
for the upstream codebase. If you are here for the module API specifications and
have no interest in your module being merged upstream, you can safely skip to
those sections.

Please make an attempt to follow the [PEP 8 Guidelines][2] in your
contributions.

Chandere does not aim for any compatibility with Python <= 3.4, so Python 3.5
features such as type hinting and the async/await syntax can and should be used.

Tests can be run from the repository's root with "make test".

## Implementing a Module for Chandere

As of the current version, the API is unstable and subject to change. Please
keep this in mind when developing modules.

A module docstring is expected, which is used when the module is listed by
commands such as --list-actions

Additionally, `__author__`, `__licence__`, and `__version__` are recognized.

Command-line arguments can be specified for an individual module. Simply expose
an instance of argparse.ArgumentParser, named `PARSER` from your module. Its
help information will be seamlessly integrated when Chandere's help page is
displayed. **If your module does not require arguments,** you can safely omit
the `PARSER` variable.

**Please note the following:** It is the responsibility of your module to parse
arguments. When this is done depends on the type of module (see below).
Additionally, arguments will be passed to your module in the form of a list, and
a good portion of them will not be defined within your `PARSER`. Rather than
parsing arguments with `ArgumentParser.parse_args`, you should use
`ArgumentParser.parse_known_args`. If you care for being idiomatic, the
following is in good taste:

```
args, _ = PARSER.parse_known_args(argv)
```

### Adding Support for an Action

Aside from `PARSER` as mentioned above, the following functions are expected to
be exposed:

```
# Entry point to the action.
def invoke(scraper: object, targets: list, argv: list) -> Coroutine
```

### Adding Support for a Website

Aside from `PARSER` as mentioned above, the following functions are expected to
be exposed:

```
# Parses targets into a format that will be understood by other exposed functions in this module.
def parse_target(target: str) -> Any
```

The following may be exposed as appropriate. Action modules should check for
their presence before blindly invoking them.

```
# Yields posts in a target.
def collect_posts(target: str) -> AsyncGenerator[dict]

# Yields files in a target, represented as tuples of the post and a url to the file resource.
def collect_files(target: str) -> AsyncGenerator[Tuple[dict, str]]
```


[1]: http://jakob.space/
[2]: https://www.python.org/dev/peps/pep-0008/
