def choose_mainworld(db_name):
#!/usr/bin/python

# Mainworld Selector
# by Sean Nelson

#   The goal is to read the Orbital Bodies table generated from the
#   First In program and adjust by the Mainworld_Calc module

#   The output is a new column in the Orbital Bodies Table.  It needs to run after First In and Mainworld_Calc



    import sqlite3
    import PySimpleGUI as sg
        
    import traceback
    import sys
    
    
    
    
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    sql3_select_loc = """           SELECT  location
                                    FROM    stellar_bodies
                                    WHERE   orbits > 0"""
                            
    sql3_select_locorb = """        SELECT  location,
                                            location_orbit,
                                            mainworld_calc  
                                    FROM    main_world_eval
                                    WHERE   location = ? """             
                            
    sql3_insert_status = """        UPDATE    main_world_eval
                                    SET       mainworld_status = 'Y' 
                                    WHERE     location_orbit = ? """
                                    
    loc_list = list()
    
    
    c.execute(sql3_select_loc)
    allrows = c.fetchall()
    for row in allrows:
    
        loc_list.append(row[0])
        
    loc_list = set(loc_list)
    loc_len = len(loc_list)
    for j,n in enumerate(loc_list):

        sg.one_line_progress_meter('Universe Generation Underway', j+1, loc_len, 'System Count')


        c.execute(sql3_select_locorb,(n,))
        allrows = c.fetchall()
        top_calc = -1000000
        top_locorb = 0
        for row in allrows:
            if row[2] > top_calc:
                top_calc = row[2]
                top_locorb = row[1]

        if top_calc >= -1000000:
#            print('Trying to write to DB')
            try:
                c.execute(sql3_insert_status,[top_locorb,])
                conn.commit()
            except:
                print('Write failed',top_locorb)
                print('SQLite traceback: ')
                exc_type, exc_value, exc_tb = sys.exc_info()
                print(traceback.format_exception(exc_type, exc_value, exc_tb))

        else:
            print('Location ERROR!!',top_calc,top_locorb)
#        
    

    conn.close()        
    