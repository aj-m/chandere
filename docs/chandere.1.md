% CHANDERE(1)
% Jakob L. Kreuze
% December 2017

# NAME

chandere – an asynchronous archiving tool for various imageboards, textboards,
and Boorus

# SYNOPSIS

chandere _TARGETS_ [-w _website_] [-a _action_] ...

# EXAMPLES

chandere _/fit/17018018_

Download all images from 'https://boards.4chan.org/fit/thread/17018018/' into
the current working directory, preserving the original filenames.

chandere -o _"{index}.{ext}"_ _/fit/17018018_

Perform the same as the above, but instead save every image to a filename
containing the index at which it was encountered.

chandere _/tech/_ -w _8chan_

Download all images from 'https://8ch.net/tech/res/589254.html'.

# GENERAL OPTIONS

**-h**, **--help**
:   Display a help page and exit.

**-V**, **--version**
:   Display the current version and exit.

**-v**, **--verbose**
:   Provides more verbose runtime information.

**--list-actions**
:   Display all actions that can be specified with -a.

**--list-websites**
:   Display all websites that can be specified with -w.

**-a**, **--action**
:   The action to be performed on all collected posts. Defaults to 'download',
    which will download all images from the targets.

**-w**, **--website**
:   The website to scrape from. Defaults to '4chan'.

**--custom-action**
:   Path to a python script exposing the action API to be used.

**--custom-scraper**
:   Path to a python script exposing the scraping API to be used.
