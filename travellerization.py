#!/usr/bin/python

# Travellerization
# by Sean Nelson

#   A program to teach Sean the Python programming language
#   The goal is to read the Orbital Bodies table generated from the
#   First In program and adjust by the Mainworld_Calc module
#   and build a new table using Traveller 5 stats

#   The output is a new Traveller5 table.  It needs to run after First In, Mainworld_Calc,
#   and Mainworld Selector

#   Currently only populating the mainworlds


#   COMPLETE:  Need to add a routine to get belts and GG totals
#   COMPLETE:  Stellar information added from all three stellar tables



import sqlite3
import random
#random.seed(100)

def capture_primary_stats():
    sql3_select_p_stars = """  SELECT   location, 
                                        luminosity_class, 
                                        spectral_type,
                                        belts,
                                        gg,
                                        orbits
                                FROM    tb_stellar_primary """
                                
    c.execute(sql3_select_p_stars)
    allrows = c.fetchall()
    p_stars_dict = {}
    for row in allrows:
        p_stars_dict[row[0]] = {    'p_lumc'        :row[1],
                                    'p_spec'        :row[2],
                                    'no_belts'      :row[3],
                                    'no_gg'         :row[4],
                                    'worlds'        :row[5]}

    return p_stars_dict

def capture_secondary_stats():
    sql3_select_c_stars = """  SELECT   location, 
                                        luminosity_class, 
                                        spectral_type
                                FROM    tb_stellar_secondary """
                                
    c.execute(sql3_select_c_stars)
    allrows = c.fetchall()
    c_stars_dict = {}
    for row in allrows:
        c_stars_dict[row[0]] = {    'c_lumc'        :row[1],
                                    'c_spec'        :row[2]}

    return c_stars_dict
    
def capture_tertiary_stats():
    sql3_select_t_stars = """  SELECT   location, 
                                        luminosity_class, 
                                        spectral_type
                                FROM    tb_stellar_tertiary """
                                
    c.execute(sql3_select_t_stars)
    allrows = c.fetchall()
    t_stars_dict = {}
    for row in allrows:
        t_stars_dict[row[0]] = {    't_lumc'        :row[1],
                                    't_spec'        :row[2]}

    return t_stars_dict    

    

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

   
def tohex(dec):
    if dec > 15: dec = 15
    x = (dec % 16)
    digits = "0123456789ABCDEF"
    rest = dec / 16
    # if (rest == 0):
    return digits[int(x)]
    # return tohex(rest) + digits[int(x)]

def create_t5_table():
    sql_create_tb_t5_table = """CREATE TABLE    tb_t5( 
                                                location_orb TEXT PRIMARY KEY,
                                                location TEXT,
                                                starport TEXT,
                                                size INTEGER,
                                                atmosphere INTEGER,
                                                hydrographics INTEGER,
                                                population INTEGER,
                                                government INTEGER,
                                                law INTEGER,
                                                tech_level INTEGER,
                                                uwp TEXT,
                                                remarks TEXT,
                                                ix TEXT,
                                                ex TEXT,
                                                cx TEXT,
                                                n TEXT,
                                                bases TEXT,
                                                zone TEXT,
                                                pbg TEXT,
                                                w TEXT,
                                                allegiance TEXT,
                                                stars TEXT
                                                
                                                
                                                );"""
    c.execute('DROP TABLE IF EXISTS tb_t5')
    c.execute(sql_create_tb_t5_table)  

def get_starport(location, population):
# Using First In rules for Starport
    c_starport = 'Z'
    
    dice = roll_dice(3,'Starport A',location)
    if population >= 6:
        if dice < population + 3: 
            c_starport = 'A'
            return c_starport
            
    dice = roll_dice(3,'Starport B',location)
    if population >= 6:
        if dice < population + 6: 
            c_starport = 'B'
            return c_starport   

    dice = roll_dice(3,'Starport C',location)
    if dice < population + 9: 
            c_starport = 'C'
            return c_starport

    dice = roll_dice(3,'Starport D',location)            
    if dice < population + 8:
            c_starport = 'D'
            return c_starport
            
    dice = roll_dice(3,'Starport E',location)            
    if dice < 15:
            c_starport = 'E'
            return c_starport
    
    dice = roll_dice(3,'Starport X',location)
    c_starport = 'X'
    return c_starport
        
def get_population(location):
        dice = roll_dice(2,'Population',location) - 2
        if dice == 10:
          dice = roll_dice(2,'Population',location) + 3
        return dice
        
def get_belts(location,gg_belt_stats):
    c_no_belts = -1
    c_no_belts = gg_belt_stats[location]['no_belts']
    return c_no_belts
    
def get_gg(location,gg_belt_stats):
    c_no_gg = -1
    c_no_gg = gg_belt_stats[location]['no_gg']
    return c_no_gg
        
        
def get_pop_mod(location,population):
    if population != 0:    
        c_pop_mod = str(random.randrange(0,10))
    else:
        c_pop_mod = 0
    return c_pop_mod
    
def get_bases(location, starport):
    str_base = 'X'
    base_list = list()
    if starport == 'D': 
        dice = roll_dice(2,'Scout Base',location)
        if dice <= 7: base_list.append('S')
    elif starport == 'C': 
        dice = roll_dice(2,'Scout Base',location)
        if dice <= 6: base_list.append('S')    
    elif starport == 'B': 
        dice1 = roll_dice(2,'Scout Base',location)
        dice2 = roll_dice(2,'Naval Base',location)
        if dice1 <= 5: base_list.append('S') 
        if dice2 <= 5: base_list.append('N')
    elif starport == 'A':
        dice1 = roll_dice(2,'Scout Base',location)
        dice2 = roll_dice(2,'Naval Base',location)
        if dice1 <= 4: base_list.append('S') 
        if dice2 <= 6: base_list.append('N')
    
    if 'S' in base_list:
        if 'N' in base_list:
            str_base = 'NS'
        else: str_base = 'S'
    elif 'N' in base_list: str_base = 'N'
    else: str_base = '-'
        
    return str_base

def get_atmosphere(pressure,composition):
    c_atmosphere = -1
    if pressure == 0: c_atmosphere = 0
    elif pressure == 0.1: c_atmosphere = 1
    elif composition == 'Exotic': c_atmosphere = 10
    elif composition == 'Corrosive': c_atmosphere = 11
    elif composition == 'GG': c_atmosphere = 1 #need a function to get GG moon data
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
    
def get_hydrographics(body, hydro):
    c_hydro = -1
    if body == 'Gas Giant': c_hydro = 1 # add a function to get a GG moon data
    else: c_hydro = hydro
    return c_hydro
    
def get_size(body, size):
    c_size = -1
    if body == 'Gas Giant': c_size = '1' # add a function to get a GG moon data
    else: c_size = size
    return c_size

def get_government(location, population):
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
    print ('Tech',starport,dice,starport_mod,size_mod,atmosphere_mod,hydro_mod,pop_mod,gov_mod)
    if population == 0: dice = 0
    return dice
#    
def remark_check(*varg):
    rem_result = False
    for i in varg:
        if i[0] in i[1]: 
            rem_result = True
            print ('In',i[0],i[1])
        else: 
            print ('Out',i[0],i[1])
            return False
    return rem_result

        
    
def get_remarks(starport, size, atmosphere, hydrographics, population, government):   
    remarks_list = list()
   
    if remark_check((size,(0,)),(atmosphere,(0,)),(hydrographics,(0,))):
        remarks_list.append('As')

    atm_de = (2,3,4,5,6,7,8,9)
    hyd_de = (0,)
    if remark_check((atmosphere,atm_de),(hydrographics,hyd_de)):
        remarks_list.append('De')
            
    atm_fl = (10,11,12)
    hyd_fl = (1,2,3,4,5,6,7,8,9,10)
    if remark_check((atmosphere,atm_fl),(hydrographics,hyd_fl)):
        remarks_list.append('Fl')
            
    siz_ga = (6,7,8)
    atm_ga = (5,6,8)
    hyd_ga = (5,6,7)
    if remark_check((size,siz_ga),(atmosphere,atm_ga),(hydrographics,hyd_ga)):
        remarks_list.append('Ga')

    siz_he = (3,4,5,6,7,8,9,10,11,12)
    atm_he = (2,4,7,9,10,11,12)
    hyd_he = (0,1,2)
    if remark_check((size,siz_he),(atmosphere,atm_he),(hydrographics,hyd_he)):
        remarks_list.append('He')
                
    atm_ic = (0,1)
    hyd_ic = (1,2,3,4,5,6,7,8,9,10)
    print (atmosphere, hydrographics)
    if remark_check((atmosphere,atm_ic),(hydrographics,hyd_ic)):
            print('Found ice! <<<<<<<<<<<<<<<<<<<<<<<<<')
            remarks_list.append('Ic')
    else: print ('No Ice!')
    print (remarks_list)
            
            
    siz_oc = (10,11,12)
    atm_oc = (3,4,5,6,7,8,9,10,11,12)
    hyd_oc = (10,)
    if remark_check((size,siz_oc),(atmosphere,atm_oc),(hydrographics,hyd_oc)):
        remarks_list.append('Oc')
                
    if atmosphere == 0: remarks_list.append('Va')
    
    siz_wa = (3,4,5,6,7,8,9,10)
    atm_wa = (3,4,5,6,7,8,9)
    hyd_wa = (10,)
    if remark_check((size,siz_wa),(atmosphere,atm_wa),(hydrographics,hyd_wa)):
        remarks_list.append('Wa')

    pop_ba = (0,)
    gov_ba = (0,)
    law_ba = (0,)
    if remark_check((population,pop_ba),(government,gov_ba),(law_level,law_ba)):
        remarks_list.append('Ba')
            
    if 0 < population < 4: remarks_list.append('Lo')

    if 3 < population < 7: remarks_list.append('Ni')

    if population == 8: remarks_list.append('Ph')

    if population > 8: remarks_list.append('Hi')
    
    atm_pa = (4,5,6,7,8,9)
    hyd_pa = (4,5,6,7,8)
    pop_pa = (4,8)
    if remark_check((atmosphere,atm_pa),(hydrographics,hyd_pa),(population,pop_pa)):
        remarks_list.append('Pa')    
    
    atm_ag = (4,5,6,7,8,9)
    hyd_ag = (4,5,6,7,8)
    pop_ag = (5,6,7)
    if remark_check((atmosphere,atm_ag),(hydrographics,hyd_ag),(population,pop_ag)):
        remarks_list.append('Ag')      
    
    atm_na = (0,1,2,3)
    hyd_na = (0,1,2,3)
    pop_na = (6,7,8,9,10,11,12,13,14,15,16,17,18,19,20)
    if remark_check((atmosphere,atm_na),(hydrographics,hyd_na),(population,pop_na)):
        remarks_list.append('Na')

    atm_px = (2,3,10,11)
    hyd_px = (1,2,3,4,5)
    pop_px = (3,4,5,6)
    law_px = (6,7,8,9)
    if remark_check((atmosphere,atm_px),(hydrographics,hyd_px),(population,pop_px),(law_level,law_px)):
        remarks_list.append('Px')
        
    atm_pi = (0,1,2,3,4,7,9)
    pop_pi = (7,8)
    if remark_check((atmosphere,atm_pi),(population,pop_pi)):
        remarks_list.append('Pi')    
        
    atm_in = (0,1,2,3,4,7,9,10,11,12)
    pop_in = (9,10,11,12,13,14,15,16,17,18,19,20)
    if remark_check((atmosphere,atm_in),(population,pop_in)):
        remarks_list.append('In')  

    atm_po = (2,3,4,5)
    hyd_po = (0,1,2,3)
    if remark_check((atmosphere,atm_po),(hydrographics,hyd_po)):
        remarks_list.append('Po')        

    atm_pr = (6,8)
    pop_pr = (5,9)
    if remark_check((atmosphere,atm_pr),(population,pop_pr)):
        remarks_list.append('Pr')   
   

    atm_ri = (6,8)
    pop_ri = (6,7,8)
    if remark_check((atmosphere,atm_ri),(population,pop_ri)):
        remarks_list.append('Ri')   
        
    
   
    return remarks_list
    
def get_ix(uwp, remarks, bases):
    c_ix = 0
    if uwp[0] in ('A','B'): c_ix += 1
    elif uwp[0] in ('D','E','X'): c_ix -= 1
    if uwp[8] in ['A','B','C','D','E','F','G','H']: c_ix += 1
    if uwp[8] in ['G','H']: c_ix += 1
    if uwp[8] in ['0','1','2','3','4','5','6','7','8']: c_ix -= 1
    if 'Ag' in remarks: c_ix += 1 
    if 'Hi' in remarks: c_ix += 1 
    if 'In' in remarks: c_ix += 1 
    if 'Ri' in remarks: c_ix += 1 
    if uwp[4] in ['0','1','2','3','4','5','6']: c_ix -= 1
    if 'N' in bases:
        if 'S' in bases: c_ix += 1
    
    return c_ix
    
def get_ex(ix, tech_level, population, remarks, belts, gg, location):
    
    resources = roll_dice(2, 'Ex res', location)
    if tech_level >= 8: 
        resources += gg
        resources += belts
    if resources < 0: resources = 0    
    resources = tohex(resources)
        
    labor = population - 1
    if labor < 0: labor = 0
    labor = tohex(labor)
    
    if 'Ba' in remarks: infrastructure = 0
    elif 'Lo' in remarks: infrastructure = 1
    elif 'Ni' in remarks: infrastructure = roll_dice(1, 'Ex infra Ni',location) + ix
    else: infrastructure = roll_dice(2, 'Ex infra', location) + ix
    if infrastructure < 0: infrastructure = 0
    infrastructure = tohex(infrastructure)
 
    
    efficiency = roll_dice(2, "Ex eff", location) - 7
    if efficiency < 0:
        return('(' + str(resources) + str(labor) + str(infrastructure) + str(efficiency) + ')')
    else:    
        return('(' + str(resources) + str(labor) + str(infrastructure) + '+' + str(efficiency) + ')')
        

def get_cx(population, ix, tech_level, location):
    homogeneity = population + roll_dice(2, 'Cx homo', location) - 7
    if homogeneity < 1:  homogeneity = 1
    homogeneity = tohex(homogeneity)
    
    acceptance = int(population) + int(ix)
    if acceptance < 1: acceptance = 1  
    acceptance = tohex(acceptance)

    
    strangeness = roll_dice(2, 'Cx strange', location) - 7 + 5
    if strangeness < 1: strangeness = 1
    strangeness = tohex(strangeness)
    
    symbols = (roll_dice(2, 'Cx symbols', location) - 7 + tech_level)
    if symbols < 1: symbols = 1
    symbols = tohex(symbols)
    
    if population == 0: return '[0000]'
    else: return ('[' + str(homogeneity) + str(acceptance) + str(strangeness) + str(symbols) + ']')
    
    
def get_zone(starport, population, government, law_level):
    zone = '-'
    if starport == 'X':
        zone = 'R'
    
    if (government + law_level) >= 22:  zone = 'R'
    elif (government + law_level) >= 20:  zone = 'A'
    
    return zone

def get_noble(remarks, ix):
    noble_list = list()

    if ix >= 4: noble_list.append('f')
    if ('Hi') in remarks: noble_list.append('E')
    elif ('In') in remarks: noble_list.append('E')
    if ('Ph') in remarks: noble_list.append('e')
    if ('Pi') in remarks: noble_list.append('D')
    if ('Ri') in remarks: noble_list.append('C')
    elif ('Ag') in remarks: noble_list.append('C')
    if ('Pa') in remarks: noble_list.append('c')
    elif ('Pr') in remarks: noble_list.append('c')

    noble_list.append('B')
    
    return noble_list
    
def get_worlds(location,gg_belt_stats):
    c_no_worlds = -1
    c_no_worlds = gg_belt_stats[location]['worlds']
    return c_no_worlds

def get_stars(location,p_star_dict,c_star_dict,t_star_dict):
    stars_text = str(p_star_dict[location]['p_spec']) + ' ' +str(p_star_dict[location]['p_lumc'])
    if location in c_star_dict.keys():
        stars_text = stars_text + ' ' + str(
                                        c_star_dict[location]['c_spec']) + ' ' +str(
                                        c_star_dict[location]['c_lumc'])
    
    if location in t_star_dict.keys():
        stars_text = stars_text + ' ' + str(
                                        t_star_dict[location]['t_spec']) + ' ' +str(
                                        t_star_dict[location]['t_lumc'])    
    return stars_text
    
   
# MAIN PROGRAM
    
conn = sqlite3.connect('D:/Dropbox/Code/Python Scripts/modules/FirstInMods/firstin.db')
c = conn.cursor()
create_t5_table()

p_stars_dict = capture_primary_stats()
c_stars_dict = capture_secondary_stats()
t_stars_dict = capture_tertiary_stats()


sql3_select_locorb = """        SELECT  *  
                                FROM    tb_orbital_bodies 
                                WHERE   mainworld_status = 'Y' """

c.execute(sql3_select_locorb)
allrows = c.fetchall()

for row in allrows:
    print (row[0])
    population = get_population(row[0])
    pop_mod = get_pop_mod(row[0],population)
    belts = get_belts(row[1],p_stars_dict)
    gg = get_gg(row[1],p_stars_dict)
    w = get_worlds(row[1],p_stars_dict)
    pbg = str(str(pop_mod) + str(belts) + str(gg))
    starport = get_starport(row[0], population)
    bases = get_bases(row[0],starport)

    
    atmosphere = get_atmosphere(row[15],row[17])
    hydrographics = get_hydrographics(row[5],row[16])
    size = get_size(row[5],row[6])
    government = get_government(row[0], population)    
    law_level = get_law_level(row[0], government)
    tech_level = get_tech_level(row[0], starport, size, atmosphere, hydrographics, population, government)
    remarks = get_remarks(starport, size, atmosphere, hydrographics, population, government)
    str_remarks = ' '.join(remarks)
    
    int_size = size
    uwp = (starport + tohex(int(size))\
           + tohex(int(atmosphere)) \
           + tohex(int(hydrographics)) \
           + tohex(int(population)) \
           + tohex(int(government)) \
           + tohex(int(law_level)) \
           + '-'
           + tohex(int(tech_level)))
           
    ix = get_ix(uwp, remarks, bases)
    if ix >= 0:
        str_ix = ('{+' + str(ix) + '}')
    else:
        str_ix = ('{' + str(ix) + '}')
        
    ex = get_ex(ix, tech_level, population, remarks, belts, gg, row[0])
    
    cx = get_cx(population, ix, tech_level, row[0])
    
    zone = get_zone(starport, population, government, law_level)
    allegiance = 'Im'
    n_list = get_noble(remarks, ix)
    n = ''.join(n_list)
    stars = get_stars(row[1],p_stars_dict,c_stars_dict, t_stars_dict)
    


    

    sqlcommand = '''    INSERT INTO tb_t5 ( location_orb, 
                                            location, 
                                            starport, 
                                            size,
                                            atmosphere, 
                                            hydrographics, 
                                            population, 
                                            government,
                                            law,
                                            tech_level,
                                            bases,
                                            pbg,
                                            remarks,
                                            uwp,
                                            ix,
                                            ex,
                                            cx,
                                            zone,
                                            n,
                                            allegiance,
                                            w,
                                            stars)                                            
                                            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
                        
    body_row =          (str(row[0]),
                        str(row[1]),
                        starport,
                        size,
                        atmosphere,
                        hydrographics,
                        population,
                        government,
                        law_level,
                        tech_level,
                        bases,
                        pbg,
                        str_remarks,
                        uwp,
                        str_ix,
                        ex,
                        cx,
                        zone,
                        n,
                        allegiance,
                        w,
                        stars)
                    

                        
    
    c.execute(sqlcommand, body_row) 








conn.commit()
conn.close()