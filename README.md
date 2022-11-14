traveller-universe-creator 
aka Bartleby's Sector Builder

v 1.0 - 2022-11-12

The goal is to generate an entire Traveller sector of stars, planets, moons using "realistic" scientific models

Description:

After running the generate_menu.py program, four files will be produced and placed in the /sector_db folder.
  - A SQLite database with all of the system data (titled with the name of the sector with the extension .db)
  - A tab delimited text file for system data import into the TravellerMap website (title + '_tab.txt')
  - Text file for route data import into the TravellerMap website (title + '-routes.txt')
  - A file named 'sec_m01_m01.dat' for import into Shawn Driscoll's excellent: https://github.com/ShawnDriscoll/PyMapGen

How to Run?

Option 1:  From the installer
 - download and run the install_sector.exe file - it will export everything you need in the directory you choose
 - run generate_menu.exe to generate a DB
 - find generated DBs in /sector_db
 - run browse_sector.exe to view a sector
 - optionally use a DB browser (like https://sqlitebrowser.org/) to look at every piece of data for each planet/system
 - please note:  the example-66 database in the /sector_db directory MUST be there for browse_sector to work.  Do not remove it.
 
 
Option 2: From the code - requires python environment
 - environment imports are below in the FAQ
 - run generate_menu.py to generate a DB
 - find generated DBs in /sector_db
 - run browse_sector.py to view a sector
 - optionally use a DB browser (like https://sqlitebrowser.org/) to look at every piece of data for each planet/system
 - please note:  the example-66 database in the /sector_db directory MUST be there for browse_sector to work.  Do not remove it.

FAQ:
Q:  What does the program do?

A:  After setting the parameters you want, it produces a traveller sector and provides the information in separate files explained above.

The text files can be used to visualize the sector using https://travellermap.com/ or PyMapGen at https://github.com/ShawnDriscoll/PyMapGen

The db file houses information for every star and planet in the sector.  It includes UWPs for mainworld and non-mainworlds.
You can browse and search this database using the excellent SQLite browser from: https://sqlitebrowser.org/

Q:  What Traveller rules does it use?

A:  It uses mostly GURPS First In for the science stuff (like stellar details, and planet temperature).  
    T5 rules for the Traveller stuff (like law level and influence scores).
    I have also been using parts of Architect of Worlds (a modern update to First In by the same creator)

Q:  How do you run it?

A:  Run the generate_menu to create a sector.  Run the browse_sector to explore the sectors you create.

Q:  What imports do I need?

A:
	PySimpleGUI     v4.60.3
	pandas          v1.4.2
	numpy           v1.22.3
	networkx        v2.8.4
	matplotlib      v3.5.2
	pillow          v9.2
	pyInstaller	v4.8

Q:  Where do the planet names come from

A:  They come from all over the internet, but most come from: https://simplemaps.com/data/world-cities

Q:  What are these other non-python files?

A:

traveller_map_poster.html:  a spartan method of using the travellermap API to build sector maps for the sectors you build.
Choose the tab and route file and click submit and an image map of your sector will be created by travellermap.

names.csv: Used to create planet/moon names and can be modified to add or remove names you prefer or dislike.  
Be careful if you remove too many names as the program requires thousands and will crash if it runs out (it does not use the same one twice)

trade_goods.csv:  Copied from T5 and used to show wants and surpluses in each system.  Feel free to modify to taste.

txt files:  various First In tables used to create the science stuff.  Feel free to modify but be careful - you void the warranty if you mess with this stuff.

Q:  Where can I find more info?

A:  I hang out at COTI (https://www.travellerrpg.com/) from time to time and discuss it there.  

I also made some YouTube vidoes walking through the program:  https://www.youtube.com/channel/UCJVDA8TEy3aRHwrGVTsNJBg



