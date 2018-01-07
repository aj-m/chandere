![Chandere][img_1]
An extremely modular asynchronous archiving tool for various imageboards,
textboards, and Boorus.

As of 2.5.0, Chandere is abandoned. It has gone through several rewrites, and
does not have a large enough userbase to motivate me to continue maintaining
it. The current state of the repository is very unstable and marks an attempt at
making a more modular interface for adding website and action support.
[2.4.1][4] is stable and works, if you wish to use Chandere. If you are
interested in picking up development and maintenance, see [HACKING.md][1] and
consider contacting me.

Chandere is free software, licensed under the [GNU General Public License.][2]

[![Build Status](https://travis-ci.org/TsarFox/chandere.svg?branch=master)](https://travis-ci.org/TsarFox/chandere)  [![PyPI Version](https://img.shields.io/pypi/v/Chandere.svg)](https://pypi.python.org/pypi/Chandere/)  [![AUR Version](https://img.shields.io/aur/version/chandere2.svg)](https://aur.archlinux.org/packages/chandere2/)  [![License](https://img.shields.io/github/license/tsarfox/chandere.svg)](https://www.gnu.org/licenses/gpl.html)


# Supported Websites
* 4chan
* 8chan
* danbooru
* dangeru


# Supported Features
* Downloading files
* Archiving to CSV


# Installation

Chandere is packaged in the [AUR][3], so **Arch Linux** users are encouraged to
install Chandere with makepkg.

If you are running a distribution for which Chandere is not yet packaged, or are
not running Linux, the suggested means of installation is through Pip.

```
$ # It is recommended that you use the latest version of pip and setuptools when installing Chandere.
# pip install --upgrade pip setuptools
# pip install --upgrade chandere
```

If Chandere is installed with Pip or setup.py, manpages will have to be manually
moved to your manpath.

```
$ make doc
# cp docs/*.1.gz /usr/share/man/man1 # The destination path may be different on your system.
```


# Examples

```
chandere /fit/17018018
```

Download all images from 'https://boards.4chan.org/fit/thread/17018018/' into
the current working directory, preserving the original filenames.

```
chandere -o "{index}.{ext}" /fit/17018018
```

Perform the same as the above, but instead save every image to a filename
containing the index at which it was encountered.

```
chandere /tech/ -w 8chan
```

Download all images from 'https://8ch.net/tech/res/589254.html'.


# Extending

See [HACKING.md][2].


# TODO

* Handle files of the same name in the download.py action.
* Fix ordering of TARGETS.
* Expose an API such that Chandere can be used as a library.

[1]: https://github.com/TsarFox/chandere/blob/master/HACKING.md
[2]: http://gnu.org/licenses/gpl.html
[3]: https://aur.archlinux.org/packages/chandere/
[4]: https://github.com/TsarFox/chandere/releases/tag/v2.4.1

[img_1]: https://raw.githubusercontent.com/TsarFox/chandere/master/chandere_logo.png
