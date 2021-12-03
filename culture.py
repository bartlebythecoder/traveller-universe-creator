# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 15:44:10 2021

@author: sean
"""
def create_culture_table(seed_number,db_name):
    
    import sqlite3
    import random
    from traveller_functions import hex_to_int, cx_values
    random.seed(seed_number)
    
    def create_culture_table():
        sql_create_tb_far_trader_table = """CREATE TABLE    perceived_culture( 
                                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            location TEXT,
                                                            age TEXT,
                                                            appearance TEXT,
                                                            tendency TEXT,
                                                            materialism TEXT,
                                                            honesty TEXT,
                                                            bravery TEXT,
                                                            social_conflict TEXT,
                                                            work_ethic TEXT,
                                                            consumerism TEXT,
                                                            spiritual_outlook TEXT,
                                                            status_quo_outlook TEXT,
                                                            custom TEXT,
                                                            interests TEXT,
                                                            common_skills TEXT)

                                                            ;"""
                                                        
        c.execute('DROP TABLE IF EXISTS perceived_culture')
        c.execute(sql_create_tb_far_trader_table)  
        
    # MAIN PROGRAM
        
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    create_culture_table()    
    
    
    age_list = ['infant-centric','infants neither seen nor heard','youth-centric','no youth culture'
                'young adult-centric','adult-centric','adult-centric','adult-centric','revere seniors','revere seniors','seniors reviled']
    appearance_list = ['dirty','clean','unkempt','immaculate','casual','formal','average','average','average']
    tendency_list = ['perceptive','violent','vain','selfish','kind','careless','capricious','serious','trusting','suspicious',
                     'studious','cruel','loquacious','curious','non-curious','intelligent','anti-intellectual','impulsive','empathetic',
                     'cheerful','morose','sensitive','insensitive','humble','haughty','even-tempered','hot-tempered','relaxed',
                     'black and white - no gray','pragmatic','sexist','obsessed','peaceful','fashionable','war']
    materialism_list = ['minimal possessions','average','average','average','modest possessions','covet possessions']
    honesty_list = ['scrupulous','honour-bound','truthful','average','average','average','average','deceitful','untrustworthy']
    bravery_list = ['average','average','average','foolhardy','brave','cautious','reject bravery as an ideal']
    work_ethic_list = ['very relaxed','relaxed','average','average','average','driven','beyond driven']
    social_conflict_list = ['average','average','average','conflict adverse','conflict phobic','enjoy conflict','thrive on conflict']
    consumerism_list = ['miserly','conservative spender','average','average','spendthrift','wasteful']
    spiritual_outlook_list = ['martyr-like','devout','reverent','moderate','moderate','questioning','irreverent']
    status_quo_outlook_list = ['radical','progressive','progressive','conservative','conservative','progressive','progressive','conservative',
                        'conservative','reactionary']
    custom_role_list = ['everyone','everyone','everyone','everyone','everyone','everyone','everyone','everyone','everyone','everyone',
                        'natives','citizens','visitors','certain political groups','certain sex','law enforcement','entertainers',
                        'heroes','athletes','certain races','relgious figures','military figures','certain occupations','political figures',
                        'medical professionals','certain age groups','scientists','academics','low social class','high social class',
                        'criminals','socialites','celebrities','workers','off-worlders/travellers']
    custom_list = ['same clothes for all sexes','unusual clothes','unusual headgear','shaved heads','hair never cut','unusual hair color',
                   'unusual hair styles','unusual eyebrows','unusual facial alterations','unusual body alterations','unusual fingernails',
                   'unusual toe nails','unusual cosmetics','unusual jewelry','unusual accessories','unusual handgear','tatooing on face',
                   'tatooing on body','hidden tatooing','unusual foods','unusual beverages','unusual food preparation','segregated at meals',
                   'vegetarian','vegan','certain colored food','certain shaped food','certain food sources','eat in special location',
                   'eat only in private','eat in special orientation','eat with unusual utensils','eat only at home','eat at unusual times',
                   'eat only at certain times','rituals before eating','rituals after eating','one group eats leftovers',
                   'cannabalistic','live privately','live in small groups','live in special locations','live at work',
                   'live under special conditions','confined to quarters','live under special care','have extravagant quarters',
                   'have minimal quarters','have unusual quarters','quarters must be visited','live with extended families',
                   'live in communal housing','live only in certain terrain','must move around','unsual media','unusual starport',
                   'unusual lifecycle','unusual social standings','unusual trade','unusual nobility','unusual reproduction','conspiracy-driven']
    interests_list = ['religion','philosophy','economics','sports','politics','legends','history','nature','horticulture','handicrafts',
                      'foods','wines and spirits','gambling','drugs']

    
    
    
    
    

    
    sql3_select_tb_t5 = """     SELECT  s.location,
                                        s.remarks,
                                        s.ix,
                                        s.ex,
                                        s.cx
                                FROM    system_stats s"""
                                    
    c.execute(sql3_select_tb_t5)
    allrows = c.fetchall()
    
   
    
    for row in allrows:


        location            = str(row[0])    
        remarks             = str(row[1])
        ix                  = str(row[2])
        ex                  = str(row[3])
        cx                  = str(row[4])
        
        (cx_het_no,cx_acc_no,cx_str_no,cx_sym_no) = cx_values(cx)
        
        if cx_het_no == 0 and cx_acc_no == 0 and cx_str_no == 0 and cx_sym_no == 0:
            age = 'n/a'
            appearance = 'n/a'
            tendency = 'n/a'
            materialism = 'n/a'
            honesty = 'n/a'
            bravery = 'n/a'
            work_ethic = 'n/a'
            social_conflict = 'n/a'
            consumerism = 'n/a'
            spiritual_outlook = 'n/a'
            status_quo_outlook = 'n/a'
            custom = 'n/a'
            interests = 'n/a'
            common_skills = 'n/a'

            
        else:
        
            age                 = random.choice(age_list)
            appearance          = random.choice(appearance_list)
            tendency            = random.choice(tendency_list)
            materialism         = random.choice(materialism_list)
            honesty             = random.choice(honesty_list)
            bravery             = random.choice(bravery_list)
            work_ethic          = random.choice(work_ethic_list)
            social_conflict     = random.choice(social_conflict_list)
            consumerism         = random.choice(consumerism_list)
            spiritual_outlook   = random.choice(spiritual_outlook_list)
            status_quo_outlook  = random.choice(status_quo_outlook_list)
            custom              = random.choice(custom_role_list) + ' ' + random.choice(custom_list)
            interests           = random.choice(interests_list)
            common_skills       = ''
            
            
            dc_common_skills = {
                'Va': 'Vacc Suit-0 ',
                'Ag': 'Animal-0 ',
                'As': 'Zero G-0 ',
                'De': 'Survival-0 ',
                'Fl': 'Hostile Env-0 ',
                'Ga': 'Trader-0 ',
                'He': 'Hostile Env-0 ',
                'Oc': 'Hi G-0 ',
                'Wa': 'Seafarer-0 ',
                'Lo': 'Flyer-0 ',
                'Ni': 'Driver-0 ',
                'Hi': 'Streetwise-0 ',
                'Pa': 'Trader-0 ',
                'Na': 'Survery-0 ',
                'Pi': 'JOT-0 ',
                'In': 'Elec or Mech-0 ',
                'Po': 'Steward-0 ',
                'Pr': 'Craft-0 ',
                'Ri': 'Art-0 '}
            
            common_skill_list = []
            for key in dc_common_skills:
                if key in remarks:
                    common_skill_list.append(dc_common_skills[key])
            common_skill_list = set(common_skill_list)
            for each in common_skill_list:
                common_skills += each
                
            


        sqlcommand = '''    INSERT INTO perceived_culture (   
                                                    location,
                                                    age,
                                                    appearance,
                                                    tendency,
                                                    materialism,
                                                    honesty,
                                                    bravery,
                                                    work_ethic,
                                                    social_conflict,
                                                    consumerism,
                                                    spiritual_outlook,
                                                    status_quo_outlook,
                                                    custom,
                                                    interests,
                                                    common_skills)                                        
                                                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
        
                
        body_row =     (location,
                        age,
                        appearance,
                        tendency,
                        materialism,
                        honesty,
                        bravery,
                        work_ethic,
                        social_conflict,
                        consumerism,
                        spiritual_outlook,
                        status_quo_outlook,
                        custom,
                        interests,
                        common_skills)
                    
          
        c.execute(sqlcommand, body_row) 
        
    
    
    
    
    
    
    conn.commit()
    conn.close()
    
    
    
    
    
    