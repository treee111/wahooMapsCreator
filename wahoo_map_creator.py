"""
executable file to create up-to-date map-files for the Wahoo ELEMNT and Wahoo ELEMNT BOLT
"""
#!/usr/bin/python

# import official python packages

# import custom python packages
from common_python.input import process_call_of_the_tool
from common_python.file_directory_functions import initialize_work_directories
from common_python.osm_maps_functions import OsmMaps

# logging used in the terminal output:
# # means top-level command
# ! means error
# + means additional comment in a working-unit

# handle GUI and CLI processing via one function and different cli-calls
oInputData = process_call_of_the_tool()

# Is there something to do?
oInputData.is_required_input_given_or_exit(issue_message=True)

initialize_work_directories()

oOSMmaps = OsmMaps(oInputData)

# Read json file
# Check for expired land polygons file and download, if too old
# Check for expired .osm.pbf files and download, if too old
oOSMmaps.process_input(oInputData.border_countries)
oOSMmaps.check_and_download_files()


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
oOSMmaps.make_and_zip_files(oInputData.keep_map_folders, '.map.lzma')

# Make Cruiser map files zip file
if oInputData.save_cruiser is True:
    oOSMmaps.make_and_zip_files(oInputData.keep_map_folders, '.map')
