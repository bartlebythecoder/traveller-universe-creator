def choose_mainworld(db_name):
#!/usr/bin/python

# Mainworld Selector
# by Sean Nelson

#   A program to teach Sean the Python programming language
#   The goal is to read the Orbital Bodies table generated from the
#   First In program and adjust by the Mainworld_Calc module

#   The output is a new column in the Orbital Bodies Table.  It needs to run after First In and Mainworld_Calc

# Open the SQLite 3 database

    import sqlite3
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    sql3_select_loc = """           SELECT  location
                                    FROM    stellar_bodies
                                    WHERE   orbits > 0 """
                            
    sql3_select_locorb = """        SELECT  location,
                                            location_orbit,
                                            mainworld_calc  
                                    FROM    orbital_bodies
                                    WHERE   location = ? """             
                            
    sql3_insert_status = """        UPDATE    orbital_bodies
                                    SET       mainworld_status = ? 
                                    WHERE     location_orbit = ? """
                                    
    loc_list = list()
    c.execute(sql3_select_loc)
    allrows = c.fetchall()
    for row in allrows:
    
        loc_list.append(row[0])
    
    for n in loc_list:
        c.execute(sql3_select_locorb,(n,))
        allrows = c.fetchall()
        top_calc = -1000000
        top_locorb = 0
        for row in allrows:
            if row[2] > top_calc:
                top_calc = row[2]
                top_locorb = row[1]
        if top_calc > -1000000:
            c.execute(sql3_insert_status,('Y',top_locorb))
#        print (n, top_locorb, top_calc)
    
    conn.commit()
    conn.close()        
