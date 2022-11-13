"""
executable file to create up-to-date map-files for the Wahoo ELEMNT and Wahoo ELEMNT BOLT
"""
#!/usr/bin/python

# import official python packages
import logging

# import custom python packages
from wahoomc.input import process_call_of_the_tool, cli_init
from wahoomc.setup_functions import initialize_work_directories, \
    check_installation_of_required_programs, write_config_file, \
    adjustments_due_to_breaking_changes, copy_jsons_from_repo_to_user

from wahoomc.osm_maps_functions import OsmMaps
from wahoomc.osm_maps_functions import OsmData

# logging used in the terminal output:
# # means top-level command
# ! means error
# + means additional comment in a working-unit


def run(run_level):
    """
    main program run
    """
    # create logger
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.INFO)

    initialize_work_directories()
    adjustments_due_to_breaking_changes()
    check_installation_of_required_programs()

    if run_level == 'init':
        o_input_data = cli_init()
    else:
        # handle GUI and CLI processing via one function and different cli-calls
        o_input_data = process_call_of_the_tool()

    if o_input_data.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if run_level == 'init':
        copy_jsons_from_repo_to_user('tag_wahoo_adjusted')
        copy_jsons_from_repo_to_user('.', 'tags-to-keep.json')
    else:
        # Is there something to do?
        o_input_data.is_required_input_given_or_exit(issue_message=True)

        o_osm_data = OsmData()
        # Check for not existing or expired files. Mark for download, if dl is needed
        o_downloader = o_osm_data.process_input_of_the_tool(o_input_data)

        # Download files marked for download
        o_downloader.download_files_if_needed()

        o_osm_maps = OsmMaps(o_osm_data)

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
        o_osm_maps.make_and_zip_files('.map.lzma', o_input_data.zip_folder)

        # Make Cruiser map files zip file
        if o_input_data.save_cruiser is True:
            o_osm_maps.make_and_zip_files('.map', o_input_data.zip_folder)

    # run was successful --> write config file
    write_config_file()
