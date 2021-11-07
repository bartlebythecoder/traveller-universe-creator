# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 23:19:42 2021

@author: sean
"""

import PySimpleGUI as sg
import sqlite3
import pandas as pd
import numpy as np
from PIL import Image, ImageTk
import os
import io

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter  # useful for `logit` scale
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import PySimpleGUI as sg
from matplotlib import style

matplotlib.use('TkAgg')


sg.theme('DarkBlue')  

# ------------------------------------------------------------------------------
# use PIL to read data of one image
# ------------------------------------------------------------------------------


def get_img_data(f, maxsize=(1200, 850), first=False):
    """Generate image data using PIL
    """
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:                     # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)
# ------------------------------------------------------------------------------


def clear_images():
    for li in list_images:
        window[li[0]].hide_row()

def add_image(image_var):
        window[image_var].unhide_row()
        
        
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close('all')





# ------------------------------- MATPLOTLIB CODE HERE -------------------------------

# fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
# t = np.arange(0, 3, .01)
# fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
######################################################################################
f= Figure(figsize=(4,5),dpi=100)

style.use("dark_background")
a = f.add_subplot(111)

a.clear()
a.set_xticks([])
a.set_yticks([])
xcoordinates = []
ycoordinates = []



def get_coordinates(thedataframe):
    xcoordinates = []
    ycoordinates = []
    

    coord_list = list(thedataframe['location'])


    for coord in coord_list:

        x_axis = int(coord[0:2])
    
        mod = x_axis % 2
        if mod > 0:
            top_y_limit = 41
        else: top_y_limit = 40.5
        y_axis = (top_y_limit-int(coord[2:4]))
        xcoordinates.append(x_axis)
        ycoordinates.append(y_axis)

    return(xcoordinates,ycoordinates)
        



def animate(chart_title,color_choice,plot_size,*args):
   
    a.clear()
    a.set_xticks([])
    a.set_yticks([])
    xcoordinates = []
    ycoordinates = []
    
    for arg_num, arg in enumerate(args):
        
        color_choice_s = color_choice[arg_num]

        xcoordinates,ycoordinates = get_coordinates(arg)
        a.set_title(chart_title, color='white')
        a.scatter(xcoordinates,ycoordinates,c=color_choice_s,s=plot_size)
        
        
        name_list = arg['location'].tolist()
        label_color = 'White'
        if len(name_list) <= 50:
            name_coords = list(zip(xcoordinates,ycoordinates))
            row_num = 0
            for each_item in name_coords:
                row_name = name_list[row_num]
                a.text(each_item[0]-2,each_item[1],row_name,fontsize = 10,color = label_color)
                row_num += 1

    f.tight_layout()    
    f.canvas.draw_idle()
    

   
    

# ------------------------------- END OF MATPLOTLIB CODE -------------------------------




folder = 'images/'

# PIL supported image types
img_types = (".png", ".jpg", "jpeg", ".tiff", ".bmp")

# get list of files in folder
flist0 = os.listdir(folder)

# create sub list of image files (no sub folders, no wrong file types)
fnames = [f for f in flist0 if os.path.isfile(

os.path.join(folder, f)) and f.lower().endswith(img_types)]
filename = os.path.join(folder, '22a.png') 




option_list = []



# Load up columns from example database
db_name = 'sector_db/example-66.db'
conn = sqlite3.connect(db_name)
c = conn.cursor()


main_sql_query = '''SELECT * FROM main_worlds'''
df_main = pd.read_sql_query(main_sql_query,conn)
m_labels = []
m_labels = list(df_main.columns)
m_labels_len = len(m_labels)

detail_sql_query = '''SELECT m.system_name, m.location, o.body, o.wtype as type, o.day, o.year,
o.gravity, o.atmos_pressure, o.atmos_composition, o.temperature, o.climate, 
o.impact_moons as moons, 
j.stellar_distance as stellar_distance, 
j.jump_point_Mm as jump_point_distance, 
j.planet_stellar_masked as stellar_mask,
j.hrs_1g,j.hrs_2g,j.hrs_3g,j.hrs_4g,j.hrs_5g,j.hrs_6g
FROM main_worlds m
LEFT JOIN orbital_bodies o
ON m.location_orb = o.location_orbit
LEFT JOIN journey_data j
ON j.location_orbit = m.location_orb
'''
df_details = pd.read_sql_query(detail_sql_query,conn)
d_labels = []
d_labels = list(df_details.columns)
d_labels.remove('location')
d_labels_len = len(d_labels)

economic_sql_query = '''SELECT * FROM far_trader'''
df_economic = pd.read_sql_query(economic_sql_query,conn)
e_labels = []
e_labels = list(df_economic.columns)
e_labels.remove('location')
e_labels.remove('id')
e_labels_len = len(e_labels)



conn.commit()  
c.close()
conn.close()  



column_one = [
    [sg.Text("SYSTEMS")],
    [sg.Listbox(option_list,enable_events=True,size=(20,30),key=('-LOCATIONS-'))]
]



column_two = [[sg.Text("UWP Categories")], 
                [sg.HSeparator()],]
column_three = [[sg.Text("Main World Details")], 
                      [sg.HSeparator()],]
for m in m_labels:
    column_two += [sg.Text(m+':',enable_events = True,key=(m),pad=(0,0))],
    column_three += [sg.Text('|',enable_events = True,key=(m+'i'),pad=(0,0))],
                     
column_four = [[sg.Text("Scientific Categories")], 
                [sg.HSeparator()],]
column_five = [[sg.Text("Main World Details")], 
                      [sg.HSeparator()],]        
for d in d_labels:
    column_four += [sg.Text(d+':',enable_events = True,key=(d),pad=(0,0))],
    column_five += [sg.Text('|',enable_events = True,key=(d+'i'),pad=(0,0))],
    
    
column_four += [[sg.Text("Economic Categories",pad=(5,(15,2)))], 
                [sg.HSeparator()],]
column_five += [[sg.Text("Main World Details",pad=(5,(15,2)))], 
                      [sg.HSeparator()],]        

column_six = [[sg.Canvas(key='-CANVAS-')],
              [sg.Button('Sector',key=('-SECTOR-')),sg.Button('Earth-like',key=('-EARTH-')),
               sg.Button('Subsector'),sg.Button('System')]
              ]
              


for e in e_labels:
    column_four += [sg.Text(e+':',enable_events = True,key=(e),pad=(0,0))],
    column_five += [sg.Text('|',enable_events = True,key=(e+'i'),pad=(0,0))],
    
 
list_images = [['mask','Completely Stellar Masked'],
               ['ocean','Earth-like World'],
               ['exotic','Exotic Atmosphire'],
               ['corrosive','Corrosive Atmosphire'],
               ['vacuum','Vacuum World'],
               ['asteroid','Planetary Belt'],
               ['garden','Garden World'],
               ['light','Low Gravity World'],
               ['heavy','High Gravity World'],
               ['hot','Unhinhabitable Heat'],
               ['cold','Uninhabitable Cold'],
               ['hipop','High Population World'],
               ['wealthy','Wealthy (high GWP)'],
               ['industrial','Industrial Economy'],
               ['agricultural','Agricultural Economy'],
               ['important','Important World'],
               ['naval','Naval Base Present'],
               ['scout','Scout Base Present'],
               ['prison','Interplanetary Prison'],
               ['moon','Main world is a moon']
 
               ]


remarks_list = [['In', 'industrial'],
                ['Ag', 'agricultural'],
                ['Va', 'vacuum'],
                ['As', 'asteroid'],
                ['Ga', 'garden'],
                ['Hi', 'hipop'],
                ['Px', 'prison']]
                



                         

image_layout = []
for li in list_images:
    filename = os.path.join(folder,li[0]+'.png') 
    image_layout += [sg.Image(data=get_img_data(filename, first=True),
                    tooltip=li[1], enable_events = True,key=(li[0]))],
    





layout = [   
    [sg.Text("""Browse Window""")],
    [sg.HSeparator()],
    [
          sg.Text('Choose A Sector', size=(15, 1), auto_size_text=False, justification='right'),
          sg.In(size=(20,1),enable_events=True,key=('-DB-'),justification='right'),
          sg.FileBrowse(file_types=(("Database Files","*.db"),),
                                               enable_events=True,
                                               initial_folder=("sector_db")),
          sg.VSeparator(),
          sg.Button('Stellar',key=('-STELLAR-')),
          sg.Button('Full System', key=('-SYSTEM-')),
          sg.VSeparator(),
          sg.VSeparator(),
          sg.Button('Exit'),
    ],
    [sg.HSeparator(), 
     ],
    
    [
     
     sg.Column(column_one),
     sg.VSeparator(),
     sg.Column(column_two),
     sg.Column(column_three),
     sg.Column(image_layout),
     sg.VSeparator(), 
     sg.Column(column_four),
     sg.Column(column_five),     
     sg.VSeparator(), 
     sg.Column(column_six),   
     ],
    
]

# Create the Window
window = sg.Window("""Bartleby's Sector Builder""", layout,size=(1200,700))
# Event Loop to process "events" and get the "values" of the inputs


fig_canvas_agg = None

while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
        break
    
    if event == '-DB-':


        try:
            db_name = values['-DB-']
            conn = sqlite3.connect(db_name)
            c = conn.cursor()
            df = pd.read_sql_query(main_sql_query,conn)
            

            
            df_details = pd.read_sql_query(detail_sql_query,conn)
            print('made it out of df')

            df_details['atmos_pressure'] = round(df_details['atmos_pressure'],2)
            df_details['jump_point_distance'] = round(df_details['jump_point_distance'],1)# otherwise crazy decimals added
            


            
            df_economic = pd.read_sql_query(economic_sql_query,conn)
            df_economic['exchange'] = round(df_economic['exchange'],2)  # otherwise crazy decimals added

            
            df['loc_name'] = df['location'] + '-' + df['system_name']
            df_details['loc_name'] = df_details['location'] + '-' + df_details['system_name']
            option_list = list(df['loc_name'])
            window['-LOCATIONS-'].update(option_list)
            
            if fig_canvas_agg:
            # ** IMPORTANT ** Clean up previous drawing before drawing again
                delete_figure_agg(fig_canvas_agg)
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
            detail_info = df_details[df_details['location'] == location]
            economic_info = df_economic[df_economic['location'] == location]

            

            for m in m_labels:
                m_value = list(loc_info[m])
                m_value = m_value[0]
                window[m+'i'].update(m_value)


            for d in d_labels:
                d_value = list(detail_info[d])
                d_value = d_value[0]
                window[d+'i'].update(d_value)
                
            for e in e_labels:
                e_value = list(economic_info[e])
                e_value = e_value[0]
                window[e+'i'].update(e_value)
                


              
            clear_images()
            

            if list(detail_info['gravity'])[0] > 1.50:
                add_image('heavy')
            elif list(detail_info['gravity'])[0] < 0.50:
                add_image('light')    
                
            if list(detail_info['type'])[0] == "Ocean*":
                add_image('ocean')
            if list(detail_info['atmos_composition'])[0][0] == "E":
                add_image('exotic')
            elif list(detail_info['atmos_composition'])[0][0] == "C":
                add_image('corrosive')
            if list(detail_info['temperature'])[0] > 324:
                add_image('hot')
            if list(detail_info['temperature'])[0] < 239:
                add_image('cold')
            if list(detail_info['body'])[0] == 'Impact Moon' or \
            list(detail_info['body'])[0] == 'Natural Moon':
                add_image('moon')
            
            importance = list(loc_info['ix'])[0]
            for i in ['{','}']: importance = importance.strip(i)
            importance = int(importance)
            if importance >= 4: add_image('important')
                
            bases = list(loc_info['bases'])[0]
            if 'N' in bases or 'B' in bases:
                add_image('naval')
            if 'S' in bases or 'B' in bases:
                add_image('scout')
            for rem in remarks_list:
                if rem[0] in list(loc_info['remarks'])[0]: add_image(rem[1])
                
            gwp = list(economic_info['gwp'])[0]
            gwp_string = "{:,}".format(gwp)

            if int(gwp) >= 1000000: add_image('wealthy')
            
            if list(detail_info['stellar_mask'])[0] == 'total': add_image('mask')
                
            if fig_canvas_agg:
                # ** IMPORTANT ** Clean up previous drawing before drawing again
                delete_figure_agg(fig_canvas_agg)




            # add the plot to the window
            
            if fig_canvas_agg:
            # ** IMPORTANT ** Clean up previous drawing before drawing again
                delete_figure_agg(fig_canvas_agg)            

            stell_colors =['dimgray','Blue']
            plot_list  = [30]

            
            animate(location_orb_name,stell_colors,plot_list,df,loc_info)    





            fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, f)
                

        except:
            print('Did not catch location')
        
    elif event == '-STELLAR-':
        try:
            print('pressed STELLAR')
            sg.popup('Coming Soon!')    
        except:
            print('Failed Stellar button')
            
    elif event == '-SYSTEM-':
        try:
            print('pressed SYSTEM')
            sg.popup('Coming Soon!')    
        except:
            print('Failed System button')



    elif event == '-EARTH-':
        try:
            
            if fig_canvas_agg:
            # ** IMPORTANT ** Clean up previous drawing before drawing again
                delete_figure_agg(fig_canvas_agg)    
            
            
            
            print('pressed Earth-like')
            df_special_earth = (df_details.query('type == "Ocean*"'))

            stell_colors =['dimgray','Green']
            plot_list  = [30,65]
            
            print('Calling Earth Animate')
            animate('Earth-like worlds',stell_colors,plot_list,df,df_special_earth)
        
        
            # add the plot to the window
            
        


        
            fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, f)
        
        
        
        
        except:
            print('Failed Earth button')

    elif event == '-SECTOR-':
        try:  

            # add the plot to the window
            
            if fig_canvas_agg:
            # ** IMPORTANT ** Clean up previous drawing before drawing again
                delete_figure_agg(fig_canvas_agg)            

            stell_colors =['dimgray','Blue']
            plot_list  = [30]

            
            animate(location_orb_name,stell_colors,plot_list,df,loc_info)    

            fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, f) 
            
        except:
            print('Failed Sector button')



window.close()