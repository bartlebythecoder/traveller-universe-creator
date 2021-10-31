 traveller-universe-creator
v.06
2021-10-31

 Sector Generation
 by Sean Nelson

 The goal is to generate an entire Traveller sector of stars, planets, moons using the latest scientific models.

 Possible Improvements Pending (likely in this order):

   - Build a GUI for browsing data
   - Rework/audit/validate the Traveller stat creation for mainworlds, nonmainworlds, moons
   - Rewrite Stellar creation rules using  Architect of Worlds
   - Create worlds using Architect of Worlds
   - Export data to a PDF for publishing

To Do list complete:


   - COMPLETE 2021 10 31 v.06: Moons details added to orbital_body table
   - COMPLETE 2021 10 28: Moons created using Architect of Worlds
   - COMPLETE 2021 10 27: Density added for GG
   - COMPLETE 2021 10 26: Orbital Bodies around all stellar objects
   - COMPLETE 2021 10 26: Incorporate Forbidden Zones for planet orbits
   - COMPLETE 2021 10 25: Very Close Binaries combine stellar info for orbit creation
   - COMPLETE 2021 10 25: Distant stellar bodies added



Description:

This program builds a traveller sector and stores the data in two forms:
-SQLite database
-Text file for import into the TravellerMap website


FAQ:
Q:  What does the program do?

A:  After setting the parameters you want, it produces a traveller sector and provides the information in two separate files. 
The first file is a txt file that matches the T5 format for the TravellerMap website.  The information can be cut and pasted and placed directly into that site's custom map option.

The second file is a database file (using SQLite DB) that houses information for every star and planet in the sector.  It includes UWPs for mainworld and non-mainworlds.
You can browse and search this database using the excellent SQLite browser from: https://sqlitebrowser.org/

Q:  What Traveller rules does it use?

A:  It uses GURPS First In for the science stuff (like stellar details, and planet temperature) and T5 rules for the Traveller stuff (like law level and influence scores)

Q:  How do you run it?

A:  Run the TUC_menu.py from your python environment

Q:  What imports do I need?

A:  tkinter, pandas, numpy, sqlite3, random, 



