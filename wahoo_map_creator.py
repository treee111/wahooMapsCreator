"""
executable file to create up-to-date map-files for the Wahoo ELEMNT and Wahoo ELEMNT BOLT
"""
#!/usr/bin/python

# import official python packages
import sys

# import custom python packages
from common_python.osm_maps_functions import OsmMaps
from common_python.input import Input

# logging used in the terminal output:
# # means top-level command
# ! means error
# + means additional comment in a working-unit

oInput = Input()

if oInput.gui_mode:
    oInputData = oInput.start_gui()
else:
    oInputData = oInput.cli_arguments()

# Is there something to do?
if oInputData.country == "none" or oInputData.country == "":
    sys.exit("Nothing to do. Start with -h or --help to see command line options."
             "Or in the GUI select a country to create maps for.")

oOSMmaps = OsmMaps(oInputData.force_processing)

# Read json file
# Check for expired land polygons file and download, if too old
# Check for expired .osm.pbf files and download, if too old
oOSMmaps.process_input(oInputData.country, oInputData.border_countries)
oOSMmaps.check_and_download_files(
    oInputData.max_days_old, oInputData.force_download)


if oInputData.only_merge is False:
    # Filter tags from country osm.pbf files'
    oOSMmaps.filter_tags_from_country_osm_pbf_files()

    # Generate land
    oOSMmaps.generate_land()

    # Generate sea
    oOSMmaps.generate_sea()

    # Split filtered country files to tiles
    oOSMmaps.split_filtered_country_files_to_tiles()

# Merge splitted tiles with land an sea
oOSMmaps.merge_splitted_tiles_with_land_and_sea(oInputData.border_countries)

# Creating .map files
oOSMmaps.create_map_files(oInputData.save_cruiser, oInputData.tag_wahoo_xml)

# Zip .map.lzma files
oOSMmaps.zip_map_files()

# Make Cruiser map files zip file
if oInputData.save_cruiser is True:
    oOSMmaps.make_cruiser_files()
