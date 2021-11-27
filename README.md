 traveller-universe-creator
v0.8.2 - Fixed Error With Density 4 sectors
2021-11-24

 Sector Generation
 by Sean Nelson

 The goal is to generate an entire Traveller sector of stars, planets, moons using the latest scientific models.

 Possible Improvements Pending (likely in this order):

   - Rewrite Stellar creation rules using  Architect of Worlds
   - Create worlds using Architect of Worlds
   - Export data to a PDF for publishing

New With This Version (8.2):

   - Added 40,000+ new names to names.csv with credit and thanks to https://simplemaps.com/data/world-cities
   - Resolved the issue of Density 4 sectors running out of names
   - Updated PyMapGen .dat extract to fix Sector name reading



Description:

This program builds a traveller sector and stores the data in three files:
-SQLite database
-Text file for system data import into the TravellerMap website
-Text file for route data import into the TravellerMap website


FAQ:
Q:  What does the program do?

A:  After setting the parameters you want, it produces a traveller sector and provides the information in two separate files. 
The first file is a txt file that matches the T5 format for the TravellerMap website.  The information can be cut and pasted and placed directly into that site's custom map option.

The second file is a database file (using SQLite DB) that houses information for every star and planet in the sector.  It includes UWPs for mainworld and non-mainworlds.
You can browse and search this database using the excellent SQLite browser from: https://sqlitebrowser.org/

Q:  What Traveller rules does it use?

A:  It uses GURPS First In for the science stuff (like stellar details, and planet temperature) and T5 rules for the Traveller stuff (like law level and influence scores)

Q:  How do you run it?

A:  Run the generate_men.py from your python environment to create a sector.  Run the browse_sector to explore the sectors you create.

Q:  What imports do I need?

A:  tkinter, pandas, numpy, sqlite3, random, io, networkx



