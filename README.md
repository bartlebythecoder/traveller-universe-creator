 traveller-universe-creator
v.05
2021-10-28

 Sector Generation
 by Sean Nelson

 The goal is to generate a sector of Traveller star systems


 Possible Improvements Pending:

   - Rewrite Stellar creation rules using  Architect of Worlds
   - Create worlds using Architect of Worlds
   - Expand moon data 
   - Build a GUI for browsing data
   - Export data to a PDF for publishing

To Do list complete:

   - COMPLETE 2021 10 28: Moons created using Architect of Worlds
   - COMPLETE 2021 10 27: Density added for GG
   - COMPLETE 2021 10 26: Orbital Bodies around all stellar objects
   - COMPLETE 2021 10 26: Incorporate Forbidden Zones for planet orbits
   - COMPLETE 2021 10 25: Very Close Binaries combine stellar info for orbit creation
   - COMPLETE 2021 10 25: Distant stellar bodies added
   - COMPLETE: Add Stellar Age
   - COMPLETE: Appropriate Planet Size modifiers
   - COMPLETE: Stellar data loaded in a database. 
   - COMPLETE: White Dwarf details and orbital bodies
   - COMPLETE: Rolls are added to a table with relevant data
   - FIXED: Minimum 25 size for GG    


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



