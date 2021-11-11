def build_travellermap_file(db_name):


# Traveller Map
# by Sean Nelson


#   Open the SQLite 3 database

    import sqlite3
    trav_filename = db_name + '.txt'
    
    with open(trav_filename, 'w') as f:
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
    
     
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    sql3_select_locorb = """        SELECT  location,                             
                                            system_name,
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
                                         
                                    FROM    main_worlds
                                    """
    
    
    c.execute(sql3_select_locorb)
    allrows = c.fetchall()
#    stall = input('Wait hold on.  About to open the file')

    with open(trav_filename, 'a') as f:
#        stall = input('Wait hold on.  File opened')    
        for row in allrows:
#            print(row[0], row[5], row[6])
            f.write('\t'.join(row[0:]) + '\t'+ '\n')
    
    conn.commit()
    conn.close()