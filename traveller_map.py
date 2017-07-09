#!/usr/bin/python

# Traveller Map
# by Sean Nelson

#   A program to teach Sean the Python programming language
#   The goal is to export a file that can be ready by travellermap.com

#   Open the SQLite 3 database

import sqlite3

with open('C:/Users/sean/Dropbox/Code/Python Scripts/modules/FirstInMods/travinfile.txt', 'w') as f:
    f.write('Hex' + '\t' \
    + 'Name' + '\t' \
    + 'UWP' + '\t' \
    + 'Bases' + '\t' \
    + 'Remarks' + '\t' \
    + 'Zone' + '\t' \
    + 'PBG' + '\t' \
    + 'Allegiance' + '\t' \
    + 'Stars' +  '\t' \
    + '{Ix}' +  '\t' \
    + '(Ex)' +  '\t' \
    + '[Cx]' +  '\t' \
    + 'Nobility' + '\t' \
    + 'W' + '\t' \
    + '\n')

    
conn = sqlite3.connect('C:/Users/sean/Dropbox/Code/Python Scripts/modules/FirstInMods/firstin3000_project.db')
c = conn.cursor()

sql3_select_locorb = """        SELECT  location, 
                                        name,
                                        uwp,
                                        bases,
                                        remarks,
                                        zone,
                                        pbg,
                                        allegiance,
                                        stars,
                                        ix,
                                        ex,
                                        cx,
                                        n,
                                        w
                                     
                                FROM    tb_t5
                                """


c.execute(sql3_select_locorb)
allrows = c.fetchall()
with open('C:/Users/sean/Dropbox/Code/Python Scripts/modules/FirstInMods/travinfile.txt', 'a') as f:
    
    for row in allrows:
        print(row[0], row[5], row[6])
        f.write('\t'.join(row[0:]) + '\t'+ '\n')

conn.commit()
conn.close()