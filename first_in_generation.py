def generate_stars(makeit_list):


# First In Generation
# by Sean Nelson

# A program to teach Sean the Python programming language
# The goal is to generate a series of star systems for Traveller using the First In ruleset


# Possible Improvements Pending:

#   Things skipped that need to be added:
#   - Distant companions are only notified by adding a * to the Distant value.  
#       -Need a separate file with details?
#   - Planetoid modifiers (when near a Gas Giant) were not included.
#   - Not building planetary bodies in binary and trinary systems
#       - Very close companions should have details combined
#       - Other companions must handle Forbidden Zone
#       - Orbital bodies for non-primary stars
#   - Gas Giant details (including moons)
#   - Expand moon data
#   - Add tidal effects
#   - World Types are straight from the table, should have variation as per the rules



#   - To Do list complete:
#   - COMPLETE: Add Stellar Age
#   - COMPLETE: Appropriate Planet Size modifiers
#   - COMPLETE: Validate order in orbits of secondary and tertiary 
#       - (Tertiary are automatically set to distant orbits)
#   - COMPLETE: Stellar data loaded in a database. 
#   - COMPLETE: White Dwarf details and orbital bodies
#   - COMPLETE: Rolls are added to a table with relevant data
#   - FIXED: Minimum 25 size for GG    


    import csv
    import time
    import sqlite3
    import math 
    import random
    

    
    def create_tables(c,conn):
        sql_create_tb_stellar_primary = """CREATE TABLE tb_stellar_primary( 
            location TEXT PRIMARY KEY,
            system_type TEXT,
            luminosity_class TEXT,
            spectral_type TEXT,
            age REAL,
            stellar_radius REAL,
            b_o_r REAL,
            bode_c REAL,
            orbits INTEGER,
            belts INTEGER,
            gg INTEGER
            );"""
        c.execute('DROP TABLE IF EXISTS tb_stellar_primary')
        c.execute(sql_create_tb_stellar_primary) 
        
        sql_create_tb_stellar_secondary = """CREATE TABLE tb_stellar_secondary( 
            location TEXT PRIMARY KEY,
            luminosity_class TEXT,
            spectral_type TEXT,
            age REAL,
            orbit_description TEXT,
            avg_orbit REAL,
            orbital_ecc REAL,
            min_orbit REAL,
            max_orbit REAL,
            b_o_r REAL,
            bode_c REAL,
            orbits INTEGER
            );"""
        c.execute('DROP TABLE IF EXISTS tb_stellar_secondary')
        c.execute(sql_create_tb_stellar_secondary) 
        
        sql_create_tb_stellar_tertiary = """CREATE TABLE tb_stellar_tertiary( 
            location TEXT PRIMARY KEY,
            luminosity_class TEXT,
            spectral_type TEXT,
            age REAL,
            orbit_description TEXT,
            avg_orbit REAL,
            orbital_ecc REAL,
            min_orbit REAL,
            max_orbit REAL,
            b_o_r REAL,
            bode_c REAL,
            orbits INTEGER
            );"""
        c.execute('DROP TABLE IF EXISTS tb_stellar_tertiary')
        c.execute(sql_create_tb_stellar_tertiary)    

        
        sql_create_tb_orbital_bodies = """CREATE TABLE tb_orbital_bodies( 
            location_orbit TEXT PRIMARY KEY,
            location TEXT,
            orbit INTEGER,
            distance REAL,
            zone TEXT,
            body TEXT,
            size integer,
            density REAL,
            mass REAL,
            gravity REAL,
            moons INTEGER,
            year REAL,
            day INTEGER,
            size_class TEXT,
            wtype TEXT,
            atmos_pressure FLOAT,
            hydrographics INTEGER,
            atmos_composition TEXT,
            temperature INTEGER,
            climate TEXT,
            mainworld_calc FLOAT,
            mainworld_status TEXT DEFAULT 'N'
            );"""
        c.execute('DROP TABLE IF EXISTS tb_orbital_bodies')
        c.execute(sql_create_tb_orbital_bodies)   
        
        
        sql_create_tb_dice_table = """CREATE TABLE tb_fi_dice_rolls( 
            location TEXT,
            number INTEGER,
            reason TEXT,
            total INTEGER
            );"""
        c.execute('DROP TABLE IF EXISTS tb_fi_dice_rolls')
        c.execute(sql_create_tb_dice_table)  
        
    
    def roll_dice(no_dice, why, location):
        no_dice_loop = no_dice + 1  #increment by one for the FOR loop
        sum_dice = 0
        for dice_loop in range (1,no_dice_loop):
            sum_dice = sum_dice + random.randrange(1,7)
            
        c.execute("INSERT INTO tb_fi_dice_rolls (location, number, reason, total) VALUES(?, ?, ?, ?)",
               (str(location), 
                no_dice,
                why,
                sum_dice))
                
        return sum_dice   
    
       
    def four_root(num):
        num = float(num)
        return float(num ** 0.25)
 
    
           
        
    def get_multiple_stars(location):
    #   A function that returns the # of stars in the system
        mult_roll = roll_dice(3,'# of stars',location)
        if mult_roll <= MULTIPLE_STAR_CHANCE_S:
            rolled_multiple = "Solo"
        elif mult_roll <= MULTIPLE_STAR_CHANCE_B:
            rolled_multiple = "Binary"
        else:
            rolled_multiple = "Trinary"
        return rolled_multiple
        
    def get_luminosity_class(location):
    #   A function that returns the stellar luminosity
        lum_roll = roll_dice(3,'stellar luminosity',location)
        if lum_roll <= LUM_CLASS_CHANCE_III:
            rolled_lum = "III"
        elif lum_roll <= LUM_CLASS_CHANCE_V:   
            rolled_lum = "V"
        else:
            rolled_lum = "D"
            
        return rolled_lum   
        
    def get_spectral(location):
    #   A function that returns the spectral class
        spec_roll = roll_dice(3,'spectral class',location)
        if spec_roll <= SPEC_CLASS_CHANCE_A:
            rolled_spec = "A"
        elif spec_roll <= SPEC_CLASS_CHANCE_F:
            rolled_spec = "F"
        elif spec_roll <= SPEC_CLASS_CHANCE_G:
            rolled_spec = "G"
        elif spec_roll <= SPEC_CLASS_CHANCE_K:
            rolled_spec = "K"
        else:
            rolled_spec = "M"
        
        subspec_roll = roll_dice(1,'sub spectral class',location)
        if subspec_roll <4:
            subspec = "0"
        else:
            subspec = "5"
        finalspec = (rolled_spec + subspec)
        return finalspec
        
    def get_stellarcharsv():
    # Loading the Stellar Characteristics for Class V Table         
        temp_stellarcharsv = {}
        for line in open("Star Characteristics V.txt"):
            data = line.strip().split(',')
            temp_stellarcharsv[data[0]] = dict(zip(('temperature', 'luminosity', 'mass', 'radius', 'lifespan'), data[1:]))
          
        return temp_stellarcharsv
    
    def get_stellarcharsiii():
    # Loading the Stellar Characteristics for Class V Table         
        temp_stellarcharsiii = {}
        for line in open("Star Characteristics III.txt"):
            data = line.strip().split(',')
            temp_stellarcharsiii[data[0]] = dict(zip(('temperature', 'luminosity', 'mass', 'radius', 'lifespan'), data[1:]))
          
        return temp_stellarcharsiii    
        
    def get_orbitalzone():
    # Loading the Orbital Zones Table          
        temp_orbitalzone = {}
        for line in open("Orbital Zones Table.txt"):
            data = line.strip().split(',')
            temp_orbitalzone[data[0]] = dict(zip(('inner_limit', 'life_zone_min', 'life_zone_max', 'snow_line', 'outer_limit'), data[1:])) 
        
        return temp_orbitalzone
        
    def get_companion_separation():
    # Loading the Orbital Separation Table 
        temp_orbitalsep = {}
        for line in open("Orbital Separation Table.txt"):
            data = line.strip().split(',')
            temp_orbitalsep[data[0]] = dict(zip(('separation', 'orbital_mod'), data[1:])) 
        
        return temp_orbitalsep
        
    def get_planet_density_table():
    # Loading the Planet Density Table
        temp_planet_density = {}
        for line in open("Planet Density Table.txt"):
            data = line.strip().split(',')
            temp_planet_density[data[0]] = dict(zip(('inside_snow_line', 'outside_snow_line'), data[1:])) 
           
        return temp_planet_density
        
    def get_world_type_table():
    # Loading the World Type Table
        temp_world_type = {}
        for line in open("World Type Table.txt"):
            data = line.strip().split(',')
            temp_world_type[data[0]] = dict(zip(('Inner Zone', 'Life Zone', 'Middle Zone', 'Outer Zone', 'Forbidden'), data[1:])) 
           
        return temp_world_type
        
    
    def populate_orbit_distance(D,B):
    # Uses a list and Bodes law to return the orbital distances
        od_list = list()
        od_list.append(0)
        od_list.append(D)
        od_list.append(D + B)
        od_list.append(D + B * 2)
        od_list.append(D + B * 4)
        od_list.append(D + B * 8)
        od_list.append(D + B * 16)
        od_list.append(D + B * 32)
        od_list.append(D + B * 64)
        od_list.append(D + B * 128)
        od_list.append(D + B * 256)
        od_list.append(D + B * 512)
        od_list.append(D + B * 1024)
        od_list.append(D + B * 2048)
        od_list.append(D + B * 999999999)
    
        return od_list
    
    def generate_common_stellar_data(spec,lumc,location):
    # Generate common stellar stats for any type of star
    # Return the details as a list (common list)
    
        if lumc == 'V':
            stellar_temp = CHARSV[spec]["temperature"]
            stellar_luminosity = CHARSV[spec]["luminosity"]
            stellar_mass = CHARSV[spec]["mass"]
            stellar_radius = CHARSV[spec]["radius"]
            temp_stellar_lifespan = CHARSV[spec]["lifespan"]
            # for main sequence(V) planets this number is maximum age.  We need to assign an age for this particular star
            adjust_age = roll_dice(2, 'stellar age',location)
            if adjust_age > float(temp_stellar_lifespan):
                adjust_age = temp_stellar_lifespan
            stellar_lifespan = str(adjust_age)
            
            orbital_inner_limit = OZONE[spec]["inner_limit"]
            orbital_lz_min = OZONE[spec]["life_zone_min"]
            orbital_lz_max = OZONE[spec]["life_zone_max"]
            orbital_snow_line = OZONE[spec]["snow_line"]
            orbital_outer_limit = OZONE[spec]["outer_limit"]
        elif lumc == 'III':
            stellar_temp = CHARSIII[spec]["temperature"]
            stellar_luminosity = CHARSIII[spec]["luminosity"]
            stellar_mass = CHARSIII[spec]["mass"]
            stellar_radius = CHARSIII[spec]["radius"]
            stellar_lifespan = CHARSIII[spec]["lifespan"]        
            orbital_inner_limit = -1
            orbital_lz_min = -1
            orbital_lz_max = -1
            orbital_snow_line = -1
            orbital_outer_limit = -1                    
        else:
            stellar_temp = 0
            stellar_luminosity = 0.001
            stellar_mass = 0.14 + (roll_dice(3, 'wD Mass', location) * 0.04)
            stellar_radius = 0.00003
            stellar_lifespan = 0
            orbital_inner_limit = 0.1
            orbital_lz_min = 0.15
            orbital_lz_max = 0.15
            orbital_snow_line = 0.19
            orbital_outer_limit = 2  
    
    #calculate the orbits
        base_orbital_radius_int = (roll_dice(1,'base orbital radius',location) + 1)
        base_orbital_radius = float(base_orbital_radius_int/2)
        base_orbital_radius = float(base_orbital_radius) * float(orbital_inner_limit)
        bode_roll = roll_dice(1,'bode constant roll',location)
        if bode_roll < 3:
            bode_constant = 0.3
        elif bode_roll < 5:
            bode_constant = 0.35
        else:
            bode_constant = 0.4
    
        orbits_distance_list = list()
        orbits_distance_list = populate_orbit_distance(base_orbital_radius, bode_constant)
            
        orbits = -1
        loop_a = 0
    
        if base_orbital_radius > 0:
            while (float(orbits_distance_list[loop_a]) < float(orbital_outer_limit)):
                loop_a = loop_a + 1
        orbits = loop_a - 1 #above while will go one too far, needs to be corrected
            
    
        common_list = list()
        common_list =  (stellar_temp,
                        stellar_luminosity,
                        stellar_mass,
                        stellar_radius,
                        stellar_lifespan,
                        orbital_inner_limit,
                        orbital_lz_min,
                        orbital_lz_max,
                        orbital_snow_line,
                        orbital_outer_limit,
                        round(base_orbital_radius,4),
                        bode_constant,
                        orbits)     
        
        return common_list
    
        
    def populate_primary_dict(location, psd_spectral_type,psd_luminosity_class,psd_multiple_star_status):
    # Populate the primary stellar dictionary stats 
        
        p_common_stellar_data = list()
        p_common_stellar_data = generate_common_stellar_data(psd_spectral_type,psd_luminosity_class,location)
        
        psd_stellar_dict = {"p_system_type"         : psd_multiple_star_status,
                            "p_luminosity_class"    : psd_luminosity_class,
                            "p_spectral_type"       : psd_spectral_type,
                            "p_temperature"         : p_common_stellar_data[0],
                            "p_luminosity"          : p_common_stellar_data[1],
                            "p_mass"                : p_common_stellar_data[2],
                            "p_radius"              : p_common_stellar_data[3],
                            "p_age"                 : p_common_stellar_data[4],
                            "p_inner_limit"         : p_common_stellar_data[5],
                            "p_lz_min"              : p_common_stellar_data[6],
                            "p_lz_max"              : p_common_stellar_data[7],
                            "p_snow_line"           : p_common_stellar_data[8],
                            "p_outer_limit"         : p_common_stellar_data[9],
                            "p_base_orbital_radius" : p_common_stellar_data[10],
                            "p_bode_constant"       : p_common_stellar_data[11],
                            "p_orbits"              : p_common_stellar_data[12],
                            "p_belts"            : 0,
                            "p_gg"               : 0}                          
    
                            
        return psd_stellar_dict
    
    def find_csd_spectral_type(third_roll,prime_spec_type):
    # Use the spectral type of the primary to find the spectral type of the companion
    
        if third_roll < 5:
            spec_diff = 0
        elif third_roll == 4:
            spec_diff = 1
        elif third_roll == 5:
            spec_diff = 2
        else:
            spec_diff = 3
        
        spec_list = ["A","F","G","K","M"]
        spec_number = spec_list.index(prime_spec_type[0])
        spec_number = spec_number + spec_diff
        if spec_number > 4:
            spec_number = 4
        companion_spec = (spec_list[spec_number] + '5')
        return companion_spec
    
    def get_orbit_ecc(o_separation, location):
        ecc_list = list()
        ecc_list = [0.05,0.1,0.2,0.3,0.4,0.4,0.5,0.5,0.5,0.6,0.6,0.7,0.7,0.8,0.9,0.95]
        ecc_roll = roll_dice(3, 'orbital eccentricity',location)
        if o_separation == "Very Close":
            ecc_roll = ecc_roll - 6
        elif o_separation == "Close":
            ecc_roll = ecc_roll - 4
        elif o_separation == "Moderate":
            ecc_roll = ecc_roll - 2
    
        if ecc_roll < 3:
            ecc_roll = 3
        elif ecc_roll > 18:
            ecc_roll = 18
        
        #adjust ecc_roll to match list index (0 to 15)
        ecc_roll = ecc_roll - 3
        
        orbit_ecc = 0
        orbit_ecc = ecc_list[ecc_roll]
    
        return orbit_ecc
    
        
    def get_companion_orbit(n,c_sep,location):
        
    #   n represents which number star this is in the system
    #   c_sep is the companion separation dictionary
    
    #   First In asks for any star beyond the second to have a plus 6.  
    #   Or suggests just arbitrarily picking an orbit that works
    #   Recent astronomy suggests most third stars are distant - so we will just do that.
    #   Adding 13 to the role will ensure that
    
        if n > 2:
            die_mod = 13
        else:
            die_mod = 0
        sep_roll_lu = "X"
        sep_roll = roll_dice(3,'separation distance',location) + die_mod
        if sep_roll <= 6:
            sep_roll_lu = "6"
        elif sep_roll <= 9:
            sep_roll_lu = "9"
        elif sep_roll <= 11:
            sep_roll_lu = "11"
        elif sep_roll <= 14:
            sep_roll_lu = "14"
        else:
            sep_roll_lu = "15"
            
        sep_dict = {}
        sep_dict = c_sep
        
        # Below is the separation description from the Orbital Separation Table
        sep_desc = sep_dict[sep_roll_lu]['separation']                      
        # Below is the radius multiplier from the Orbital Separation Table
        sep_rad_mod = round(float(sep_dict[sep_roll_lu]['orbital_mod']),4)  
        
        sep_rad_roll = roll_dice(2, 'separation radius multiplier',location)
        sep_rad_final = float(sep_rad_mod + sep_rad_roll)
        
          
        #check to see if the companion is Distant and has its own companion.  For now mark with an asterisk in Separation description
    
        if sep_desc == "Distant":
            check_distant = roll_dice(3, 'distant companion check',location)
            if check_distant >= DISTANT_COMPANION_CHANCE:
                sep_desc = "Distant*"
    
       
        orbital_ecc = float(get_orbit_ecc(sep_desc,location))
        
        min_orbit = (1 - orbital_ecc) * sep_rad_final
        max_orbit = (1.00 + orbital_ecc) * sep_rad_final
       
        
        
        sep_list = list()
        sep_list = (sep_roll,
                    sep_desc,
                    sep_rad_mod,
                    sep_rad_roll,
                    sep_rad_final,
                    orbital_ecc,
                    round(min_orbit,2),
                    round(max_orbit),)
                    
        
                    
        return sep_list
        
    def populate_companion_dict(location, primary_dict,companion):
    # Populate the companion stellar dictionary stats
    # companion = the number of star in the system (2 = secondary, 3 = tertiary)
    
    
        star_no = companion
        csd_orbit = list()
        csd_orbit = get_companion_orbit(star_no,COMP_SEP,location)
     
        sec_lum_roll_a = roll_dice(1, 'comp lum class #1',location)
        sec_lum_roll_b = roll_dice(1, 'comp lum class #2',location)
        csd_spec_roll = roll_dice(1, 'comp spec roll',location)
        
        if primary_dict["p_luminosity_class"] == "D":
            csd_luminosity_class = "D"
            csd_spectral_type = "w"
        elif primary_dict["p_luminosity_class"] == "V":
            if sec_lum_roll_a < 5:
                csd_luminosity_class = "V"
                csd_spectral_type = find_csd_spectral_type(csd_spec_roll,primary_dict["p_spectral_type"])
            else:
                if sec_lum_roll_b < 5:
                    csd_luminosity_class = "V"
                    csd_spectral_type = "M5"
                else:
                    csd_luminosity_class = "D"
                    csd_spectral_type = "w"
        elif primary_dict["p_luminosity_class"] == "III":
            if sec_lum_roll_a < 5:
                csd_luminosity_class = "III"
                csd_spectral_type = find_csd_spectral_type(csd_spec_roll,primary_dict["p_spectral_type"])
            elif sec_lum_roll_a == 5:
                csd_luminosity_class = "V"
                csd_spectral_type = find_csd_spectral_type(csd_spec_roll,primary_dict["p_spectral_type"])
            else:
                if sec_lum_roll_b < 5:
                    csd_luminosity_class = "V"
                    csd_spectral_type = "M5"
                else:
                    csd_luminosity_class = "D"
                    csd_spectral_type = "w"
        
        else:
            csd_luminosity_class = "X"
            csd_spectral_type = "X"
         
        
    
        c_common_stellar_data = list()
        c_common_stellar_data = generate_common_stellar_data(csd_spectral_type,csd_luminosity_class,location)
    
       
        
        
        companion_dict = {}    
        if companion == 2:
            companion_dict = {  "s_orbit_desc"          : csd_orbit[1],
                                "s_lum_roll_a"          : sec_lum_roll_a,
                                "s_lum_roll_b"          : sec_lum_roll_b,
                                "s_spec_roll"           : csd_spec_roll,
                                "s_luminosity_class"    : csd_luminosity_class,
                                "s_spectral_type"       : csd_spectral_type,
                                "s_sep_roll"            : csd_orbit[0],
                                "s_rad_mod"             : csd_orbit[2],
                                "sep_rad_roll"          : csd_orbit[3],
                                "sep_rad_final"         : csd_orbit[4],
                                "s_orbital_ecc"         : csd_orbit[5],
                                "s_min_orbit"           : csd_orbit[6],
                                "s_max_orbit"           : csd_orbit[7],                            
                                "s_temperature"         : c_common_stellar_data[0],
                                "s_luminosity"          : c_common_stellar_data[1],
                                "s_mass"                : c_common_stellar_data[2],
                                "s_radius"              : c_common_stellar_data[3],
                                "s_age"                 : c_common_stellar_data[4],
                                "s_inner_limit"         : c_common_stellar_data[5],
                                "s_lz_min"              : c_common_stellar_data[6],
                                "s_lz_max"              : c_common_stellar_data[7],
                                "s_snow_line"           : c_common_stellar_data[8],
                                "s_outer_limit"         : c_common_stellar_data[9],
                                "s_base_orbital_radius" : c_common_stellar_data[10],
                                "s_bode_constant"       : c_common_stellar_data[11],
                                "s_orbits"              : c_common_stellar_data[12]}   
    
            # write to the database - build the secondary stellar table
        
            c.execute("INSERT INTO tb_stellar_secondary (location, luminosity_class, spectral_type, age, orbit_description, avg_orbit, orbital_ecc, min_orbit, max_orbit, b_o_r, bode_c, orbits) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (str(location), 
                                csd_luminosity_class,
                                csd_spectral_type,
                                c_common_stellar_data[4],
                                csd_orbit[1],
                                csd_orbit[4],
                                csd_orbit[5],
                                csd_orbit[6],
                                csd_orbit[7],
                                c_common_stellar_data[10],
                                c_common_stellar_data[11],
                                c_common_stellar_data[12]))
    
        
    #        conn.commit()                      
    
                                
        else:     
    
     
        
            companion_dict = {  "t_orbit_desc"          : csd_orbit[1],
                                "t_luminosity_class"    : csd_luminosity_class,
                                "t_spectral_type"       : csd_spectral_type,
                                "t_sep_roll"            : csd_orbit[0],
                                "t_rad_mod"             : csd_orbit[2],
                                "sep_rad_roll"          : csd_orbit[3],
                                "sep_rad_final"         : csd_orbit[4],
                                "t_orbital_ecc"         : csd_orbit[5],
                                "t_min_orbit"           : csd_orbit[6],
                                "t_max_orbit"           : csd_orbit[7],  
                                "t_temperature"         : c_common_stellar_data[0],
                                "t_luminosity"          : c_common_stellar_data[1],
                                "t_mass"                : c_common_stellar_data[2],
                                "t_radius"              : c_common_stellar_data[3],
                                "t_age"                 : c_common_stellar_data[4],
                                "t_inner_limit"         : c_common_stellar_data[5],
                                "t_lz_min"              : c_common_stellar_data[6],
                                "t_lz_max"              : c_common_stellar_data[7],
                                "t_snow_line"           : c_common_stellar_data[8],
                                "t_outer_limit"         : c_common_stellar_data[9],
                                "t_base_orbital_radius" : c_common_stellar_data[10],
                                "t_bode_constant"       : c_common_stellar_data[11],
                                "t_orbits"              : c_common_stellar_data[12]}    
    
        
            # write to the database - build the tertiary stellar table
        
            c.execute("INSERT INTO tb_stellar_tertiary (location, luminosity_class, spectral_type, age, orbit_description, avg_orbit, orbital_ecc, min_orbit, max_orbit, b_o_r, bode_c, orbits) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (str(location), 
                                csd_luminosity_class,
                                csd_spectral_type,
                                c_common_stellar_data[4],
                                csd_orbit[1],
                                csd_orbit[4],
                                csd_orbit[5],
                                csd_orbit[6],
                                csd_orbit[7],
                                c_common_stellar_data[10],
                                c_common_stellar_data[11],
                                c_common_stellar_data[12]))
        
        return companion_dict
    
    def get_size(r,z,s,location):
    # returns the planetary size
    # r = orbit number from the primary dictionary
    # z = zone type - full list
    # s = spectral type
    
        size_roll = roll_dice(2, 'size roll',location)
    
        if r == 1:
            size_roll = size_roll - 4
        elif z[r] != "Outer Zone":
            size_roll = size_roll - 2
        elif z[r-1] != "Outer Zone":
            size_roll = size_roll + 6
        elif z[r-2] != "Outer Zone":
            size_roll = size_roll + 4
        
        if s == "M0":
            size_roll = size_roll - 1
        elif s == "M5":
            size_roll = size_roll - 2
            
        if size_roll < 1:
            size_roll = 1
        
        return size_roll
    
    def get_gg_size(r,z,s,location):
        gg_size_int = get_size(r,z,s,location)
        gg_size_int = gg_size_int * 5
        if gg_size_int < 25: gg_size_int = 25
        return gg_size_int
            
    def get_planet_density(p_star_dict,zone,planet_size,location):
        density_float = 0
        age_float = float(p_star_dict["p_age"])
        age_mod = age_float / 2
        density_roll = roll_dice(3, 'density roll',location)
        density_float = (density_roll - age_mod)/10
        size_adjust = planet_size
        if size_adjust <= 3:
            size_adjust = 3
        elif size_adjust <= 5:
            size_adjust = 5
        elif size_adjust <= 8:
            size_adjust = 8
        else:
            size_adjust = 1000
        
        density_final = -10    
        density_age_dict = {}
        density_age_dict = get_planet_density_table()
        if zone == "Outer Zone":
            size_str = str(size_adjust)
            density_look = float(density_age_dict[size_str]["outside_snow_line"])
            density_final = density_look + density_float
    
        else:
            size_str = str(size_adjust)
            density_look = float(density_age_dict[size_str]["inside_snow_line"])
            density_final = density_look + density_float
    
           
        return density_final
            
    def get_moons(body, distance, location):
        # provide the orbital body and its distance and return the number of moons
        
        moon_no = 0
        
        if body == "Planet":
            moon_no = roll_dice(1, 'planet moon', location)
            moon_no = moon_no - 4
            if moon_no < 1:
                moon_no = 0
        elif body == "Gas Giant":
            moon_no = roll_dice(4, 'GG moon', location)
        else:
            moon_no = 0
        
        return moon_no   
    
    def get_year(mass, distance):
        # return the planetary year in earth years (orbital period)
        # mass = mass of the primary
        # distance = orbital radius of planet
        distance_float = float(distance)
        mass_float = float(mass)
        temp_year = (distance_float**3) / mass_float
        temp_year = round(math.sqrt(temp_year),2)
        return temp_year
        
    def get_day(size, location):
        # return the planetary day in earth hours (rotation period)
        # size is planetary size_adjust
        # First In also used Tidal Lock, not used here
        
        day_roll = roll_dice(3, 'day roll', location)
        day_mod = 0
        
        if size != 0:
            if size < 3:
                day_mod = 10
            elif size <6:
                day_mod = 8
            elif size <9:
                day_mod = 6
            else:
                day_mod = -1
            day_int = day_roll + day_mod
        else:
            day_int = 0
        
        return day_int
        
    def get_world_size_class(world_mass, world_size, body_type):
    
        world_size_class = "Not Found"
        if body_type == "Planetoid Belt":
            world_size_class = "Belt"
        elif body_type == "Gas Giant":
            world_size_class = "Gas Giant"
        elif body_type == "Lost":
            world_size_class = "Lost"
        elif body_type == "Planet":
            world_size_parameter = round((7.93) * world_mass / world_size,2)
            if world_size_parameter <= .13:
                world_size_class = "Tiny"
            elif world_size_parameter <= .24:
                world_size_class = "Very Small"
            elif world_size_parameter <= .38:
                world_size_class = "Small"
            elif world_size_parameter <= 1.73:
                world_size_class = "Standard"
            else:
                world_size_class = "Large"
        else:
            world_size_class = "Enigma"
        
        return world_size_class
    
    def get_world_type(size_class, zone):    
        world_type_var = "Something Crazy"
        world_type_var = WORLD_TYPE[size_class][zone]
        return world_type_var
        
    def get_atmos_pressure(size_class, world_type, location):
        atmos_var = -1
        if size_class == 'Tiny':
            atmos_var = 0.0
        elif size_class == 'Very Small':
            atmos_var = 0.1
        elif world_type == 'Belt':
            atmos_var = 0.0
        elif world_type == 'Gas Giant':
            atmos_var = 10.0
        elif world_type == 'Greenhouse':
            atmos_var = 2.0
        else:
            atmos_var = roll_dice(3,'atmos roll',location) * 0.1
            
        return atmos_var
            
    def get_hydro_pct(size_class, world_type, atmos_pressure, zone, primary_type, orbit_distance, snow_line, location):
        clear_for_hydro = True
        hydro_var = -1
        hydro_mod = 0
        ok_class = ('Large', 'Standard', 'Small')
        ok_atmos = 0.2
        not_ok_zone = ('Inner')
        
        if str(size_class) not in ok_class:
            clear_for_hydro = False
            hydro_var = -2
            
        if float(atmos_pressure) < float(ok_atmos):
            clear_for_hydro = False
            hydro_var = -3
            
        if zone == not_ok_zone:
            clear_for_hydro = False
            hydro_var = -4
            
        if float(orbit_distance) > (float(snow_line) * 3):
            clear_for_hydro = False
            hydro_var = -5
     
        if primary_type[0] == 'M': hydro_mod += 2
        if primary_type[0] == 'K': hydro_mod += 1
        if primary_type[0] == 'F': hydro_mod -= 1
        if primary_type[0] == 'A': hydro_mod -= 2
        
        if world_type[0] == 'D':
            if zone == 'Life Zone': hydro_mod -= 8
            elif zone == 'Middle Zone': hydro_mod -= 6
        elif world_type[0] == 'H': hydro_mod -= 2
    
     
        if clear_for_hydro == True:
            hydro_var = roll_dice(2, 'hydro roll',location) - 2
           
        hydro_var = hydro_var + hydro_mod
        
        if hydro_var < 0: hydro_var = 0
        if hydro_var > 10: hydro_var = 10
        
       
        return hydro_var
     
    def check_sulfur(location):
            if roll_dice(3, 'sulfur roll',location) > 12:
                atm = 'Corrosive'
            else:
                atm = 'Exotic'
            return atm
            
    def check_pollutant(location):
            if roll_dice(3, 'tainted roll',location) > 11:
                atm = 'Tainted'
            else:
                atm = 'Standard'
            return atm
                
                
    def get_atmos_comp(world_type,location):
        get_atmos_c_var = 'N/A'
        if world_type.find('(SG)') > 0:
            get_atmos_c_var = 'Corrosive'
        elif world_type.find('(A)') > 0:
            get_atmos_c_var = 'Corrosive'
        elif world_type.find('(N)') > 0:
            get_atmos_c_var = check_sulfur(location)
        elif world_type.find('Gas') == 0:
            get_atmos_c_var = 'GG'
        elif world_type[0] == 'D':
            get_atmos_c_var = check_sulfur(location)
        elif world_type.find('Green') == 0:
            get_atmos_c_var = 'Corrosive'
        elif world_type[0] == 'O':
            get_atmos_c_var = check_pollutant(location)
        else: get_atmos_c_var = 'None'
        
        return get_atmos_c_var
    
        
    def get_albedo(world_type, hydro):
        c_albedo = -1
        if world_type.find('(SG)') > 0:
            c_albedo = 0.50
        elif world_type.find('(A)') > 0:
            c_albedo = 0.50
        elif world_type.find('(N)') > 0:
            c_albedo = 0.20
        elif world_type[0] == 'D':
            c_albedo = 0.02
        elif world_type[0] == 'R':
            c_albedo = 0.02
        elif world_type[0] == 'I':
            c_albedo = 0.45
        elif world_type[0] == 'O':
            if hydro < 3:
                c_albedo = 0.02
            elif hydro < 6:
                c_albedo = 0.10
            elif hydro < 9:
                c_albedo = 0.20
            else:
                c_albedo = 0.28
        
        return c_albedo
    
    def get_greenhouse(world_type, atmos_pressure, gravity):
        c_greenhouse = -1
        greenhouse_factor = -1
        if world_type[0] == 'H':
            c_greenhouse = 0.2
        elif world_type[0] == 'O':
            c_greenhouse = 0.15
        elif world_type[0] == 'D':
            c_greenhouse = 0.10
        else:
            c_greenhouse = 0.00
        
        if gravity > 0:
            greenhouse_factor = c_greenhouse * (atmos_pressure / gravity)
        else:
            greenhouse_factor = 0
        return greenhouse_factor
        
    def get_blackbody(luminosity, orbit_distance):
        c_blackbody = -1
        c_blackbody = (278 * (four_root(luminosity)) / (math.sqrt(orbit_distance)))
        return c_blackbody
        
    def get_temperature(world_type, hydro, atmos_pressure, gravity, luminosity, orbit_distance,location):
        albedo = get_albedo(world_type, hydro)
        greenhouse = get_greenhouse(world_type, atmos_pressure, gravity)
        blackbody = get_blackbody(luminosity, orbit_distance)
        c_temperature = -1
    
        c_temperature = blackbody * (four_root(1 - albedo)) * (1 + greenhouse)
        
        return round(c_temperature,2)
        
    def get_climate(temperature, world_type):
        c_climate = 'N/A'
        if world_type[0] == 'O':
            if temperature <= 238: c_climate = 'Uninhabitable (Frigid)'
            elif temperature <= 249: c_climate = 'Frozen'
            elif temperature <= 260: c_climate = 'Very Cold'
            elif temperature <= 272: c_climate = 'Cold'
            elif temperature <= 283: c_climate = 'Chilly'
            elif temperature <= 294: c_climate = 'Cool'
            elif temperature <= 302: c_climate = 'Earth-normal'
            elif temperature <= 308: c_climate = 'Warm'
            elif temperature <= 313: c_climate = 'Tropical'
            elif temperature <= 319: c_climate = 'Hot'
            elif temperature <= 324: c_climate = 'Very Hot'
            else: c_climate = 'Uninhabitable (Torrid)'
        return c_climate
    
        
        
        
    def populate_planetary_orbits(location,p_star_dict,s_star_dict,stellar_number):
        # location is the parsec location
        # p_star_dict = is the dictionary of the current primary star
        # s_star_dict = is the dictionary of the current secondary star (if there is one).
        # **Update 2021 - stellar_number identifies which star the body is orbiting
        
        # This function populates the orbital bodies around the primary 
        # At the moment it ignores any secondary or tertiary stars
        
        # Account for the fact there might not be a companion description.
        description = s_star_dict.get("s_orbit_desc",None) 
        primary_rows = 0
        
        # This checks if there is a companion, if so remove the orbital bodies.
        primary_rows = p_star_dict["p_orbits"]
        if description != None:
            p_star_dict["p_orbits"] = primary_rows
            forbidden_inner = s_star_dict['s_min_orbit'] * 0.3
            forbidden_outer = s_star_dict['s_max_orbit'] * 3
            
        else:
            forbidden_inner = 0
            forbidden_outer = 0
      
        zones = list()
        zone_objects = list()
        size = list()
        density = list()
        mass = list()
        gravity = list()
        moons = list()
        year = list()
        day = list()
        size_class = list()
        wtype = list()
        atmos_press = list()
        hydro_pct = list()
        atmos_comp = list()
        temperature = list()
        climate = list()
        no_gg = 0
        no_belts = 0
        new_orbits = p_star_dict["p_orbits"]
    
        
        zones.append("Star")
        zone_objects.append("Star")
        size.append(0)
        density.append(0)
        mass.append(0)
        gravity.append(0)
        moons.append(0)
        year.append(0)
        day.append(0)
        size_class.append(0)
        wtype.append(0)
        atmos_press.append(0)
        hydro_pct.append(0)
        atmos_comp.append(0)
        temperature.append(0)
        climate.append(0)
    
       
        if primary_rows > 0:
            current_row = 0
            dice_location = str(location) + str(current_row)
            distance_list = populate_orbit_distance(p_star_dict["p_base_orbital_radius"],p_star_dict["p_bode_constant"])
            # Build planet info in separate lists
            while current_row < primary_rows:
                gg_check = roll_dice(3,'GG check',dice_location)
                planetoid_roll = roll_dice(3, 'planetoid check',dice_location)
                current_row = current_row + 1
                current_distance = round(distance_list[current_row],4)
                if forbidden_inner < current_distance < forbidden_outer:
                    zones.append("Forbidden")
                    zone_objects.append("Lost")
                    size.append(0)
                    density.append(0)
                elif current_distance < float(p_star_dict["p_inner_limit"]):
                    zones.append("Beyond Inner")
                    zone_objects.append("Vapour")
                    size.append(0)
                    density.append(0)
                elif current_distance < float(p_star_dict["p_lz_min"]):
                    zones.append("Inner Zone")
                    if gg_check <= 3:
                        zone_objects.append("Gas Giant")
                        size_int = get_gg_size(current_row,zones,p_star_dict["p_spectral_type"],location)
                        size.append(size_int)
                        density.append(1)
                        no_gg += 1
                    else:
                        if planetoid_roll <= 6:
                            zone_objects.append("Planetoid Belt")
                            size.append(0)
                            density.append(0)
                            no_belts += 1
                        else:
                            zone_objects.append("Planet")
                            size_int = get_size(current_row,zones,p_star_dict["p_spectral_type"],location)
                            size.append(size_int)
                            lookup_density = get_planet_density(p_star_dict, zones[current_row], size_int,location)
                            density.append(lookup_density)
                             
                elif current_distance < float(p_star_dict["p_lz_max"]):
                    zones.append("Life Zone")
                    if gg_check <= 4:
                        zone_objects.append("Gas Giant")
                        size_int = get_gg_size(current_row,zones,p_star_dict["p_spectral_type"],location)
                        size.append(size_int)
                        density.append(1)
                        no_gg += 1
                    else:
                        if planetoid_roll <= 6:
                            zone_objects.append("Planetoid Belt")
                            size.append(0)
                            density.append(0)
                            no_belts += 1
                        else:
                            zone_objects.append("Planet")
                            size_int = get_size(current_row,zones,p_star_dict["p_spectral_type"],location)
                            size.append(size_int)   
                            lookup_density = get_planet_density(p_star_dict, zones[current_row], size_int,location)
                            density.append(lookup_density)
                            
                elif current_distance < float(p_star_dict["p_snow_line"]):
                    zones.append("Middle Zone")
                    if gg_check <= 7:
                        zone_objects.append("Gas Giant")
                        size_int = get_gg_size(current_row,zones,p_star_dict["p_spectral_type"],location)
                        size.append(size_int)
                        density.append(1)
                        no_gg += 1
                    else:
                        if planetoid_roll <= 6:
                            zone_objects.append("Planetoid Belt")
                            size.append(0)
                            density.append(0)
                            no_belts += 1
                        else:
                            zone_objects.append("Planet")
                            size_int = get_size(current_row,zones,p_star_dict["p_spectral_type"],location)
                            size.append(size_int)   
                            lookup_density = get_planet_density(p_star_dict, zones[current_row], size_int,location)
                            density.append(lookup_density)
                            
                else:
                    zones.append("Outer Zone")
    
                    if gg_check <= 14:
                        zone_objects.append("Gas Giant")
                        size_int = get_gg_size(current_row,zones,p_star_dict["p_spectral_type"],location)
                        size.append(size_int)
                        density.append(1)
                        no_gg += 1
                    else:
                        if planetoid_roll <= 6:
                            zone_objects.append("Planetoid Belt")
                            size.append(0)
                            density.append(0)
                            no_belts += 1
                        else:
                            zone_objects.append("Planet") 
                            size_int = get_size(current_row,zones,p_star_dict["p_spectral_type"],location)
                            size.append(size_int)       
                            lookup_density = get_planet_density(p_star_dict, zones[current_row], size_int,location)
                            density.append(lookup_density)                        
            
                if zones[current_row] != 'Forbidden':
                    calc_mass = round((density[current_row] * (size[current_row]**3)) / 2750 ,2)
                    mass.append(calc_mass)
                    
                    if size[current_row] == 0:
                        calc_gravity = 0
                    else:
                        calc_gravity = round((62.9 * calc_mass) / (size[current_row] ** 2),2)
                    
                    gravity.append(calc_gravity)
    
                    moons.append(get_moons(zone_objects[current_row],current_distance,location))
                    year.append(get_year(p_star_dict["p_mass"],current_distance))
                    day.append(get_day(size[current_row],location))
                    size_class.append(get_world_size_class(mass[current_row],size[current_row],zone_objects[current_row]))
                    wtype.append(get_world_type(size_class[current_row], zones[current_row]))
                    atmos_press.append(get_atmos_pressure(size_class[current_row], wtype[current_row],location))
                    
                    hydro_pct.append(get_hydro_pct( size_class[current_row], 
                                                    wtype[current_row],
                                                    atmos_press[current_row],
                                                    zones[current_row],
                                                    p_star_dict["p_spectral_type"],
                                                    current_distance,
                                                    p_star_dict["p_snow_line"],
                                                    location))
                                                    
                    atmos_comp.append(get_atmos_comp(wtype[current_row],location))
                    temperature.append(get_temperature( wtype[current_row], 
                                                        hydro_pct[current_row], 
                                                        atmos_press[current_row],
                                                        gravity[current_row],
                                                        p_star_dict["p_luminosity"],
                                                        current_distance,
                                                        location))
    
                    climate.append(get_climate(temperature[current_row], wtype[current_row]))
    
                    
                    ob_db_key = (str(location) + '-' + str(stellar_number) + '-' + str(current_row)) 
                    
                    
                    sqlcommand = '''    INSERT INTO tb_orbital_bodies (location_orbit, 
                                        location, 
                                        orbit, 
                                        distance,
                                        zone, 
                                        body, 
                                        size, 
                                        density,
                                        mass,
                                        gravity,
                                        moons,
                                        year,
                                        day,
                                        size_class,
                                        wtype,
                                        atmos_pressure,
                                        hydrographics,
                                        atmos_composition,
                                        temperature,
                                        climate) 
                                        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
                                        
                    body_row =          (str(ob_db_key),
                                        str(location),
                                        current_row,
                                        current_distance,
                                        zones[current_row],
                                        zone_objects[current_row],
                                        size[current_row],
                                        density[current_row],
                                        mass[current_row],
                                        gravity[current_row],
                                        moons[current_row],
                                        year[current_row],
                                        day[current_row],
                                        size_class[current_row],
                                        wtype[current_row],
                                        atmos_press[current_row],
                                        hydro_pct[current_row],
                                        atmos_comp[current_row],
                                        temperature[current_row],
                                        climate[current_row])
                                        
                    
                    c.execute(sqlcommand, body_row)           
                else:
                    new_orbits -= 1
                    primary_rows -= 1
                    current_row -= 1
                    
        else:
            pass
        
        p_star_dict["p_orbits"] = new_orbits
        p_star_dict["p_gg"] = no_gg
        p_star_dict["p_belts"] = no_belts
            
        return p_star_dict
    
    
    def populate_db_tables(primary_dict):
    
        c.execute("INSERT INTO tb_stellar_primary (location, system_type, luminosity_class, spectral_type, age, stellar_radius, \
                  b_o_r, bode_c, orbits, gg, belts) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                 (str(parsec), 
                    primary_stellar_dict_r["p_system_type"],
                    primary_stellar_dict_r["p_luminosity_class"],
                    primary_stellar_dict_r["p_spectral_type"],
                    primary_stellar_dict_r["p_age"],
                    primary_stellar_dict_r["p_radius"],
                    primary_stellar_dict_r["p_base_orbital_radius"],
                    primary_stellar_dict_r["p_bode_constant"],
                    primary_stellar_dict_r["p_orbits"],
                    primary_stellar_dict_r["p_gg"],
                    primary_stellar_dict_r["p_belts"]))
    
    
        
        
    #Main Program
    

    ###########################################################
    #   Break down input variable 'makeit_list'
#                 0   random_seed_input, 
#                 1   sector_name_input,
#                 2   density_input,
#                 3   lumiii_input,
#                 4   lumv_input,
#                 5   spectrala_input,
#                 6   spectralf_input,
#                 7   spectralg_input,
#                 8   spectralk_input,
#                 9   solo_input,
#                 10   binary_input,
#                 11  distant_input
    seed_number = makeit_list[0]
    random.seed(seed_number)
    
    SECTORS = 1   #Program set for building one sector at this time.  More than one sector will just erase the previous.
    DB_NAME = makeit_list[1] + '.db'
    LIKELIHOOD = int(makeit_list[2])
    LUM_CLASS_CHANCE_III = int(makeit_list[3])
    LUM_CLASS_CHANCE_V = int(makeit_list[4])
    SPEC_CLASS_CHANCE_A = int(makeit_list[5])
    SPEC_CLASS_CHANCE_F = int(makeit_list[6])
    SPEC_CLASS_CHANCE_G = int(makeit_list[7])
    SPEC_CLASS_CHANCE_K = int(makeit_list[8])
    MULTIPLE_STAR_CHANCE_S = int(makeit_list[9])
    MULTIPLE_STAR_CHANCE_B = int(makeit_list[10])
    DISTANT_COMPANION_CHANCE = int(makeit_list[11])
    ############################################################
    
    # Load the external tables into memory
    CHARSV = {}
    CHARSV = get_stellarcharsv()
    
    CHARSIII = {}
    CHARSIII = get_stellarcharsiii()
    
    OZONE = {}
    OZONE = get_orbitalzone()
    
    COMP_SEP = {}
    COMP_SEP = get_companion_separation()
    
    WORLD_TYPE = {}
    WORLD_TYPE = get_world_type_table()
    
    
    # Open the SQLite 3 database
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
     
    
    create_tables(c,conn)
    
    
    
    total_systems = 0
    
    
    #   Loop for each sector
    for a in range(0,SECTORS):
        astring = str(a)
    
    #   Loop for each parsec in a subsector
        for x in range (1,33):
            if x < 10:
                xstring = ("0" + str(x))
            else:
                xstring = (str(x))
            for y in range (1,41):
                if y < 10:
                    ystring = ("0" + str(y))
                else:           
                    ystring = (str(y))
                parsec = str(xstring + ystring)                
    #           Generate a random d6 to check for system presence against LIKELIHOOD
                rollgen = roll_dice(1, 'system presence',parsec)
              
    ###################################################################################
    # This section builds the system                                                  #
    ###################################################################################
                if rollgen >= LIKELIHOOD:  
                    systempresent = True
                    multiple_star_status = get_multiple_stars(parsec)
                    luminosity_class = get_luminosity_class(parsec)
                    if luminosity_class == "D":
                         spectral_type = "w"
                    else:
                        spectral_type = get_spectral(parsec)
    
                  
                    primary_stellar_dict_r = {}  
                    primary_stellar_dict_r = populate_primary_dict( parsec, 
                                                                    spectral_type,
                                                                    luminosity_class,
                                                                    multiple_star_status)
                    
                    total_systems = total_systems + 1
                   
                  
#                    print(parsec + ':' + primary_stellar_dict_r["p_system_type"])
    
                    
                    secondary_stellar_dict_r = {}  
                    comp_no = 2 # this is the second star in the system
                    if primary_stellar_dict_r["p_system_type"] != "Solo":
                        secondary_stellar_dict_r = populate_companion_dict( parsec, 
                                                                            primary_stellar_dict_r,
                                                                            comp_no)    
                  
                    tertiary_stellar_dict_r = {}  # one row in the stellar dictionary for tertiaries
                    comp_no = 3 # this is the third star in the system
                    if primary_stellar_dict_r["p_system_type"] == "Trinary":
                        tertiary_stellar_dict_r = populate_companion_dict(  parsec,
                                                                            primary_stellar_dict_r,
                                                                            comp_no)    
     
                    stellar_number = 1  # Future use to populate secondary and tertiary stars
                    primary_stellar_dict_r = populate_planetary_orbits(parsec,primary_stellar_dict_r, secondary_stellar_dict_r,stellar_number)
                    
                    populate_db_tables(primary_stellar_dict_r)
                    
    ####################################################################################
                    
    
                else:
                    systempresent = False
    print(total_systems,'different systems generated.')           
    conn.commit()  
    c.close()
    conn.close()
    
    
    
       
    
    
    
    
    
        
