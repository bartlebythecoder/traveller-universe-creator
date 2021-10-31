# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 12:41:35 2021

@author: sean
"""
import PySimpleGUI as sg
from traveller_master import make_sector_master


def makeit(makeit_list):
    

    print(makeit_list)
    make_sector_master(makeit_list)
    
    


sg.theme('DarkBlue')   # Add a touch of color
# All the stuff inside your window.

left_layout = [
    [sg.Text("PARAMETERS")],
    [sg.Text('System Density')],
    [sg.Text('File Name')],
    [sg.Text('Random Seed')]
]

middle_layout =  [

    [sg.Text("OPTIONS")],
    [sg.InputText(size=(4,1))],
    [sg.InputText(size=(10,1))],
    [sg.InputText(size=(4,1))],
]

right_layout = [
    [sg.Text("NOTES")],
    [sg.Text("1d6 >= # results in a system present")],
    [sg.Text("Db and txt files will be created in /Sector")],
    [sg.Text("Using the same seed with the same density will produce the same sector")]
    
]



layout = [   
    [sg.Text("""Generate Window""")],
    [sg.HSeparator()],
    [
     
     sg.Column(left_layout),
     sg.VSeparator(),
     sg.Column(middle_layout),
     sg.VSeparator(),
     sg.Column(right_layout)
    ],
    [sg.Button('Generate'), sg.Button('Cancel')]
    
]

# Create the Window
window = sg.Window("""Bartleby's Sector Builder""", layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    try:
        print('You entered ', values[2], values[3], values[4])
        density_input = values[2]
        sector_name_input = values[3]
        random_seed_input = values[4]
        lumiii_input = 3
        lumv_input = 14
        spectrala_input = 4
        spectralf_input = 6
        spectralg_input = 8
        spectralk_input = 10
        solo_input = 13
        binary_input = 17
        distant_input = 11
        makeit_list = [ random_seed_input, 
                    sector_name_input,
                    density_input,
                    lumiii_input,
                    lumv_input,
                    spectrala_input,
                    spectralf_input,
                    spectralg_input,
                    spectralk_input,
                    solo_input,
                    binary_input,
                    distant_input]
        makeit(makeit_list)
        break
    
    except:
        print(values)
        break

    

window.close()