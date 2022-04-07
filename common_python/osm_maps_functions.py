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
from common_python import file_directory_functions as fd_fct
from common_python import constants
from common_python import constants_functions as const_fct

from common_python.downloader import Downloader
from common_python.geofabrik import Geofabrik

log = logging.getLogger('main-logger')


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
    file_path_jsons = os.path.join(fd_fct.COMMON_DIR, 'json')

    for folder in fd_fct.get_folders_in_folder(file_path_jsons):
        for file in fd_fct.get_filenames_of_jsons_in_folder(os.path.join(file_path_jsons, folder)):

            # get content of json in folder
            content = fd_fct.read_json_file(
                os.path.join(file_path_jsons, folder, file + '.json'))

            # check tiles values against input x/y combination
            for tile in content:
                if tile['x'] == xy_combination['x'] and tile['y'] == xy_combination['y']:
                    return tile


def log_subprocess_output(pipe):
    for line in iter(pipe.readline, b''):  # b'\n'-separated lines
        log.info('subprocess:%r', line.decode("utf-8").strip())


def run_subprocess_and_log_output(cmd, cwd=""):
    if not cwd:
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)

    with process.stdout:
        # log_subprocess_output(process.stdout)
        for line in iter(process.stdout.readline, b''):  # b'\n'-separated lines
            log.debug('subprocess:%r', line.decode("utf-8").strip())
    return process.wait()  # 0 means success


class OsmMaps:
    """
    This is a OSM data class
    """

    osmosis_win_file_path = os.path.join(
        fd_fct.TOOLING_WIN_DIR, 'Osmosis', 'bin', 'osmosis.bat')

    def __init__(self, o_input_data):
        self.force_processing = ''
        # Number of workers for the Osmosis read binary fast function
        self.workers = '1'

        self.tiles = []
        self.border_countries = {}
        self.country_name = ''

        self.o_input_data = o_input_data
        self.o_downloader = Downloader(
            o_input_data.max_days_old, o_input_data.force_download)

        if 8 * struct.calcsize("P") == 32:
            self.osmconvert_path = os.path.join(
                fd_fct.TOOLING_WIN_DIR, 'osmconvert')
        else:
            self.osmconvert_path = os.path.join(
                fd_fct.TOOLING_WIN_DIR, 'osmconvert64-0.8.8p')

    def process_input(self, calc_border_countries):
        """
        Process input: get relevant tiles and if border countries should be calculated
        The three primary inputs are giving by a separate value each and have separate processing:
        1. .json file with tiles
        2. country name
        3. x/y combinations
        """
        # option 1: have a .json file as input parameter
        if self.o_input_data.tile_file:
            # logging
            log.info(f'+ Input json file: {self.o_input_data.tile_file}.')

            if os.path.isfile(self.o_input_data.tile_file):
                self.tiles = fd_fct.read_json_file(self.o_input_data.tile_file)

                # country name is the last part of the input filename
                self.country_name = os.path.split(
                    self.o_input_data.tile_file)[1][:-5]

                # calc border country when input tiles via json file
                calc_border_countries = True

        # option 2: input a country as parameter, e.g. germany
        elif self.o_input_data.country:
            # logging
            log.info(f'+ Input country : {self.o_input_data.country}.')

            # option 2a: use Geofabrik-URL to calculate the relevant tiles
            if self.o_input_data.geofabrik_tiles:
                self.force_processing = self.o_downloader.check_and_download_geofabrik_if_needed()

                o_geofabrik = Geofabrik(self.o_input_data.country)
                self.tiles = o_geofabrik.get_tiles_of_country()

            # option 2b: use static json files in the repo to calculate relevant tiles
            else:
                json_file_path = os.path.join(fd_fct.COMMON_DIR, 'json',
                                              const_fct.get_region_of_country(self.o_input_data.country), self.o_input_data.country + '.json')
                self.tiles = fd_fct.read_json_file(json_file_path)

            # country name is the input argument
            self.country_name = self.o_input_data.country

        # option 3: input a x/y combinations as parameter, e.g. 134/88  or 133/88,130/100
        elif self.o_input_data.xy_coordinates:
            # logging
            log.info(
                f'+ Input X/Y coordinates : {self.o_input_data.xy_coordinates}.')

            # # option 3a: use Geofabrik-URL to get the relevant tiles
            if self.o_input_data.geofabrik_tiles:
                sys.exit("X/Y coordinated via Geofabrik not implemented now")

            # option 3b: use static json files in the repo to get relevant tiles
            else:
                xy_coordinates = get_xy_coordinates_from_input(
                    self.o_input_data.xy_coordinates)

                # loop through x/y combinations and find each tile in the json files
                for xy_comb in xy_coordinates:
                    self.tiles.append(get_tile_by_one_xy_combination_from_jsons(
                        xy_comb))

                    # country name is the X/Y combinations separated by minus
                    # >1 x/y combinations are separated by underscore
                    if not self.country_name:
                        self.country_name = f'{xy_comb["x"]}-{xy_comb["y"]}'
                    else:
                        self.country_name = f'{self.country_name}_{xy_comb["x"]}-{xy_comb["y"]}'

            # calc border country when input X/Y coordinates
            calc_border_countries = True

        # Build list of countries needed
        self.border_countries = {}
        if calc_border_countries:
            self.calc_border_countries()
        else:
            self.border_countries[self.country_name] = {}

    def check_and_download_files(self):
        """
        trigger check of land_polygons and OSM map files if not existing or are not up-to-date
        """

        self.o_downloader.tiles_from_json = self.tiles
        self.o_downloader.border_countries = self.border_countries

        force_processing = self.o_downloader.check_and_download_files_if_needed()

        # if download is needed or force_processing given via input --> force_processing = True
        if force_processing or self.o_input_data.force_processing or self.force_processing:
            self.force_processing = True
        else:
            self.force_processing = False

    def calc_border_countries(self):
        """
        calculate relevant border countries for the given tiles
        """

        # Build list of countries needed
        for tile in self.tiles:
            for country in tile['countries']:
                if country not in self.border_countries:
                    self.border_countries[country] = {}

        # logging
        log.info(f'+ Count of Border countries: {len(self.border_countries)}')
        for country in self.border_countries:
            log.info(f'+ Border country: {country}')

    def filter_tags_from_country_osm_pbf_files(self):
        """
        Filter tags from country osm.pbf files
        """

        log.info('# Filter tags from country osm.pbf files')

        # Windows
        if platform.system() == "Windows":
            for key, val in self.border_countries.items():
                out_file_o5m = os.path.join(fd_fct.OUTPUT_DIR,
                                            f'outFile-{key}.o5m')
                out_file_o5m_filtered = os.path.join(fd_fct.OUTPUT_DIR,
                                                     f'outFileFiltered-{key}.o5m')
                out_file_o5m_filtered_names = os.path.join(fd_fct.OUTPUT_DIR,
                                                           f'outFileFiltered-{key}-Names.o5m')

                if not os.path.isfile(out_file_o5m_filtered) or self.force_processing is True:
                    log.info('+ Converting map of %s to o5m format', key)
                    cmd = [self.osmconvert_path]
                    cmd.extend(['-v', '--hash-memory=2500', '--complete-ways',
                                '--complete-multipolygons', '--complete-boundaries',
                                '--drop-author', '--drop-version'])
                    cmd.append(val['map_file'])
                    cmd.append('-o='+out_file_o5m)

                    result = run_subprocess_and_log_output(cmd)
                    if result != 0:
                        log.error('Error in OSMConvert with country: %s', key)
                        sys.exit()

                    log.info(
                        '# Filtering unwanted map objects out of map of %s', key)
                    cmd = [os.path.join(fd_fct.TOOLING_WIN_DIR, 'osmfilter')]
                    cmd.append(out_file_o5m)
                    cmd.append('--keep="' + constants.FILTERED_TAGS_WIN + '"')
                    cmd.append('--keep-tags=all type= layer= "' +
                               constants.FILTERED_TAGS_WIN + '"')
                    cmd.append('-o=' + out_file_o5m_filtered)

                    result = run_subprocess_and_log_output(cmd)
                    if result != 0:
                        log.error('Error in OSMFilter with country: %s', key)
                        sys.exit()

                    cmd = [os.path.join(fd_fct.TOOLING_WIN_DIR, 'osmfilter')]
                    cmd.append(out_file_o5m)
                    cmd.append(
                        '--keep="' + constants.FILTERED_TAGS_WIN_NAMES + '"')
                    cmd.append('--keep-tags=all type= name= layer= "' +
                               constants.FILTERED_TAGS_WIN_NAMES + '"')
                    cmd.append('-o=' + out_file_o5m_filtered_names)

                    result = run_subprocess_and_log_output(cmd)
                    if result != 0:
                        log.error('Error in OSMFilter with country: %s', key)
                        sys.exit()

                    os.remove(out_file_o5m)

                val['filtered_file'] = out_file_o5m_filtered
                val['filtered_file_names'] = out_file_o5m_filtered_names

        # Non-Windows
        else:
            for key, val in self.border_countries.items():
                out_file_o5m_filtered = os.path.join(fd_fct.OUTPUT_DIR,
                                                     f'filtered-{key}.o5m.pbf')
                out_file_o5m_filtered_names = os.path.join(fd_fct.OUTPUT_DIR,
                                                           f'outFileFiltered-{key}-Names.o5m.pbf')
                if not os.path.isfile(out_file_o5m_filtered) or self.force_processing is True:
                    log.info('+ Create filtered country file for %s', key)

                    # https://docs.osmcode.org/osmium/latest/osmium-tags-filter.html
                    cmd = ['osmium', 'tags-filter', '--remove-tags']
                    cmd.append(val['map_file'])
                    cmd.extend(constants.FILTERED_TAGS)
                    cmd.extend(['-o', out_file_o5m_filtered])
                    cmd.append('--overwrite')

                    result = run_subprocess_and_log_output(cmd)
                    if result != 0:
                        log.error('Error in Osmium with country: %s', key)
                        sys.exit()

                    cmd = ['osmium', 'tags-filter', '--remove-tags']
                    cmd.append(val['map_file'])
                    cmd.extend(constants.FILTERED_TAGS_NAMES)
                    cmd.extend(['-o', out_file_o5m_filtered_names])
                    cmd.append('--overwrite')

                    result = run_subprocess_and_log_output(cmd)
                    if result != 0:
                        log.error('Error in Osmium with country: %s', key)
                        sys.exit()

                val['filtered_file'] = out_file_o5m_filtered
                val['filtered_file_names'] = out_file_o5m_filtered_names

        # logging
        log.info('# Filter tags from country osm.pbf files: OK')

    def generate_land(self):
        """
        Generate land for all tiles
        """

        log.info('# Generate land')

        tile_count = 1
        for tile in self.tiles:
            land_file = os.path.join(fd_fct.OUTPUT_DIR,
                                     f'{tile["x"]}', f'{tile["y"]}', 'land.shp')
            out_file = os.path.join(fd_fct.OUTPUT_DIR,
                                    f'{tile["x"]}', f'{tile["y"]}', 'land')

            # create land.dbf, land.prj, land.shp, land.shx
            if not os.path.isfile(land_file) or self.force_processing is True:
                log.info(
                    '+ Generate land %s of %s for Coordinates: %s,%s', tile_count, len(self.tiles), tile["x"], tile["y"])
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
                cmd.append(fd_fct.LAND_POLYGONS_PATH)

                result = run_subprocess_and_log_output(cmd)

            # create land1.osm
            if not os.path.isfile(out_file+'1.osm') or self.force_processing is True:
                # Windows
                if platform.system() == "Windows":
                    cmd = ['python', os.path.join(fd_fct.COMMON_DIR,
                                                  'shape2osm.py'), '-l', out_file, land_file]

                # Non-Windows
                else:
                    cmd = ['python3', os.path.join(fd_fct.COMMON_DIR,
                                                   'shape2osm.py'), '-l', out_file, land_file]

                result = run_subprocess_and_log_output(cmd)
            tile_count += 1

        # logging
        log.info('# Generate land: OK')

    def generate_sea(self):
        """
        Generate sea for all tiles
        """

        log.info('# Generate sea')

        tile_count = 1
        for tile in self.tiles:
            out_file = os.path.join(fd_fct.OUTPUT_DIR,
                                    f'{tile["x"]}', f'{tile["y"]}', 'sea.osm')
            if not os.path.isfile(out_file) or self.force_processing is True:
                log.info(
                    '+ Generate sea %s of %s for Coordinates: %s,%s', tile_count, len(self.tiles), tile["x"], tile["y"])
                with open(os.path.join(fd_fct.COMMON_DIR, 'sea.osm')) as sea_file:
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

                    with open(out_file, 'w') as output_file:
                        output_file.write(sea_data)
            tile_count += 1

        # logging
        log.info('# Generate sea: OK')

    def split_filtered_country_files_to_tiles(self):
        """
        Split filtered country files to tiles
        """

        log.info('# Split filtered country files to tiles')
        tile_count = 1
        for tile in self.tiles:

            for country, val in self.border_countries.items():
                log.info(
                    '+ Splitting tile %s of %s for Coordinates: %s,%s from map of %s', tile_count, len(self.tiles), tile["x"], tile["y"], country)
                out_file = os.path.join(fd_fct.OUTPUT_DIR,
                                        f'{tile["x"]}', f'{tile["y"]}', f'split-{country}.osm.pbf')
                out_file_names = os.path.join(fd_fct.OUTPUT_DIR,
                                              f'{tile["x"]}', f'{tile["y"]}', f'split-{country}-names.osm.pbf')
                out_merged = os.path.join(fd_fct.OUTPUT_DIR,
                                          f'{tile["x"]}', f'{tile["y"]}', 'merged.osm.pbf')
                if not os.path.isfile(out_merged) or self.force_processing is True:
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

                        result = run_subprocess_and_log_output(cmd)
                        if result != 0:
                            log.error(
                                'Error in Osmosis with country: %s', country)
                            sys.exit()

                        cmd = [self.osmconvert_path,
                               '-v', '--hash-memory=2500']
                        cmd.append('-b='+f'{tile["left"]}' + ',' + f'{tile["bottom"]}' +
                                   ',' + f'{tile["right"]}' + ',' + f'{tile["top"]}')
                        cmd.extend(
                            ['--complete-ways', '--complete-multipolygons', '--complete-boundaries'])
                        cmd.append(val['filtered_file_names'])
                        cmd.append('-o='+out_file_names)

                        result = run_subprocess_and_log_output(cmd)
                        if result != 0:
                            log.error(
                                'Error in Osmosis with country: %s', country)
                            sys.exit()

                    # Non-Windows
                    else:
                        cmd = ['osmium', 'extract']
                        cmd.extend(
                            ['-b', f'{tile["left"]},{tile["bottom"]},{tile["right"]},{tile["top"]}'])
                        cmd.append(val['filtered_file'])
                        cmd.extend(['-s', 'smart'])
                        cmd.extend(['-o', out_file])
                        cmd.extend(['--overwrite'])

                        result = run_subprocess_and_log_output(cmd)
                        if result != 0:
                            log.error(
                                'Error in Osmosis with country: %s', country)
                            sys.exit()

                        cmd = ['osmium', 'extract']
                        cmd.extend(
                            ['-b', f'{tile["left"]},{tile["bottom"]},{tile["right"]},{tile["top"]}'])
                        cmd.append(val['filtered_file_names'])
                        cmd.extend(['-s', 'smart'])
                        cmd.extend(['-o', out_file_names])
                        cmd.extend(['--overwrite'])

                        result = run_subprocess_and_log_output(cmd)
                        if result != 0:
                            log.error(
                                'Error in Osmosis with country: %s', country)
                            sys.exit()

                        log.info(val['filtered_file'])

            tile_count += 1

        log.info('# Split filtered country files to tiles: OK')

    def merge_splitted_tiles_with_land_and_sea(self, calc_border_countries):
        """
        Merge splitted tiles with land an sea
        """

        log.info('# Merge splitted tiles with land an sea')
        tile_count = 1
        for tile in self.tiles:
            log.info(
                '+ Merging tiles for tile %s of %s for Coordinates: %s,%s', tile_count, len(self.tiles), tile["x"], tile["y"])

            out_tile_dir = os.path.join(fd_fct.OUTPUT_DIR,
                                        f'{tile["x"]}', f'{tile["y"]}')
            out_file = os.path.join(out_tile_dir, 'merged.osm.pbf')

            land_files = glob.glob(os.path.join(out_tile_dir, 'land*.osm'))

            if not os.path.isfile(out_file) or self.force_processing is True:
                # sort land* osm files
                self.sort_osm_files(tile)

                # Windows
                if platform.system() == "Windows":
                    cmd = [self.osmosis_win_file_path]
                    loop = 0
                    # loop through all countries of tile, if border-countries should be processed.
                    # if border-countries should not be processed, only process the "entered" country
                    for country in tile['countries']:
                        if calc_border_countries or country in self.border_countries:
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
                    cmd.extend(['--tag-transform', 'file=' + os.path.join(fd_fct.COMMON_DIR,
                                                                          'tunnel-transform.xml'), '--wb', out_file, 'omitmetadata=true'])

                # Non-Windows
                else:
                    cmd = ['osmium', 'merge', '--overwrite']
                    # loop through all countries of tile, if border-countries should be processed.
                    # if border-countries should not be processed, only process the "entered" country
                    for country in tile['countries']:
                        if calc_border_countries or country in self.border_countries:
                            cmd.append(os.path.join(
                                out_tile_dir, f'split-{country}.osm.pbf'))
                            cmd.append(os.path.join(
                                out_tile_dir, f'split-{country}-names.osm.pbf'))

                    for land in land_files:
                        cmd.append(land)
                    cmd.append(os.path.join(out_tile_dir, 'sea.osm'))
                    cmd.extend(['-o', out_file])

                result = run_subprocess_and_log_output(cmd)
                if result != 0:
                    log.error(
                        'Error in Osmosis with tile: %s,%s', tile["x"], tile["y"])
                    sys.exit()

            tile_count += 1

        # logging
        log.info('# Merge splitted tiles with land an sea: OK')

    def sort_osm_files(self, tile):
        """
        sort land*.osm files to be in this order: nodes, then ways, then relations.
        this is mandatory for osmium-merge since:
        https://github.com/osmcode/osmium-tool/releases/tag/v1.13.2
        """

        log.info('# Sorting land* osm files')

        # get all land* osm files
        land_files = glob.glob(os.path.join(fd_fct.OUTPUT_DIR,
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

        result = run_subprocess_and_log_output(cmd)
        if result != 0:
            log.error(
                'Error in Osmosis with sorting land* osm files of tile: %s,%s', tile["x"], tile["y"])
            sys.exit()

        # logging
        log.info('# Sorting land* osm files: OK')

    def create_map_files(self, save_cruiser, tag_wahoo_xml):
        """
        Creating .map files
        """

        log.info('# Creating .map files')

        # Number of threads to use in the mapwriter plug-in
        threads = str(multiprocessing.cpu_count() - 1)
        if int(threads) < 1:
            threads = 1

        tile_count = 1
        for tile in self.tiles:
            log.info(
                '+ Creating map file for tile %s of %s for Coordinates: %s,%s', tile_count, len(self.tiles), tile["x"], tile["y"])
            out_file = os.path.join(fd_fct.OUTPUT_DIR,
                                    f'{tile["x"]}', f'{tile["y"]}.map')
            if not os.path.isfile(out_file+'.lzma') or self.force_processing is True:
                merged_file = os.path.join(fd_fct.OUTPUT_DIR,
                                           f'{tile["x"]}', f'{tile["y"]}', 'merged.osm.pbf')

                # Windows
                if platform.system() == "Windows":
                    cmd = [self.osmosis_win_file_path, '--rbf', merged_file,
                           'workers=' + self.workers, '--mw', 'file='+out_file]
                # Non-Windows
                else:
                    cmd = ['osmosis', '--rb', merged_file,
                           '--mw', 'file='+out_file]

                cmd.append(
                    f'bbox={tile["bottom"]:.6f},{tile["left"]:.6f},{tile["top"]:.6f},{tile["right"]:.6f}')
                cmd.append('zoom-interval-conf=10,0,17')
                cmd.append('threads=' + threads)
                # should work on macOS and Windows
                cmd.append(
                    f'tag-conf-file={os.path.join(fd_fct.COMMON_DIR, "tag_wahoo_adjusted", tag_wahoo_xml)}')

                result = run_subprocess_and_log_output(cmd)
                if result != 0:
                    log.error(
                        'Error in Osmosis with country: c // tile: %s,%s', tile["x"], tile["y"])
                    sys.exit()

                # Windows
                if platform.system() == "Windows":
                    cmd = [os.path.join(fd_fct.TOOLING_WIN_DIR, 'lzma'), 'e', out_file,
                           out_file+'.lzma', f'-mt{threads}', '-d27', '-fb273', '-eos']
                # Non-Windows
                else:
                    # force overwrite of output file and (de)compress links
                    cmd = ['lzma', out_file, '-f']

                    # --keep: do not delete source file
                    if save_cruiser:
                        cmd.append('--keep')

                result = run_subprocess_and_log_output(cmd)

            # Create "tile present" file
            with open(out_file + '.lzma.12', 'wb') as tile_present_file:
                tile_present_file.close()

            tile_count += 1

        # logging
        log.info('# Creating .map files: OK')

    def make_and_zip_files(self, keep_map_folders, extension):
        """
        Zip .map or .map.lzma files
        postfix: '.map.lzma' for Wahoo tiles
        postfix: '.map' for Cruiser map files
        """

        if extension == '.map.lzma':
            folder_name = self.country_name
        else:
            folder_name = self.country_name + '-maps'

        log.info('# Zip: %s files', extension)
        log.info('+ Country: %s', self.country_name)

        # Check for us/utah etc names
        try:
            res = self.country_name.index('/')
            self.country_name = self.country_name[res+1:]
        except ValueError:
            pass

        # copy the needed tiles to the country folder
        log.info('Copying %s tiles to output folders', extension)
        for tile in self.tiles:
            src = os.path.join(f'{fd_fct.OUTPUT_DIR}',
                               f'{tile["x"]}', f'{tile["y"]}') + extension
            dst = os.path.join(
                f'{fd_fct.OUTPUT_DIR}', folder_name, f'{tile["x"]}', f'{tile["y"]}') + extension
            outdir = os.path.join(
                f'{fd_fct.OUTPUT_DIR}', folder_name, f'{tile["x"]}')
            if not os.path.isdir(outdir):
                os.makedirs(outdir)
            try:
                shutil.copy2(src, dst)
            except Exception as exception:
                log.error(
                    'Error copying %s files for country %s: %s', extension, self.country_name, exception)
                sys.exit()

            if extension == '.map.lzma':
                src = src + '.12'
                dst = dst + '.12'
                if not os.path.isdir(outdir):
                    os.makedirs(outdir)
                try:
                    shutil.copy2(src, dst)
                except Exception as exception:
                    log.error(
                        'Error copying version files for country %s: %s', self.country_name, exception)
                    sys.exit()

        # Windows
        if platform.system() == "Windows":
            path_7za = os.path.join(fd_fct.TOOLING_WIN_DIR, '7za')
            cmd = [path_7za, 'a', '-tzip']

            cmd.extend(
                [folder_name + '.zip', os.path.join(".", folder_name, "*")])

        # Non-Windows
        else:
            cmd = ['zip', '-r']

            cmd.extend(
                [folder_name + '.zip', folder_name])

        result = run_subprocess_and_log_output(cmd, cwd=fd_fct.OUTPUT_DIR)

        # Keep (True) or delete (False) the country/region map folders after compression
        if keep_map_folders is False:
            try:
                shutil.rmtree(os.path.join(
                    f'{fd_fct.OUTPUT_DIR}', folder_name))
            except OSError:
                log.error(
                    'Error, could not delete folder %s', os.path.join(fd_fct.OUTPUT_DIR, folder_name))

        # logging
        log.info('# Zip %s files: OK', extension)
