#!/usr/bin/python

# Master program for Traveller universe build

import random
from first_in_generation import generate_stars
from mainworld_calculator import generate_mainworld_scores
from mainworld_selector import choose_mainworld
from travellerization import add_traveller_stats
from traveller_map import build_travellermap_file
from non_mw import generate_non_mainworlds
from far_trader import generate_far_trader_stats

seed_number = input ('What random seed should I use?  ')

generate_stars(seed_number)
generate_mainworld_scores()
choose_mainworld()
add_traveller_stats(seed_number)
build_travellermap_file()
generate_non_mainworlds(seed_number)
generate_far_trader_stats(seed_number)


