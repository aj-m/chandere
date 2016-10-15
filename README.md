![Chandere2](https://raw.github.com/TsarFox/chandere2/master/Chandere2_Logo.png "Chandere2")
========
## A command-line utility programmed and maintained by [Jakob.](http://tsar-fox.com/)
A better image/file downloader and thread archiver for Futaba-styled imageboards, such as 4chan and 8chan.

Chandere2 is a rewrite of Chandere1.0 using asynchronous concurrency. It runs on all versions of Python newer than 3.5.

Chandere2 is free software, licensed under the [GNU General Public License.](http://gnu.org/licenses/gpl.html)

[![Build Status](https://travis-ci.org/TsarFox/chandere2.svg?branch=master)](https://travis-ci.org/TsarFox/chandere2)  [![PyPI Downloads](https://img.shields.io/pypi/dm/Chandere2.svg)](https://pypi.python.org/pypi/Chandere2/)  [![License](https://img.shields.io/github/license/tsarfox/chandere2.svg)](https://www.gnu.org/licenses/gpl.html)


Primary Features
================

* Able to scrape from multiple boards and threads simutaneously.
* Archives to several formats, including SQLite and plaintext.


Installation
============

Currently, the most reliable way to install Chandere2 is through Pip.

    $ # It is recommended that you use the latest version of pip and setuptools when installing Chandere.
    $ pip install --upgrade pip setuptools

    $ pip install --upgrade chandere2

Alternatively, setup.py in the repository's root directory can be used. Using Pip is recommended over this method.

    # python setup.py install


Tutorial
========

Chandere2 has several mode of operations. When no particular mode is specified, the default is to try to connect to the specified targets and print the response headers.

    $ chandere2 /g/
    CONNECTED: a.4cdn.org/g/threads.json
    ...

More than one target can be specified, as well.

    $ chandere2 /g/ /3
    ...

Targets can also refer to a thread, rather than an entire board if a thread ID is appended to the board initial.

    $ chandere2 /g/51971506

Now with the basics of specifying targets, we can get into more useful modes of operation. To download every file in a board or thread, use the "-d" or "--download" argument.

    $ chandere2 /g/51971506 -d
    ...

That will download everything into the current working directory, though, which is often not desired. The output path with the "-o" or "--output" parameter.

    $ chandere2 /g/51971506 -d -o Stallman

All of these examples will scrape from 4chan. An alternate imageboard can be specified with "-i". Available imageboard aliases are listed when Chandere2 is run with "--list-imageboards".

    $ chandere2 --list-imageboards
    Available Imageboard Aliases: lainchan, 4chan
    $ chandere2 /cyb/ -d -o Cyberpunk -i lainchan


Options
-------
**Documentation**
* -h, --help | Display a list of available command-line arguments.
* -v, --version | Display the current version of Chandere2.
* --list-imageboards | List the available imageboard aliases.

**Scraping**
* targets | Pairs of a board and optionally a thread ID to connect to. If a thread is not specified, Chandere2 will attempt to scrape the entire board.
* -i, --imageboard | Specify the imageboard to connect to. Available aliases are listed with "--list-imageboards"
* -d, --download | Crawl for and download all of the files in a board/thread.
* -a, --archive | Crawl for and archive all of the posts in a board/thread.
* --continuous | Rather than quitting as soon as the task is done, Chandere2 will attempt to continuously refresh and check for new posts until a SIGINT is received.
* --ssl | Use HTTPS if available.
* --nocap | Will not attempt to limit the number of concurrent connections. This generates a very large amount of network traffic and will certainly hammer servers. Please only use this if you know what you're doing.

**Output**
* --debug | Indicates that every log message should be shown during runtime. This is helpful when opening a bug report.
* -o, --output | Designates the output directory if operating in File Downloading mode, or the file to output to if operating in Archiving mode. Defaults to the current working directory.
* --output-format | Specify the format that output should be put into. Can be either "plaintext" or "sqlite". The default is plaintext.


TODO
====
[TODO](/TODO.md)
