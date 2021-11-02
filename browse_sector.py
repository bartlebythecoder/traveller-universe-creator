# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 23:19:42 2021

@author: sean
"""

import PySimpleGUI as sg
import sqlite3
import pandas as pd
import numpy as np


 
list_test = ['hello','how','are','you']
sector_name = 'Nothing Yet'

sg.theme('DarkBlue')  

option_list = []


planet_text = 'Waiting for system to be selected'


# Load up columns from example database
db_name = 'sector_db/example.db'
conn = sqlite3.connect(db_name)
c = conn.cursor()
sql_query = '''SELECT * FROM main_worlds'''
df = pd.read_sql_query(sql_query,conn)
l_labels = []
l_labels = list(df.columns)
l_labels_len = len(l_labels)
conn.commit()  
c.close()
conn.close()  


system_layout = []
system_info_layout = []

for l in l_labels:
    system_layout += [sg.Text(l+':',enable_events = True,key=(l))],
    system_info_layout += [sg.Text('l',enable_events = True,key=(l+'i'))],
                     
                    

    
 
print(l_labels)
    

left_layout = [
    [sg.Text("SYSTEMS")],
    [sg.Listbox(option_list,enable_events=True,size=(20,30),key=('-LOCATIONS-'))]
]





layout = [   
    [sg.Text("""Browse Window""")],
    [sg.HSeparator()],
    [
          sg.Text('Choose A Sector', size=(15, 1), auto_size_text=False, justification='right'),
          sg.In(size=(20,1),enable_events=True,key=('-DB-'),justification='right'),
          sg.FileBrowse(file_types=(("Database Files","*.db"),),
                                               enable_events=True,
                                               initial_folder=("sector_db")),
    ],
    [
     
     sg.Column(left_layout),
     sg.VSeparator(),
     sg.Column(system_layout),
     sg.Column(system_info_layout),
    ],
    [sg.Button('Exit')],

    
]

# Create the Window
window = sg.Window("""Bartleby's Sector Builder""", layout,size=(1200,800))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
        break
    
    if event == '-DB-':


        try:
            db_name = values['-DB-']
            conn = sqlite3.connect(db_name)
            c = conn.cursor()
            df = pd.read_sql_query(sql_query,conn)
            df['loc_name'] = df['location'] + '-' + df['system_name']
            option_list = list(df['loc_name'])
            window['-LOCATIONS-'].update(option_list)
        except:
            print('sql fail')
            
    

        conn.commit()  
        c.close()
        conn.close()  
        
        
    elif event == '-LOCATIONS-':
        try:
            location_orb_name = values['-LOCATIONS-'][0]
            location = values['-LOCATIONS-'][0][0:4]
            loc_info = df.loc[df['location'] == location]
            for l in l_labels:
                l_value = list(loc_info[l])
                i_value = l_value[0]
                window[l+'i'].update(i_value)


        except:
            print('Did not catch location')


  
    



window.close()