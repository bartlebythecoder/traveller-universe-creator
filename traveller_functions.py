# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 16:35:43 2021

@author: sean
"""

import random

def integer_root(expo,num):
    num = float(num)
    root_expo = 1/expo
    return float(num ** root_expo)

def tohex(dec):
    if dec > 15: dec = 15
    x = (dec % 16)
    digits = "0123456789ABCDEF"
    #rest = dec / 16
    # if (rest == 0):
    return digits[int(x)]
    # return tohex(rest) + digits[int(x)]
    
def hex_to_int(hex_val):
    response = -1
    try:
        hex_list = ['A','B','C','D','E','F']
        hex_dict = {'F': 15,
                    'E': 14,
                    'D': 13,
                    'C': 12,
                    'B': 11,
                    'A': 10}  
        if hex_val in hex_list: response = int(hex_dict[hex_val])
        else: response = int(response)
        return response
    except:
        print('failed hex to int with',hex_val)
        
def cx_values(cx):
        het_no = hex_to_int(cx[0])
        acc_no = hex_to_int(cx[1])
        sta_no = hex_to_int(cx[2])
        sym_no = hex_to_int(cx[3])
        return (het_no,acc_no,sta_no,sym_no)
    
    
def roll_dice(no_dice, why, location, conn, c):
    
    
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

def get_description(upp_type,upp_value):
    description = ''
    if upp_type == 'starport':
        dy_upp = {'A': 'Excellent',
                  'B': 'Good',
                  'C': 'Routine',
                  'D': 'Poor',
                  'E': 'Frontier',
                  'F': 'Spaceport - Good',
                  'G': 'Spaceport - Poor',
                  'H': 'Spaceport - Basic',
                  'X': 'None',
                  'Y': 'None'}
    elif upp_type == 'remarks':
        dy_upp = {'Oc': 'Ocean World',
                  'Va': 'Vacuum',
                  'Wa': 'Water World',
                  'Ba': 'Barren',
                  'Di': 'Dieback',
                  'Lo': 'Low Population',
                  'Hi': 'Hi Population',
                  'Ni': 'Non-Industrial',
                  'Ph': 'Pre-High Population',
                  'Pa': 'Pre-Agricultural',
                  'Ag': 'Agricultural',
                  'Na': 'Non-Agrictultural',
                  'Px': 'Prison or Exile Camp',
                  'Pi': 'Pre-Industrial',
                  'In': 'Industrial',
                  'Po': 'Poor',
                  'Pr': 'Pre-Rich',
                  'Ri': 'Rich',
                  'As': 'Asteroid Belt',
                  'De': 'Desert',
                  'Fl': 'Fluid',
                  'Ga': 'Garden World',
                  'Ic': 'Ice-Capped',
                  'He': 'Hell World'}
    elif upp_type == 'atmosphere':
        dy_upp = {'0':  'Vacuum',
                  '1':  'Trace',
                  '2':  'Very thin, tainted',
                  '3':  'Thin',
                  '4':  'Thin, tainted',
                  '5':  'Thin',
                  '6':  'Standard',
                  '7':  'Standad, tainted',
                  '8':  'Dense',
                  '9':  'Dense, tainted',
                  'A':  'Exotic',
                  'B':  'Corrosive',
                  'C':  'Insidious',
                  'D':  'Dense High',
                  'E':  'Thin Low',
                  'F':  'Unusual'
                  }
    elif upp_type == 'size':
        dy_upp = {'0': 'Asteroid Belt',
                  '1': '1,000 miles 1,600 km',
                  '2': '2,000 miles 3,200 km',
                  '3': '3,000 miles 4,800 km',
                  '4': '4,000 miles 6,400 km',
                  '5': '5,000 miles 8,000 km',
                  '6': '6,000 miles 9,600 km',
                  '7': '7,000 miles 11,200 km',
                  '8': '8,000 miles 12,800 km',
                  '9': '9,000 miles 14,400 km',
                  'A': '10,000 miles 16,000 km',
                  'B': '11,000 miles 17,600 km',
                  'C': '12,000 miles 19,200 km',
                  'D': '13,000 miles 20,800 km',
                  'E': '14,000 miles 22,400 km',
                  'F': '15,000 miles 24,000 km'}
    elif upp_type == 'government':
        dy_upp = {'0': 'No Government Structure.',
                  '1': 'Company/ Corporation.',
                  '2': 'Participating Democracy',
                  '3': 'Self-Perpetuating Oligarchy',
                  '4': 'Representative Democracy',
                  '5': 'Feudal Technocracy',
                  '6': 'Captive Government / Colony',
                  '7': 'Balkanization',
                  '8': 'Civil Service Bureaucracy',
                  '9': 'Impersonal Bureaucracy',
                  'A': 'Charismatic Dictatorship' ,
                  'B': 'Non-Charismatic Dictatorship',
                  'C': 'Charismatic Oligarchy',
                  'D': 'Religious Dictatorship',
                  'E': 'Religious Autocracy',
                  'F': 'Totalitarian Oligarchy'}
    elif upp_type == 'law':
        dy_upp = {
            '0': 'No Law. No prohibitions.',
            '1': 'Low Law. Prohibition of WMD, Psi weapons.',
            '2': 'Low Law. Prohibition of “Portable” Weapons.',
            '3': 'Low Law. Prohibition of Acid, Fire, Gas.',
            '4': 'Moderate Law. Prohibition of Laser, Beam.',
            '5': 'Moderate Law. No Shock,EMP,Rad, Mag, Grav.',
            '6': 'Moderate Law. Prohibition of Machineguns.',
            '7': 'Moderate Law. Prohibition of Pistols.',
            '8': 'High Law. Open display of weapons prohibited.',
            '9': 'High Law. No weapons outside the home.',
            'A': 'Extreme Law. All weapons prohibited.',
            'B': 'Extreme Law. Continental passports required.',
            'C': 'Extreme Law. Unrestricted invasion of privacy.',
            'D': 'Extreme Law. Paramilitary law enforcement.',
            'E': 'Extreme Law. Full-fledged police state.',
            'F': 'Extreme Law. Daily life rigidly controlled.',
            'G': 'Extreme Law. Disproportionate punishment.',
            'H': 'Extreme Law. Legalized oppressive practices.',
            'J': 'Extreme Law. Routine oppression.'
            }
    
    if upp_type == 'remarks':
        for x, y in dy_upp.items():
            if upp_value.find(x) >= 0:
                description += y + '. '          
    else:
        description = dy_upp[upp_value]     
    return description