def generate_non_mainworlds(seed_number,db_name):


# Non Main World
# by Sean Nelson

#   A program to teach Sean the Python programming language
#   The goal is to read the Orbital Bodies table generated from the
#   First In program and and build a new table using Traveller 5 stats
#   Non Mainworld bodies.  Mainworld bodies are produced in Travellerization

    
    
    import sqlite3
    import random
    random.seed(seed_number)
    
    
    def get_system_name(name_list):
        names_left = len(name_list)
        name_picked = name_list[random.randrange(0,names_left)]
        name_fixed = name_picked.rstrip('\n')
        name_list.remove(name_picked)
        return name_fixed
    
    
    
    def roll_dice(no_dice, why, location):
        no_dice_loop = no_dice + 1  #increment by one for the FOR loop
        sum_dice = 0
        for dice_loop in range (1,no_dice_loop):
            sum_dice = sum_dice + random.randrange(1,7)
            
        c.execute("INSERT INTO die_rolls (location, number, reason, total) VALUES(?, ?, ?, ?)",
               (str(location), 
                no_dice,
                why,
                sum_dice))
                
        return sum_dice   
    
       
    def tohex(dec):
        if dec > 15: dec = 15
        x = (dec % 16)
        digits = "0123456789ABCDEF"
        rest = dec / 16
        # if (rest == 0):
        return digits[int(x)]
        # return tohex(rest) + digits[int(x)]
        
        
    def capture_mainworld_stats():
        sql3_select_tb_t5 = """     SELECT  location, 
                                            population,
                                            government
                                    FROM    main_worlds """
                                    
        c.execute(sql3_select_tb_t5)
        allrows = c.fetchall()
        mw_dict = {}
        for row in allrows:
            mw_dict[row[0]] = {     'population'        :row[1],
                                    'government'        :row[2]}
        return mw_dict        
    
    def create_tb_non_mw_table():
        sql_create_tb_non_mw_table = """CREATE TABLE    exo_worlds( 
                                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        location_orb TEXT,
                                                        location TEXT,
                                                        spaceport TEXT,
                                                        size INTEGER,
                                                        atmosphere INTEGER,
                                                        hydrographics INTEGER,
                                                        population INTEGER,
                                                        government INTEGER,
                                                        law INTEGER,
                                                        tech_level INTEGER,
                                                        uwp TEXT);"""
                                                        
        c.execute('DROP TABLE IF EXISTS exo_worlds')
        c.execute(sql_create_tb_non_mw_table)  
        
    def get_population(location,mw_dict):
        dice = roll_dice(2,'Population',location) - 4
    
        if dice > mw_dict[location]['population']:
            dice = mw_dict[location]['population'] - 1
        
        if dice < 0: dice = 0
        return dice    
            
    def get_spaceport(location,population):
        
        if population == 0:
            spaceport = 'Y'
        else:
            dice = roll_dice(1,'Spaceport',location) - population
            if dice >= 4: spaceport = 'F'
            elif dice == 3: spaceport = 'G'
            elif 1 <= dice <=2 : spaceport = 'H'
            else: spaceport = 'Y'
        
        
        return spaceport
        
    def get_atmosphere(pressure,composition):
        c_atmosphere = -1
        if pressure == 0: c_atmosphere = 0
        elif pressure == 0.1: c_atmosphere = 1
        elif composition == 'Exotic': c_atmosphere = 10
        elif composition == 'Corrosive': c_atmosphere = 11
        elif composition == 'GG': c_atmosphere = 1 
        elif composition == 'Standard':
            if pressure < 0.5: c_atmosphere = 3 
            elif pressure < 0.8: c_atmosphere = 5
            elif pressure < 1.2: c_atmosphere = 6
            elif pressure < 1.5: c_atmosphere = 8
            else: c_atmosphere = 13
        elif composition == 'Tainted':
            if pressure < 0.5: c_atmosphere = 2 
            elif pressure < 0.8: c_atmosphere = 4
            elif pressure < 1.2: c_atmosphere = 7
            elif pressure < 1.5: c_atmosphere = 9
            else: c_atmosphere = 12
        
        return c_atmosphere
        
       
    
    def get_government(location, population, mw_government):
        if mw_government == '6':
            dice = 6
        else:
            dice = roll_dice(2,'Government',row[0]) + population - 7  
            if dice < 0: dice = 0
            elif dice > 15: dice = 15
            if population == 0: dice = 0    
        return dice
        
    def get_law_level(location, government):
        dice = roll_dice(2,'Law Level',row[0]) + government - 7 
        if dice < 0: dice = 0
        elif dice > 15: dice = 15
        if population == 0: dice = 0
        return dice
        
    def get_tech_level(location, starport, size, atmosphere, hydrographics, population, government):
    
        starport_mod = -100
        starport_mod_dict = {'A':6, 'B':4, 'C':2, 'X':-4}
        if starport in starport_mod_dict.keys():
            starport_mod = starport_mod_dict[starport]
        else: starport_mod = 0
        
        size_mod = -100
        size_mod_dict = {'0':2, '1':2, '2':1, '3':1, '4':1}
        if str(size) in size_mod_dict.keys():
            size_mod = size_mod_dict[str(size)]
        else: size_mod = 0    
        
        int_atmos = int(atmosphere)
        atmosphere_mod = -100
        if int_atmos <= 3: atmosphere_mod = 1
        elif int_atmos >= 10: atmosphere_mod = 1
        else: atmosphere_mod = 0
        
        hydro_mod = -100
        if hydrographics == 9:  hydro_mod = 1
        elif hydrographics == 10: hydro_mod = 2
        else: hydro_mod = 0
        
        pop_mod = -100
        if population <= 5: pop_mod = 1
        elif population == 9: pop_mod = 2
        elif population >= 10: pop_mod = 4
        else: pop_mod = 1
        
        gov_mod = -100
        if government == 0: gov_mod = 1
        elif government == 5: gov_mod = 1
        elif government == 13: gov_mod = -2
        else: gov_mod = 0
        
        dice =  roll_dice(1, 'Tech roll', location) \
                + starport_mod \
                + size_mod  \
                + atmosphere_mod \
                + hydro_mod \
                + pop_mod \
                + gov_mod 
#        print ('Tech',starport,dice,starport_mod,size_mod,atmosphere_mod,hydro_mod,pop_mod,gov_mod)
        if population == 0: dice = 0
        return dice
            
            
    
    # MAIN PROGRAM
    
    name_list = open("names.csv", "r").readlines()
        
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    create_tb_non_mw_table()
    mw_dict = capture_mainworld_stats()
    
    try:
        sql3_select_locorb = """        SELECT  m.location_orbit,
                                                m.location,
                                                o.atmos_pressure,
                                                o.atmos_composition, 
                                                o.body, 
                                                o.hydrographics, 
                                                o.size 
                                        FROM    main_world_eval m
                                        LEFT JOIN orbital_bodies o
                                        ON o.location_orbit = m.location_orbit
                                        WHERE   mainworld_status != 'Y' """
        
        c.execute(sql3_select_locorb)
        allrows = c.fetchall()
    except: 
        print('problem with selecting from main_world_eval and orbital bodies')
    
    for row in allrows:
#        print (row[0])
        
        if row[4] != "Gas Giant":

            population = get_population(row[1],mw_dict)
            spaceport = get_spaceport(row[0],population)
            atmosphere = get_atmosphere(row[2],row[3])
            hydrographics = row[5]
            size = row[6]
            government = get_government(row[1], population,mw_dict[row[1]]['government'])    
            law_level = get_law_level(row[1], government)
            tech_level = get_tech_level(row[1], spaceport, size, atmosphere, hydrographics, population, government)
        
        else:
            population = 0
            spaceport = 'Y'
            atmosphere = 15
            hydrographics = 0
            size = row[6]
            government = 0
            law_level = 0
            tech_level = 0
            

        uwp = (spaceport + tohex(int(size))\
               + tohex(int(atmosphere)) \
               + tohex(int(hydrographics)) \
               + tohex(int(population)) \
               + tohex(int(government)) \
               + tohex(int(law_level)) \
               + '-'
               + tohex(int(tech_level)))            
            
        main_world = 0
        
        # sqlcommand = '''    INSERT INTO exo_worlds ( location_orb, 
        #                                             location, 
        #                                             spaceport, 
        #                                             size,
        #                                             atmosphere, 
        #                                             hydrographics, 
        #                                             population, 
        #                                             government,
        #                                             law,
        #                                             tech_level,
        #                                             uwp)                                            
        #                                             VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    
                            
        # body_row =          (str(row[0]),
        #                     str(row[1]),
        #                     spaceport,
        #                     size,
        #                     atmosphere,
        #                     hydrographics,
        #                     population,
        #                     government,
        #                     law_level,
        #                     tech_level,
        #                     uwp)
                        
      
        # c.execute(sqlcommand, body_row) 
    
    
##################################################################################################    
#  This code will replace above.
#  Instead of a new table, add to traveller_stats

        system_name = get_system_name(name_list)
    
        sqlcommand = '''    INSERT INTO traveller_stats(location_orb, 
                                                    location, 
                                                    system_name,
                                                    starport, 
                                                    size,
                                                    atmosphere, 
                                                    hydrographics, 
                                                    population, 
                                                    government,
                                                    law,
                                                    tech_level,
                                                    main_world)                                            
                                                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    
                            
        body_row =          (str(row[0]),
                            str(row[1]),
                            system_name,
                            spaceport,
                            size,
                            atmosphere,
                            hydrographics,
                            population,
                            government,
                            law_level,
                            tech_level,
                            main_world)
                        
      
        c.execute(sqlcommand, body_row)     
    
    
    conn.commit()
    conn.close()