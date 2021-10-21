# -*- coding: utf-8 -*-
"""
# Journey Data


Created on Wed Oct 20 16:35:07 2021

@author: sean
"""

def build_journey_table(seed_number,db_name):
    
    import sqlite3
    import random
    import pandas as pd
    import numpy as np

    
    random.seed(seed_number)
    
    conn = sqlite3.connect(db_name+'.db')
    c = conn.cursor()


    
    sql_orbital = '''SELECT location_orbit, location, distance, size from tb_orbital_bodies'''
    df_orbital_bodies = pd.read_sql_query(sql_orbital,conn)

    sql_stellar = '''SELECT location, stellar_radius from tb_stellar_primary'''
    df_stellar = pd.read_sql_query(sql_stellar,conn)

    
    df_journey = df_orbital_bodies.merge(df_stellar, how='left', on='location')
    
    
    
    df_journey['stellar_mask_km'] = df_journey['stellar_radius'] * 200 * 149597871
    stellar_mask_km = df_journey['stellar_mask_km']    
    

    df_journey['planetary_mask_km'] = df_journey['size'] * 160930
    df_journey['planetary_distance_km'] = df_journey['distance'] * 149597871
    

    planet_km = df_journey['planetary_distance_km']
    planet_mask = df_journey['planetary_mask_km']

    
    df_journey['planetary_mask_end_km'] = planet_km + planet_mask
    planet_mask_end = df_journey['planetary_mask_end_km'] 
    
   
    # Set the status of any stellar masking
    conditions  = [ stellar_mask_km > planet_mask_end, 
                   (stellar_mask_km < planet_mask_end) & (stellar_mask_km > planet_km), 
                    stellar_mask_km < planet_km ]
    choices     = [ "total", 'partial', 'none' ]
    df_journey['planet_stellar_masked'] = np.select(conditions, choices, default=np.nan) 

    df_journey['jump_point_km'] = np.where(stellar_mask_km > planet_mask_end,
                                           stellar_mask_km - planet_km,
                                           planet_mask_end - planet_km)
    d_a_1g = df_journey['jump_point_km']*1000/9.8
    d_a_2g = df_journey['jump_point_km']*1000/(9.8*2)

    for x in range(1,8):
        d_a = df_journey['jump_point_km']*1000/(9.8 * x)
        sqrt_d_a = d_a**0.5
        ix_hrs = 'hrs_' + str(x) + 'g'
        df_journey[ix_hrs] = round(sqrt_d_a*2/3600,1)


    df_journey.to_sql('journey_data', conn)

    conn.commit()  
    c.close()
    conn.close()
    
    print('Complete')