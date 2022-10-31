"""
functions and object for managing OSM maps
"""
#!/usr/bin/python

# import official python packages
import glob
import multiprocessing
import os
import struct
import subprocess
import sys
import platform
import shutil
import logging

# import custom python packages
from wahoomc.file_directory_functions import read_json_file, \
    get_folders_in_folder, get_filenames_of_jsons_in_folder, create_empty_directories, write_json_file_generic
from wahoomc.constants_functions import get_path_to_static_tile_json, translate_tags_to_keep, \
    get_tooling_win_path, get_tag_wahoo_xml_path, TagWahooXmlNotFoundError

from wahoomc.constants import USER_WAHOO_MC
from wahoomc.constants import USER_OUTPUT_DIR
from wahoomc.constants import RESOURCES_DIR
from wahoomc.constants import LAND_POLYGONS_PATH
from wahoomc.constants import VERSION

from wahoomc.downloader import Downloader
from wahoomc.geofabrik import Geofabrik

log = logging.getLogger('main-logger')


class TileNotFoundError(Exception):
    """Raised when no tile is found for x/y combination"""


def get_xy_coordinates_from_input(input_xy_coordinates):
    """
    extract/split x/y combinations by given X/Y coordinates.
    input should be "188/88" or for multiple values "188/88,100/10,109/99".
    returns a list of x/y combinations as integers
    """

    xy_combinations = []

    # split by "," first for multiple x/y combinations, then by "/" for x and y value
    for xy_coordinate in input_xy_coordinates.split(","):
        splitted = xy_coordinate.split("/")

        if len(splitted) == 2:
            xy_combinations.append(
                {"x": int(splitted[0]), "y": int(splitted[1])})

    return xy_combinations


def get_tile_by_one_xy_combination_from_jsons(xy_combination):
    """
    get tile from json files by given X/Y coordinate combination
    """
    # go through all files in all folders of the "json" directory
    file_path_jsons = os.path.join(RESOURCES_DIR, 'json')

    for folder in get_folders_in_folder(file_path_jsons):
        for file in get_filenames_of_jsons_in_folder(os.path.join(file_path_jsons, folder)):

            # get content of json in folder
            content = read_json_file(
                os.path.join(file_path_jsons, folder, file + '.json'))

            # check tiles values against input x/y combination
            for tile in content:
                if tile['x'] == xy_combination['x'] and tile['y'] == xy_combination['y']:
                    return tile

    # if function is processed until here, there is no tile found for the x/y combination --> Exception
    raise TileNotFoundError


def run_subprocess_and_log_output(cmd, error_message, cwd=""):
    """
    run given cmd-subprocess and issue error message if wished
    """
    if not cwd:
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
            for line in iter(process.stdout.readline, b''):  # b'\n'-separated lines
                try:
                    log.debug('subprocess:%r', line.decode("utf-8").strip())
                except UnicodeDecodeError:
                    log.debug('subprocess:%r', line.decode("latin-1").strip())
    else:
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd) as process:
            for line in iter(process.stdout.readline, b''):  # b'\n'-separated lines
                try:
                    log.debug('subprocess:%r', line.decode("utf-8").strip())
                except UnicodeDecodeError:
                    log.debug('subprocess:%r', line.decode("latin-1").strip())

    if error_message and process.wait() != 0:  # 0 means success
        log.error(error_message)
        sys.exit()


class OsmData():  # pylint: disable=too-few-public-methods
    """
    object with all internal parameters to process maps
    """

    def __init__(self):
        """
        xxx
        """
        self.force_processing = False
        self.tiles = []
        self.border_countries = {}
        self.country_name = ''

    def process_input_of_the_tool(self, o_input_data):
        """
        Process input: get relevant tiles and if border countries should be calculated
        The three primary inputs are giving by a separate value each and have separate processing:
        1. country name
        2. x/y combinations

        # Check for not existing or expired files. Mark for download, if dl is needed
        # - land polygons file
        # - .osm.pbf files

        steps in this function:
        1. take over input paramters (force_processing is changed in the function further down)
        2. check + download geofabrik file if geofabrik-processing
        3. calculate relevant tiles for map creation
        4. calculate border countries for map creation
        5. evaluate the country-name for folder cration during processing
        6. calculate if force_processing should be set to true
        """

        o_downloader = Downloader(
            o_input_data.max_days_old, o_input_data.force_download, self.tiles, self.border_countries)
        # takeover what is given by user first for force_processing
        self.force_processing = o_input_data.force_processing

        log.info('-' * 80)

        # geofabrik file
        if o_input_data.geofabrik_tiles and \
                o_downloader.should_geofabrik_file_be_downloaded():
            self.force_processing = True
            o_downloader.download_geofabrik_file()

        # calc tiles
        if o_input_data.country:
            self.calc_tiles_country(o_input_data)
        elif o_input_data.xy_coordinates:
            self.calc_tiles_xy(o_input_data)

        # calc border countries
        log.info('-' * 80)
        if o_input_data.country:
            self.calc_border_countries_country(o_input_data)
        elif o_input_data.xy_coordinates:
            self.calc_border_countries()
        # log border countries when and when not calculated to output the processed country(s)
        self.log_border_countries()

        # calc country name
        if o_input_data.country:
            # country name is the input argument
            self.country_name = o_input_data.country
        elif o_input_data.xy_coordinates:
            self.calc_country_name_xy()

        # calc force processing
        # Check for not existing or expired files. Mark for download, if dl is needed
        o_downloader.check_land_polygons_file()
        o_downloader.check_osm_pbf_file()

        # If one of the files needs to be downloaded, reprocess all files
        if o_downloader.need_to_dl:
            self.force_processing = True

        return o_downloader

    def calc_tiles_country(self, o_input_data):
        """
        option 1: input a country as parameter, e.g. germany
        """
        log.info('# Input country: %s.', o_input_data.country)

        # option 1a: use Geofabrik-URL to calculate the relevant tiles
        if o_input_data.geofabrik_tiles:
            o_geofabrik = Geofabrik(o_input_data.country)
            self.tiles = o_geofabrik.get_tiles_of_country()

        # option 1b: use static json files in the repo to calculate relevant tiles
        else:
            json_file_path = get_path_to_static_tile_json(
                o_input_data.country)
            self.tiles = read_json_file(json_file_path)

    def calc_tiles_xy(self, o_input_data):
        """
        option 2: input a x/y combinations as parameter, e.g. 134/88  or 133/88,130/100
        """
        log.info(
            '# Input X/Y coordinates: %s.', o_input_data.xy_coordinates)

        # option 2a: use Geofabrik-URL to get the relevant tiles
        if o_input_data.geofabrik_tiles:
            sys.exit("X/Y coordinated via Geofabrik not implemented now")

        # option 2b: use static json files in the repo to get relevant tiles
        else:
            xy_coordinates = get_xy_coordinates_from_input(
                o_input_data.xy_coordinates)

            # loop through x/y combinations and find each tile in the json files
            for xy_comb in xy_coordinates:
                try:
                    self.tiles.append(get_tile_by_one_xy_combination_from_jsons(
                        xy_comb))

                except TileNotFoundError:
                    pass

    def calc_border_countries_country(self, o_input_data):
        """
        calculate the border countries for the given tiles when input is a country
        - if CLI/GUI input by user
        """
        if o_input_data.process_border_countries:
            self.calc_border_countries()
        # set the to-be-processed country as border country
        else:
            self.border_countries[o_input_data.country] = {}

    def calc_border_countries(self):
        """
        calculate the border countries for the given tiles. i.e.
        - if CLI/GUI input by user
        - if processing x/y coordinates
        """
        log.info('# Determine involved/border countries')

        # Build list of countries needed
        for tile in self.tiles:
            for country in tile['countries']:
                if country not in self.border_countries:
                    self.border_countries[country] = {}

    def log_border_countries(self):
        """
        write calculated border countries/involved countries to log
        """
        for country in self.border_countries:
            log.info('+ Involved country: %s', country)

        # input can be only one country, if there are more than one,
        # border countries must be selected
        if len(self.border_countries) > 1:
            log.info('+ Border countries will be processed')

    def find_tiles_for_xy_combinations(self, xy_coordinates):
        """
        loop through x/y combinations and find each tile in the json files
        """
        for xy_comb in xy_coordinates:
            try:
                self.tiles.append(get_tile_by_one_xy_combination_from_jsons(
                    xy_comb))

            except TileNotFoundError:
                pass

    def calc_country_name_xy(self):
        """
        country name is the X/Y combinations separated by minus
        >1 x/y combinations are separated by underscore
        """
        for tile in self.tiles:
            if not self.country_name:
                self.country_name = f'{tile["x"]}-{tile["y"]}'
            else:
                self.country_name = f'{self.country_name}_{tile["x"]}-{tile["y"]}'


class OsmMaps:
    """
    This is a OSM data class
    """

    osmosis_win_file_path = get_tooling_win_path(
        ['Osmosis', 'bin', 'osmosis.bat'])

    # Number of workers for the Osmosis read binary fast function
    workers = '1'

    def __init__(self, o_osm_data):
        self.o_osm_data = o_osm_data

        if 8 * struct.calcsize("P") == 32:
            self.osmconvert_path = get_tooling_win_path(['osmconvert'])
        else:
            self.osmconvert_path = get_tooling_win_path(
                ['osmconvert64-0.8.8p'])

        create_empty_directories(
            USER_OUTPUT_DIR, self.o_osm_data.tiles, self.o_osm_data.border_countries)

    def filter_tags_from_country_osm_pbf_files(self):  # pylint: disable=too-many-statements
        """
        Filter tags from country osm.pbf files
        """

        log.info('-' * 80)
        log.info('# Filter tags from country osm.pbf files')

        for key, val in self.o_osm_data.border_countries.items():
            # evaluate contry directory, create if not exists
            country_dir = os.path.join(USER_OUTPUT_DIR, key)

            # set names for filtered files for WIN, later on add ".pbf" for macOS/Linux
            out_file_o5m_filtered_win = os.path.join(country_dir,
                                                     'filtered.o5m')
            out_file_o5m_filtered_names_win = os.path.join(country_dir,
                                                           'filtered_names.o5m')

            # Windows
            if platform.system() == "Windows":
                out_file_o5m = os.path.join(country_dir, 'outFile.o5m')
                # only create o5m file if not there already or force processing (no user input possible)
                # --> speeds up processing if one only wants to test tags / POIs
                if not os.path.isfile(out_file_o5m) or self.o_osm_data.force_processing is True:
                    log.info('+ Converting map of %s to o5m format', key)
                    cmd = [self.osmconvert_path]
                    cmd.extend(['-v', '--hash-memory=2500', '--complete-ways',
                                '--complete-multipolygons', '--complete-boundaries',
                                '--drop-author', '--drop-version'])
                    cmd.append(val['map_file'])
                    cmd.append('-o='+out_file_o5m)

                    run_subprocess_and_log_output(
                        cmd, f'! Error in OSMConvert with country: {key}')
                else:
                    log.info('+ Map of %s already in o5m format', key)

                # filter out tags:
                # - if no filtered files exist
                # - force processing is set (this is also when new map files were dowwnloaded)
                # - the defined TAGS_TO_KEEP_UNIVERSAL constants have changed are changed (user input or new release)
                if not os.path.isfile(out_file_o5m_filtered_win) or not os.path.isfile(out_file_o5m_filtered_names_win) \
                        or self.o_osm_data.force_processing is True or self.tags_are_identical_to_last_run(key) is False:
                    log.info(
                        '+ Filtering unwanted map objects out of map of %s', key)
                    cmd = [get_tooling_win_path(['osmfilter'])]
                    cmd.append(out_file_o5m)
                    cmd.append(
                        '--keep="' + translate_tags_to_keep(sys_platform=platform.system()) + '"')
                    cmd.append('--keep-tags="all type= layer= ' +
                               translate_tags_to_keep(sys_platform=platform.system()) + '"')
                    cmd.append('-o=' + out_file_o5m_filtered_win)

                    run_subprocess_and_log_output(
                        cmd, f'! Error in OSMFilter with country: {key}')

                    cmd = [get_tooling_win_path(['osmfilter'])]
                    cmd.append(out_file_o5m)
                    cmd.append(
                        '--keep="' + translate_tags_to_keep(
                            name_tags=True, sys_platform=platform.system()) + '"')
                    cmd.append('--keep-tags="all type= name= layer= ' +
                               translate_tags_to_keep(
                                   name_tags=True, sys_platform=platform.system()) + '"')
                    cmd.append('-o=' + out_file_o5m_filtered_names_win)

                    run_subprocess_and_log_output(
                        cmd, f'! Error in OSMFilter with country: {key}')

                val['filtered_file'] = out_file_o5m_filtered_win
                val['filtered_file_names'] = out_file_o5m_filtered_names_win

            # Non-Windows
            else:
                out_file_pbf_filtered_mac = f'{out_file_o5m_filtered_win}.pbf'
                out_file_pbf_filtered_names_mac = f'{out_file_o5m_filtered_names_win}.pbf'

                # filter out tags:
                # - if no filtered files exist
                # - force processing is set (this is also when new map files were dowwnloaded)
                # - the defined TAGS_TO_KEEP_UNIVERSAL constants have changed are changed (user input or new release)
                if not os.path.isfile(out_file_pbf_filtered_mac) or not os.path.isfile(out_file_pbf_filtered_names_mac) \
                        or self.o_osm_data.force_processing is True or self.tags_are_identical_to_last_run(key) is False:
                    log.info(
                        '+ Filtering unwanted map objects out of map of %s', key)

                    # https://docs.osmcode.org/osmium/latest/osmium-tags-filter.html
                    cmd = ['osmium', 'tags-filter', '--remove-tags']
                    cmd.append(val['map_file'])
                    cmd.extend(translate_tags_to_keep(
                        sys_platform=platform.system()))
                    cmd.extend(['-o', out_file_pbf_filtered_mac])
                    cmd.append('--overwrite')

                    run_subprocess_and_log_output(
                        cmd, f'! Error in Osmium with country: {key}')

                    cmd = ['osmium', 'tags-filter', '--remove-tags']
                    cmd.append(val['map_file'])
                    cmd.extend(translate_tags_to_keep(
                        name_tags=True, sys_platform=platform.system()))
                    cmd.extend(['-o', out_file_pbf_filtered_names_mac])
                    cmd.append('--overwrite')

                    run_subprocess_and_log_output(
                        cmd, f'! Error in Osmium with country: {key}')

                val['filtered_file'] = out_file_pbf_filtered_mac
                val['filtered_file_names'] = out_file_pbf_filtered_names_mac

            # write config file for country
            self.write_country_config_file(key)

        log.info('+ Filter tags from country osm.pbf files: OK')

    def generate_land(self):
        """
        Generate land for all tiles
        """

        log.info('-' * 80)
        log.info('# Generate land for each coordinate')

        tile_count = 1
        for tile in self.o_osm_data.tiles:
            land_file = os.path.join(USER_OUTPUT_DIR,
                                     f'{tile["x"]}', f'{tile["y"]}', 'land.shp')
            out_file_land1 = os.path.join(USER_OUTPUT_DIR,
                                          f'{tile["x"]}', f'{tile["y"]}', 'land')

            # create land.dbf, land.prj, land.shp, land.shx
            if not os.path.isfile(land_file) or self.o_osm_data.force_processing is True:
                log.info(
                    '+ Coordinates: %s,%s. (%s of %s)', tile["x"], tile["y"], tile_count, len(self.o_osm_data.tiles))
                cmd = ['ogr2ogr', '-overwrite', '-skipfailures']
                # Try to prevent getting outside of the +/-180 and +/- 90 degrees borders. Normally the +/- 0.1 are there to prevent white lines at border borders.
                if tile["x"] == 255 or tile["y"] == 255 or tile["x"] == 0 or tile["y"] == 0:
                    cmd.extend(['-spat', f'{tile["left"]:.6f}',
                                f'{tile["bottom"]:.6f}',
                                f'{tile["right"]:.6f}',
                                f'{tile["top"]:.6f}'])
                else:
                    cmd.extend(['-spat', f'{tile["left"]-0.1:.6f}',
                                f'{tile["bottom"]-0.1:.6f}',
                                f'{tile["right"]+0.1:.6f}',
                                f'{tile["top"]+0.1:.6f}'])
                cmd.append(land_file)
                cmd.append(LAND_POLYGONS_PATH)

                run_subprocess_and_log_output(
                    cmd, f'! Error generating land for tile: {tile["x"]},{tile["y"]}')

            # create land1.osm
            if not os.path.isfile(out_file_land1+'1.osm') or self.o_osm_data.force_processing is True:
                # Windows
                if platform.system() == "Windows":
                    cmd = ['python', os.path.join(RESOURCES_DIR,
                                                  'shape2osm.py'), '-l', out_file_land1, land_file]

                # Non-Windows
                else:
                    cmd = ['python', os.path.join(RESOURCES_DIR,
                                                  'shape2osm.py'), '-l', out_file_land1, land_file]

                run_subprocess_and_log_output(
                    cmd, f'! Error creating land.osm for tile: {tile["x"]},{tile["y"]}')
            tile_count += 1

        log.info('+ Generate land for each coordinate: OK')

    def generate_sea(self):
        """
        Generate sea for all tiles
        """

        log.info('-' * 80)
        log.info('# Generate sea for each coordinate')

        tile_count = 1
        for tile in self.o_osm_data.tiles:
            out_file_sea = os.path.join(USER_OUTPUT_DIR,
                                        f'{tile["x"]}', f'{tile["y"]}', 'sea.osm')
            if not os.path.isfile(out_file_sea) or self.o_osm_data.force_processing is True:
                log.info(
                    '+ Coordinates: %s,%s. (%s of %s)', tile["x"], tile["y"], tile_count, len(self.o_osm_data.tiles))
                with open(os.path.join(RESOURCES_DIR, 'sea.osm'), encoding="utf-8") as sea_file:
                    sea_data = sea_file.read()

                    # Try to prevent getting outside of the +/-180 and +/- 90 degrees borders. Normally the +/- 0.1 are there to prevent white lines at tile borders
                    if tile["x"] == 255 or tile["y"] == 255 or tile["x"] == 0 or tile["y"] == 0:
                        sea_data = sea_data.replace(
                            '$LEFT', f'{tile["left"]:.6f}')
                        sea_data = sea_data.replace(
                            '$BOTTOM', f'{tile["bottom"]:.6f}')
                        sea_data = sea_data.replace(
                            '$RIGHT', f'{tile["right"]:.6f}')
                        sea_data = sea_data.replace(
                            '$TOP', f'{tile["top"]:.6f}')
                    else:
                        sea_data = sea_data.replace(
                            '$LEFT', f'{tile["left"]-0.1:.6f}')
                        sea_data = sea_data.replace(
                            '$BOTTOM', f'{tile["bottom"]-0.1:.6f}')
                        sea_data = sea_data.replace(
                            '$RIGHT', f'{tile["right"]+0.1:.6f}')
                        sea_data = sea_data.replace(
                            '$TOP', f'{tile["top"]+0.1:.6f}')

                    with open(out_file_sea, mode='w', encoding="utf-8") as output_file:
                        output_file.write(sea_data)
            tile_count += 1

        log.info('+ Generate sea for each coordinate: OK')

    def split_filtered_country_files_to_tiles(self):
        """
        Split filtered country files to tiles
        """

        log.info('-' * 80)
        log.info('# Split filtered country files to tiles')
        tile_count = 1
        for tile in self.o_osm_data.tiles:

            for country, val in self.o_osm_data.border_countries.items():
                if country not in tile['countries']:
                    continue
                log.info(
                    '+ Coordinates: %s,%s / %s (%s of %s)', tile["x"], tile["y"], country, tile_count, len(self.o_osm_data.tiles))
                out_file = os.path.join(USER_OUTPUT_DIR,
                                        f'{tile["x"]}', f'{tile["y"]}', f'split-{country}.osm.pbf')
                out_file_names = os.path.join(USER_OUTPUT_DIR,
                                              f'{tile["x"]}', f'{tile["y"]}', f'split-{country}-names.osm.pbf')

                # split filtered country files to tiles every time because the result is different per constants (user input)
                # Windows
                if platform.system() == "Windows":
                    cmd = [self.osmconvert_path,
                           '-v', '--hash-memory=2500']
                    cmd.append('-b='+f'{tile["left"]}' + ',' + f'{tile["bottom"]}' +
                               ',' + f'{tile["right"]}' + ',' + f'{tile["top"]}')
                    cmd.extend(
                        ['--complete-ways', '--complete-multipolygons', '--complete-boundaries'])
                    cmd.append(val['filtered_file'])
                    cmd.append('-o='+out_file)

                    run_subprocess_and_log_output(
                        cmd, f'! Error in Osmosis with country: {country}. Win/out_file')

                    cmd = [self.osmconvert_path,
                           '-v', '--hash-memory=2500']
                    cmd.append('-b='+f'{tile["left"]}' + ',' + f'{tile["bottom"]}' +
                               ',' + f'{tile["right"]}' + ',' + f'{tile["top"]}')
                    cmd.extend(
                        ['--complete-ways', '--complete-multipolygons', '--complete-boundaries'])
                    cmd.append(val['filtered_file_names'])
                    cmd.append('-o='+out_file_names)

                    run_subprocess_and_log_output(
                        cmd, '! Error in Osmosis with country: {country}. Win/out_file_names')

                # Non-Windows
                else:
                    cmd = ['osmium', 'extract']
                    cmd.extend(
                        ['-b', f'{tile["left"]},{tile["bottom"]},{tile["right"]},{tile["top"]}'])
                    cmd.append(val['filtered_file'])
                    cmd.extend(['-s', 'smart'])
                    cmd.extend(['-o', out_file])
                    cmd.extend(['--overwrite'])

                    run_subprocess_and_log_output(
                        cmd, '! Error in Osmosis with country: {country}. macOS/out_file')

                    cmd = ['osmium', 'extract']
                    cmd.extend(
                        ['-b', f'{tile["left"]},{tile["bottom"]},{tile["right"]},{tile["top"]}'])
                    cmd.append(val['filtered_file_names'])
                    cmd.extend(['-s', 'smart'])
                    cmd.extend(['-o', out_file_names])
                    cmd.extend(['--overwrite'])

                    run_subprocess_and_log_output(
                        cmd, '! Error in Osmosis with country: {country}. macOS/out_file_names')

            tile_count += 1

        log.info('+ Split filtered country files to tiles: OK')

    def merge_splitted_tiles_with_land_and_sea(self, process_border_countries):
        """
        Merge splitted tiles with land an sea
        """

        log.info('-' * 80)
        log.info('# Merge splitted tiles with land an sea')
        tile_count = 1
        for tile in self.o_osm_data.tiles:  # pylint: disable=too-many-nested-blocks
            log.info(
                '+ Merging tiles for tile %s of %s for Coordinates: %s,%s', tile_count, len(self.o_osm_data.tiles), tile["x"], tile["y"])

            out_tile_dir = os.path.join(USER_OUTPUT_DIR,
                                        f'{tile["x"]}', f'{tile["y"]}')
            out_file_merged = os.path.join(out_tile_dir, 'merged.osm.pbf')

            land_files = glob.glob(os.path.join(out_tile_dir, 'land*.osm'))

            # merge splitted tiles with land and sea every time because the result is different per constants (user input)
            # sort land* osm files
            self.sort_osm_files(tile)

            # Windows
            if platform.system() == "Windows":
                cmd = [self.osmosis_win_file_path]
                loop = 0
                # loop through all countries of tile, if border-countries should be processed.
                # if border-countries should not be processed, only process the "entered" country
                for country in tile['countries']:
                    if process_border_countries or country in self.o_osm_data.border_countries:
                        cmd.append('--rbf')
                        cmd.append(os.path.join(
                            out_tile_dir, f'split-{country}.osm.pbf'))
                        cmd.append('workers=' + self.workers)
                        if loop > 0:
                            cmd.append('--merge')

                        cmd.append('--rbf')
                        cmd.append(os.path.join(
                            out_tile_dir, f'split-{country}-names.osm.pbf'))
                        cmd.append('workers=' + self.workers)
                        cmd.append('--merge')

                        loop += 1

                for land in land_files:
                    cmd.extend(
                        ['--rx', 'file='+os.path.join(out_tile_dir, f'{land}'), '--s', '--m'])
                cmd.extend(
                    ['--rx', 'file='+os.path.join(out_tile_dir, 'sea.osm'), '--s', '--m'])
                cmd.extend(['--tag-transform', 'file=' + os.path.join(RESOURCES_DIR,
                                                                      'tunnel-transform.xml'), '--wb', out_file_merged, 'omitmetadata=true'])

            # Non-Windows
            else:
                cmd = ['osmium', 'merge', '--overwrite']
                # loop through all countries of tile, if border-countries should be processed.
                # if border-countries should not be processed, only process the "entered" country
                for country in tile['countries']:
                    if process_border_countries or country in self.o_osm_data.border_countries:
                        cmd.append(os.path.join(
                            out_tile_dir, f'split-{country}.osm.pbf'))
                        cmd.append(os.path.join(
                            out_tile_dir, f'split-{country}-names.osm.pbf'))

                for land in land_files:
                    cmd.append(land)
                cmd.append(os.path.join(out_tile_dir, 'sea.osm'))
                cmd.extend(['-o', out_file_merged])

            run_subprocess_and_log_output(
                cmd, f'! Error in Osmosis with tile: {tile["x"]},{tile["y"]}')

            tile_count += 1

        log.info('+ Merge splitted tiles with land an sea: OK')

    def sort_osm_files(self, tile):
        """
        sort land*.osm files to be in this order: nodes, then ways, then relations.
        this is mandatory for osmium-merge since:
        https://github.com/osmcode/osmium-tool/releases/tag/v1.13.2
        """

        log.info('-' * 80)
        log.info('# Sorting land* osm files')

        # get all land* osm files
        land_files = glob.glob(os.path.join(USER_OUTPUT_DIR,
                                            f'{tile["x"]}', f'{tile["y"]}', 'land*.osm'))

        # Windows
        if platform.system() == "Windows":
            for land in land_files:
                cmd = [self.osmosis_win_file_path]

                cmd.extend(['--read-xml', 'file='+os.path.join(land)])
                cmd.append('--sort')
                cmd.extend(['--write-xml', 'file='+os.path.join(land)])

        # Non-Windows
        else:
            for land in land_files:
                cmd = ['osmium', 'sort', '--overwrite']
                cmd.append(land)
                cmd.extend(['-o', land])

        run_subprocess_and_log_output(
            cmd, f'Error in Osmosis with sorting land* osm files of tile: {tile["x"]},{tile["y"]}')

        log.info('+ Sorting land* osm files: OK')

    def create_map_files(self, save_cruiser, tag_wahoo_xml):
        """
        Creating .map files
        """

        log.info('-' * 80)
        log.info('# Creating .map files for tiles')

        # Number of threads to use in the mapwriter plug-in
        threads = multiprocessing.cpu_count() - 1
        if int(threads) < 1:
            threads = 1

        tile_count = 1
        for tile in self.o_osm_data.tiles:
            log.info(
                '+ Coordinates: %s,%s (%s of %s)', tile["x"], tile["y"], tile_count, len(self.o_osm_data.tiles))

            out_file_map = os.path.join(USER_OUTPUT_DIR,
                                        f'{tile["x"]}', f'{tile["y"]}.map')

            # apply tag-wahoo xml every time because the result is different per .xml file (user input)
            merged_file = os.path.join(USER_OUTPUT_DIR,
                                       f'{tile["x"]}', f'{tile["y"]}', 'merged.osm.pbf')

            # Windows
            if platform.system() == "Windows":
                cmd = [self.osmosis_win_file_path, '--rbf', merged_file,
                       'workers=' + self.workers, '--mw', 'file='+out_file_map]
            # Non-Windows
            else:
                cmd = ['osmosis', '--rb', merged_file,
                       '--mw', 'file='+out_file_map]

            cmd.append(
                f'bbox={tile["bottom"]:.6f},{tile["left"]:.6f},{tile["top"]:.6f},{tile["right"]:.6f}')
            cmd.append('zoom-interval-conf=10,0,17')
            cmd.append(f'threads={threads}')
            # add path to tag-wahoo xml file
            try:
                cmd.append(
                    f'tag-conf-file={get_tag_wahoo_xml_path(tag_wahoo_xml)}')
            except TagWahooXmlNotFoundError:
                log.error(
                    'The tag-wahoo xml file was not found: ˚%s˚. Does the file exist and is your input correct?', tag_wahoo_xml)
                sys.exit()

            run_subprocess_and_log_output(
                cmd, f'Error in creating map file via Osmosis with tile: {tile["x"]},{tile["y"]}. mapwriter plugin installed?')

            # Windows
            if platform.system() == "Windows":
                cmd = [get_tooling_win_path(['lzma']), 'e', out_file_map,
                       out_file_map+'.lzma', f'-mt{threads}', '-d27', '-fb273', '-eos']
            # Non-Windows
            else:
                # force overwrite of output file and (de)compress links
                cmd = ['lzma', out_file_map, '-f']

                # --keep: do not delete source file
                if save_cruiser:
                    cmd.append('--keep')

            run_subprocess_and_log_output(
                cmd, f'! Error creating map files for tile: {tile["x"]},{tile["y"]}')

            # Create "tile present" file
            with open(out_file_map + '.lzma.17', mode='wb') as tile_present_file:
                tile_present_file.close()

            tile_count += 1

        log.info('+ Creating .map files for tiles: OK')

    def make_and_zip_files(self, extension, zip_folder):
        """
        make or make and zip .map or .map.lzma files
        extension: '.map.lzma' for Wahoo tiles
        extension: '.map' for Cruiser map files
        """

        if extension == '.map.lzma':
            folder_name = self.o_osm_data.country_name
        else:
            folder_name = self.o_osm_data.country_name + '-maps'

        log.info('-' * 80)
        log.info('# Create: %s files', extension)
        log.info('+ Country: %s', self.o_osm_data.country_name)

        # Check for us/utah etc names
        try:
            res = self.o_osm_data.country_name.index('/')
            self.o_osm_data.country_name = self.o_osm_data.country_name[res+1:]
        except ValueError:
            pass

        # copy the needed tiles to the country folder
        log.info('+ Copying %s tiles to output folders', extension)
        for tile in self.o_osm_data.tiles:
            src = os.path.join(f'{USER_OUTPUT_DIR}',
                               f'{tile["x"]}', f'{tile["y"]}') + extension
            dst = os.path.join(
                f'{USER_WAHOO_MC}', folder_name, f'{tile["x"]}', f'{tile["y"]}') + extension
            self.copy_to_dst(extension, src, dst)

            if extension == '.map.lzma':
                src = src + '.17'
                dst = dst + '.17'
                self.copy_to_dst(extension, src, dst)

        if zip_folder:
            # Windows
            if platform.system() == "Windows":
                cmd = [get_tooling_win_path(['7za']), 'a', '-tzip']

                cmd.extend(
                    [folder_name + '.zip', os.path.join(".", folder_name, "*")])

            # Non-Windows
            else:
                cmd = ['zip', '-r']

                cmd.extend(
                    [folder_name + '.zip', folder_name])

            run_subprocess_and_log_output(
                cmd, f'! Error zipping map files for folder: {folder_name}', cwd=USER_WAHOO_MC)

            # Delete the country/region map folders after compression
            try:
                shutil.rmtree(os.path.join(
                    f'{USER_WAHOO_MC}', folder_name))
            except OSError:
                log.error(
                    '! Error, could not delete folder %s', os.path.join(USER_WAHOO_MC, folder_name))

            log.info('+ Zip %s files: OK', extension)

        log.info('+ Create %s files: OK', extension)

    def copy_to_dst(self, extension, src, dst):
        """
        Zip .map or .map.lzma files
        postfix: '.map.lzma' for Wahoo tiles
        postfix: '.map' for Cruiser map files
        """
        outdir = os.path.dirname(dst)

        # first create the to-directory if not already there
        os.makedirs(outdir, exist_ok=True)

        try:
            shutil.copy2(src, dst)
        except Exception as exception:  # pylint: disable=broad-except
            log.error(
                '! Error copying %s files for country %s: %s', extension, self.o_osm_data.country_name, exception)
            sys.exit()

    def write_country_config_file(self, country):
        """
        Write country config file into _tiles/{country} directory
        """
        # Data to be written
        configuration = {
            "version_last_run": VERSION,
            "tags_last_run": translate_tags_to_keep()
        }

        write_json_file_generic(os.path.join(
            USER_OUTPUT_DIR, country, ".config.json"), configuration)

    def tags_are_identical_to_last_run(self, country):
        """
        compare tags of this run with used tags from last run stored in _tiles/{country} directory
        """
        tags_are_identical = True

        try:
            country_config = read_json_file(os.path.join(
                USER_OUTPUT_DIR, country, ".config.json"))
            if not country_config["tags_last_run"] == translate_tags_to_keep(sys_platform=platform.system()):
                tags_are_identical = False
        except (FileNotFoundError, KeyError):
            tags_are_identical = False

        return tags_are_identical
