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
    
    conn = sqlite3.connect(db_name)
    c = conn.cursor()


    try:
        sql_orbital = '''SELECT location_orbit, location, stellar_distance, size, stellar_orbit_no from orbital_bodies'''
        df_orbital_bodies = pd.read_sql_query(sql_orbital,conn)
    except:
        print(db_name,'Journey Table:  Failed building orbital table')
    
    
    try:
        sql_stellar = '''SELECT location, radius as stellar_radius, companion_class from stellar_bodies'''
        df_stellar = pd.read_sql_query(sql_stellar,conn)
    except:
        print(db_name,'Journey Table:  Failed building stellar table')
        
   
    
    try:
    
        df_orbital_bodies['left_match'] = df_orbital_bodies.location_orbit.str.slice(0, 6)


        df_stellar['match'] = df_stellar['location'] + '-' + df_stellar['companion_class']

        
        df_journey = pd.merge(df_orbital_bodies,df_stellar, how='left', left_on='left_match', right_on='match')
    
    except:    
        print('Journey Table: Failed at df merge')
        
        
        
    try:
        df_journey['stellar_mask_Mm'] = df_journey['stellar_radius'] * 200 * 149598.073 # convert radius in AU to Mm
        stellar_mask_Mm = df_journey['stellar_mask_Mm']    
        
    
        df_journey['planetary_mask_Mm'] = round(df_journey['size'] * 1.690 * 100,3)
        df_journey['planetary_distance_Mm'] = df_journey['stellar_distance'] * 149598.073
        
    
        planet_Mm = df_journey['planetary_distance_Mm']
        planet_mask = df_journey['planetary_mask_Mm']
    
        
        df_journey['planetary_mask_end_Mm'] = planet_Mm + planet_mask
        planet_mask_end = df_journey['planetary_mask_end_Mm'] 
        
       
        # Set the status of any stellar masking
        conditions  = [ stellar_mask_Mm > planet_mask_end, 
                       (stellar_mask_Mm < planet_mask_end) & (stellar_mask_Mm > planet_Mm), 
                        stellar_mask_Mm < planet_Mm ]
        choices     = [ 'total', 'partial', 'none' ]
        df_journey['planet_stellar_masked'] = np.select(conditions, choices, default=np.nan) 
    
        df_journey['jump_point_Mm'] = np.where(stellar_mask_Mm > planet_mask_end,
                                               stellar_mask_Mm - planet_Mm,
                                               planet_mask_end - planet_Mm)

    except:
        print('Journey Table: Failed at calculations')

    try:
        for x in range(1,8):
            d_a = df_journey['jump_point_Mm']*1000000/(9.8 * x)
            sqrt_d_a = d_a**0.5
            ix_hrs = 'hrs_' + str(x) + 'g'
            df_journey[ix_hrs] = round(sqrt_d_a*2/3600,1)
    except:
        print('Journey Table: Failed at Acceleration Measurements')


    df_journey.to_sql('journey_data', conn)

    conn.commit()  
    c.close()
    conn.close()
    
