![Chandere][img_1]
## A command-line utility programmed and maintained by [Jakob.][1]
An extremely modular asynchronous archiving tool for various imageboards,
textboards, and Boorus.

Chandere 2.5.0 is currently in the alpha state of development, and is likely to
bring many bugs. See [HACKING.md][2] for information on reporting issues.

Chandere is free software, licensed under the [GNU General Public License.][3]

[![Build Status](https://travis-ci.org/TsarFox/chandere.svg?branch=master)](https://travis-ci.org/TsarFox/chandere)  [![PyPI Version](https://img.shields.io/pypi/v/Chandere.svg)](https://pypi.python.org/pypi/Chandere/)  [![AUR Version](https://img.shields.io/aur/version/chandere.svg)](https://aur.archlinux.org/packages/chandere/)  [![License](https://img.shields.io/github/license/tsarfox/chandere.svg)](https://www.gnu.org/licenses/gpl.html)


# Websites Supported by the Default Distribution
* 4chan


# Features Supported by the Default Distribution
* Downloading all files present.


# Installation
**Arch Linux** users are encouraged to install Chandere using Pacman, as it is
packaged in the [AUR.][4]

```
$ # If the PKGBUILD is in the current working directory:
$ makepkg -si
```

If you are running a distribution for which Chandere is not yet packaged, or are
not running Linux, the recommended means of installation is through Pip.

```
$ # It is recommended that you use the latest version of pip and setuptools when installing Chandere.
# pip install --upgrade pip setuptools
# pip install --upgrade chandere
```

`setup.py` in the repository's root directory can be used if Pip is not
available, however this is not recommended.

```
# python setup.py install
```

If Chandere is installed with Pip or setup.py, manpages will have to be manually
moved to your manpath.

```
$ make doc
# cp docs/*.1.gz /usr/share/man/man1 # The destination path may be different on your system.
```


# Tutorial

TODO


# Extending

TODO


# TODO

## Short Term Proposals
* Fix ordering of TARGETS.
* Add support for HTTP/SOCKS proxying and Hidden Services.

## Long Term Proposals
* GUI

[1]: http://jakob.space/
[2]: https://github.com/TsarFox/chandere/blob/master/HACKING.md
[3]: http://gnu.org/licenses/gpl.html
[4]: https://aur.archlinux.org/packages/chandere/

[img_1]: https://raw.githubusercontent.com/TsarFox/chandere/master/chandere_logo.png
