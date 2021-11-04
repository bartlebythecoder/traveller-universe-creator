def make_sector_master(makeit_list):

    # Master program for Traveller universe build
    
    # The goal is to generate a sector of Traveller star systems


# Possible Improvements Pending:

#   - GUI Browser
#   - Rewrite Stellar creation rules using  Architect of Worlds
#   - Create worlds using Architect of Worlds
#   - Expand moon data 
#   - Jump and Trade routs




#   - To Do list complete:

#   - COMPLETE 2021 10 28: Moons created using Architect of Worlds
#   - COMPLETE 2021 10 27: Density added for GG
#   - COMPLETE 2021 10 26: Orbital Bodies around all stellar objects
#   - COMPLETE 2021 10 26: Incorporate Forbidden Zones for planet orbits
#   - COMPLETE 2021 10 25: Very Close Binaries combine stellar info for orbit creation
#   - COMPLETE 2021 10 25: Distant stellar bodies added
#   - COMPLETE: Add Stellar Age
#   - COMPLETE: Appropriate Planet Size modifiers
#   - COMPLETE: Stellar data loaded in a database. 
#   - COMPLETE: White Dwarf details and orbital bodies
#   - COMPLETE: Rolls are added to a table with relevant data
#   - FIXED: Minimum 25 size for GG    

    
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
    import PySimpleGUI as sg
    
    seed_number = makeit_list[0]
    
    print('v0.61 Stellar Companion Update')
    db_name = 'sector_db/' + makeit_list[1] + '.db'
    print('Generating Stars and Planets')
    generate_stars(db_name,makeit_list)
    print('Evaluating each orbital body for main world suitability')
    generate_mainworld_scores(db_name)
    print('Finalizing main world selections and building mainworld table')
    choose_mainworld(db_name)
    print('Travellerizing the main worlds')
    add_traveller_stats(seed_number,db_name)
    print('Building Traveller Map extract')
    build_travellermap_file(db_name)
    print('Building exo-world table for non-main worlds') 
    generate_non_mainworlds(seed_number,db_name)
    print('Building Far Trader table')
    generate_far_trader_stats(seed_number,db_name)
    print('Building the Journey stats table')
    build_journey_table(seed_number,db_name)
    print('Process Complete')

    sg.popup('Sector completed successfully')    

