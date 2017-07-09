#!/usr/bin/python

# Master program for Traveller universe build
# Should run first_in_generationn, mainworld_calulator, mainworld_selector, travellerization
import random

def get_seed():
    seed_input = input ('What random seed should I use?  ')
    return seed_input
    
def set_seed(seed_number):
    random.seed(seed_number)
    print ('Setting seed: ', seed_number)
    stall = input ('Hit Enter')
    
seed_number = get_seed()
set_seed(seed_number)

import first_in_generation
import mainworld_calculator
import mainworld_selector
import travellerization
import traveller_map
import non_mw
import far_trader


