def generate_far_trader_stats(seed_number,db_name):

# Far Trader
# by Sean Nelson

#   A program to teach Sean the Python programming language
#   The goal is to create a table with mainworld merchant stats
#   Using GURPS Far Tarder info

    import sqlite3
    import random
    #random.seed(100)
    
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
        
    
       
    def create_tb_far_trader_table():
        sql_create_tb_far_trader_table = """CREATE TABLE    tb_far_trader( 
                                                            location TEXT PRIMARY KEY,
                                                            wtn INTEGER,
                                                            gwp INTEGER,
                                                            exchange)
                                                            ;"""
                                                        
        c.execute('DROP TABLE IF EXISTS tb_far_trader')
        c.execute(sql_create_tb_far_trader_table)  
        
    def get_exchange(starport, tech_level):
        starport_ex_dict = {'A':1,'B':0.95,'C':0.90,'D':0.85,'E':0.80,'X':0.20}
        tech_mod = (15 - tech_level) * 0.05
        exchange = 1 - tech_mod
        if exchange < 0: exchange = 0
        return exchange
    
    # MAIN PROGRAM
        
    conn = sqlite3.connect(db_name+'.db')
    c = conn.cursor()
    create_tb_far_trader_table()    
    
    sql3_select_tb_t5 = """     SELECT  location,
                                        starport,
                                        population,
                                        tech_level,
                                        remarks
                                FROM    tb_t5 """
                                    
    c.execute(sql3_select_tb_t5)
    allrows = c.fetchall()
        
    for row in allrows:
#        print (row[0])
        location = str(row[0])
        starport = str(row[1])
        population = int(row[2])
        tech_level = int(row[3])
        remarks = str(row[4])
        if population > 0:
        
            uwtn = -100
            tl_mod = -100
            pop_mod = -100
            port_mod = -100
            wtn = -100
            
            pop_mod = round(population/2,1)
            if tech_level <= 2: tl_mod = -0.5
            elif tech_level <= 5: tl_mod = 0
            elif tech_level <= 8: tl_mod = 0.5
            elif tech_level <= 11: tl_mod = 1
            elif tech_level <= 13: tl_mod = 1.5
            else: tl_mod = 2
            
            uwtn = round(tl_mod + pop_mod,2)
#            print (uwtn)
            
            port_dict = {   'A':(1.5,1,1,0.5,0.5,0,0,0),
                            'B':(1,1,0.5,0.5,0,0,-0.5,-1),
                            'C':(1,0.5,0.5,0,0,-0.5,-1,-1.5),
                            'D':(0.5,0.5,0,0,-0.5,-1,-1.5,-2),
                            'E':(+0.5,0,0,-0.5,-1,-1.5,-2,-2.5),
                            'X':(0,0,-2.5,-3,-3.5,-4,-4.5,-5)}
                            
            mod_uwtn = int(uwtn)
            if mod_uwtn > 7: mod_uwtn = 7
            elif mod_uwtn < 0: mod_uwtn = 0
            
            port_mod = port_dict[starport][mod_uwtn]
#            print (port_mod)
            
            wtn = uwtn + port_mod
#            print (wtn)
            
            bpr = -100
            bpr_list = (55,85,135,220,350,560,895,1430,2290,3660,5860,9375,15000,24400,40000,60000)
            tl_lookup = tech_level
            if tl_lookup > 15: tl_lookup = 15
            bpr = bpr_list[tl_lookup]
#            print(bpr)
            
            bpr_trade_mod = 1
            
            if 'Ri' in remarks:  bpr_trade_mod = bpr_trade_mod * 1.6
            if 'In' in remarks:  bpr_trade_mod = bpr_trade_mod * 1.4
            if 'Ag' in remarks:  bpr_trade_mod = bpr_trade_mod * 1.2
            if 'Po' in remarks:  bpr_trade_mod = bpr_trade_mod * 0.8
            if 'Ni' in remarks:  bpr_trade_mod = bpr_trade_mod * 0.8
            if 'As' in remarks:  bpr_trade_mod = bpr_trade_mod * 0.8
            elif 'De' in remarks:  bpr_trade_mod = bpr_trade_mod * 0.8
            elif 'Fl' in remarks:  bpr_trade_mod = bpr_trade_mod * 0.8
            elif 'Ic' in remarks:  bpr_trade_mod = bpr_trade_mod * 0.8
            elif 'Va' in remarks:  bpr_trade_mod = bpr_trade_mod * 0.8
            
            bpr_trade = bpr * bpr_trade_mod
#            print(bpr_trade)
            
            gwp = round(bpr_trade * population * 10,0)
#            print(gwp)
            
            exchange = get_exchange(starport, tech_level)
    		
        else: 
            wtn = 0
            gwp = 0
            exchange = 0
            
        sqlcommand = '''    INSERT INTO tb_far_trader ( location,
                                                            wtn,
                                                            gwp,
                                                            exchange)                                        
                                                    VALUES(?, ?, ?, ?) '''
    
                    
        body_row =          (location,
                            wtn,
                            gwp,
                            exchange)
                        
      
        c.execute(sqlcommand, body_row) 
            
    conn.commit()
    conn.close()