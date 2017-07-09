#!/usr/bin/python

# A one time script to load constant data from the First In charts into a database

import sqlite3

def create_tables(c,conn):
    sql_create_tb_stellar_charts = """CREATE TABLE tb_stellar_charts( 
        luminosity_class TEXT,
        spectral_type TEXT,
        radius REAL,
        hundred_diameter REAL,
        far_life_zone REAL,
        time_to_lz_1g REAL,
        time_to_lz_2g REAL,
        time_to_lz_3g REAL,
        lz_in_100d BOOLEAN
        );"""
    c.execute('DROP TABLE IF EXISTS tb_stellar_charts')
    c.execute(sql_create_tb_stellar_charts) 

def create_planet_size_tables(c,conn):
    sql_create_tb_planet_charts = """CREATE TABLE tb_planet_charts( 
        size INTEGER,
        d100_km REAL,
        d100_au REAL,
        time_to_100d_1g REAL,
        time_to_100d_2g REAL,
        time_to_100d_3g REAL);"""
    c.execute('DROP TABLE IF EXISTS tb_planet_charts')
    c.execute(sql_create_tb_planet_charts) 

def get_stellarcharsv():
# Loading the Stellar Characteristics for Class V Table         
    temp_stellarcharsv = {}
    for line in open(FILE_PATH + "/Star Characteristics V.txt"):
        data = line.strip().split(',')
        temp_stellarcharsv[data[0]] = dict(zip(('temperature', 'luminosity', 'mass', 'radius', 'lifespan'), data[1:]))
      
    return temp_stellarcharsv

def get_stellarcharsiii():
# Loading the Stellar Characteristics for Class V Table         
    temp_stellarcharsiii = {}
    for line in open(FILE_PATH + "/Star Characteristics III.txt"):
        data = line.strip().split(',')
        temp_stellarcharsiii[data[0]] = dict(zip(('temperature', 'luminosity', 'mass', 'radius', 'lifespan'), data[1:]))
      
    return temp_stellarcharsiii    
    
def get_orbitalzone():
# Loading the Orbital Zones Table          
    temp_orbitalzone = {}
    for line in open(FILE_PATH + "/Orbital Zones Table.txt"):
        data = line.strip().split(',')
        temp_orbitalzone[data[0]] = dict(zip(('inner_limit', 'life_zone_min', 'life_zone_max', 'snow_line', 'outer_limit'), data[1:])) 
    return temp_orbitalzone

def get_config():
#   A function that retrieves the config file
    ficonfig = open("D:\Dropbox\Code\Python Scripts\modules\FirstInMods\First In.cfg", "r").readlines()
	#ficonfig = open("C:\Users\sean\Dropbox\Code\Python Scripts\modules\FirstInMods\First In.cfg.surface", "r").readlines()
    
    return ficonfig

def get_time_days(gravities, meters):
    time_days = round(((2 * ((meters/(gravities * 10)) ** 0.5))/ 3600 / 24),2)
    return time_days



configlist = get_config()
FILE_PATH = str(configlist[23])

CHARSV = {}
CHARSV = get_stellarcharsv()

CHARSIII = {}
CHARSIII = get_stellarcharsiii()

OZONE = {}
OZONE = get_orbitalzone()


  


# Open the SQLite 3 database

#conn = sqlite3.connect(FILE_PATH + '/firstin.db')
conn = sqlite3.connect(FILE_PATH + '/firstin3000_project.db')
c = conn.cursor()

create_tables(c,conn)
create_planet_size_tables(c,conn)

for row in CHARSV:
    
    sqlcommand = '''    INSERT INTO tb_stellar_charts (luminosity_class, 
                        spectral_type, radius, hundred_diameter,far_life_zone,
                        lz_in_100d,time_to_lz_1g,time_to_lz_2g,time_to_lz_3g) 
                        VALUES(?,?,?,?,?,?,?,?,?) '''

    hund_d_calc = float(CHARSV[row]["radius"]) * 200
    life_zone_calc = float(OZONE[row]["life_zone_max"])
    if life_zone_calc > 0:
        if hund_d_calc > life_zone_calc:  
            mask_calc = True
            distance_au = hund_d_calc - life_zone_calc
            distance_m  = distance_au * 1.496e+11
            time_d_1g   = get_time_days(1,distance_m)
            time_d_2g   = get_time_days(2,distance_m)
            time_d_3g   = get_time_days(3,distance_m)

        else: 
            mask_calc = False
            time_d_1g   = 0
            time_d_2g   = 0
            time_d_3g   = 0
    else: 
        mask_calc = False
        time_d_1g   = 0
        time_d_2g   = 0
        time_d_3g   = 0

                        
    body_row =          ('V',
                        row,
                        CHARSV[row]["radius"],
                        hund_d_calc,
                        life_zone_calc,
                        mask_calc,
                        time_d_1g,
                        time_d_2g,
                        time_d_3g
                        )
                        

    c.execute(sqlcommand, body_row)   

for i in range(0,16):
    sqlcommand = '''    INSERT INTO tb_planet_charts (  size,
                                                        d100_km,
                                                        d100_au,
                                                        time_to_100d_1g,
                                                        time_to_100d_2g,
                                                        time_to_100d_3g) 
                        VALUES(?,?,?,?,?,?) '''    
    size = i
    d100_km = 1600 * i * 100
    d100_au = round(d100_km / 1.496e+8,4)
    time_to_100d_1g = get_time_days(1,d100_km*1000)
    time_to_100d_2g = get_time_days(2,d100_km*1000)
    time_to_100d_3g = get_time_days(3,d100_km*1000)

    body_row =          (   size,
                            d100_km,
                            d100_au,
                            time_to_100d_1g,
                            time_to_100d_2g,
                            time_to_100d_3g
                        )
                        

    c.execute(sqlcommand, body_row)   




conn.commit()  
c.close()
conn.close()