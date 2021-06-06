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

# ToDo: This might not work - Properly import in Windows!
# import custom python packages
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from common_resources import file_directory_functions
from common_resources import osm_maps_functions
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

CurDir = os.getcwd() # Current Directory

MAP_PATH = os.path.join (CurDir, 'Maps')
OUT_PATH = os.path.join (CurDir, 'Output')
land_polygons_file = os.path.join (CurDir, 'land-polygons-split-4326', 'land_polygons.shp')
url = ''

# Tags to keep
filtered_tags = 'access= admin_level= aerialway= aeroway= barrier= boundary= bridge= highway= natural= oneway= place= railway= tracktype= tunnel= waterway='



if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} Country name part of a .json file.')
    sys.exit()

x = OSM_Maps(sys.argv[1], Max_Days_Old, Force_Processing, workers, threads, Save_Cruiser)

if x.region == '' :
    print ('Invalid country name.')
    sys.exit()

print('\n\n# read json file')
with open(os.path.join ('json', region, sys.argv[1] + '.json')) as f:
    country = json.load(f)
f.close()
if country == '' :
    print ('json file could not be opened.')
    sys.exit()

# Check for expired land polygons file and download, if too old
# osm_maps_functions.checkAndDownloadLandPoligonsFile(Max_Days_Old, Force_Processing)
x.checkAndDownloadLandPoligonsFile()

# Check for expired .osm.pbf files and download, if too old
# osm_maps_functions.checkAndDownloadOsmPbfFile(country, Max_Days_Old, Force_Processing)
x.checkAndDownloadOsmPbfFile()

# Filter tags from country osm.pbf files'
x.filterTagsFromCountryOsmPbdFiles()

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