![Chandere2](https://raw.github.com/TsarFox/chandere2/master/Chandere2_Logo.png "Chandere2")
========
## A utility programmed and maintained by [Jakob.](http://tsar-fox.com/)
A better image/file downloader and thread archiver for Futaba-styled imageboards, such as 4chan.

Chandere2 is an asynchronous rewrite of Chandere 1.0. It runs on all versions of Python newer than 3.4.

Chandere2 is free software, licensed under the [GNU General Public License.](http://gnu.org/licenses/gpl.html)

[![Build Status](https://travis-ci.org/TsarFox/chandere2.svg?branch=master)](https://travis-ci.org/TsarFox/chandere2)  [![PyPI Downloads](https://img.shields.io/pypi/dm/Chandere2.svg)](https://pypi.python.org/pypi/Chandere2/)  [![License](https://img.shields.io/github/license/tsarfox/chandere2.svg)](https://www.gnu.org/licenses/gpl.html)


Primary Features
================

* Able to scrape from multiple boards and threads at once.
* Offers official support for 4chan, 8chan and Lainchan.
* Capable of archiving to a Sqlite3 database, as well as plaintext.


Benchmarks
==========

Chandere1.0.0 Downloading All Images in a /tech/ Thread (No Concurrent Connection Cap)
--------------------------------------------------------------------------------------

        [jakob@Epsilon Chandere2]$ time chandere /tech/643887 -c 8chan -o /tmp -d
        ...
        [Consumer Thread] INFO: Waiting for downloads to finish...
        [MainThread] INFO: Task completed.
        
        real         0m10.451s
        user         0m0.477s
        sys          0m0.017s


Chandere2.1.0.dev1 Downloading All Images in a /tech/ Thread (Max 8 Concurrent Connections)
-------------------------------------------------------------------------------------------

        [jakob@Epsilon Chandere2]$ time python -m chandere2 /tech/643887 -i 8chan -o /tmp -d
        ...
        
        real        0m4.619s
        user        0m0.323s
        sys         0m0.020s


Chandere1.0.0 Archiving All of /g/ (No Concurrent Connection Cap)
-----------------------------------------------------------------

        [jakob@Epsilon Chandere2]$ time chandere /g/ -a
        [MainThread] INFO: Task completed.
        
        real         1m10.907s
        user         0m51.073s
        sys          0m16.707s


Chandere2.1.0.dev1 Archiving All of /g/ (Max 8 Concurrent Connections)
----------------------------------------------------------------------

        [jakob@Epsilon Chandere2]$ time python -m chandere2 /g/ -a
        
        real   1m6.648s
        user   0m48.730s
        sys    0m16.193s


Installation
============

Currently, the most reliable way to install Chandere2 is through Pip.

    # It is recommended that you use the latest version of pip and setuptools when installing Chandere.
    $ pip install --upgrade pip setuptools

    $ pip install --upgrade chandere2


Tutorial
========

Chandere2 only really requires one argument to run. The following command will attempt to make a connection to http://boards.4chan.org/g/ and show the response headers.

    $ chandere2 /g/
    CONNECTED: a.4cdn.org/g/threads.json
    ...

Accessing multiple boards at once is just as simple, just add another one as an argument.

    $ chandere2 /g/ /3/
    ...

A specific thread can also be specified by placing the thread number after the board.

    $ chandere2 /g/51971506

Now with the basics of specifying where to scrape from, we can actually use the tool. The default mode of operation is "test connection", but we can do more than that. To download every file in a board/thread use the "-d" or "--download" argument.

    $ chandere2 /g/51971506 -d
    ...

This will download everything into the current working directory, though. Maybe we don't want that. We can specify the output path with the "-o" or "--output" parameter.

    $ chandere2 /g/51971506 -d -o Stallman

Pretty neat, but maybe we're a lainon and don't care much for 4chan. The imageboard can be specified with -i. An alias can be used if it is listed by the "--list-imageboards" parameter.

    $ chandere2 --list-imageboards
    Available Imageboard Aliases: lainchan, 4chan
    $ chandere2 /cyb/ -d -o Cyberpunk -i lainchan


Options
-------
**Documentation**
* -h, --help | Display a list of available command-line flags.
* -v, --version | Display the version of Chandere2 that is currently installed.
* --list-imageboards | List available imageboard aliases.

**Scraping**
* targets | Pairs of a board and optionally a thread to connect to. If a thread is not specified, Chandere2 will attempt to scrape the entire board.
* -i, --imageboard | Specify the imageboard to connect to. Aliases are listed with "--list-imageboards"
* -d, --download | Crawl for and download all of the files in a board/thread.
* -a, --archive | Crawl for and archive all of the posts in a board/thread.
* --continuous | If Chandere2 is run with this flag, it will attempt to continuously refresh and check for new posts until a SIGINT is received, rather than quitting as soon as the task is done.
* --ssl | Use HTTPS if available. Chandere does not attempt to verify the signature of the server it is connecting to.
* --nocap | Will not attempt to limit the number of concurrent connections. Please do not use this unless you know what you're doing.

**Output**
* --debug | Indicates that every log message should be shown during runtime. This is helpful when opening a bug report.
* -o, --output | Designates the output directory if Chandere is operating in File Downloading mode, or the file to output to if Chandere is operating in Archiving mode. Defaults to the current working directory.
* --output-format | Specify the format that output should be put into. Can be either "plaintext" or "sqlite".


TODO
====
[TODO](/TODO.md)
