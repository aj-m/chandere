![Chandere2](https://raw.github.com/TsarFox/chandere2/master/Chandere2_Logo.png "Chandere2")
========
## A command-line utility programmed and maintained by [Jakob.](http://tsar-fox.com/)
A better image/file downloader and thread archiver for Futaba-styled imageboards, such as 4chan and 8chan.

Chandere2 is a rewrite of Chandere1.0 using asynchronous concurrency. It runs on all versions of Python newer than 3.5.

Chandere2 is free software, licensed under the [GNU General Public License.](http://gnu.org/licenses/gpl.html)

[![Build Status](https://travis-ci.org/TsarFox/chandere2.svg?branch=master)](https://travis-ci.org/TsarFox/chandere2)  [![PyPI Downloads](https://img.shields.io/pypi/dm/Chandere2.svg)](https://pypi.python.org/pypi/Chandere2/)  [![License](https://img.shields.io/github/license/tsarfox/chandere2.svg)](https://www.gnu.org/licenses/gpl.html)


Primary Features
----------------

- Scraping from multiple boards and threads simutaneously
- Archiving to several formats, including SQLite and plaintext.
- Post filtering with syntax similar to that of 4chan's.


Installation
------------

Currently, the most reliable way to install Chandere2 is through Pip.

    $ # It is recommended that you use the latest version of pip and setuptools when installing Chandere.
    $ pip install --upgrade pip setuptools

    $ pip install --upgrade chandere2

Alternatively, setup.py in the repository's root directory can be used. Using Pip is recommended over this method.

    # python setup.py install


Tutorial
--------

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

Post filtering is by far the least intuitive feature to use, though it should feel somewhat familiar to anyone who has used 4chan's built in filtering system. Rather than being limited to five post fields, any field in the json output can be filtered. The following example will only download WEBM and MP4 videos, and will ignore files with the MD5 checksum of "Q0GnSJ3ej7ikA3dfYiXJMA==".

     $ chandere2 /gif/9463458 -d --filter ext:/[!(.webm)(.mp4)]/ md5:Q0GnSJ3ej7ikA3dfYiXJMA==

While filter patterns can be as simple as the md5sum in the example above, there are several features to make filtering more useful. When several words or phrases are joined with spaces, the filtering engine will check to see if the pattern occurs in any order. Double quotes can be used to force the order of a match; for example, '--filter com:"that feel when"' will not filter "when that feel" in a comment body. Regular expressions can be used as long as the regexp is enclosed in forward slashes.


TODO
----
[TODO](/TODO.md)
