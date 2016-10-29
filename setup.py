#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from chandere2 import __version__


def long_description():
    with open("README.md") as description:
        return description.read()


setup(
    name="Chandere2",
    license="GPLv3+",
    version=__version__,
    author="Jakob Tsar-Fox",
    author_email="jakob@memeware.net",
    maintainer="Jakob Tsar-Fox",
    maintainer_email="jakob@memeware.net",
    url="http://tsar-fox.com/projects/chandere2",
    description="A better image/file downloader and thread archiver for Futaba-styled imageboards, such as 4chan.",
    long_description=long_description(),
    download_url="https://github.com/TsarFox/chandere2",
    packages=["chandere2"],
    include_package_data=True,
    install_requires=["aiohttp"],
    extras_require={},
    tests_require=["pytest", "tox", "hypothesis"],
    entry_points={"console_scripts": ["chandere2 = chandere2.core:main"]},
    keywords="downloader archiver imageboard",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Communications :: BBS",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards",
        "Topic :: Text Processing",
        "Topic :: Utilities"
    ]
)
