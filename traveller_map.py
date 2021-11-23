def build_travellermap_file(db_name):


# Traveller Map
# by Sean Nelson
# Generate a TravellerMap-like extract for import into Traveller Map or other programs


#   Open the SQLite 3 database

    import sqlite3
    
    
    def tohex(dec):
        if dec > 15: dec = 15
        x = (dec % 16)
        digits = "0123456789ABCDEF"
        rest = dec / 16
        # if (rest == 0):
        return digits[int(x)]
        # return tohex(rest) + digits[int(x)]
    
    
# Main Program
    
    trav_filename = db_name + '.txt'    
    with open(trav_filename, 'w') as f:
        f.write('Hex' + '\t' \
        + 'Name' + '\t' \
        + 'UWP' + '\t' \
        + 'Remarks' + '\t' \
        + '{Ix}' +  '\t' \
        + '(Ex)' +  '\t' \
        + '[Cx]' +  '\t' \
        + 'Nobility' + '\t' \
        + 'Bases' + '\t' \
        + 'Zone' + '\t' \
        + 'PBG' + '\t' \
        + 'W' + '\t' \
        + 'Allegiance' + '\t' \
        + 'Stars' + '\n')
    
     
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    sql3_select_locorb = """        SELECT  t.*,
                                            s.*
                                    FROM    traveller_stats t
                                    LEFT JOIN system_stats s
                                    ON t.location = s.location
                                    WHERE t.main_world = 1
                                    """
    
    
    c.execute(sql3_select_locorb)
    allrows = c.fetchall()
#    stall = input('Wait hold on.  About to open the file')

    with open(trav_filename, 'a') as f:
#        stall = input('Wait hold on.  File opened')    
        for row in allrows:
            location = row[2]
            name = row[3]
            uwp = (row[4] \
                + tohex(int(row[5]))\
                + tohex(int(row[6])) \
                + tohex(int(row[7])) \
                + tohex(int(row[8])) \
                + tohex(int(row[9])) \
                + tohex(int(row[10])) \
                + '-'
                + tohex(int(row[11])))

            remarks = row[15]
            ix = row[16]
            ex = row[17]
            cx = row[18]
            n = row[19]
            bases = row[20]
            zone = row[21]
            pbg = row[22]
            w = row[23]
            allegiance = row[24]
            stars=row[25]
#            print(row[2], uwp)
            tab = '\t'           
            try:
                f.write(location + tab + 
                        name + tab +    
                        uwp + tab +
                        remarks + tab +
                        ix + tab +
                        ex + tab +
                        cx + tab +
                        n + tab +
                        bases + tab +
                        zone + tab +
                        pbg + tab +
                        w + tab +
                        allegiance + tab +
                        stars +                         
                        '\n')
            except:
                print('Failed to update',trav_filename,uwp)
    
    conn.commit()
    conn.close()