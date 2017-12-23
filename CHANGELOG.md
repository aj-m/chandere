This document records all notable changes to Chandere.


## Version 2.5.0
** Major rewrite of program in an attempt to make it more modular and easily extensible. **
* Rename to "Chandere."
  * The "2" was appended in an attempt to keep this repository separate from an
    older, synchronous version of the software, but that repository has since
    been removed from Github.
* The codebase has been completely rewritten, and now operates on a system of
  modularized website scrapers and actions. Adding support for a new website or
  task no longer requires fiddling with fragile "contexts.
* The following features have been temporarily removed:
  * Archiving posts to plaintext, SQL.
  * Post filtering.
  * Hammering the servers with --continuous
* Support for the following websites has been temporarily removed on a provisional basis:
  * 76chan
  * endchan
  * lainchan
  * nextchan
  * uboachan


## Version 2.4.1
* No major changes, just a new stable release with some fixes for new aiohttp.


## Version 2.4.0
* Added support for Uboachan.
* Implemented handling for when the network is down or the imageboard is unreachable.
* Database archives now have a separate table for each board.
* Fixed several issues with continuous mode.
* Tracebacks are no longer shown when a user issues a signal interrupt.


## Version 2.3.1.post1
* Very minor bugfix for the changed 8chan API.


## Version 2.3.1
* Fixed issues with image downloading on 8chan and Nextchan.
* Fixed issue regarding archiving to plaintext for Endchan and Nextchan.


## Version 2.3.0
* Added support for 76chan, Endchan and Nextchan.


## Version 2.2.0
* Implemented 4chan-style post filtering.
* Text fields are now unescaped when being archived to an Sqlite database.
* Added caching capability so posts aren't handled several times.


## Version 2.1.0
* Initial development snapshot.
