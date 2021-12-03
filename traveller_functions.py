# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 16:35:43 2021

@author: sean
"""
def integer_root(expo,num):
    num = float(num)
    root_expo = 1/expo
    return float(num ** root_expo)

def tohex(dec):
    if dec > 15: dec = 15
    x = (dec % 16)
    digits = "0123456789ABCDEF"
    rest = dec / 16
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