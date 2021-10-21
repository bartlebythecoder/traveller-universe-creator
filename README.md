# traveller-universe-creator
v.03
2021-10-21 
- Added a table with journey times to and from jump points
- Updated location_orbit field to include which stellar mass is being orbited (primary, secondary, tertiary)

Description:

This program builds a traveller sector and stores the data in two forms:
-SQLite database
-Text file for import into the TravellerMap website

You can run it one of two ways:
1)  WINDOWS - no Python environment:  The TUC.zip includes all of the necessary code in one exe file (called TUC_menu.exe), with some flat files for changing parameters
Installation for TUC.zip.  Download and extract in a dedicated folder.  Run TUC.exe.  Wait ten seconds for the menu to pop up.

2)  WINDOWS - Python environment:  You can grab all of the source py files and associated flat files and run the TUC_menu.py from your python environment

FAQ:
What does the program do?

After setting the parameters you want, it produces a traveller sector and provides the information in two separate files. 
The first file is a txt file that matches the T5 format for the TravellerMap website.  The information can be cut and pasted and placed directly into that site's custom map option.

The second file is a database file (using SQLite DB) that houses information for every star and planet in the sector.  It includes UWPs for mainworld and non-mainworlds.
You can browse and search this database using the excellent SQLite browser from: https://sqlitebrowser.org/

What Traveller rules does it use?

It uses GURPS First In for the science stuff (like stellar details, and planet temperature) and T5 rules for the Traveller stuff (like law level and influence scores)






