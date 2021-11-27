def build_travellermap_file(db_name,sector_name):


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
        
        
    def pad_space(detail,total):
        spaces = total - len(detail)
        for x in range(0,spaces):
            detail += ' '
        return detail
    
    
# Main Program
    

     
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
    
    
      
    conn.commit()
    conn.close()  
    
    
    ### Produce an extract T5 tab delimited file for use with Traveller Map
    
    trav_filename = db_name + '_tab' + '.txt'    
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
                
                
    ### Produce a column-specific file for use with PyMapGen

    trav_filename = 'sector_db\sec_m01_m01.dat'    
    with open(trav_filename, 'w') as f:
        f.write(
"""


# """ + sector_name + """
# 0,0

# Name:""" + sector_name + """\n

# Milieu: 

# Credits:

# Source:   

# Subsector A: A
# Subsector B: B
# Subsector C: C
# Subsector D: D
# Subsector E: E
# Subsector F: F
# Subsector G: G
# Subsector H: H
# Subsector I: I
# Subsector J: J
# Subsector K: K
# Subsector L: L
# Subsector M: M
# Subsector N: N
# Subsector O: O
# Subsector P: P







Hex  Name                 UWP       Remarks                   {Ix}   (Ex)    [Cx]   N    B  Z PBG W  A    Stellar        
---- -------------------- --------- ------------------------- ------ ------- ------ ---- -- - --- -- ---- ---------------
"""
                )   

        for row in allrows:
            location = row[2]
            
            name = pad_space(row[3],20)
                        
            uwp = (row[4] \
                + tohex(int(row[5]))\
                + tohex(int(row[6])) \
                + tohex(int(row[7])) \
                + tohex(int(row[8])) \
                + tohex(int(row[9])) \
                + tohex(int(row[10])) \
                + '-'
                + tohex(int(row[11])))
                


            remarks = pad_space(row[15],25)
            ix = pad_space(row[16],6)
            ex = pad_space(row[17],7)
            cx = pad_space(row[18],6)
            n = pad_space(row[19],4)
            bases = pad_space(row[20],2)
            zone = row[21]
            pbg = row[22]
            w = pad_space(row[23],2)
            allegiance = pad_space(row[24],4)
            stars=pad_space(row[25],15)

            tab = ' '           
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
                

