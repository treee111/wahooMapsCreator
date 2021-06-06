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

x = OSM_Maps(sys.argv[1], Max_Days_Old, Force_Processing, workers)

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


print('\n\n# Creating .map files')
TileCount = 1
for tile in country:
    print(f'\n\nCreating map file for tile {TileCount} of {len(country)} for Coordinates: {tile["x"]}, {tile["y"]}')
    outFile = os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}.map')
    if not os.path.isfile(outFile+'.lzma') or Force_Processing == 1:
        mergedFile = os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', 'merged.osm.pbf')
        cmd = [os.path.join (CurDir, 'Osmosis', 'bin', 'osmosis.bat'), '--rbf', mergedFile, 'workers='+workers, '--mw', 'file='+outFile]
        cmd.append(f'bbox={tile["bottom"]:.6f},{tile["left"]:.6f},{tile["top"]:.6f},{tile["right"]:.6f}')
        cmd.append('zoom-interval-conf=10,0,17')
        cmd.append('threads='+threads)
        cmd.append('tag-conf-file=' + os.path.join (CurDir, 'tag-wahoo.xml'))
        #cmd.append('tag-conf-file=tag-mapping.xml')
        # print(cmd)
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f'Error in Osmosis with country: {c}')
            sys.exit()        

        print('\n# compress .map file')
        cmd = ['lzma', 'e', outFile, outFile+'.lzma', f'-mt{threads}', '-d27', '-fb273', '-eos']
        # print(cmd)
        subprocess.run(cmd)
    TileCount += 1

print('\n# zip .map.lzma files')

countryName = os.path.split(sys.argv[1])
print(countryName[1])
# Make Wahoo zip file
cmd = ['7za', 'a', '-tzip', '-m0=lzma', '-mx9', '-mfb=273', '-md=1536m', countryName[1] + '.zip']
#cmd = ['7za', 'a', '-tzip', '-m0=lzma', countryName[1] + '.zip']

for tile in country:
    cmd.append(os.path.join(f'{tile["x"]}', f'{tile["y"]}.map.lzma'))
#print(cmd)
subprocess.run(cmd, cwd=OUT_PATH)

# Make Cruiser map files zip file
if Save_Cruiser == 1:
    cmd = ['7za', 'a', '-tzip', '-m0=lzma', countryName[1] + '-maps.zip']
    for tile in country:
        cmd.append(os.path.join(f'{tile["x"]}', f'{tile["y"]}.map'))
    #print(cmd)
    subprocess.run(cmd, cwd=OUT_PATH)