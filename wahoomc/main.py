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
    adjustments_due_to_breaking_changes, copy_jsons_from_repo_to_user, \
    check_installed_version_against_latest_pypi, check_installation_of_programs_credentials_for_contour_lines
from wahoomc.downloader import download_tooling

from wahoomc.osm_maps_functions import OsmMaps
from wahoomc.osm_maps_functions import CountryOsmData, XYOsmData

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

    # initializing work directories needs to be the first call,
    # because other setup stuff relies on that (breaking changes)
    check_installed_version_against_latest_pypi()
    initialize_work_directories()
    adjustments_due_to_breaking_changes()
    download_tooling()
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

        if o_input_data.contour:
            check_installation_of_programs_credentials_for_contour_lines()

        if o_input_data.country:
            o_osm_data = CountryOsmData(o_input_data)
        elif o_input_data.xy_coordinates:
            o_osm_data = XYOsmData(o_input_data)

        # Check for not existing or expired files. Mark for download, if dl is needed
        o_osm_data.process_input_of_the_tool()
        o_downloader = o_osm_data.get_downloader()

        # Download files marked for download
        o_downloader.download_files_if_needed()

        o_osm_maps = OsmMaps(o_osm_data)

        # Filter tags from country osm.pbf files'
        o_osm_maps.filter_tags_from_country_osm_pbf_files()

        # Generate land
        o_osm_maps.generate_land()

        # Generate sea
        o_osm_maps.generate_sea()

        # Generate elevation
        if o_input_data.contour:
            o_osm_maps.generate_elevation(o_input_data.use_srtm1)

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
