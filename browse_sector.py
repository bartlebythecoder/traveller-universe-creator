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
        
        
def select_images(loc_info,system_info,detail_info,economic_info):
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
    if list(detail_info['body'])[0] == 'Gas Giant':
        add_image('gas giant')
    if list(loc_info['atmosphere'])[0] == 0:
        add_image('vacuum')
    if list(loc_info['size'])[0] == 0:
        add_image('asteroid')        
    
    importance = list(system_info['ix'])[0]
    for i in ['{','}']: importance = importance.strip(i)
    importance = int(importance)
    if importance >= 4: add_image('important')
        
    bases = list(system_info['bases'])[0]
    if 'N' in bases or 'B' in bases:
        add_image('naval')
    if 'S' in bases or 'B' in bases:
        add_image('scout')
    for rem in remarks_list:
        if rem[0] in list(system_info['remarks'])[0]: add_image(rem[1])
        
    gwp = list(economic_info['gwp'])[0]
    gwp_string = "{:,}".format(gwp)

    if int(gwp) >= 1000000: add_image('wealthy')
    
    if list(detail_info['stellar_mask'])[0] == 'total': add_image('mask')
    
    
    
def update_stats(loc_info,system_info,detail_info,economic_info,m_labels,s_labels,d_labels,e_labels):
    
                for m in m_labels:
                    m_value = list(loc_info[m])
                    m_value = m_value[0]
                    window[m+'i'].update(m_value)
                    
                for s in s_labels:
                    s_value = list(system_info[s])
                    s_value = s_value[0]
                    window[s+'i'].update(s_value)
    
    
                for d in d_labels:
                    d_value = list(detail_info[d])
                    d_value = d_value[0]
                    window[d+'i'].update(d_value)
                    
                for e in e_labels:
                    e_value = list(economic_info[e])
                    e_value = e_value[0]
                    window[e+'i'].update(e_value)
        
        
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
location = '-99'
detail_flag = 'main_world'  # flag used to mark whether the details should be main world or exo worlds.



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
        



def animate(chart_title,color_choice,plot_size,label_choice,*args):
   
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
        
        if label_choice == "num":
            name_list = arg['location'].tolist()
        else:
            name_list = arg['system_name'].tolist()
        label_color = 'White'
        if len(name_list) <= 100:
            name_coords = list(zip(xcoordinates,ycoordinates))
            row_num = 0
            for each_item in name_coords:
                row_name = name_list[row_num]
                a.text(each_item[0]-2,each_item[1],row_name,fontsize = 10,color = label_color)
                row_num += 1

    f.tight_layout()    
    f.canvas.draw_idle()
    

   
def draw_map():
    print('Map is selected')
    if values['-NUM-'] is True:
        print('Numbers were chosen')
        label_choice = 'num'
    else:
        print('Names were chosen')
        label_choice = 'name'
        
        
        
    if values['-FULL-'] is True:
        print('Full Sector was chosen')
        stell_colors =['dimgray','Blue']
        plot_list  = [30]
        animate(location_orb_name,stell_colors,plot_list,label_choice,df,loc_info)   
        
    else:
        print('Earth Like Planets was chosen')
        df_special_earth = (df_details.query('type == "Ocean*"'))
        stell_colors =['dimgray','Green']
        plot_list  = [30,65]
        animate('Earth-like worlds',stell_colors,plot_list,label_choice,df,df_special_earth)








folder = 'images/'

# PIL supported image types
img_types = (".png", ".jpg", "jpeg", ".tiff", ".bmp")

# get list of files in folder
flist0 = os.listdir(folder)

# create sub list of image files (no sub folders, no wrong file types)
fnames = [f for f in flist0 if os.path.isfile(

os.path.join(folder, f)) and f.lower().endswith(img_types)]


option_list = []



db_name = 'C:/Users/sean/Documents/GitHub/traveller-universe-creator/sector_db/example-66.db'

list_images = [['mask','Completely Stellar Masked'],
               ['ocean','Ocean or Earth-like World'],
               ['exotic','Exotic Atmosphire'],
               ['corrosive','Corrosive Atmosphire'],
               ['vacuum','Vacuum World'],
               ['asteroid','Object is Planetary Belt'],
               ['light','Low Gravity World'],
               ['heavy','High Gravity World'],
               ['hot','Unhinhabitable Heat'],
               ['cold','Uninhabitable Cold'],
               ['hipop','High Population World'],
               ['wealthy','Wealthy System'],
               ['industrial','Industrial Economy'],
               ['agricultural','Agricultural Economy'],
               ['important','Important System'],
               ['naval','Naval Base Present'],
               ['scout','Scout Base Present'],
               ['prison','Interplanetary Prison Present'],
               ['moon','Object is a moon'],
               ['gas giant','Object is a gas giant']
 
               ]


remarks_list = [['In', 'industrial'],
                ['Ag', 'agricultural'],
                ['Hi', 'hipop'],
                ['Px', 'prison']]
                

conn = sqlite3.connect(db_name)
c = conn.cursor()


new_main_query = '''SELECT *
FROM traveller_stats    
WHERE main_world = 1'''


df_new_main = pd.read_sql_query(new_main_query,conn)

m_labels = []
m_labels = list(df_new_main.columns)
m_labels_len = len(m_labels)


system_main_query = '''SELECT location,
remarks,
ix,
ex,
cx,
n,
bases,
zone,
pbg,
w,
allegiance,
stars
FROM system_stats
'''


df_system_main = pd.read_sql_query(system_main_query,conn)
s_labels = []
s_labels = list(df_system_main.columns)
s_labels.remove('location')
s_labels_len = len(s_labels)




new_detail_sql_query = '''SELECT t.system_name, t.location, o.body, o.wtype as type, o.day, o.year,
o.gravity, o.atmos_pressure, o.atmos_composition, o.temperature, o.climate, 
o.impact_moons, o.natural_moons,
j.stellar_distance as stellar_distance, 
j.jump_point_Mm as jump_point_distance, 
j.planet_stellar_masked as stellar_mask,
j.hrs_1g,j.hrs_2g,j.hrs_3g,j.hrs_4g,j.hrs_5g,j.hrs_6g,
e.mainworld_calc
FROM traveller_stats t
LEFT JOIN orbital_bodies o
ON t.location_orb = o.location_orbit
LEFT JOIN journey_data j
ON j.location_orbit = t.location_orb
LEFT JOIN main_world_eval e
ON t.location_orb = e.location_orbit
WHERE t.main_world = 1
'''

df_details = pd.read_sql_query(new_detail_sql_query,conn)
d_labels = []
d_labels = list(df_details.columns)
d_labels.remove('location')
d_labels.remove('system_name')
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

###################Layouts

def make_win1():

    column_one = [
        [sg.Text("SYSTEMS")],
        [sg.Listbox(option_list,enable_events=True,size=(25,32),key=('-LOCATIONS-'))]
    ]
    
    
    
    column_two = [[sg.Text("UWP Categories")], 
                    [sg.HSeparator()],]
    column_three = [[sg.Text("World Details")], 
                          [sg.HSeparator()],]
    for m in m_labels:
        column_two += [sg.Text(m+':',enable_events = True,key=(m),pad=(0,0))],
        column_three += [sg.Text('|',enable_events = True,key=(m+'i'),pad=(0,0))],
        
    
    column_two += [[sg.Text("System Categories",pad=(5,(15,2)))], 
                    [sg.HSeparator()],]
    column_three += [[sg.Text("System-wide Details",pad=(5,(15,2)))], 
                          [sg.HSeparator()],]
    
    for s in s_labels:
        column_two += [sg.Text(s+':',enable_events = True,key=(s),pad=(0,0))],
        column_three += [sg.Text('|',enable_events = True,key=(s+'i'),pad=(0,0))],
                         
    column_four = [[sg.Text("Scientific Categories")], 
                    [sg.HSeparator()],]
    column_five = [[sg.Text("World Details")], 
                          [sg.HSeparator()],]        
    for d in d_labels:
        column_four += [sg.Text(d+':',enable_events = True,key=(d),pad=(0,0))],
        column_five += [sg.Text('|',enable_events = True,key=(d+'i'),pad=(0,0))],
        
        
    column_four += [[sg.Text("Economic Categories",pad=(5,(15,2)))], 
                    [sg.HSeparator()],]
    column_five += [[sg.Text("System-wide Details",pad=(5,(15,2)))], 
                          [sg.HSeparator()],]                
    
    for e in e_labels:
        column_four += [sg.Text(e+':',enable_events = True,key=(e),pad=(0,0))],
        column_five += [sg.Text('|',enable_events = True,key=(e+'i'),pad=(0,0))],
    
    
    
    map_options = [
    [sg.Radio('Show Selected','-DISPLAY-',key=('-FULL-'),default=True,pad=(0,0))],
    [sg.Radio('Find Earth Like','-DISPLAY-',key=('-EARTH-'),pad=(0,0))],
    ]
        
    label_options = [
    [sg.Radio('Num','-OVERLAY-',key=('-NUM-'),default=True,pad=(0,0))],
    [sg.Radio('Name','-OVERLAY-',key=('-NAME-'),pad=(0,0))],
    ]
          
        
    
        
    
        
    column_six = [[sg.Canvas(key='-CANVAS-')],
                 [sg.Column(map_options),
                  sg.Column(label_options),
                  sg.Button('Map',key=('-MAP-'))], 
                  ]
    
    
    #              [sg.Radio('Sector',key=('-SECTOR-')),sg.Button('Earth-like',key=('-EARTH-')),
    #               sg.Button('Subsector'),sg.Button('System'),
    
    
    
    
    
    
                             
    
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
              sg.Button('Main World',key=('-MAIN-')),
              sg.Button('Full System', key=('-SYSTEM-')),
              sg.VSeparator(),
              sg.Button('Stellar',key=('-STELLAR-')),
              sg.Button('Culture', key=('-CULTURE-')),
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
    return sg.Window("""Bartleby's Sector Builder""", layout,size=(1200,700),finalize=True)



def make_win2(star_columns,star_list,location):
    
        
    try:
            
        
        star_column_one = []
        star_column_two = []
        star_column_three = []
        star_column_four = []
        star_width = 300
                
        print('Entering star loop')
        


        for s_num, s in enumerate(star_list[0]):

            star_column_one += [sg.Text(star_columns[s_num]+':')],
            star_column_two += [sg.Text(s)],
    

        if len(star_list) > 1:
            
            star_width = 350

               
            for s_num, s in enumerate(star_list[1]):
    
                star_column_three += [sg.Text(s)],

        if len(star_list) == 3:
            
            star_width = 400

               
            for s_num, s in enumerate(star_list[2]):
    
                star_column_four += [sg.Text(s)],





    
        print('Setting new layout')    
        star_layout = [
                 [sg.Column(star_column_one),sg.Column(star_column_two),
                  sg.Column(star_column_three),sg.Column(star_column_four)],
                 [sg.Button('Exit')]
                 ]
    except:
             sg.Popup('Failed star layout')
            
  
     
        
        
        
            
    return sg.Window('Stellar Details',star_layout,size=(star_width,800),finalize=True)





def make_win3(culture_columns,culture_list,location):
    
       
    try:
            
        
        culture_column_one = []
        culture_column_two = []

                
        print('Entering Culture loop')
     


        for s_num, s in enumerate(culture_list[0]):

            culture_column_one += [sg.Text(culture_columns[s_num]+':')],
            culture_column_two += [sg.Text(s)],
    

    
        print('Setting new layout')    
        culture_layout = [
                 [sg.Column(culture_column_one),sg.Column(culture_column_two)],
                 [sg.HSeparator()],
                 [sg.Button('Exit')]
                 ]
    except:
             sg.Popup('Failed culture layout')
       
        
        
            
    return sg.Window('Perceived Cultural Details',culture_layout,size=(550,500),finalize=True)






# Create the Window
window1, window2, window3 = make_win1(), None, None        # start off with 1 window open
# Event Loop to process "events" and get the "values" of the inputs


fig_canvas_agg = None

while True:
    window, event, values = sg.read_all_windows()
    
    if event == sg.WIN_CLOSED or event == 'Exit':
           window.close()
           if window == window2:       # if closing win 2, mark as closed
               window2 = None
           if window == window3:       # if closing win 3, mark as closed
               window3 = None
           elif window == window1:     # if closing win 1, exit program
               break
        
    if event == '-DB-':

        

        db_name = values['-DB-']

        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        df = pd.read_sql_query(new_main_query,conn)
        df_system = pd.read_sql_query(system_main_query,conn)
        df_stellar = pd.read_sql_query('SELECT * FROM stellar_bodies',conn)
        df_culture = pd.read_sql_query('SELECT * FROM perceived_culture',conn)
        

        
        df_details = pd.read_sql_query(new_detail_sql_query,conn)
        
        
        print('made it out of df')

        df_details['atmos_pressure'] = round(df_details['atmos_pressure'],2)
        df_details['jump_point_distance'] = round(df_details['jump_point_distance'],1)# otherwise crazy decimals added
        df_details['mainworld_calc'] = round(df_details['mainworld_calc'],2)            


        
        df_economic = pd.read_sql_query(economic_sql_query,conn)
        df_economic['exchange'] = round(df_economic['exchange'],2)  # otherwise crazy decimals added

        

        exo_sql_query =  '''SELECT t.*,
        s.remarks,
        s.ix,
        s.ex,
        s.cx,
        s.n,
        s.bases,
        s.zone,
        s.pbg,
        s.w,
        s.allegiance,
        stars
        FROM traveller_stats t   
        LEFT JOIN system_stats s ON s.location=t.location'''
        
            
        df_exo = pd.read_sql_query(exo_sql_query,conn)
        
        exo_detail_sql_query = '''SELECT t.system_name, t.location, t.location_orb, 
        o.body, o.wtype as type, o.day, o.year,
        o.gravity, o.atmos_pressure, o.atmos_composition, o.temperature, o.climate, 
        o.impact_moons, o.natural_moons,
        j.stellar_distance as stellar_distance, 
        j.jump_point_Mm as jump_point_distance, 
        j.planet_stellar_masked as stellar_mask,
        j.hrs_1g,j.hrs_2g,j.hrs_3g,j.hrs_4g,j.hrs_5g,j.hrs_6g,
        e.mainworld_calc
        FROM traveller_stats t
        LEFT JOIN orbital_bodies o
        ON t.location_orb = o.location_orbit
        LEFT JOIN journey_data j
        ON j.location_orbit = t.location_orb
        LEFT JOIN main_world_eval e
        ON t.location_orb = e.location_orbit
        '''

        df_exo_details = pd.read_sql_query(exo_detail_sql_query,conn)

        df_exo_details['atmos_pressure'] = round(df_exo_details['atmos_pressure'],2)
        df_exo_details['jump_point_distance'] = round(df_exo_details['jump_point_distance'],1)
        df_exo_details['mainworld_calc'] = round(df_exo_details['mainworld_calc'],2)   






        df['loc_name'] = df['location'] + '-' + df['system_name']
        df_details['loc_name'] = df_details['location'] + '-' + df_details['system_name']
        option_list = list(df['loc_name'])
        window['-LOCATIONS-'].update(option_list)
        
        if fig_canvas_agg:
        # ** IMPORTANT ** Clean up previous drawing before drawing again
            delete_figure_agg(fig_canvas_agg)

            
    

        conn.commit()  
        c.close()
        conn.close()  


    if event == '-MAIN-':
        detail_flag = 'main_world'
        window['-LOCATIONS-'].update(option_list)
        
        
    elif event == '-LOCATIONS-':
        try:
            
            location = values['-LOCATIONS-'][0][0:4]
            
            
            if detail_flag == 'main_world':
                
                location_orb_name = values['-LOCATIONS-'][0]
            
                loc_info = df.loc[df['location'] == location]
                system_info = df_system.loc[df_system['location'] == location]
                detail_info = df_details[df_details['location'] == location]
                economic_info = df_economic[df_economic['location'] == location]
    
                update_stats(loc_info,system_info,detail_info,economic_info,m_labels,s_labels,d_labels,e_labels)
    

    
                try:
                  
                    clear_images()
                    select_images(loc_info,system_info,detail_info,economic_info)
        

                
                except:
                    sg.Popup('Failed during Mainworld image creation')
                
            else:
                
                print('Exo Flag')
                
                location_orb_name = values['-LOCATIONS-'][0]
                


                try:
                    loc_info = df_exo.loc[df_exo['location_orb'] == location_orb_name]
                    detail_info = df_exo_details[df_exo_details['location_orb'] == location_orb_name]
                    economic_info = df_economic[df_economic['location'] == location]
                except:
                    sg.Popup('Loc Info fail in Exo assignments')
                
               
    
                try:
                    update_stats(loc_info,system_info,detail_info,economic_info,m_labels,s_labels,d_labels,e_labels)
    

                except:
                    sg.Popup('for loops failed in Exo Assignments')
                    
    
                try:
                  
                    clear_images()
                    select_images(loc_info,system_info,detail_info,economic_info)
        
                
                except:
                    sg.Popup('Failed during non-mainworld Image creation')

            
           
            try:  
                
                
                
                if fig_canvas_agg:
                # ** IMPORTANT ** Clean up previous drawing before drawing again
                    delete_figure_agg(fig_canvas_agg)            
    
                
                print('Map is selected')
                draw_map()
                    
                    
                fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, f)
    
                
            except:
                print('Failed Map button')
                    

                

        except:
            sg.popup('Error in LOCATION: '+detail_flag)
        
    elif event == '-STELLAR-' and not window2:
        try:
            print('pressed STELLAR')
            
            star_list=[]
            df_star = df_stellar.loc[df_stellar['location'] == location]    
            star_columns = list(df_star.columns)
            for s in range(0,df_star.shape[0]):
                row = ''
                row=df_star.iloc[s]
                star_list.append(row)
            window2 = make_win2(star_columns,star_list,location)
  

        except:
            print('Failed Stellar button')
            
    elif event == '-CULTURE-' and not window3:
        try:
            print('pressed Culture')
            
            culture_list=[]
            df_this_culture = df_culture.loc[df_culture['location'] == location]    
            culture_columns = list(df_this_culture.columns)
            for s in range(0,df_this_culture.shape[0]):
                row = ''
                row=df_this_culture.iloc[s]
                culture_list.append(row)
            window3 = make_win3(culture_columns,culture_list,location)
  

        except:
            print('Failed Culture button')
            
    elif event == '-SYSTEM-':
        try:
            print('pressed SYSTEM')
            detail_flag = 'exo_world'
            
            
            loc_info = df_exo.loc[df_exo['location_orb'] == location_orb_name]
            detail_info = df_exo_details[df_exo_details['location_orb'] == location_orb_name]
            economic_info = df_economic[df_economic['location'] == location]
            

            exo_location_orb_name = values['-LOCATIONS-'][0]
            exo_location = values['-LOCATIONS-'][0][0:4]
           
            exo_loc_info = df_exo.loc[df_exo['location'] == location]
            exo_detail_info = df_details[df_details['location'] == location]

            economic_info = df_economic[df_economic['location'] == location]            
            economic_info['exchange'] = round(economic_info['exchange'],2)  # otherwise crazy decimals added    

            exo_loc_info['loc_name'] = exo_loc_info['location_orb'] 

            exo_list = list(exo_loc_info['loc_name'])
            exo_list.sort()
            window['-LOCATIONS-'].update(exo_list)               
                


        except:
            print('Failed System button.  Location was:',location)


           
    elif event == '-MAP-':
        try:  
            if fig_canvas_agg:
                # ** IMPORTANT ** Clean up previous drawing before drawing again
                    delete_figure_agg(fig_canvas_agg)            
            
                
            draw_map()
            
            
            fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, f)
            
           
        except:
            print('Failed draw_map()')



window.close()