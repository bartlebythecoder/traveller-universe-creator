
#!/usr/bin/python
"""
Created on Mon Jul  8 17:33:12 2019

@author: sean
"""

# graph_sector.py
# STILL UNDER CONSTRUCTION
# This will produce visualizations of the created sectors

import pandas as pd
import sqlite3
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
import re
import ntpath






import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from matplotlib import pyplot as plt



LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
style.use("dark_background")

f= Figure(figsize=(6,7),dpi=100)

def file_open():

    root.filename =  filedialog.askopenfilename(title = "Select the database file",
                     filetypes = (("db files","*.db"),("all files","*.*")))
    conn = sqlite3.connect(root.filename)
    c = conn.cursor()
    df = pd.read_sql_query('''SELECT
                           stellar_bodies.location,
                           luminosity_class,
                           spectral_type,
                           orbits,
                           age,
                           belts,
                           gg,
                           main_worlds.system_name,
                           main_worlds.location as tf_loc
                           FROM stellar_bodies
                           LEFT JOIN main_worlds on main_worlds.location = stellar_bodies.location''', conn)
    df_world_uwp = pd.read_sql_query('''SELECT 
                orbital_bodies.location,
                stellar_distance as distance,
                orbital_bodies.zone,
                body,
                density,
                gravity,
                atmos_pressure,
                temperature,
                main_worlds.location as mw_loc,
                main_worlds.system_name,
                main_worlds.starport,
                main_worlds.size,
                main_worlds.atmosphere,
                main_worlds.hydrographics,
                main_worlds.population,
                main_worlds.government,
                main_worlds.law,
                main_worlds.tech_level,
                main_worlds.remarks,
                main_worlds.ix
                FROM main_worlds
                LEFT JOIN orbital_bodies
                ON main_worlds.location_orb = orbital_bodies.location_orbit''', conn)
                
    df_world_uwp['ix'] = df_world_uwp['ix'].apply(lambda x: int(re.sub('{|}', '', x)))
    print("Confirming df load",df_world_uwp)
    conn.commit()  
    c.close()
    conn.close()
    db_name = ntpath.basename(root.filename)

    return([df,df_world_uwp,db_name])
    
def get_file_action():
    global df
    global df_world_uwp
    global db_name
        
    df,df_world_uwp,db_name = file_open() 
    f.canvas.draw_idle()
    

def validate_something(*args):
    print('Yes validated')
    print(*args)

    
def move_cursor(a):
    print('Moving cursor')
    global cursor_y 
    cursor_y += 1
    print(cursor_y)    
    
    xcoordinates,ycoordinates = get_coordinates(df)
    a.scatter(xcoordinates[cursor_x],ycoordinates[cursor_y],c='White', s=30, marker = "*")
    print(xcoordinates,ycoordinates)
    print('cursor',xcoordinates[cursor_x],ycoordinates[cursor_y])
    
    
    
    f.canvas.draw_idle()

def qf():
    global root
    print("Shutting Down")
    root.quit()
    app.destroy()


    

def not_ready():
    tk.messagebox.showinfo("Information","Not supported just yet!")
  


def mouse_x_y(event):
    coords = (event.x, event.y)
    print(test)




def animate(chart_title,label_list,color_list,plot_list,*args):
    global cursor_x
    global cursor_y 
    global db_name
    
  
    
    a = f.add_subplot(111)




    a.clear()
    a.set_xticks([])
    a.set_yticks([])
    xcoordinates = []
    ycoordinates = []


    

    chart_title = db_name + '\n' + chart_title
    
    for arg_num, arg in enumerate(args):
        
        try:
            print(arg.system_name)
        except:
            print('Cannot find system name')
  
        xcoordinates,ycoordinates = get_coordinates(arg)

        color_choice = color_list[arg_num]
        label_choice = label_list[arg_num]
        plot_size = plot_list[arg_num]
        
        a.set_title(chart_title, color='white')
        a.scatter(xcoordinates,ycoordinates,c=color_choice,label=label_choice, s=plot_size)

    
        name_list = arg['system_name'].tolist()
        label_color = 'White'
        if len(name_list) <= 10:
            name_coords = list(zip(xcoordinates,ycoordinates))
            row_num = 0
            for each_item in name_coords:
                row_name = name_list[row_num]
                a.text(each_item[0]-2,each_item[1],row_name,fontsize = 10,color = label_color)
                row_num += 1
            

           
   


    #a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3, ncol=2, borderaxespad=0)
    a.legend(bbox_to_anchor=(1, 0, 0, 0),ncol=2)
#    app.bind("<Down>",lambda ignore_var: move_cursor(a))
    f.tight_layout()

    
    
    f.canvas.draw_idle()


    

        
    
    
def stellarmenu_action():
    df_binary = df.query('system_type == "Binary"')
    df_solo = df.query('system_type == "Solo"')
    df_trinary = df.query('system_type == "Trinary"')  
    stell_colors =['Green','Blue','Red']
    stell_labels = ['Solo','Binary','Trinary']
    plot_list = [65,65,65]
    animate('System Type',stell_labels,stell_colors,plot_list ,df_solo,df_binary,df_trinary)    
    
def luminosity_action():
    df_lum_d = df.query('luminosity_class == "D"')
    df_lum_v = df.query('luminosity_class == "V"')
    df_lum_iii = df.query('luminosity_class == "III"')  
    stell_colors =['Green','Blue','Red']
    stell_labels = ['Class V, Main Sequence','Class D, White Dwarf','Class III, Giant']
    plot_list = [65,30,100]
    animate('Luminosity Class',stell_labels,stell_colors,plot_list,df_lum_v,df_lum_d,df_lum_iii)     
    
def spectral_type_action():
    df_spectral_m = df.query('spectral_type == "M5" | spectral_type == "M0" ')
    df_spectral_k = df.query('spectral_type == "K5" | spectral_type == "K0" ')
    df_spectral_g = df.query('spectral_type == "G5" | spectral_type == "G0" ')
    df_spectral_f = df.query('spectral_type == "F5" | spectral_type == "F0" ')
    df_spectral_a = df.query('spectral_type == "A5" | spectral_type == "A0" ')
    df_spectral_w = df.query('spectral_type == "w"')
    stell_colors =['Red','Orange','Yellow','Wheat','White','Grey']
    stell_labels = ['Type M','Type K','Type G','Type F','Type A','Type w']
    plot_list  = [65,65,65,65,65,30]
    animate('Spectral Type',stell_labels,stell_colors,plot_list,df_spectral_m,df_spectral_k,df_spectral_g,
            df_spectral_f,df_spectral_a,df_spectral_w)  
    
def stellar_age_action():
    df_spectral_age_small = df.query('age < 4')
    df_spectral_age_medium = df.query('age >= 4 & age <=8')
    df_spectral_age_large = df.query('age >8')
    stell_colors =['Blue','Green','Red']
    stell_labels = ['Under 4 billion years','4 to 8 billion years','Over 8 billion years']
    plot_list  = [30,65,100]
    animate('Age in Billions of Years',stell_labels,stell_colors,plot_list,df_spectral_age_small,
            df_spectral_age_medium,df_spectral_age_large)
    
def stellar_orbits_action():
    df_spectral_orbits_small = df.query('orbits < 6')
    df_spectral_orbits_medium = df.query('orbits >= 6 & orbits <=8')
    df_spectral_orbits_large = df.query('orbits >8')
    stell_colors =['Blue','Green','Red']
    stell_labels = ['Under 4 orbital zones','4 to 8 orbital zones','Over 8 orbital zones']
    plot_list  = [30,65,100]
    animate("Number of Orbital Zones Around Primary",stell_labels,stell_colors,plot_list,df_spectral_orbits_small,
            df_spectral_orbits_medium,df_spectral_orbits_large)
    
def stellar_belts_action():
    df_spectral_belts_none = df.query('belts == 0')
    df_spectral_belts_one = df.query('belts == 1')
    df_spectral_belts_two_or_more = df.query('belts >= 2')
    stell_colors =['Grey','Green','Red']
    stell_labels = ['No belts present','One belt present','More than one belt present']
    plot_list  = [30,65,100]
    animate("Number of Planetary Belts",stell_labels,stell_colors,plot_list,df_spectral_belts_none,
            df_spectral_belts_one,df_spectral_belts_two_or_more)    
    
def stellar_giants_action():
    df_spectral_giants_none = df.query('gg == 0')
    df_spectral_giants_one = df.query('gg == 1 ')
    df_spectral_giants_two_or_three = df.query('gg >= 2 & gg < 4')
    df_spectral_giants_four_or_more = df.query('gg >= 4')
    stell_colors =['Grey','Green','Orange','Red']
    stell_labels = ['No GG present','1 GG present',
                    '2 or 3 GG present','4> GG present']
    plot_list  = [30,65,65,100]
    animate('Number of Gas Giants in Orbit',stell_labels,stell_colors,plot_list,df_spectral_giants_none,
            df_spectral_giants_one,df_spectral_giants_two_or_three,df_spectral_giants_four_or_more)    
    

def starport_action():
    df_starport_a = df_world_uwp.query('starport == "A"')
    df_starport_b = df_world_uwp.query('starport == "B"')
    df_starport_c = df_world_uwp.query('starport == "C"')
    df_starport_d = df_world_uwp.query('starport == "D"')
    df_starport_e = df_world_uwp.query('starport == "E"')
    df_starport_x = df_world_uwp.query('starport == "X"')    
    stell_colors =['Green','Turquoise','Blue','Salmon','Orange','Red']
    stell_labels = ['Class A','Class B','Class C','Class D','Class E','Class X']
    plot_list  = [90,65,65,65,65,30]
    animate('Mainworld Starport Class',stell_labels,stell_colors,plot_list,df_starport_a,df_starport_b,df_starport_c,df_starport_d,
            df_starport_e,df_starport_x)  
    
def planetary_size_action():
    df_planetary_size_small = df_world_uwp.query('size < 2')
    df_planetary_size_medium = df_world_uwp.query('size >= 2 & size <=6')
    df_planetary_size_large = df_world_uwp.query('size >6')
    stell_colors =['Blue','Green','Red']
    stell_labels = ['Size 0 or 1','Size 2 to 6','Size 7 or higher']
    plot_list  = [30,65,100]
    animate('Mainworld Size Code',stell_labels,stell_colors,plot_list,df_planetary_size_small,
            df_planetary_size_medium,df_planetary_size_large)
    
def planetary_atmosphere_action():
    df_planetary_atmosphere_breathable = df_world_uwp.query('atmosphere == 5 |atmosphere == 6|atmosphere == 8')
    df_planetary_atmosphere_not_breathable = df_world_uwp.query('(atmosphere > 0 & atmosphere < 5) |atmosphere == 7|atmosphere == 9')
    df_planetary_atmosphere_dangerous = df_world_uwp.query('atmosphere >9')
    df_planetary_atmosphere_none = df_world_uwp.query('atmosphere <=0')
    df_planetary_size_large = df_world_uwp.query('size >6')
    stell_colors =['Green','Blue','Red','Grey']
    stell_labels = ['Breathable','Not Breathable','Dangerous','No atmosphere']
    plot_list  = [65,65,65,30]
    animate('Mainworld Atmosphere Code',stell_labels,stell_colors,plot_list,df_planetary_atmosphere_breathable,
            df_planetary_atmosphere_not_breathable,
            df_planetary_atmosphere_dangerous,
            df_planetary_atmosphere_none)
    
    
def planetary_hydrographics_action():
    df_planetary_hydrographics_high = df_world_uwp.query('hydrographics >= 8')
    df_planetary_hydrographics_none = df_world_uwp.query('hydrographics <= 0')
    df_planetary_hydrographics_low = df_world_uwp.query('hydrographics > 0 & hydrographics <2')
    df_planetary_hydrographics_mid = df_world_uwp.query('hydrographics >= 2 & hydrographics <= 7')
    


    stell_colors =['Grey','Green','Teal','Blue']
    stell_labels = ['No Hydro %','<20% Hydro %','20% to 80% Hydro','>80% Hydro %',]
    plot_list  = [30,65,65,65]
    animate('Mainworld Hydrographics %',stell_labels,stell_colors,plot_list,
            df_planetary_hydrographics_none,
            df_planetary_hydrographics_low, 
            df_planetary_hydrographics_mid,
            df_planetary_hydrographics_high)
    
def planetary_population_action():
    df_planetary_population_high = df_world_uwp.query('population > 7')
    df_planetary_population_none = df_world_uwp.query('population <= 0')
    df_planetary_population_mid = df_world_uwp.query('population > 4 & population <=7')
    df_planetary_population_low = df_world_uwp.query('population <= 4 & population > 0')


    stell_colors =['Grey','Green','Blue','Red']
    stell_labels = ['Population 0','Population 1 to 4','Population 5 to 7','Population 8 or higher']
    plot_list  = [30,65,65,65]
    animate('Mainworld Population Code',stell_labels,stell_colors,plot_list,
            df_planetary_population_none,
            df_planetary_population_low, 
            df_planetary_population_mid,
            df_planetary_population_high)
    
def planetary_government_action():
    df_planetary_government_high = df_world_uwp.query('government > 8')
    df_planetary_government_none = df_world_uwp.query('government <= 0')
    df_planetary_government_mid = df_world_uwp.query('government > 3 & government <=8')
    df_planetary_government_low = df_world_uwp.query('government <= 3 & government > 0')


    stell_colors =['Grey','Green','Blue','Red']
    stell_labels = ['Government 0','Government 1 to 3','Government 4 to 8','Government 9 or higher']
    plot_list  = [30,65,65,65]
    animate('Mainworld Government Code',stell_labels,stell_colors,plot_list,
            df_planetary_government_none,
            df_planetary_government_low, 
            df_planetary_government_mid,
            df_planetary_government_high)    
    
def planetary_law_action():
    df_planetary_law_high = df_world_uwp.query('law > 8')
    df_planetary_law_none = df_world_uwp.query('law <= 0')
    df_planetary_law_mid = df_world_uwp.query('law > 3 & law <=8')
    df_planetary_law_low = df_world_uwp.query('law <= 3 & law > 0')


    stell_colors =['Grey','Green','Blue','Red']
    stell_labels = ['Law Level 0','Law Level 1 to 3','Law Level 4 to 8','Law Level 9 or higher']
    plot_list  = [30,65,65,65]
    animate('Mainworld Law Level Code',stell_labels,stell_colors,plot_list,
            df_planetary_law_none,
            df_planetary_law_low, 
            df_planetary_law_mid,
            df_planetary_law_high)        
    
def planetary_tech_action():
    df_planetary_tech_high = df_world_uwp.query('tech_level > 11')
    df_planetary_tech_none = df_world_uwp.query('tech_level <= 0')
    df_planetary_tech_mid = df_world_uwp.query('tech_level > 6 & tech_level <=11')
    df_planetary_tech_low = df_world_uwp.query('tech_level <= 6 & tech_level > 0')


    stell_colors =['Grey','Green','Blue','Red']
    stell_labels = ['Tech Level 0','Tech Level 1 to 6','Tech Level 7 to 11','Tech Level 12 or higher']
    plot_list  = [30,65,65,65]
    animate('Mainworld Tech Level Code',stell_labels,stell_colors,plot_list,
            df_planetary_tech_none,
            df_planetary_tech_low, 
            df_planetary_tech_mid,
            df_planetary_tech_high)      
    
def body_action():
    df_planet = df_world_uwp.query('body == "Planet"')
    df_belt = df_world_uwp.query('body == "Planetoid Belt"')
    df_gg = df_world_uwp.query('body == "Gas Giant"')
    stell_colors =['Green','Grey','Orange']
    stell_labels = ['Planet','Asteroid Belt','Gas Giant Moon']
    plot_list  = [65,30,100]
    animate('Mainworld Planetary Type',stell_labels,stell_colors,plot_list,df_planet,df_belt,df_gg)      
    
def distance_action():
    df_distance_far = df_world_uwp.query('distance > 1.50')
    df_distance_close = df_world_uwp.query('distance <= .5')
    df_distance_medium = df_world_uwp.query('distance > .5 & distance <=1.50')
    stell_colors =['Green','Blue','Red']
    stell_labels = ['Med (0.5 to 1.5 AU)','Far (>1.5 AU)','Close (<0.5 AU)']
    plot_list  = [65,65,65]
    animate('Mainworld Distance to Primary (in AU)',stell_labels,stell_colors,plot_list,
            df_distance_medium,
            df_distance_far, 
            df_distance_close)          
    
def zone_action():
    df_zone_inner = df_world_uwp.query('zone == "Inner Zone"')
    df_zone_outer = df_world_uwp.query('zone == "Outer Zone"')
    df_zone_life = df_world_uwp.query('zone == "Life Zone"')
    df_zone_middle = df_world_uwp.query('zone == "Middle Zone"')
    stell_colors =['Red','Blue','Green','Grey']
    stell_labels = ['Inner Zone','Outer Zone','Life Zone','Middle Zone']
    plot_list  = [65,65,65,65]
    animate('Mainworld Orbital Zone',stell_labels,stell_colors,plot_list,
            df_zone_inner,
            df_zone_outer, 
            df_zone_life,
            df_zone_middle)           
    
def gravity_action():
    df_gravity_high = df_world_uwp.query('gravity > 1.25')
    df_gravity_low = df_world_uwp.query('gravity <= .75')
    df_gravity_medium = df_world_uwp.query('gravity > .75 & gravity <=1.25')
    stell_colors =['Green','Red','Blue']
    stell_labels = ['Med (0.75 to 1.25 G)','High (>1.25 G)','Low (<0.75 G)']
    plot_list  = [65,100,30]
    animate('Mainworld Gravity (in Gs)',stell_labels,stell_colors,plot_list,
            df_gravity_medium,
            df_gravity_high, 
            df_gravity_low) 
    
def atmos_press_action():
    df_ap_high = df_world_uwp.query('atmos_pressure > 1.2')
    df_ap_low = df_world_uwp.query('atmos_pressure <= .7')
    df_ap_medium = df_world_uwp.query('atmos_pressure > .7 & atmos_pressure <=1.2')
    stell_colors =['Green','Red','Blue']
    stell_labels = ['Med (0.7 to 1.2)','High (>1.2)','Low (<0.7)']
    plot_list  = [65,100,30]
    animate('Mainworld Atmospheric Pressure (in Earth units)',stell_labels,stell_colors,plot_list,
            df_ap_medium,
            df_ap_high, 
            df_ap_low) 
    
   
def temperature_action():
    df_temp_torrid = df_world_uwp.query('temperature > 324')
    df_temp_hot = df_world_uwp.query('temperature <= 324 & temperature > 303')
    df_temp_normal = df_world_uwp.query('temperature <= 303 & temperature > 294')
    df_temp_cold =  df_world_uwp.query('temperature <= 294 & temperature > 238')
    df_temp_frigid = df_world_uwp.query('temperature <= 238')
    stell_colors =['Red','Orange','Green','skyblue','Blue']
    stell_labels = ['Extreme Heat (>324K)','Hot (303-324K)','Earth-Like (294-303K)','Cold (238-294K)','Extreme Cold(<238K)']
    plot_list  = [65,65,65,65,65,65]
    animate('Mainworld Average Temperature (Kelvin)',stell_labels,stell_colors,plot_list,
            df_temp_torrid,
            df_temp_hot, 
            df_temp_normal,            
            df_temp_cold,
            df_temp_frigid)     


def influence_action():
    df_influence_high = df_world_uwp.query('ix > 3')
    df_influence_moderate = df_world_uwp.query('ix >= 0 & ix <= 3')
    df_influence_negative = df_world_uwp.query('ix < 0')
    stell_colors =['Green','Blue','Red']
    stell_labels = ['High (ix > 3)','Moderate (ix 0-3)','Negative (ix <0)']
    plot_list  = [100,65,30]
    animate('Mainworld Influence Score (T5 Ix)',stell_labels,stell_colors,plot_list,
            df_influence_high,
            df_influence_moderate, 
            df_influence_negative) 


def world_remarks_action():
    df_vacc = df_world_uwp.query('remarks.str.contains("Va")')
    df_fluid = df_world_uwp.query('remarks.str.contains("Fl")')
    df_water = df_world_uwp.query('remarks.str.contains("Wa") or remarks.str.contains("Oc")')
    df_desert = df_world_uwp.query('remarks.str.contains("De")')
    df_hell = df_world_uwp.query('remarks.str.contains("He")')
    df_garden = df_world_uwp.query('remarks.str.contains("Ga")')
    stell_labels = ['N/A','Vacuum World','Fluid World','Water World','Desert World','Hell World','Garden World']
    stell_colors =['Grey','Brown','Purple','Blue','Orange','Red','Green']
    plot_list  = [30,65,65,65,65,65,65]
    animate('World Remarks',stell_labels,stell_colors,plot_list,
            df,
            df_vacc,
            df_fluid,
            df_water,
            df_desert,
            df_hell,
            df_garden)    
    
def special_cat():
    df_special_earth = (df_world_uwp.query('temperature <= 303 & \
                                           temperature > 294 &  \
                                           atmos_pressure > .7 & \
                                           atmos_pressure <=1.2 & \
                                           gravity > .75 & \
                                           gravity <=1.25 & \
                                           (atmosphere == 6 | atmosphere ==5 | atmosphere == 8) & \
                                           hydrographics > 0'))
    df_special_dune = df_world_uwp.query('temperature <= 324 & \
                                         temperature > 303 & \
                                         atmos_pressure > .7 & \
                                         atmos_pressure <=1.2 & \
                                         gravity > .75 & \
                                         gravity <=1.25 & \
                                          (atmosphere == 6 | atmosphere ==5 | atmosphere == 8) & \
                                         hydrographics <= 2')
    df_special_hoth = df_world_uwp.query('temperature <= 294 & \
                                         temperature > 238 & \
                                         atmos_pressure > .7 & \
                                         atmos_pressure <=1.2 & \
                                         gravity > .75 & \
                                         gravity <=1.25 & \
                                          (atmosphere == 6 | atmosphere ==5 | atmosphere == 8) & \
                                         hydrographics > 0')
    stell_labels = ['N/A','Earth-Like','Dune-Like','Hoth-Like']
    stell_colors =['Grey','Green','Brown','Blue']
    plot_list  = [30,65,65,65]
    animate('Mainworlds Similar to Sci-Fi Worlds',stell_labels,stell_colors,plot_list,
            df,
            df_special_earth,
            df_special_dune,
            df_special_hoth)      
    

    

class sectorvisapp(tk.Tk):
    def __init__(self, *args, **kwargs):

        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self,"sunburst.ico")
        tk.Tk.wm_title(self,"TUC")
            
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=get_file_action)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=qf)
        menubar.add_cascade(label="File",menu=filemenu)
        
        stellarmenu = tk.Menu(menubar, tearoff=0)
        stellarmenu.add_command(label="Luminosity Class", command=luminosity_action)
        stellarmenu.add_command(label="Spectral Type", command=spectral_type_action)      
        stellarmenu.add_command(label="Age", command=stellar_age_action)
        stellarmenu.add_command(label="# Orbits", command=stellar_orbits_action)
        stellarmenu.add_command(label="# Belts", command=stellar_belts_action)
        stellarmenu.add_command(label="# Gas Giants", command=stellar_giants_action)
        menubar.add_cascade(label="Primary",menu=stellarmenu)

        uwpwmenu = tk.Menu(menubar, tearoff=0)
        uwpwmenu.add_command(label="Starport", command=starport_action)
        uwpwmenu.add_command(label="Size", command=planetary_size_action)
        uwpwmenu.add_command(label="Atmosphere", command=planetary_atmosphere_action)      
        uwpwmenu.add_command(label="Hydrographics", command=planetary_hydrographics_action)
        uwpwmenu.add_command(label="Population", command=planetary_population_action)
        uwpwmenu.add_command(label="Government", command=planetary_government_action)
        uwpwmenu.add_command(label="Law Level", command=planetary_law_action)
        uwpwmenu.add_command(label="Tech Level", command=planetary_tech_action)        
        uwpwmenu.add_command(label="Influence", command=influence_action)        
        uwpwmenu.add_command(label="World Remarks", command=world_remarks_action)
        
        menubar.add_cascade(label="UWP",menu=uwpwmenu)      

        planetarymenu = tk.Menu(menubar, tearoff=0)
        planetarymenu.add_command(label="Mainworld Body", command=body_action)
        planetarymenu.add_command(label="Distance", command=distance_action)
        planetarymenu.add_command(label="Orbital Zone", command=zone_action)      
        planetarymenu.add_command(label="Gravity", command=gravity_action)
        planetarymenu.add_command(label="Atmos. Press.", command=atmos_press_action)
        planetarymenu.add_command(label="Temperature", command=temperature_action)
        menubar.add_cascade(label="Main World",menu=planetarymenu)     

        specialmenu = tk.Menu(menubar, tearoff=0)
        specialmenu.add_command(label="Sci-Fi like worlds", command=special_cat)
        menubar.add_cascade(label="Special Worlds",menu=specialmenu)                                       




        
        
        tk.Tk.config(self, menu=menubar)
        
        self.frames = {}
        
        for F in (StartPage, SectorMap):
        
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column = 0, sticky="nsew")

        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
        


        
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Sector Visualization Menu", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
     
       
        button1 = ttk.Button(self, text="Load a Database",
                            command=get_file_action)
        button1.pack()
        
        button2 = ttk.Button(self, text="View a Sector Map",
                             
                            command=lambda: controller.show_frame(SectorMap))
        button2.pack()

        
        button3 = ttk.Button(self, text="Exit",
                            command=lambda: qf())
        button3.pack()
        



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
        
        


class SectorMap(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self,parent)        
        label = ttk.Label(self, text='Sector Map', font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()


        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.NONE, expand = True)

        
        toolbar= NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack()
    

          
         

# Global Variables
cursor_x = 0
cursor_y = 0        
db_name = ''
# df = dataframe of all primary stars
# df_world_uwp = dataframe of all mainworlds and stats


    




 
root = Tk()
root.withdraw()
#df,df_world_uwp,db_name = file_open()     
        
app = sectorvisapp()
app.geometry("500x850")
#animate(df) 
app.mainloop()



#
#

#plt.show
#
