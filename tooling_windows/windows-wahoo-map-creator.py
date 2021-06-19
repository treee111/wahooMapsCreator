#!/usr/bin/python
#-*- coding:utf-8 -*-

# import official python packages
import multiprocessing
import sys

# import custom python packages
# ToDo: This might not work - Properly import in Windows!
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from common_resources.osm_maps_functions import OsmMaps

########### Configurable Parameters

# Maximum age of source maps or land shape files before they are redownloaded
MAX_DAYS_OLD = 14

# Force download of source maps and the land shape file
# If 0 use Max_Days_Old to check for expired maps
# If 1 force redownloading of maps and landshape
FORCE_DOWNLOAD = 0

# Force (re)processing of source maps and the land shape file
# If 0 use Max_Days_Old to check for expired maps
# If 1 force processing of maps and landshape
FORCE_PROCESSING = 0

# Save uncompressed maps for Cruiser
SAVE_CRUISER = 0

# Number of threads to use in the mapwriter plug-in
THREADS = str(multiprocessing.cpu_count() - 1)
if int(THREADS) < 1:
    THREADS = 1
# Or set it manually to:
#threads = 1
#print(f'threads = {threads}/n')

# Number of workers for the Osmosis read binary fast function
WORKERS = '1'

########### End of Configurable Parameters

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} Country name part of a .json file.')
    sys.exit()

oOSMmaps = OsmMaps(sys.argv[1], MAX_DAYS_OLD,
                FORCE_DOWNLOAD, FORCE_PROCESSING,
                WORKERS, THREADS, SAVE_CRUISER)

# if x.region == '' :
#     print ('Invalid country name.')
#     sys.exit()

# Read json file
oOSMmaps.read_json_file()

# Check for expired land polygons file and download, if too old
# osm_maps_functions.checkAndDownloadLandPoligonsFile(Max_Days_Old, Force_Processing)
oOSMmaps.check_and_download_land_poligons_file()

# Check for expired .osm.pbf files and download, if too old
# osm_maps_functions.checkAndDownloadOsmPbfFile(country, MaoOSMmaps_Days_Old, Force_Processing)
oOSMmaps.check_and_download_osm_pbf_file()

# Filter tags from country osm.pbf files'
oOSMmaps.filter_tags_from_country_osm_pbf_files()

# Generate land
oOSMmaps.generate_land()

# Generate sea
oOSMmaps.generate_sea()

# Split filtered country files to tiles
oOSMmaps.split_filtered_country_files_to_tiles()

# Merge splitted tiles with land an sea
oOSMmaps.merge_splitted_tiles_with_land_and_sea()

# Creating .map files
oOSMmaps.create_map_files()

# Zip .map.lzma files
oOSMmaps.zip_map_files()

# Make Cruiser map files zip file
oOSMmaps.make_cruiser_files()