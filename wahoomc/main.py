"""
executable file to create up-to-date map-files for the Wahoo ELEMNT and Wahoo ELEMNT BOLT
"""
#!/usr/bin/python

# import official python packages
import logging

# import custom python packages
from wahoomc.input import process_call_of_the_tool
from wahoomc.setup_functions import initialize_work_directories
from wahoomc.setup_functions import move_old_content_into_new_dirs
from wahoomc.setup_functions import check_installation_of_required_programs
from wahoomc.osm_maps_functions import OsmMaps

# logging used in the terminal output:
# # means top-level command
# ! means error
# + means additional comment in a working-unit


def run():
    """
    main program run
    """
    # create logger
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)

    check_installation_of_required_programs()

    # handle GUI and CLI processing via one function and different cli-calls
    o_input_data = process_call_of_the_tool()

    # Is there something to do?
    o_input_data.is_required_input_given_or_exit(issue_message=True)

    initialize_work_directories()
    move_old_content_into_new_dirs()

    o_osm_maps = OsmMaps(o_input_data)

    # Read json file
    # Check for expired land polygons file and download, if too old
    # Check for expired .osm.pbf files and download, if too old
    o_osm_maps.process_input(o_input_data.process_border_countries)
    o_osm_maps.check_and_download_files()

    if o_input_data.only_merge is False:
        # Filter tags from country osm.pbf files'
        o_osm_maps.filter_tags_from_country_osm_pbf_files()

        # Generate land
        o_osm_maps.generate_land()

        # Generate sea
        o_osm_maps.generate_sea()

        # Split filtered country files to tiles
        o_osm_maps.split_filtered_country_files_to_tiles()

    # Merge splitted tiles with land an sea
    o_osm_maps.merge_splitted_tiles_with_land_and_sea(
        o_input_data.process_border_countries)

    # Creating .map files
    o_osm_maps.create_map_files(o_input_data.save_cruiser,
                                o_input_data.tag_wahoo_xml)

    # Zip .map.lzma files
    o_osm_maps.make_and_zip_files(
        o_input_data.keep_map_folders, '.map.lzma', o_input_data.zip_folder)

    # Make Cruiser map files zip file
    if o_input_data.save_cruiser is True:
        o_osm_maps.make_and_zip_files(
            o_input_data.keep_map_folders, '.map', o_input_data.zip_folder)
