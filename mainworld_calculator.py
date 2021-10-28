def generate_mainworld_scores(db_name):
#!/usr/bin/python

# Mainworld Calculator
# by Sean Nelson

#   A program to teach Sean the Python programming language
#   The goal is to read the Orbital Bodies table generated from the
#   First In program and score the potential for each body being a mainworld

#   The output is a new column in the Orbital Bodies Table.  It needs to run after First In.



# Open the SQLite 3 database

    import sqlite3
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    
    
    
    sql3_select = """ SELECT    location_orbit,
                                location, 
                                orbit, 
                                gravity, 
                                hydrographics,
                                wtype,
                                atmos_composition,
                                climate,
                                distance,
                                temperature,
                                zone
                        FROM    orbital_bodies """
    
    
    sql3_insert_calc = """  UPDATE    orbital_bodies
                            SET       mainworld_calc = ? 
                            WHERE     location_orbit = ?"""
                            
    c.execute(sql3_select)
    allrows = c.fetchall()
    for row in allrows:
    #    print('Row ->', row)
        mainworld_calc = 0
        if row[5] == 'Gas Giant': mainworld_calc -= 500
        elif row[5] == 'Belt': mainworld_calc -= 100
        if row[3] < 0.5: mainworld_calc += 10
        elif row[3] < 2: mainworld_calc += 100
        if row[4] > 0: mainworld_calc += 500
        if row[5][0] == 'O':  mainworld_calc += 2000
        elif row[5][0] == 'B': mainworld_calc += 100
        if row[6] == 'Standard':  mainworld_calc += 5000
        if row[7] == 'Earth-normal': mainworld_calc += 5000
        if 238 < row[9] < 325:  mainworld_calc += 1000
        if row[9] == 'Life Zone': mainworld_calc += 10000
    
        mainworld_calc += row[8]
    
        c.execute(sql3_insert_calc,(mainworld_calc,row[0]))
    #    print (mainworld_calc)
    
    
        
        
    conn.commit()
    conn.close()
