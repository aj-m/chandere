![Chandere][img_1]
## A command-line utility programmed and maintained by [Jakob.][1]
An asynchronous file downloader and archiving tool for various imageboards,
textboards, and Boorus, with the goal of being as fast and universal as
possible.

Chandere is free software, licensed under the [GNU General Public License.][2]

[![Build Status](https://travis-ci.org/TsarFox/chandere.svg?branch=master)](https://travis-ci.org/TsarFox/chandere)  [![PyPI Version](https://img.shields.io/pypi/v/Chandere.svg)](https://pypi.python.org/pypi/Chandere/)  [![AUR Version](https://img.shields.io/aur/version/chandere.svg)](https://aur.archlinux.org/packages/chandere/)  [![License](https://img.shields.io/github/license/tsarfox/chandere.svg)](https://www.gnu.org/licenses/gpl.html)


# Supported Websites
* 4chan


# Features
* ¯\_(ツ)_/¯


# Installation
**Arch Linux** users are able to install Chandere using Pacman, as it is packaged in the [AUR.][3]

    $ makepkg -si

If you are running a distribution for which Chandere is not packaged, or are not running Linux, the most reliable way to install Chandere is through Pip.

    $ # It is recommended that you use the latest version of pip and setuptools when installing Chandere.
    # pip install --upgrade pip setuptools
    # pip install --upgrade chandere

Alternatively, setup.py in the repository's root directory can be used. This is not recommended.

    # python setup.py install

If Chandere is installed with Pip or setup.py, you will have to manually move the manpages to your manpath.

   $ make doc
   # cp docs/*.1.gz /usr/share/man/man1 # The destination path may be different on your system.


# Tutorial

Chandere has several mode of operations. When no particular mode is specified, the default is to try to connect to the specified targets and print the response headers.

    $ chandere /g/
    CONNECTED: a.4cdn.org/g/threads.json
    ...

More than one target can be specified, as well.

    $ chandere /g/ /3
    ...

Targets can also refer to a thread, rather than an entire board if a thread ID is appended to the board initial.

    $ chandere /g/51971506

Now with the basics of specifying targets, we can get into more useful modes of operation. To download every file in a board or thread, use the "-d" or "--download" argument.

    $ chandere /g/51971506 -d
    ...

That will download everything into the current working directory, though, which is often not desired. The output path with the "-o" or "--output" parameter.

    $ chandere /g/51971506 -d -o Stallman

All of these examples will scrape from 4chan. An alternate imageboard can be specified with "-i". Available imageboard aliases are listed when Chandere is run with "--list-imageboards".

    $ chandere --list-imageboards
    Available Imageboard Aliases: lainchan, 4chan
    $ chandere /cyb/ -d -o Cyberpunk -i lainchan

Post filtering is by far the least intuitive feature to use, though it should feel somewhat familiar to anyone who has used 4chan's built in filtering system. Rather than being limited to five post fields, any field in the json output can be filtered. The following example will only download WEBM and MP4 videos, and will ignore files with the MD5 checksum of "Q0GnSJ3ej7ikA3dfYiXJMA==".

     $ chandere /gif/9463458 -d --filter ext:/[!(.webm)(.mp4)]/ md5:Q0GnSJ3ej7ikA3dfYiXJMA==

While filter patterns can be as simple as the md5sum in the example above, there are several features to make filtering more useful. When several words or phrases are joined with spaces, the filtering engine will check to see if the pattern occurs in any order. Double quotes can be used to force the order of a match; for example, '--filter com:"that feel when"' will not filter "when that feel" in a comment body. Regular expressions can be used as long as the regexp is enclosed in forward slashes.


# TODO

## Short Term Proposals
* Add support for HTTP/SOCKS proxying and Hidden Services.

## Long Term Proposals
* GUI

[1]: http://jakob.space/
[2]: http://gnu.org/licenses/gpl.html
[3]: https://aur.archlinux.org/packages/chandere/

[img_1]: https://a.4cdn.org/vr/4465432.json