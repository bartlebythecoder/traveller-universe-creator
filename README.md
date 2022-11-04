traveller-universe-creator
v0.9.0.2.1.01 - Updated browse_sector.py
2022-11-04

Changes this update:
- Corrected Find Earth on browse sector map
- Added Find Belt on browse sector map
- These changes not on the latest EXE file

 Sector Generation
 by Sean Nelson

 The goal is to generate an entire Traveller sector of stars, planets, moons using the latest scientific models.

 Possible Improvements Pending (likely in this order):

   - Add Trade details for each system
   - Rewrite Stellar creation rules using  Architect of Worlds
   - Create worlds using Architect of Worlds
   - Export data to a PDF for publishing

New With This Version (v0.9.0.2.1):

   - Added exe files for people without Python platforms
   - Added culture details for each system
   - New Traveller Function file with re-usable functions




Description:

This program builds a traveller sector and stores the data in three files:
  - SQLite database
  - Text file for system data import into the TravellerMap website
  - Text file for route data import into the TravellerMap website
  

How to Run?

Option 1:  From the EXEs (note - exe compiles start with a loooong wait with a blanks screen - be patient)
 - run generate_menu.exe to generate a DB
 - find generated DBs in /sector_db
 - run browse_sector.exe to view a sector
 - optionally use a DB browser (like DB browser for SQLite) to look at every piece of data for each planet/system
 
 
Option 2: From the code (better experience - but requires a Python env)
 - run generate_menu.py to generate a DB
 - find generated DBs in /sector_db
 - run browse_sector.py to view a sector
 - optionally use a DB browser (like DB browser for SQLite) to look at every piece of data for each planet/system

FAQ:
Q:  What does the program do?

A:  After setting the parameters you want, it produces a traveller sector and provides the information in two separate files. 
The first file is a txt file that matches the T5 format for the TravellerMap website.  The information can be cut and pasted and placed directly into that site's custom map option.

The second file is a database file (using SQLite DB) that houses information for every star and planet in the sector.  It includes UWPs for mainworld and non-mainworlds.
You can browse and search this database using the excellent SQLite browser from: https://sqlitebrowser.org/

Q:  What Traveller rules does it use?

A:  It uses GURPS First In for the science stuff (like stellar details, and planet temperature) and T5 rules for the Traveller stuff (like law level and influence scores).
    I have started migrating the GURPS First In calculations to use the more update Architect of Worlds by the same creator

Q:  How do you run it?

A:  Run the generate_menu.py from your python environment to create a sector.  Run the browse_sector to explore the sectors you create.

Q:  What imports do I need?

A:  tkinter, pandas, numpy, sqlite3, random, io, networkx

Q:  Where do the planet names come from

A:  They come from all over the internet, but most come from: https://simplemaps.com/data/world-cities



