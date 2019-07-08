#!/usr/bin/python
"""
Created on Sun Jul  7 15:28:06 2019

@author: sean
"""

from tkinter import *
from traveller_master import make_sector_master

top = Tk()
top.title("Traveller Sector Creator")
top.geometry("800x400")
print('Processing...')

def helloCallBack():
    msg = messagebox.showinfo( "Coming Soon", "This feature has not been built yet")
    
def makeit():
    
    random_seed_input = random_seed.get()
    sector_name_input = sector_name.get()
    density_input = density.get()
    lumiii_input = lumiii.get()
    lumv_input = lumv.get()
    spectrala_input = spectrala.get()
    spectralf_input = spectralf.get()
    spectralg_input = spectralg.get()
    spectralk_input = spectralk.get()
    solo_input = solo.get()
    binary_input = binary.get()
    distant_input = distant.get()
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
    print(makeit_list)
    make_sector_master(makeit_list)

def create_menus():    
    # create a toplevel menu
    menubar = Menu(top)

    # create a pulldown menu, and add it to the menu bar
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=helloCallBack)
    filemenu.add_command(label="Save", command=helloCallBack)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=top.destroy)
    menubar.add_cascade(label="File", menu=filemenu)

    # create more pulldown menus
    dbmenu = Menu(menubar, tearoff=0)
    dbmenu.add_command(label="Build a New Dataset", command=helloCallBack)
    dbmenu.add_command(label="Browse a Dataset", command=helloCallBack)
    dbmenu.add_command(label="Analyze a Dataset", command=helloCallBack)
    menubar.add_cascade(label="Dataset", menu=dbmenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=helloCallBack)
    menubar.add_cascade(label="Help", menu=helpmenu)
       

    # display the menu
    top.config(menu=menubar)
    

    
#Labels
Label (top,text="Traveller Sector Creator", font = 'Helvetica 18 bold').grid(row = 1, column=0,columnspan=3)
Label (top,text="Paramater Options", font="bold",relief = SUNKEN).grid(row = 2, column=0)
Label (top,text="Notes and Explanation", font="bold",relief = SUNKEN).grid(row = 2, column=2)

Label (top,text="System Density:").grid(row = 3, column=0)
Label (top,text="1d6 >= # results in a system present").grid(row = 3, column=2, sticky=W)

Label (top,text="Luminosity Class III setting:").grid(row = 4, column=0)
Label (top,text="3d6 <= # results in a Lum Class III.  This # must be less than Class V setting").grid(row = 4, column=2, sticky=W)

Label (top,text="Luminosity Class V setting:").grid(row = 5, column=0)
Label (top,text="3d6 <= # results in a Lum Class V.  This # must be higher than Class III setting").grid(row = 5, column=2, sticky=W)    


Label (top,text="Spectral Class A setting:").grid(row = 6, column=0)
Label (top,text="3d6 <= # results in a Spec Class A star.  This # must be the smallest of the Spec Class numbers").grid(row = 6, column=2, sticky=W)

Label (top,text="Spectral Class F setting:").grid(row = 7, column=0)
Label (top,text="3d6 <= # results in a Spec Class F star.  This # must be the second smallest of the Spec Class numbers").grid(row = 7, column=2, sticky=W)

Label (top,text="Spectral Class G setting:").grid(row = 8, column=0)
Label (top,text="3d6 <= # results in a Spec Class G star.  This # must be the second highest of the Spec Class numbers").grid(row = 8, column=2, sticky=W)

Label (top,text="Spectral Class K setting:").grid(row = 9, column=0)  
Label (top,text="3d6 <= # results in a Spec Class K star.  This # must be the second highest of the Spec Class numbers").grid(row = 9, column=2, sticky=W)    

Label (top,text="Solo system setting:").grid(row = 10, column=0)      
Label (top,text="3d6 <= # results in a solo star system.  This # must be less than the Binary Setting").grid(row = 10, column=2, sticky=W)

Label (top,text="Binary system setting:").grid(row = 11, column=0)  
Label (top,text="3d6 <= # results in a binary star system.  This # must be higher than the Binary Setting").grid(row = 11, column=2, sticky=W)    

Label (top,text="Distant star with a companion:").grid(row = 12, column=0)  
Label (top,text="3d6 >= # results in the distant star having a companion.  This will be marked with a * in the DB").grid(row = 12, column=2, sticky=W)

Label (top,text="Name of Sector:").grid(row = 13, column=0)   
Label (top,text="DB and txt file will be stored in the same directory as the program.  Will overwrite similar names").grid(row = 14, column=2, sticky=W)  

Label (top,text="Random Seed:").grid(row = 15, column=0)   
Label (top,text="Using the same seed with the same parameters will produce the same sector").grid(row = 15, column=2, sticky=W)  

#Text Entry
density = Entry(top, width = 2)
density.grid(row = 3, column = 1, sticky=W)
density.insert(0,'05')

lumiii = Entry(top, width = 2)
lumiii.grid(row = 4, column = 1, sticky=W)
lumiii.insert(0,'03') 

lumv = Entry(top, width = 2)
lumv.grid(row = 5, column = 1, sticky=W)
lumv.insert(0,'14')  

spectrala = Entry(top, width = 2)
spectrala.grid(row = 6, column = 1, sticky=W)
spectrala.insert(0,'04')      

spectralf = Entry(top, width = 2)
spectralf.grid(row = 7, column = 1, sticky=W)
spectralf.insert(0,'06')     

spectralg = Entry(top, width = 2)
spectralg.grid(row = 8, column = 1, sticky=W)
spectralg.insert(0,'08')  

spectralk = Entry(top, width = 2)
spectralk.grid(row = 9, column = 1, sticky=W)
spectralk.insert(0,'10')  

solo = Entry(top, width = 2)
solo.grid(row = 10, column = 1, sticky=W)
solo.insert(0,'13')  

binary = Entry(top, width = 2)
binary.grid(row = 11, column = 1, sticky=W)
binary.insert(0,'17') 

distant = Entry(top, width = 2)
distant.grid(row = 12, column = 1, sticky=W)
distant.insert(0,'11') 

sector_name = Entry(top, width = 20)
sector_name.grid(row = 13, column = 1, columnspan=2,sticky=W)
sector_name.insert(0,'test_sector') 


random_seed = Entry(top, width = 5)
random_seed.grid(row = 15, column = 1, columnspan=1,sticky=W)
random_seed.insert(0,'66') 


build_button = Button(top, text="Build the Sector", command = makeit, relief = RAISED)
build_button.grid(row = 20, column = 0, ipadx = 10, padx = 10, ipady = 5, pady = 5)   
exit_button = Button(top, text="Exit", command = top.destroy, relief = RAISED)
exit_button.grid(row = 20, column = 2, ipadx = 10, padx = 2, ipady = 5, pady = 5)      


   

top.mainloop()