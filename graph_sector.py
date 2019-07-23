
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




import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt



LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
style.use("ggplot")

f= Figure(figsize=(20,11),dpi=100)




def qf():
    print("Shutting Down")
    app.destroy()

def not_ready():
    tk.messagebox.showinfo("Information","Not supported just yet!")


def animate(label_list,color_list,plot_list,*args):

    print('Made it to animate')
    a = f.add_subplot(121)

    



    a.clear()
    a.set_xticks([])
    a.set_yticks([])
    xcoordinates = []
    ycoordinates = []
    
    arg_num = 0
    for arg in args:
        print(arg)
        xcoordinates,ycoordinates = get_coordinates(arg)
        color_choice = color_list[arg_num]
        label_choice = label_list[arg_num]
        plot_size = plot_list[arg_num]
        a.scatter(xcoordinates,ycoordinates,c=color_choice,label=label_choice, s=plot_size)
        arg_num += 1
    a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3, ncol=2, borderaxespad=0)  
    
    text_container = tk.Frame()
    text_container.pack(side="right", fill="both", expand = False)
    text_container.grid_rowconfigure(0, weight=1)
    text_container.grid_columnconfigure(0, weight=1)
    T = tk.Text(text_container, height=100, width=30)
    T.pack()
    T.insert(tk.END, "Just a text Widget\nin two lines\n")
    
    
    
    
    f.canvas.draw_idle()


    

        
    
    
def stellarmenu_action():
    df_binary = df.query('system_type == "Binary"')
    df_solo = df.query('system_type == "Solo"')
    df_trinary = df.query('system_type == "Trinary"')  
    stell_colors =['Green','Blue','Red']
    stell_labels = ['Solo','Binary','Trinary']
    plot_list = [65,65,65]
    animate(stell_labels,stell_colors,plot_list ,df_solo,df_binary,df_trinary)    
    
def luminosity_action():
    df_lum_d = df.query('luminosity_class == "D"')
    df_lum_v = df.query('luminosity_class == "V"')
    df_lum_iii = df.query('luminosity_class == "III"')  
    stell_colors =['Green','Blue','Red']
    stell_labels = ['Class V, Main Sequence','Class D, White Dwarf','Class III, Giant']
    plot_list = [65,30,100]
    animate(stell_labels,stell_colors,plot_list,df_lum_v,df_lum_d,df_lum_iii)     
    
def spectral_type_action():
    df_spectral_m = df.query('spectral_type == "M5" | spectral_type == "M0" ')
    df_spectral_k = df.query('spectral_type == "K5" | spectral_type == "K0" ')
    df_spectral_g = df.query('spectral_type == "G5" | spectral_type == "G0" ')
    df_spectral_f = df.query('spectral_type == "F5" | spectral_type == "F0" ')
    df_spectral_a = df.query('spectral_type == "A5" | spectral_type == "A0" ')
    df_spectral_w = df.query('spectral_type == "w"')
    stell_colors =['Red','Orange','Yellow','Wheat','White','Black']
    stell_labels = ['Type M','Type K','Type G','Type F','Type A','Type w']
    plot_list  = [65,65,65,65,65,30]
    animate(stell_labels,stell_colors,plot_list,df_spectral_m,df_spectral_k,df_spectral_g,
            df_spectral_f,df_spectral_a,df_spectral_w)  
    
def stellar_age_action():
    df_spectral_age_small = df.query('age < 4')
    df_spectral_age_medium = df.query('age >= 4 & age <=8')
    df_spectral_age_large = df.query('age >8')
    stell_colors =['Blue','Green','Red']
    stell_labels = ['Under 4 billion years','4 to 8 billion years','Over 8 billion years']
    plot_list  = [30,65,100]
    animate(stell_labels,stell_colors,plot_list,df_spectral_age_small,
            df_spectral_age_medium,df_spectral_age_large)
    
def stellar_orbits_action():
    df_spectral_orbits_small = df.query('orbits < 6')
    df_spectral_orbits_medium = df.query('orbits >= 6 & orbits <=8')
    df_spectral_orbits_large = df.query('orbits >8')
    stell_colors =['Blue','Green','Red']
    stell_labels = ['Under 4 orbital zones','4 to 8 orbital zones','Over 8 orbital zones']
    plot_list  = [30,65,100]
    animate(stell_labels,stell_colors,plot_list,df_spectral_orbits_small,
            df_spectral_orbits_medium,df_spectral_orbits_large)
    
def stellar_belts_action():
    df_spectral_belts_none = df.query('belts == 0')
    df_spectral_belts_one = df.query('belts == 1')
    df_spectral_belts_two_or_more = df.query('belts >= 2')
    stell_colors =['Blue','Green','Red']
    stell_labels = ['No belts present','One belt present','More than one belt present']
    plot_list  = [30,65,100]
    animate(stell_labels,stell_colors,plot_list,df_spectral_belts_none,
            df_spectral_belts_one,df_spectral_belts_two_or_more)    
    
def stellar_giants_action():
    df_spectral_giants_none = df.query('gg == 0')
    df_spectral_giants_one = df.query('gg == 1 ')
    df_spectral_giants_two_or_three = df.query('gg >= 2 & gg < 4')
    df_spectral_giants_four_or_more = df.query('gg >= 4')
    stell_colors =['Blue','Green','Orange','Red']
    stell_labels = ['No gas giants present','One gas giant present',
                    'Two or three gas giants present','At least four gas giants present']
    plot_list  = [30,65,65,100]
    animate(stell_labels,stell_colors,plot_list,df_spectral_giants_none,
            df_spectral_giants_one,df_spectral_giants_two_or_three,df_spectral_giants_four_or_more)    
    

def starport_action():
    df_starport_a = df_uwp.query('starport == "A"')
    df_starport_b = df_uwp.query('starport == "B"')
    df_starport_c = df_uwp.query('starport == "C"')
    df_starport_d = df_uwp.query('starport == "D"')
    df_starport_e = df_uwp.query('starport == "E"')
    df_starport_x = df_uwp.query('starport == "X"')    
    stell_colors =['Green','Turquoise','Blue','Salmon','Orange','Red']
    stell_labels = ['Class A','Class B','Class C','Class D','Class E','Class X']
    plot_list  = [90,65,65,65,65,30]
    animate(stell_labels,stell_colors,plot_list,df_starport_a,df_starport_b,df_starport_c,df_starport_d,
            df_starport_e,df_starport_x)  
    
def planetary_size_action():
    df_planetary_size_small = df_uwp.query('size < 2')
    df_planetary_size_medium = df_uwp.query('size >= 2 & size <=6')
    df_planetary_size_large = df_uwp.query('size >6')
    stell_colors =['Blue','Green','Red']
    stell_labels = ['Size 0 or 1','Size 2 to 6','Size 7 or higher']
    plot_list  = [30,65,100]
    animate(stell_labels,stell_colors,plot_list,df_planetary_size_small,
            df_planetary_size_medium,df_planetary_size_large)
    
def planetary_atmosphere_action():
    df_planetary_atmosphere_breathable = df_uwp.query('atmosphere == 5 |atmosphere == 6|atmosphere == 8')
    df_planetary_atmosphere_not_breathable = df_uwp.query('(atmosphere > 0 & atmosphere < 5) |atmosphere == 7|atmosphere == 9')
    df_planetary_atmosphere_dangerous = df_uwp.query('atmosphere >9')
    df_planetary_atmosphere_none = df_uwp.query('atmosphere <=0')
    df_planetary_size_large = df_uwp.query('size >6')
    stell_colors =['Green','Blue','Red','Black']
    stell_labels = ['Breathable','Not Breathable','Dangerous','No atmosphere']
    plot_list  = [65,65,65,30]
    animate(stell_labels,stell_colors,plot_list,df_planetary_atmosphere_breathable,
            df_planetary_atmosphere_not_breathable,
            df_planetary_atmosphere_dangerous,
            df_planetary_atmosphere_none)
    
    
def planetary_hydrographics_action():
    df_planetary_hydrographics_high = df_uwp.query('hydrographics >= 8')
    df_planetary_hydrographics_none = df_uwp.query('hydrographics <= 0')
    df_planetary_hydrographics_low = df_uwp.query('hydrographics > 0 & hydrographics <2')
    df_planetary_hydrographics_mid = df_uwp.query('hydrographics >= 2 & hydrographics <= 7')
    


    stell_colors =['Black','Green','Teal','Blue']
    stell_labels = ['No Hydro %','<20% Hydro %','20% to 80% Hydro','>80% Hydro %',]
    plot_list  = [30,65,65,65]
    animate(stell_labels,stell_colors,plot_list,
            df_planetary_hydrographics_none,
            df_planetary_hydrographics_low, 
            df_planetary_hydrographics_mid,
            df_planetary_hydrographics_high)
    
def planetary_population_action():
    df_planetary_population_high = df_uwp.query('population > 7')
    df_planetary_population_none = df_uwp.query('population <= 0')
    df_planetary_population_mid = df_uwp.query('population > 4 & population <=7')
    df_planetary_population_low = df_uwp.query('population <= 4 & population > 0')


    stell_colors =['Black','Green','Blue','Red']
    stell_labels = ['Population 0','Population 1 to 4','Population 5 to 7','Population 8 or higher']
    plot_list  = [30,65,65,65]
    animate(stell_labels,stell_colors,plot_list,
            df_planetary_population_none,
            df_planetary_population_low, 
            df_planetary_population_mid,
            df_planetary_population_high)
    
def planetary_government_action():
    df_planetary_government_high = df_uwp.query('government > 8')
    df_planetary_government_none = df_uwp.query('government <= 0')
    df_planetary_government_mid = df_uwp.query('government > 3 & government <=8')
    df_planetary_government_low = df_uwp.query('government <= 3 & government > 0')


    stell_colors =['Black','Green','Blue','Red']
    stell_labels = ['Government 0','Government 1 to 3','Government 4 to 8','Government 9 or higher']
    plot_list  = [30,65,65,65]
    animate(stell_labels,stell_colors,plot_list,
            df_planetary_government_none,
            df_planetary_government_low, 
            df_planetary_government_mid,
            df_planetary_government_high)    
    
def planetary_law_action():
    df_planetary_law_high = df_uwp.query('law > 8')
    df_planetary_law_none = df_uwp.query('law <= 0')
    df_planetary_law_mid = df_uwp.query('law > 3 & law <=8')
    df_planetary_law_low = df_uwp.query('law <= 3 & law > 0')


    stell_colors =['Black','Green','Blue','Red']
    stell_labels = ['Law Level 0','Law Level 1 to 3','Law Level 4 to 8','Law Level 9 or higher']
    plot_list  = [30,65,65,65]
    animate(stell_labels,stell_colors,plot_list,
            df_planetary_law_none,
            df_planetary_law_low, 
            df_planetary_law_mid,
            df_planetary_law_high)        
    
def planetary_tech_action():
    df_planetary_tech_high = df_uwp.query('tech_level > 11')
    df_planetary_tech_none = df_uwp.query('tech_level <= 0')
    df_planetary_tech_mid = df_uwp.query('tech_level > 6 & tech_level <=11')
    df_planetary_tech_low = df_uwp.query('tech_level <= 6 & tech_level > 0')


    stell_colors =['Black','Green','Blue','Red']
    stell_labels = ['Tech Level 0','Tech Level 1 to 6','Tech Level 7 to 11','Tech Level 12 or higher']
    plot_list  = [30,65,65,65]
    animate(stell_labels,stell_colors,plot_list,
            df_planetary_tech_none,
            df_planetary_tech_low, 
            df_planetary_tech_mid,
            df_planetary_tech_high)      


    

class sectorvisapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self,"sunburst.ico")
        tk.Tk.wm_title(self,"TUC Browser")
            
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=not_ready)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=qf)
        menubar.add_cascade(label="File",menu=filemenu)
        
        stellarmenu = tk.Menu(menubar, tearoff=0)
        stellarmenu.add_command(label="System Type", command = stellarmenu_action)
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
        uwpwmenu.add_command(label="Influence", command=not_ready)        
        menubar.add_cascade(label="UWP",menu=uwpwmenu)      

        planetarymenu = tk.Menu(menubar, tearoff=0)
        planetarymenu.add_command(label="Orbit", command=not_ready)
        planetarymenu.add_command(label="Distance", command=not_ready)
        planetarymenu.add_command(label="Zone", command=not_ready)      
        planetarymenu.add_command(label="Gravity", command=not_ready)
        planetarymenu.add_command(label="Moons", command=not_ready)
        planetarymenu.add_command(label="Temperature", command=not_ready)
        menubar.add_cascade(label="Main World",menu=planetarymenu)                                         




        
        
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
     
       
        button1 = ttk.Button(self, text="Sector Map",
                            command=lambda: controller.show_frame(SectorMap))
        button1.pack()
        

        
        button3 = ttk.Button(self, text="Exit",
                            command=lambda: qf())
        button3.pack()
        



def get_coordinates(thedataframe):
    xcoordinates = []
    ycoordinates = []
    for coord in thedataframe.location:
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
        label = ttk.Label(self, text="System Stellar Types", font=LARGE_FONT)
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
    
          
         


conn = sqlite3.connect('test_4.db')
c = conn.cursor()
df = pd.read_sql_query('''SELECT * FROM tb_stellar_primary''', conn)
df_uwp = pd.read_sql_query('''SELECT * FROM tb_t5''', conn)
print(df)
conn.commit()  
c.close()
conn.close()


 

     
        
app = sectorvisapp()
app.geometry("1000x800")
#animate(df) 
app.mainloop()



#
#

#plt.show
#
