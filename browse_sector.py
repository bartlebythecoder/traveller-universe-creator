# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 23:19:42 2021

v 1.0.1a  2024-04-27  Fixed Full System bug when button pressed twice in a row
v 1.1.0   2024-04-27  API connections to traveller maps
v 1.1.0a  2024-04-28  Fixed error when clicking Full System without mainworld selected
v 1.1.0b  2024-05-04  1. Fixed another error when clicking Full System without mainworld selected
                      2. Added confirmation windows for traveller map buttons  
v 1.1.0c  2024-05-05  Added ring information for each orbital body          
v 1.1.0d  2024-05-11  Moved remarks list to traveller_functions    
v 1.1.0e  2024-05-24  Added error variables to debug log in try/excepts
v 1.1.0f  2024-05-28  Fixed ring popup, and changed jump distance from Mm to MKm.
v 1.2.0a  2024-05-29  Used new get_importance()
                      Changed High and Low Gravity to match Mongoose definition (.7 and 1.4)
                      Cleaned add_images and update_stats functions
                      Added classes for PlanetInfo, ColumnLabels, Tooltips
"""

import io
import logging
import os
import platform
import sqlite3
import warnings
import webbrowser

import FreeSimpleGUI as sg
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from dataclasses import dataclass

from PIL import Image, ImageTk
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from traveller_functions import Api_image_parameters, download_image_via_api
from traveller_functions import tohex, get_description, get_remarks_list, get_importance
from export_sector import export_sector

try:
    import pyi_splash

    # Update the text on the splash screen
    pyi_splash.update_text("Processing...")

    # Close the splash screen. It does not matter when the call
    # to this function is made, the splash screen remains open until
    # this function is called or the Python program is terminated.
    pyi_splash.close()

except:
    logging.debug('Skipped Splash - Running locally')

# ------------------------------------------------------------------------------
# Prepare Logging
# ------------------------------------------------------------------------------

#Used to reset logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

#used to disable tkinter stream messages
pil_logger = logging.getLogger('PIL')
pil_logger.setLevel(logging.INFO)

logging.getLogger('PIL').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s ')
logging.getLogger('matplotlib').setLevel(logging.ERROR)
logging.debug('Program Starts')

warnings.simplefilter(action='ignore')  #

###############################

matplotlib.use('TkAgg')
sg.theme('DarkBlue')


# ------------------------------------------------------------------------------
# use PIL to read data of one image
# ------------------------------------------------------------------------------

@dataclass
class PlanetInfo:
    detail_info: pd.DataFrame
    loc_info: pd.DataFrame
    system_info: pd.DataFrame
    economic_info: pd.DataFrame


@dataclass
class ColumnLabels:
    main_labels: list
    detail_labels: list
    system_labels: list
    economic_labels: list


@dataclass
class ToolTips:
    detail_tooltips: list
    system_tooltips: list
    economic_tooltips: list


def get_img_data(f, maxsize=(1200, 850), first=False):
    """Generate image data using PIL
    """
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:  # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)


# ------------------------------------------------------------------------------


def clear_images(list_images: list):
    for li in list_images:
        window[li[0]].hide_row()


def add_image(image_var: str):
    window[image_var].unhide_row()


def select_detail_info_images(detail_info):
    if list(detail_info['gravity'])[0] >= 1.4:
        add_image('heavy')
    elif list(detail_info['gravity'])[0] <= 0.7:
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
    if list(detail_info['stellar_mask'])[0] == 'total': add_image('mask')


def select_loc_info_images(loc_info):
    if list(loc_info['atmosphere'])[0] == 0:
        add_image('vacuum')
    if list(loc_info['size'])[0] == 0:
        add_image('asteroid')


def select_system_info_images(system_info):
    importance = get_importance(list(system_info['ix'])[0])
    if importance >= 4: add_image('important')

    bases = list(system_info['bases'])[0]
    if 'N' in bases or 'B' in bases:
        add_image('naval')
    if 'S' in bases or 'B' in bases:
        add_image('scout')

    remarks_list = get_remarks_list()
    for rem in remarks_list:
        if rem[0] in list(system_info['remarks'])[0]: add_image(rem[1])


def select_economic_info_images(economic_info):
    gwp = list(economic_info['gwp'])[0]
    if int(gwp) >= 1_000_000: add_image('wealthy')


def select_all_images(planet_info):
    select_detail_info_images(planet_info.detail_info)
    select_loc_info_images(planet_info.loc_info)
    select_system_info_images(planet_info.system_info)
    select_economic_info_images(planet_info.economic_info)


def update_main_stats(planet_info, column_labels):
    for m in column_labels.main_labels:
        m_value = list(planet_info.loc_info[m])
        m_value = m_value[0]
        #                    logging.debug('Updating value ' + str(m_value))
        if m == 'starport':
            window[m + 'i'].TooltipObject.text = get_description('starport', m_value)
        elif m == 'size':
            m_value = tohex(m_value)
            window[m + 'i'].TooltipObject.text = get_description('size', m_value)
        elif m == 'atmosphere':
            m_value = tohex(m_value)
            window[m + 'i'].TooltipObject.text = get_description('atmosphere', m_value)
        elif m == 'government':
            m_value = tohex(m_value)
            window[m + 'i'].TooltipObject.text = get_description('government', m_value)
        elif m == 'law':
            m_value = tohex(m_value)
            window[m + 'i'].TooltipObject.text = get_description('law', m_value)
        elif m == 'tech_level':
            m_value = tohex(m_value)
            window[m + 'i'].TooltipObject.text = m_value
        else:
            window[m + 'i'].TooltipObject.text = m_value

        window[m + 'i'].update(m_value)


def update_system_stats(planet_info, column_labels):
    for s in column_labels.system_labels:
        s_value = list(planet_info.system_info[s])
        s_value = s_value[0]

        if s == 'remarks':
            window[s + 'i'].TooltipObject.text = get_description('remarks', s_value)
        else:
            window[s + 'i'].TooltipObject.text = s_value

            #  logging.debug('s_value during update: ' + s_value)
        window[s + 'i'].update(s_value)


def update_detail_stats(planet_info, column_labels):
    for d in column_labels.detail_labels:
        d_value = list(planet_info.detail_info[d])

        if d == 'mainworld_calc':
            d_value = f'{d_value[0]:,}'
        elif d == 'jump_point_distance':
            d_value = f'{d_value[0]:,}'
        else:
            d_value = d_value[0]

        window[d + 'i'].update(d_value)


def update_economic_stats(planet_info, column_labels):
    for e in column_labels.economic_labels:
        e_value = list(planet_info.economic_info[e])
        if e != "gwp":
            e_value = e_value[0]
        else:
            e_value = f'{e_value[0]:,}'
        window[e + 'i'].update(e_value)


def update_all_stats(planet_info, column_labels):
    update_main_stats(planet_info, column_labels)
    update_system_stats(planet_info, column_labels)
    update_detail_stats(planet_info, column_labels)
    update_economic_stats(planet_info, column_labels)


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close('all')


# ------------------------------------------------------------------------------
#  Matplotlib functions for sector map
# ------------------------------------------------------------------------------

def get_coordinates(thedataframe):
    xcoordinates = []
    ycoordinates = []

    coord_list = list(thedataframe['location'])

    for coord in coord_list:

        x_axis = int(coord[0:2])

        mod = x_axis % 2
        if mod > 0:
            top_y_limit = 41
        else:
            top_y_limit = 40.5
        y_axis = (top_y_limit - int(coord[2:4]))
        xcoordinates.append(x_axis)
        ycoordinates.append(y_axis)

    return (xcoordinates, ycoordinates)


def animate(chart_title, color_choice, plot_size, label_choice, *args):
    a.clear()
    a.set_xticks([])
    a.set_yticks([])
    xcoordinates = []
    ycoordinates = []

    for arg_num, arg in enumerate(args):

        color_choice_s = color_choice[arg_num]

        xcoordinates, ycoordinates = get_coordinates(arg)
        a.set_title(chart_title, color='white')
        a.scatter(xcoordinates, ycoordinates, c=color_choice_s, s=plot_size)

        if label_choice == "num":
            name_list = arg['location'].tolist()
        else:
            name_list = arg['system_name'].tolist()
        label_color = 'White'
        if len(name_list) <= 100:
            name_coords = list(zip(xcoordinates, ycoordinates))
            row_num = 0
            for each_item in name_coords:
                row_name = name_list[row_num]
                a.text(each_item[0] - 2, each_item[1], row_name, fontsize=10, color=label_color)
                row_num += 1

    f.tight_layout()
    f.canvas.draw_idle()


def draw_map():
    if values['-NUM-'] is True:

        label_choice = 'num'
    else:

        label_choice = 'name'

    if values['-FULL-'] is True:

        stell_colors = ['dimgray', 'Blue']
        plot_list = [30]
        animate(location_orb_name, stell_colors, plot_list, label_choice, df, loc_info)

    elif values['-EARTH-'] is True:

        df_special_earth = (df_details.query('type == "Ocean*"'))
        stell_colors = ['dimgray', 'Green']
        plot_list = [30]
        animate('Earth-like worlds', stell_colors, plot_list, label_choice, df, df_special_earth)

    else:

        df_special_belt = (df_details.query('type == "Belt"'))
        stell_colors = ['dimgray', 'Yellow']
        plot_list = [30]
        animate('Belts', stell_colors, plot_list, label_choice, df, df_special_belt)


# ------------------------------------------------------------------------------        
# PySimpleGUI Window Layout Functions
# ------------------------------------------------------------------------------

def win1_build_column_one(listbox_options):
    return [
        [sg.Text("SYSTEMS")],
        [sg.Listbox(listbox_options, enable_events=True, size=(25, 32), key=('-LOCATIONS-'))]
    ]


def win1_build_column_two():
    return [
        [sg.Text("UWP Categories")],
        [sg.HSeparator()],
    ]


def win1_build_column_three():
    return [
        [sg.Text("World Details")],
        [sg.HSeparator()],
    ]

def win1_build_column_four():
    return [
        [sg.Text("Scientific Categories")],
        [sg.HSeparator()],
    ]

def win1_build_column_five():
    return [
        [sg.Text("World Details")],
        [sg.HSeparator()],
    ]

def win1_build_all_columns(world_listbox):
    column_one = win1_build_column_one(world_listbox)
    column_two = win1_build_column_two()
    column_three = win1_build_column_three()
    column_four = win1_build_column_four()
    column_five = win1_build_column_five()
    return column_one, column_two, column_three, column_four, column_five


def win1_add_column_two_labels(column, labels_data):
    for m in labels_data.main_labels:
        logging.debug(f'label: {m}')
        column += [sg.Text(m + ':', enable_events=True, key=(m), pad=(0, 0))],
    return column


def win1_add_column_three_labels(column, labels_data):
    tooltip_info = 'Not set'
    for m in labels_data.main_labels:
        column += [sg.Text('|', enable_events=True, tooltip=tooltip_info, key=(m + 'i'), pad=(0, 0))],
    return column


def make_win1(labels_data, tooltips_data, listbox_options):

    column_one, column_two, column_three, column_four, column_five = win1_build_all_columns(listbox_options)

    column_two = win1_add_column_two_labels(column_two, labels_data)
    column_two += [[sg.Text("System Categories", pad=(5, (15, 2)))],
                   [sg.HSeparator()], ]



    column_three = win1_add_column_three_labels(column_three, labels_data)
    column_three += [[sg.Text("System-wide Details", pad=(5, (15, 2)))],
                     [sg.HSeparator()], ]

    for x, s in enumerate(labels_data.system_labels):

        remark_tt = 'Not set'
        column_two += [
            sg.Text(s + ':', enable_events=True, tooltip=tooltips_data.system_tooltips[x], key=(s), pad=(0, 0))],
        column_three += [sg.Text('|', enable_events=True, tooltip=remark_tt, key=(s + 'i'), pad=(0, 0))],








    for x, d in enumerate(column_labels.detail_labels):
        column_four += [
            sg.Text(d + ':', enable_events=True, tooltip=tooltips_data.detail_tooltips[x], key=(d), pad=(0, 0))],
        column_five += [sg.Text('|', enable_events=True, key=(d + 'i'), pad=(0, 0))],



    for x, e in enumerate(labels_data.economic_labels):
        column_four += [
            sg.Text(e + ':', enable_events=True, tooltip=tooltips_data.economic_tooltips[x], key=(e), pad=(0, 0))],
        column_five += [sg.Text('|', enable_events=True, key=(e + 'i'), pad=(0, 0))],

    map_options = [
        [sg.Radio('Show Selected', '-DISPLAY-', key=('-FULL-'), default=True, pad=(0, 0))],
        [sg.Radio('Find Earth Like', '-DISPLAY-', key=('-EARTH-'), pad=(0, 0))],
        [sg.Radio('Find Belts', '-DISPLAY-', key=('-IX-'), pad=(0, 0))],
    ]

    label_options = [
        [sg.Radio('Num', '-OVERLAY-', key=('-NUM-'), default=True, pad=(0, 0))],
        [sg.Radio('Name', '-OVERLAY-', key=('-NAME-'), pad=(0, 0))],
    ]

    column_six = [[sg.Canvas(key='-CANVAS-')],
                  [sg.Column(map_options),
                   sg.Column(label_options),
                   sg.Button('Map', key=('-MAP-'))],
                  ]

    image_layout = []
    for li in list_images:
        filename = os.path.join(folder, li[0] + '.png')
        image_layout += [sg.Image(data=get_img_data(filename, first=True),
                                  tooltip=li[1], enable_events=True, key=(li[0]))],

    layout = [
        [sg.Text("""Browse Window""")],
        [sg.HSeparator()],
        [
            sg.Text('Choose A Sector', size=(15, 1), auto_size_text=False, justification='right'),
            sg.In(size=(20, 1), enable_events=True, key=('-DB-'), justification='right'),
            sg.FileBrowse(file_types=(("Database Files", "*.db"),),
                          enable_events=True,
                          initial_folder=("sector_db")),
            sg.VSeparator(),
            sg.Button('Main World', key=('-MAIN-')),
            sg.Button('Full System', key=('-SYSTEM-')),
            sg.VSeparator(),
            sg.Button('Stellar', key=('-STELLAR-')),
            sg.Button('Culture', key=('-CULTURE-')),
            sg.Button('Trade', key=('-TRADE-')),
            sg.VSeparator(),
            sg.Button('World Map', key=('-WORLDMAP-')),
            sg.Button('Sector Map', key=('-TRAVELLERMAP-')),
            sg.VSeparator(),
            sg.Button('Sector PDF', key=('-EXPORT-')),
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
    return sg.Window("""Bartleby's Sector Builder v 1.1.0d""", layout, size=(1300, 700), finalize=True)


def make_win2(star_columns, star_list, location):
    try:

        star_column_one = []
        star_column_two = []
        star_column_three = []
        star_column_four = []
        star_width = 300

        for s_num, s in enumerate(star_list[0]):
            star_column_one += [sg.Text(star_columns[s_num] + ':')],
            star_column_two += [sg.Text(s)],

        if len(star_list) > 1:

            star_width = 350

            for s_num, s in enumerate(star_list[1]):
                star_column_three += [sg.Text(s)],

        if len(star_list) == 3:

            star_width = 400

            for s_num, s in enumerate(star_list[2]):
                star_column_four += [sg.Text(s)],

        star_layout = [
            [sg.Column(star_column_one), sg.Column(star_column_two),
             sg.Column(star_column_three), sg.Column(star_column_four)],
            [sg.Button('Exit')]
        ]
    except Exception as e:
        sg.Popup(f'Failed star layout {e}')

    return sg.Window('Stellar Details', star_layout, size=(star_width, 800), finalize=True)


def make_win3(culture_columns, culture_list, location):
    try:

        culture_column_one = []
        culture_column_two = []

        logging.debug('Entering Culture loop')
        logging.debug(culture_list)

        for s_num, s in enumerate(culture_list[0]):
            culture_column_one += [sg.Text(culture_columns[s_num] + ':')],
            culture_column_two += [sg.Text(s)],

        logging.debug('Setting new culture layout')
        logging.debug(type(culture_column_two))
        culture_layout = [
            [sg.Column(culture_column_one),
             sg.Column(culture_column_two)],

            [sg.Button('Exit')]
        ]
    except Exception as e:
        sg.Popup(f'Failed culture layout: {e}')

    return sg.Window('Perceived Cultural Details', culture_layout, size=(550, 500), finalize=True)


def make_win4(needs_list, wants_list, location):
    try:

        trade_column_one = [sg.Text('#')],
        trade_column_two = [sg.Text('GOODS NEEDED')],
        trade_column_three = [sg.Text('GOODS SURPLUS')],

        logging.debug('Entering Trade Goods loop')
        logging.debug(needs_list)

        for s_num, s in enumerate(needs_list):
            if s != ' ':
                trade_column_one += [sg.Text(str(s_num + 1) + ':')],
                trade_column_two += [sg.Text(s.lstrip())],

        for s_num, s in enumerate(wants_list):
            if s != ' ':
                trade_column_three += [sg.Text(s.lstrip())],

        logging.debug('Setting new trade layout')
        logging.debug(type(trade_column_two))
        goods_layout = [
            [sg.Column(trade_column_one),
             sg.Column(trade_column_two),
             sg.Column(trade_column_three)],
            [sg.Button('Exit')]
        ]
    except Exception as e:
        sg.Popup(f'Failed Trade Goods layout {e}')

    return sg.Window('Trade Goods, Frequently Needed and Surplus System Wide', goods_layout, size=(350, 250),
                     finalize=True)


def make_win5(db):
    logging.debug('Entered make_win5()')

    try:

        export_ss_layout = [

            [sg.Text("Subsector Letter")],
            [sg.Radio('A', "RADIO1", key='-A-', default=True),
             sg.Radio('B', "RADIO1", key='-B-'),
             sg.Radio('C', "RADIO1", key='-C-'),
             sg.Radio('D', "RADIO1", key='-D-')],
            [sg.Radio('E', "RADIO1", key='-E-', default=True),
             sg.Radio('F', "RADIO1", key='-F-'),
             sg.Radio('G', "RADIO1", key='-G-'),
             sg.Radio('H', "RADIO1", key='-H-')],
            [sg.Radio('I  ', "RADIO1", key='-I-', default=True),
             sg.Radio('J', "RADIO1", key='-J-'),
             sg.Radio('K', "RADIO1", key='-K-'),
             sg.Radio('L', "RADIO1", key='-L-')],
            [sg.Radio('M', "RADIO1", key='-M-', default=True),
             sg.Radio('N', "RADIO1", key='-N-'),
             sg.Radio('O', "RADIO1", key='-O-'),
             sg.Radio('P', "RADIO1", key='-P-')],
            [sg.Button('Generate'), sg.Button('Cancel')]

        ]

        logging.debug('Win 5 layout complete')

        # Event Loop to process "events" and get the "values" of the inputs
        window_5 = sg.Window('Choose a Subsector for Export', export_ss_layout, size=(550, 500), finalize=True)

        while True:

            export_event, export_values = window_5.read()
            if export_event == sg.WIN_CLOSED or export_event == 'Cancel':  # if user closes window or clicks cancel
                logging.debug('Window Closed')
                break

            else:
                logging.debug(f'Printing:  {export_values}')
                if export_values['-A-'] == True:
                    ss = 'A'
                elif export_values['-B-'] == True:
                    ss = 'B'
                elif export_values['-C-'] == True:
                    ss = 'C'
                elif export_values['-D-'] == True:
                    ss = 'D'
                elif export_values['-E-'] == True:
                    ss = 'E'
                elif export_values['-F-'] == True:
                    ss = 'F'
                elif export_values['-G-'] == True:
                    ss = 'G'
                elif export_values['-H-'] == True:
                    ss = 'H'
                elif export_values['-I-'] == True:
                    ss = 'I'
                elif export_values['-J-'] == True:
                    ss = 'J'
                elif export_values['-K-'] == True:
                    ss = 'K'
                elif export_values['-L-'] == True:
                    ss = 'L'
                elif export_values['-M-'] == True:
                    ss = 'M'
                elif export_values['-N-'] == True:
                    ss = 'N'
                elif export_values['-O-'] == True:
                    ss = 'O'
                elif export_values['-P-'] == True:
                    ss = 'P'

                else:
                    ss = 'A'

                logging.debug(f'SS value =  {ss}')

                export_sector(db, ss)
                break

        window_5.close()


    except Exception as e:
        sg.Popup(f'Failed export layout {e}')


def confirm_window(message_text):
    """
    Creates a confirmation window with "Continue" and "Cancel" buttons.
    Returns True if "Continue" is pressed, False otherwise.
    Provide message text to the function.
    """
    layout = [
        [sg.Text(message_text)],
        [sg.Button("Continue"), sg.Button("Cancel")]
    ]

    window = sg.Window("Confirmation", layout)
    event, values = window.read()
    window.close()

    return event == "Continue"


# Open an image using the system's default application (Windows only)
def open_image(pgn_name):
    if platform.system() == "Windows":  # Windows specific
        logging.debug("Platform is windows - opening file")
        os.startfile(png_name)
    else:  # Attempt to use a generic approach for other OSes (might require additional libraries)
        logging.debug("Platform is not windows - file is saved")


# ------------------------------- MATPLOTLIB CODE HERE -------------------------------

f = Figure(figsize=(4, 5), dpi=100)

style.use("dark_background")
a = f.add_subplot(111)

a.clear()
a.set_xticks([])
a.set_yticks([])
xcoordinates = []
ycoordinates = []
location = '-99'
detail_flag = 'main_world'  # flag used to mark whether the details should be main world or exo worlds.

folder = 'images/'

# PIL supported image types
img_types = (".png", ".jpg", "jpeg", ".tiff", ".bmp")

# get list of files in folder
flist0 = os.listdir(folder)

# create sub list of image files (no sub folders, no wrong file types)
fnames = [f for f in flist0 if os.path.isfile(

    os.path.join(folder, f)) and f.lower().endswith(img_types)]

option_list = []

db_name = 'sector_db/example-66.db'

list_images = [['mask', 'Completely Stellar Masked'],
               ['ocean', 'Ocean or Earth-like World'],
               ['exotic', 'Exotic Atmosphire'],
               ['corrosive', 'Corrosive Atmosphire'],
               ['vacuum', 'Vacuum World'],
               ['asteroid', 'Object is Planetary Belt'],
               ['light', 'Low Gravity World'],
               ['heavy', 'High Gravity World'],
               ['hot', 'Unhinhabitable Heat'],
               ['cold', 'Uninhabitable Cold'],
               ['hipop', 'High Population System'],
               ['lopop', 'Lo Population System'],
               ['barren', 'No Population in System'],
               ['wealthy', 'Wealthy System'],
               ['industrial', 'Industrial Economy'],
               ['non_industrial', 'Non-industrial Economy'],
               ['agricultural', 'Agricultural Economy'],
               ['non_agricultural', 'Non-agricultural Economy'],
               ['important', 'Important System'],
               ['naval', 'Naval Base Present'],
               ['scout', 'Scout Base Present'],
               ['prison', 'Interplanetary Prison Present'],
               ['moon', 'Object is a moon'],
               ['gas giant', 'Object is a gas giant']

               ]

conn = sqlite3.connect(db_name)
c = conn.cursor()

new_main_query = '''SELECT *
FROM traveller_stats    
WHERE main_world = 1'''

df_new_main = pd.read_sql_query(new_main_query, conn)

main_labels = []
main_labels = list(df_new_main.columns)

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
try:
    df_system_main = pd.read_sql_query(system_main_query, conn)
except Exception as e:
    logging.debug(f'Exception occured: {e}')

system_labels = []
system_labels = list(df_system_main.columns)
system_labels.remove('location')
system_tooltips = ['T5 Trade Classifications',
                   'T5 Importance',
                   'T5 Economic (Res, Lab, Infr, Eff)',
                   'T5 Culture (Het, Acc, Str, Sym)',
                   'T5 Nobility Present',
                   'T5 Bases',
                   'T5 Travel Zone',
                   'Pop sig digit, Belts, Gas Giants (primary star only)',
                   'Worlds',
                   'Allegiance',
                   'Stellar summary']

new_detail_sql_query = '''SELECT t.system_name, t.location, o.body, o.wtype as type, o.day, o.year,
o.gravity, o.atmos_pressure, o.atmos_composition, o.temperature, o.climate, 
o.impact_moons, o.natural_moons, ring,
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
try:
    df_details = pd.read_sql_query(new_detail_sql_query, conn)

except Exception as e:
    logging.debug(f'DB Exception occured: {e}')

detail_labels = []
detail_labels = list(df_details.columns)
detail_labels.remove('location')
detail_labels.remove('system_name')
detail_tooltips = ['Planet, Impact Moon, Natural Moon',
                   'World Type (GURPS First In, * indicates liquid Ocean)',
                   'Rotation Period (in hours)',
                   'Stellar Orbital Period (in Earth years)',
                   'in standard Gs',
                   'in relation to Earth',
                   'from GURPS First In',
                   'in Kelvin',
                   'from GURPS First In',
                   'from Architect of Worlds',
                   'from Architect of Worlds',
                   'ring around planet',
                   'in AUs',
                   'in Mega Kilometers (millions of km)',
                   'Stellar gravity impact to jump distance',
                   'Time to jump point (in hours) with 1G ship',
                   'Time to jump point (in hours) with 2G ship',
                   'Time to jump point (in hours) with 3G ship',
                   'Time to jump point (in hours) with 4G ship',
                   'Time to jump point (in hours) with 5G ship',
                   'Time to jump point (in hours) with 6G ship',
                   'Mainworld suitability result',
                   'test',
                   'test'
                   ]

economic_sql_query = '''SELECT * FROM far_trader'''
try:
    df_economic = pd.read_sql_query(economic_sql_query, conn)
except Exception as e:
    logging.debug(f'DB Exception occured: {e}')

economic_labels = []
economic_labels = list(df_economic.columns)
economic_labels.remove('location')
economic_labels.remove('id')
economic_labels.remove('needs')
economic_labels.remove('wants')
economic_tooltips = ['World Trade Number (GURPS Far Trader)',
                     'Gross World Product in MCr (GURPS Far Trader)',
                     'Exchange Rate (JTAS 4)']

column_labels = ColumnLabels(main_labels, detail_labels, system_labels, economic_labels)
tooltips = ToolTips(detail_tooltips, system_tooltips, economic_tooltips)

# ------------------------------------------------------------------------------
# Create the Window
# ------------------------------------------------------------------------------


window1, window2, window3, window4 = make_win1(column_labels, tooltips,
                                               option_list), None, None, None  # start off with 1 window open

# Event Loop to process "events" and get the "values" of the inputs


fig_canvas_agg = None

while True:
    window, event, values = sg.read_all_windows()

    if event == sg.WIN_CLOSED or event == 'Exit':
        window.close()
        if window == window2:  # if closing win 2, mark as closed
            window2 = None
        if window == window3:  # if closing win 3, mark as closed
            window3 = None
        if window == window4:  # if closing win 3, mark as closed
            window4 = None
        elif window == window1:  # if closing win 1, exit program
            break

    if event == '-DB-':

        db_name = values['-DB-']

        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        df = pd.read_sql_query(new_main_query, conn)

        try:

            df_system = pd.read_sql_query(system_main_query, conn)
            df_stellar = pd.read_sql_query('SELECT * FROM stellar_bodies', conn)
            df_culture = pd.read_sql_query('SELECT * FROM perceived_culture', conn)
            df_details = pd.read_sql_query(new_detail_sql_query, conn)



        except Exception as e:
            logging.debug(f'DB Exception occured: {e}')

        df_details['atmos_pressure'] = round(df_details['atmos_pressure'], 2)
        df_details['jump_point_distance'] = round(df_details['jump_point_distance'] / 1000, 2)  #convert to MKm
        df_details['mainworld_calc'] = round(df_details['mainworld_calc'], 2)

        try:
            df_economic = pd.read_sql_query(economic_sql_query, conn)
            df_economic['exchange'] = round(df_economic['exchange'], 2)  # otherwise crazy decimals added
        except Exception as e:
            logging.debug(f'DB Exception occured: {e}')

        exo_sql_query = '''SELECT t.*,
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

        try:
            df_exo = pd.read_sql_query(exo_sql_query, conn)
        except Exception as e:
            logging.debug(f'DB Exception occured: {e}')

        exo_detail_sql_query = '''SELECT t.system_name, t.location, t.location_orb, 
        o.body, o.wtype as type, o.day, o.year,
        o.gravity, o.atmos_pressure, o.atmos_composition, o.temperature, o.climate, 
        o.impact_moons, o.natural_moons, ring,
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

        try:
            df_exo_details = pd.read_sql_query(exo_detail_sql_query, conn)
        except Exception as e:
            logging.debug(f'DB Exception occured: {e}')

        df_exo_details['atmos_pressure'] = round(df_exo_details['atmos_pressure'], 2)
        df_exo_details['jump_point_distance'] = round(df_exo_details['jump_point_distance'] / 1000, 2)
        df_exo_details['mainworld_calc'] = round(df_exo_details['mainworld_calc'], 2)

        df['loc_name'] = df['location'] + '-' + df['system_name']
        df_details['loc_name'] = df_details['location'] + '-' + df_details['system_name']
        option_list = list(df['loc_name'])
        window['-LOCATIONS-'].update(option_list)

        if fig_canvas_agg:
            # ** IMPORTANT ** Clean up previous drawing before drawing again
            delete_figure_agg(fig_canvas_agg)

    if event == '-MAIN-':
        detail_flag = 'main_world'

        window['-LOCATIONS-'].update(option_list)


    elif event == '-LOCATIONS-':
        try:

            location = values['-LOCATIONS-'][0][0:4]

            if detail_flag == 'main_world':

                location_orb_name = values['-LOCATIONS-'][0]

                detail_info = df_details[df_details['location'] == location]
                loc_info = df.loc[df['location'] == location]
                system_info = df_system.loc[df_system['location'] == location]
                economic_info = df_economic[df_economic['location'] == location]
                planet_info = PlanetInfo(detail_info, loc_info, system_info, economic_info)

                update_all_stats(planet_info, column_labels)

                try:
                    clear_images(list_images)
                    select_all_images(planet_info)

                except Exception as e:
                    sg.Popup(f'Failed during Main world image creation {e}')

            else:

                location_orb_name = values['-LOCATIONS-'][0]

                try:
                    detail_info = df_exo_details[df_exo_details['location_orb'] == location_orb_name]
                    loc_info = df_exo.loc[df_exo['location_orb'] == location_orb_name]
                    system_info = df_system.loc[df_system['location'] == location]
                    economic_info = df_economic[df_economic['location'] == location]
                    planet_info = PlanetInfo(detail_info, loc_info, system_info, economic_info)
                except Exception as e:
                    sg.Popup(f'Loc Info fail in Exo assignments {e}')

                try:
                    update_all_stats(planet_info, column_labels)

                except Exception as e:
                    sg.Popup(f'for loops failed in Exo Assignments {e}')

                try:

                    clear_images(list_images)
                    select_all_images(planet_info)


                except Exception as e:
                    sg.Popup(f'Failed during non-mainworld Image creation {e}')

            try:

                if fig_canvas_agg:
                    # ** IMPORTANT ** Clean up previous drawing before drawing again
                    delete_figure_agg(fig_canvas_agg)

                draw_map()

                fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, f)

            except Exception as e:
                logging.debug(e)
                logging.debug(f'Failed Map button {e}')


        except Exception as e:
            print(e)
            sg.popup(f'Error in LOCATION: {detail_flag} {e}')

    elif event == '-STELLAR-' and not window2:
        try:
            logging.debug('pressed STELLAR')

            star_list = []
            df_star = df_stellar.loc[df_stellar['location'] == location]
            star_columns = list(df_star.columns)
            for s in range(0, df_star.shape[0]):
                row = ''
                row = df_star.iloc[s]
                star_list.append(row)
            window2 = make_win2(star_columns, star_list, location)


        except Exception as e:
            logging.debug(f'Failed Stellar button {e}')

    elif event == '-CULTURE-' and not window3:
        try:
            logging.debug('pressed Culture')

            culture_list = []
            df_this_culture = df_culture.loc[df_culture['location'] == location]
            culture_columns = list(df_this_culture.columns)
            for s in range(0, df_this_culture.shape[0]):
                row = ''
                row = df_this_culture.iloc[s]
                culture_list.append(row)
            window3 = make_win3(culture_columns, culture_list, location)


        except Exception as e:
            logging.debug(f'Failed Culture button {e}')

    elif event == '-TRADE-' and not window3:
        try:
            logging.debug('pressed Trade ' + location)
            conn = sqlite3.connect(db_name)
            c = conn.cursor()
            sql_command = "SELECT needs, wants FROM far_trader WHERE location = " + "'" + location + "'"
            c.execute(sql_command)
            logging.debug('running: ' + sql_command)
            row = c.fetchall()
            logging.debug('Far Trader select complete ')
            logging.debug(row)

            needs_list = []
            wants_list = []

            needs_text = row[0][0]
            wants_text = row[0][1]

            logging.debug('Needs list:' + needs_text)
            logging.debug('Wants list:' + wants_text)

            needs_list = needs_text.split(';')
            wants_list = wants_text.split(';')

            window4 = make_win4(needs_list, wants_list, location)

        except Exception as e:
            logging.debug(e)
            logging.debug(f'Failed Trade button {e}')

    elif event == '-SYSTEM-':
        if detail_flag == 'main_world' and location is not None and location != '-99':
            try:
                logging.debug(
                    'pressed SYSTEM with location: ' + location + '.  --LOCATIONS--' + values['-LOCATIONS-'][0])
                detail_flag = 'exo_world'

                loc_info = df_exo.loc[df_exo['location_orb'] == location_orb_name]
                detail_info = df_exo_details[df_exo_details['location_orb'] == location_orb_name]
                economic_info = df_economic[df_economic['location'] == location]

                exo_location_orb_name = values['-LOCATIONS-'][0]
                exo_location = values['-LOCATIONS-'][0][0:4]

                exo_loc_info = df_exo.loc[df_exo['location'] == location]
                exo_detail_info = df_details[df_details['location'] == location]

                economic_info = df_economic[df_economic['location'] == location]
                economic_info['exchange'] = round(economic_info['exchange'], 2)  # otherwise crazy decimals added

                exo_loc_info['loc_name'] = exo_loc_info['location_orb']

                exo_list = list(exo_loc_info['loc_name'])
                exo_list.sort()
                window['-LOCATIONS-'].update(exo_list)

            except Exception as e:
                logging.debug(f'Full system chosen but no mainworld selected {e}')
        else:
            logging.debug('Full system chosen but no mainworld selected (else statement)')

    elif event == '-MAP-':
        try:
            if fig_canvas_agg:
                # ** IMPORTANT ** Clean up previous drawing before drawing again
                delete_figure_agg(fig_canvas_agg)

            draw_map()

            fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, f)

        except Exception as e:
            # Access the error message using e.args or str(e)
            logging.debug(f"Error: {e}")  # Example usage
            logging.debug('Failed draw_map()')

    elif event == '-WORLDMAP-':

        if confirm_window('Would you like me to open a web page with a world map?'):

            logging.debug('confirmed world map')
            try:
                logging.debug('pressed World Map ' + location)
                logging.debug('location_orb_name: ' + location_orb_name)
                main_url = 'https://www.travellerworlds.com/?'

                # UWP
                url_name = loc_info.iloc[0]['system_name']
                url_hex = location
                hex_starport = loc_info.iloc[0]['starport']
                hex_size = tohex(loc_info.iloc[0]['size'])
                hex_atmo = tohex(loc_info.iloc[0]['atmosphere'])
                hex_hydro = tohex(loc_info.iloc[0]['hydrographics'])
                hex_pop = tohex(loc_info.iloc[0]['population'])
                hex_gov = tohex(loc_info.iloc[0]['government'])
                hex_law = tohex(loc_info.iloc[0]['law'])
                hex_tech = tohex(loc_info.iloc[0]['tech_level'])

                # T5 numbers
                map_ix = system_info.iloc[0]['ix']
                map_ex = system_info.iloc[0]['ex']
                map_cx = system_info.iloc[0]['cx']
                map_pbg = system_info.iloc[0]['pbg']
                map_worlds = system_info.iloc[0]['w']
                map_bases = system_info.iloc[0]['bases']
                map_zone = system_info.iloc[0]['zone']
                map_nobz = system_info.iloc[0]['n']
                map_stars = system_info.iloc[0]['stars']

                logging.debug('Mapping URL')
                url_uwp = hex_starport + hex_size + hex_atmo + hex_hydro + hex_pop + hex_gov + hex_law + '-' + hex_tech
                url = main_url + 'name=' + url_name + '&uwp=' + url_uwp + '&hex=' + location
                url += '&system=' + location_orb_name + '&seed=' + location_orb_name
                url += '&eiX=' + map_ix + '&eX=' + map_ex + '&cX=' + map_cx
                url += '&pbg=' + map_pbg + '&worlds=' + map_worlds + '&bases' + map_bases
                url += '&travelZone=' + map_zone + '&nobz=' + map_nobz + '&stellar=' + map_stars

                logging.debug('url: ' + url)
                webbrowser.open(url)

            except Exception as e:
                logging.debug(f'World Map info not available {e}')

        else:
            logging.debug('cancelled world map')

    elif event == '-TRAVELLERMAP-':
        if confirm_window('Would you like me to download the sector map image from travellermap.com?'):

            logging.debug('confirmed sector map')

            tab = db_name + '_tab.txt'
            routes = db_name + '_routes.txt'
            url = "https://travellermap.com/api/poster?style=print"
            files = {
                'file': tab,
                'metadata': routes
            }
            png_name = db_name + '_sector_map.png'

            api_parm_object = Api_image_parameters(url, files, png_name)

            download_image_via_api(api_parm_object)
            sg.Popup('Map file saved to sector directory')

            open_image(png_name)



        else:
            logging.debug('cancelled sector map')

    elif event == '-EXPORT-':
        try:
            logging.debug('Calling win 5')
            window5 = make_win5(db_name)




        except Exception as e:
            # Access the error message using e.args or str(e)
            logging.debug(f"Error: {e}")  # Example usage
            logging.debug('Export failed')

conn.commit()
c.close()
conn.close()
logging.debug('Program closed')
window.close()
