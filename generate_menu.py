# -*- coding: utf-8 -*-
"""

@author: sean
"""
import PySimpleGUI as sg
from traveller_master import make_sector_master


class Creation_Choices:
    def __init__(self, random_seed, sector_name, sector_density, settlement_mod):
        self.random_seed = random_seed
        self.sector_name = sector_name
        self.sector_density = sector_density
        self.settlement_mod = settlement_mod

  
    


sg.theme('DarkBlue')  

left_layout = [
    [sg.Text("PARAMETERS")],
    [sg.Text('System Density',tooltip = 'Chance for system in each parsec')],
    [sg.Text('Settlement Style',tooltip = 'Optionally modify stats based on location')],
    [sg.Text('Sector Name',tooltip = 'Files will be created in /sector_db')],
    [sg.Text('Random Seed',tooltip = 'Using the same seed with the same density will produce the same sector')]
]

middle_layout =  [

    [sg.Text("OPTIONS")],
    [sg.Radio('Sparse', "RADIO1", key = '-SPARSE-', tooltip='1 in 6 chance per parsec', default=True),
     sg.Radio('Scattered',"RADIO1", key = '-SCATTERED-',tooltip='2 in 6 chance per parsec'),
     sg.Radio('Standard', "RADIO1", key = '-STANDARD-', tooltip='3 in 6 chance per parsec')],
    [sg.Radio('Normal', "RADIO2", key = '-NORMAL-', tooltip='Normal Traveller Rules', default=True),
     sg.Radio('Diminishing',"RADIO2", key = '-DIMINISHING-',tooltip='Population increased in center, lowered in rim')],

    [sg.InputText(size=(10,1), key=('-NAME-'))],
    [sg.InputText(size=(4,1),key=('-SEED-'))]
]



layout = [   
    [sg.Text("""Generate Window""")],
    [sg.HSeparator()],
    [sg.Column(left_layout),
     sg.VSeparator(),
     sg.Column(middle_layout)

    ],
    [sg.Button('Generate'), sg.Button('Cancel')]
    
]

# Create the Window
window = sg.Window("""Bartleby's Sector Builder v0.9.1""", layout)
# Event Loop to process "events" and get the "values" of the inputs


while True:
    
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        print('Close')
        break
        
    else:
        print('You entered ', values['-SPARSE-'],
                              values['-SCATTERED-'], 
                              values['-STANDARD-'], 
                              values['-NAME-'], 
                              values['-SEED-'],
                              values['-NORMAL-'],
                              values['-DIMINISHING-'])
        
        if values['-SPARSE-'] == True:
            density_input = 6
        elif values['-SCATTERED-'] == True:
            density_input = 5
        else:
            density_input = 4
            
        if values['-NORMAL-'] is True:
            settlement_mod = 0    
        else:
            settlement_mod = 1
            

        sector_name_input = values['-NAME-']
        random_seed_input = values['-SEED-']
        

        
        decisions_provided = Creation_Choices(
            random_seed_input, 
            sector_name_input,
            density_input,
            settlement_mod)
        
        
        make_sector_master(decisions_provided)

        break



window.close()