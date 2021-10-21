def make_sector_master(makeit_list):

    # Master program for Traveller universe build
    
    import random
    from first_in_generation import generate_stars
    from mainworld_calculator import generate_mainworld_scores
    from mainworld_selector import choose_mainworld
    from travellerization import add_traveller_stats
    from traveller_map import build_travellermap_file
    from non_mw import generate_non_mainworlds
    from far_trader import generate_far_trader_stats
    from journey_data import build_journey_table
    
    seed_number = makeit_list[0]
    db_name = makeit_list[1]
    
    generate_stars(makeit_list)
    generate_mainworld_scores(db_name)
    choose_mainworld(db_name)
    add_traveller_stats(seed_number,db_name)
    build_travellermap_file(db_name)
    generate_non_mainworlds(seed_number,db_name)
    generate_far_trader_stats(seed_number,db_name)
    print('Calling the journey table')
    build_journey_table(seed_number,db_name)

