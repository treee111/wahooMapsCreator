#!/usr/bin/python
#-*- coding:utf-8 -*-

import getopt
import glob
import json
import multiprocessing
import os
import os.path
import requests
import subprocess
import sys
import time

# for gui
import tkinter as tk
from tkinter import ttk
from tkinter import *

# ToDo: This might not work - Properly import in Windows!
# import custom python packages
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from common_resources import file_directory_functions
from common_resources import osm_maps_functions
from common_resources import constants
from common_resources.osm_maps_functions import OSM_Maps

########### Configurable Parameters

# Maximum age of source maps or land shape files before they are redownloaded
Max_Days_Old = 14

# Force (re)processing of source maps and the land shape file
# If 0 use Max_Days_Old to check for expired maps
# If 1 force redownloading/processing of maps and landshape 
Force_Processing = 0

# Save uncompressed maps for Cruiser
Save_Cruiser = 0

# Number of threads to use in the mapwriter plug-in
threads = str(multiprocessing.cpu_count() - 1)
if int(threads) < 1:
    threads = 1
# Or set it manually to:
#threads = 1
#print(f'threads = {threads}/n')

# Number of workers for the Osmosis read binary fast function
workers = '1'

########### End of Configurable Parameters

# GUI

def create_map():
    global country_gui
    global region_gui
    region_gui = cboContinent.get().replace("-", "")
    country_gui = cboCountry.get()
    app.destroy()


def callback_continent(event):
    continent = cboContinent.get()
    cboCountry["values"] = eval(continent.replace("-", ""))
    cboCountry.current(0)
    if continent == "europe":
        cboCountry.current(14)


def switch_reload():
    if fp.get() == 0:
        enMaxOldDays.configure(state=NORMAL)
    else:
        enMaxOldDays.configure(state=DISABLED)


app = tk.Tk()
app.geometry("420x360")
app.title("Wahoo map creator")
app.option_add("*Font", "Calibri 16")
country_gui = "none"
region_gui = "none"

app.grid_rowconfigure(3, minsize=30)
app.grid_rowconfigure(6, minsize=10)
app.grid_rowconfigure(8, minsize=10)

labTop = tk.Label(app, text="Select continent and country to create a map")
labContinent = tk.Label(app, text="Select continent:")
labCountry = tk.Label(app, text='Select country:')
labMaxOld = tk.Label(app, text='Max Old Days:')

labTop.grid(column=0, row=0, columnspan=2, sticky=E, padx=5, pady=10)
labContinent.grid(column=0, row=1, sticky=E, padx=5, pady=2)
labCountry.grid(column=0, row=2, sticky=NE, padx=5, pady=2)
labMaxOld.grid(column=0, row=4, sticky=SE, padx=5)

cboContinent = ttk.Combobox(app, values=constants.continents, state="readonly", width=15)
cboCountry = ttk.Combobox(app, values=constants.europe, state="readonly", width=15)
cboContinent.grid(column=1, row=1, sticky=W, padx=10, pady=2)
cboCountry.grid(column=1, row=2, sticky=NW, padx=10, pady=2)
cboContinent.current(0)
cboCountry.current(14)
cboContinent.bind("<<ComboboxSelected>>", callback_continent)

fp = IntVar()
fp.set(Force_Processing)
maxdays = StringVar()
maxdays.set(str(Max_Days_Old))
save_cruiser_maps = IntVar()
save_cruiser_maps.set(Save_Cruiser)
enMaxOldDays = tk.Entry(app, textvar=maxdays, width=5)
enMaxOldDays.grid(column=1, row=4, sticky=SW, padx=10)
chkReloadMaps = Checkbutton(app, text="Force reload maps", var=fp, command=switch_reload)
chkReloadMaps.grid(column=1, row=5, sticky=NW, padx=5)
chkSaveCruiser = Checkbutton(app, text="Save uncompressed maps for Cruiser", var=save_cruiser_maps, command=switch_reload)
chkSaveCruiser.grid(columnspan=2, column=0, row=7, sticky=S, pady=5)

btnOK = tk.Button(app, text="Create map", width=15, command=create_map).grid(column=0, row=9, padx=15, pady=10)
btnCancel = tk.Button(app, text="Exit", width=15, command=app.destroy).grid(column=1, row=9, padx=10, pady=10)

switch_reload()
app.mainloop()  # show gui

Force_Processing = fp.get()
Save_Cruiser = save_cruiser_maps.get()
Max_Days_Old = int(maxdays.get())

print('# Force Processing = ' + str(Force_Processing))
print('# Max Days Old = ' + str(Max_Days_Old))
print('# Save Cruiser maps = ' + str(Save_Cruiser))
print(f"# GUI exits with {country_gui} in {region_gui}")
if country_gui == "none":
    sys.exit()

# End of GUI



# if len(sys.argv) != 2:
#     print(f'Usage: {sys.argv[0]} Country name part of a .json file.')
#     sys.exit()

x = OSM_Maps(country_gui, Max_Days_Old, Force_Processing, workers, threads, Save_Cruiser)

# if x.region == '' :
#     print ('Invalid country name.')
#     sys.exit()

# Read json file
x.readJsonFile()

# Check for expired land polygons file and download, if too old
# osm_maps_functions.checkAndDownloadLandPoligonsFile(Max_Days_Old, Force_Processing)
x.checkAndDownloadLandPoligonsFile()

# Check for expired .osm.pbf files and download, if too old
# osm_maps_functions.checkAndDownloadOsmPbfFile(country, Max_Days_Old, Force_Processing)
x.checkAndDownloadOsmPbfFile()

# Filter tags from country osm.pbf files'
x.filterTagsFromCountryOsmPbfFiles()

# Generate land
x.generateLand()

# Generate sea
x.generateSea()

# Split filtered country files to tiles
x.splitFilteredCountryFilesToTiles()

# Merge splitted tiles with land an sea   
x.mergeSplittedTilesWithLandAndSea()

# Creating .map files
x.createMapFiles()

# Zip .map.lzma files
x.zipMapFiles()

# Make Cruiser map files zip file
x.makeCruiserFiles()