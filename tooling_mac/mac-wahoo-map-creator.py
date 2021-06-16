#!/usr/bin/python

# import official python packages
import multiprocessing
import sys

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

# logging
# # means top-level command
# ! means error
# + means additional comment in a working-unit

if len(sys.argv) != 2:
    print(f'! Usage: {sys.argv[0]} Country name part of a .json file.')
    sys.exit()

oOSMmaps = OSM_Maps(sys.argv[1], Max_Days_Old, Force_Processing, workers, threads, Save_Cruiser)

# Read json file
oOSMmaps.readJsonFile()

# Check for expired land polygons file and download, if too old
oOSMmaps.checkAndDownloadLandPoligonsFile()

# Check for expired .osm.pbf files and download, if too old
oOSMmaps.checkAndDownloadOsmPbfFile()

# Filter tags from country osm.pbf files'
oOSMmaps.filterTagsFromCountryOsmPbfFiles()

# Generate land
oOSMmaps.generateLand()

# Generate sea
oOSMmaps.generateSea()

# Split filtered country files to tiles
oOSMmaps.splitFilteredCountryFilesToTiles()

# Merge splitted tiles with land an sea   
oOSMmaps.mergeSplittedTilesWithLandAndSea()

# Creating .map files
oOSMmaps.createMapFiles()

# Zip .map.lzma files
oOSMmaps.zipMapFiles()

# Make Cruiser map files zip file
oOSMmaps.makeCruiserFiles()