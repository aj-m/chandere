#!/usr/bin/env python

# Copyright (C) 2017 Jakob Kreuze, All Rights Reserved.
#
# This file is part of Chandere.
#
# Chandere is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Chandere is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with Chandere. If not, see <http://www.gnu.org/licenses/>.

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from chandere import __version__


def long_description():
    with open("README.md") as description:
        return description.read()


setup(
    name="Chandere",
    license="GPLv3+",
    version=__version__,
    author="Jakob Kreuze",
    author_email="jakob@memeware.net",
    maintainer="Jakob Kreuze",
    maintainer_email="jakob@memeware.net",
    url="https://github.com/TsarFox/chandere",
    description="An asynchronous image/file downloader and thread archiver for Futaba-styled imageboards, such as 4chan and 8chan.",
    long_description=long_description(),
    download_url="https://github.com/TsarFox/chandere",
    packages=["chandere"],
    include_package_data=True,
    install_requires=["aiohttp"],
    extras_require={},
    tests_require=["pytest", "tox", "hypothesis"],
    entry_points={"console_scripts": ["chandere = chandere.main:main"]},
    keywords="downloader archiver imageboard",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Topic :: Communications :: BBS",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards",
        "Topic :: Text Processing",
        "Topic :: Utilities"
    ]
)
