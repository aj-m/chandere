Change Log
==========
This document records all notable changes to Chandere2.


**Version 2.4.0**
-----------------
* Added support for Uboachan.
* Implemented handling for when the network is down or the imageboard is unreachable.
* Database archives now have a separate table for each board.
* Fixed several issues with continuous mode.
* Tracebacks are no longer shown when a user issues a signal interrupt.


**Version 2.3.1.post1**
-----------------------
* Very minor bugfix for the changed 8chan API.


**Version 2.3.1**
-----------------
* Fixed issues with image downloading on 8chan and Nextchan.
* Fixed issue regarding archiving to plaintext for Endchan and Nextchan.


**Version 2.3.0**
-----------------
* Added support for 76chan, Endchan and Nextchan.


**Version 2.2.0**
-----------------
* Implemented 4chan-style post filtering.
* Text fields are now unescaped when being archived to an Sqlite database.
* Added caching capability so posts aren't handled several times.


**Version 2.1.0**
-----------------
* Initial development snapshot.
