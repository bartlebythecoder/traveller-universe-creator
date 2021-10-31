def make_sector_master(makeit_list):

    # Master program for Traveller universe build
    
    import random
    import sqlite3
    from first_in_generation import generate_stars
    from mainworld_calculator import generate_mainworld_scores
    from mainworld_selector import choose_mainworld
    from travellerization import add_traveller_stats
    from traveller_map import build_travellermap_file
    from non_mw import generate_non_mainworlds
    from far_trader import generate_far_trader_stats
    from journey_data import build_journey_table
    
    seed_number = makeit_list[0]
    
    print('v0.3 Stellar Companion Update')
    db_name = 'sector_db/' + makeit_list[1] + '.db'
    print('Generating Stars and Planets')
    generate_stars(db_name,makeit_list)
    print('Choosing a Mainworld for each System')
    generate_mainworld_scores(db_name)
    choose_mainworld(db_name)
    print('Travellerizing the Mainworlds')
    add_traveller_stats(seed_number,db_name)
    print('Building Traveller Map extract')
    build_travellermap_file(db_name)
    print('Building exo-world table for non-Mainworlds table') 
    generate_non_mainworlds(seed_number,db_name)
    print('Building Far Trader table')
    generate_far_trader_stats(seed_number,db_name)
    print('Building the Journey stats table')
    build_journey_table(seed_number,db_name)
    print('Process Complete')



