Change Log
==========
This document records all notable changes to Chandere2.


**Version 2.4.0**
-----------------
* Added support for Uboachan.
* Implemented exception handling for when the network is down or the imageboard is unreachable.
* Archiving to SQLite now creates a separate table for every board.


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
