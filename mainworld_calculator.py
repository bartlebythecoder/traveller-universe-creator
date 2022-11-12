def generate_mainworld_scores(db_name):
#!/usr/bin/python

# Mainworld Calculator
# by Sean Nelson

#   The goal is to read the Orbital Bodies table generated from the
#   First In program and score the potential for each body being a mainworld

#   The output is a new column in the Orbital Bodies Table.  It needs to run after First In.



# Open the SQLite 3 database

    import sqlite3
    import pandas as pd
    import numpy as np
    
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    
    
    
    sql3_select = """ SELECT    o.location_orbit,
                                o.location, 
                                o.gravity, 
                                o.hydrographics,
                                o.wtype,
                                o.atmos_composition,
                                o.climate,
                                o.stellar_distance,
                                o.temperature,
                                o.zone,
                                j.planet_stellar_masked
                        FROM    orbital_bodies o
                        LEFT JOIN journey_data j
                        ON o.location_orbit = j.location_orbit"""
                        
 #   print('trying to load into DF')                    
    try:
        df = pd.read_sql_query(sql3_select,conn)
#        print('df load clearly worked')
    except:
        print('Problem - df failed')
    
    
  #  print(df.describe())
    
    


    col         = 'wtype'
    conditions  = [ df[col][0] == 'O', df[col][0] == 'H', df[col] == 'Gas Giant', df[col] == 'Belt']
    choices     = [ 50000, -1000, -1000000, -500]
    df["wtype_mod"] = np.select(conditions, choices, default=0)
    


    col         = 'gravity'
    conditions  = [ df[col] > 2, (df[col] <= 2) & (df[col]>= 0.5), df[col] <= 0.5 ]
    choices     = [ -5000, 1000,0 ]
    df["grav_mod"] = np.select(conditions, choices, default=0)


    col         = 'planet_stellar_masked'
    conditions  = [ df[col] == 'total', df[col] == 'none', df[col] == 'partial' ]
    choices     = [ -5000, 1000, 200]
    df["mask_mod"] = np.select(conditions, choices, default=0)
    
 
    col         = 'atmos_composition'
    conditions  = [ df[col] == 'Standard', df[col]=='Tainted',df[col]=='Corrosive']
    choices     = [ 50000, 10000,-1000 ]
    df["atmos_mod"] = np.select(conditions, choices, default=0)    

    col         = 'temperature'
    conditions  = [ (df[col] <= 283) & (df[col]>238),
                    (df[col] > 283) & (df[col] < 309),
                    (df[col] >= 309) & (df[col] >= 324)]
    choices     = [ 1000, 2000,1000 ]
    df["temp_mod"] = np.select(conditions, choices, default=-1000)    
    df["temp_mod"] = df["temp_mod"] - (((df["temperature"] - 283) ** 2)/10)
    
 #   print('after update')
 #   print(df.describe())
    df['mainworld_calc'] = df["wtype_mod"] +  df["grav_mod"] + df["atmos_mod"] + df["temp_mod"] + df["mask_mod"]
    df['mainworld_status'] = 'N'
    
    df_mainworld_eval = df[['location',
                            'location_orbit',
                            'wtype_mod',
                            'grav_mod',
                            'atmos_mod',
                            'temp_mod',
                            'mainworld_calc',
                            'mainworld_status']]
    
#    print(df.head())

    try:
        df_mainworld_eval.to_sql('main_world_eval', conn, if_exists='replace')
    except:
        print('Could not write back to sql')
    
       
    conn.commit()
    conn.close()
