"""
executable file to create up-to-date map-files for the Wahoo ELEMNT and Wahoo ELEMNT BOLT
"""
#!/usr/bin/python

# import official python packages
import argparse

# import custom python packages
from common_resources.osm_maps_functions import OsmMaps

# logging used in the terminal output:
# # means top-level command
# ! means error
# + means additional comment in a working-unit


# input argument creation and processing
parser = argparse.ArgumentParser(description='Create up-to-date maps for your Wahoo ELEMNT and Wahoo ELEMNT BOLT')

# country or file to create maps for
parser.add_argument("country", help="country to generate maps for")
# Maximum age of source maps or land shape files before they are redownloaded
parser.add_argument('-md', '--maxdays', help="maximum age of source maps and other files", type=int, default=14)
# Calculate also border countries of input country or not
parser.add_argument('-bc', '--bordercountries', action='store_true', help="process whole tiles which involve border countries")
# Force download of source maps and the land shape file
# If False use Max_Days_Old to check for expired maps
# If True force redownloading of maps and landshape
parser.add_argument('-d', '--forcedownload', action='store_true', help="force download of files")
# Force (re)processing of source maps and the land shape file
# If False only process files if not existing
# If True force processing of files
parser.add_argument('-p', '--forceprocessing', action='store_true', help="force processing of files")
# Save uncompressed maps for Cruiser if True
parser.add_argument('-c', '--cruiser', action='store_true', help="save uncompressed maps for Cruiser")

# get all entered arguments
args = parser.parse_args()


oOSMmaps = OsmMaps(args.forceprocessing, args.cruiser)

# Read json file
# Check for expired land polygons file and download, if too old
# Check for expired .osm.pbf files and download, if too old
oOSMmaps.process_input(args.country, args.bordercountries)
oOSMmaps.check_and_download_files(args.maxdays, args.forcedownload)

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
