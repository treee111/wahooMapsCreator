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

# import custom python packages
from common_python import file_directory_functions as fd_fct
from common_python import constants
from common_python import constants_functions as const_fct

from common_python.downloader import Downloader
from common_python.geofabrik import Geofabrik


class OsmMaps:
    """
    This is a OSM data class
    """

    osmosis_win_file_path = os.path.join(
        fd_fct.TOOLING_WIN_DIR, 'Osmosis', 'bin', 'osmosis.bat')

    def __init__(self, oInputData):
        self.force_processing = ''
        # Number of workers for the Osmosis read binary fast function
        self.workers = '1'

        self.tiles = []
        self.border_countries = {}
        self.country_name = ''

        self.o_input_data = oInputData
        self.o_downloader = Downloader(
            oInputData.max_days_old, oInputData.force_download)

        if 8 * struct.calcsize("P") == 32:
            self.osmconvert_path = os.path.join(
                fd_fct.TOOLING_WIN_DIR, 'osmconvert')
        else:
            self.osmconvert_path = os.path.join(
                fd_fct.TOOLING_WIN_DIR, 'osmconvert64-0.8.8p')

    def process_input(self, input_argument, calc_border_countries):
        """
        get relevant tiles for given input and calc border countries of these tiles
        """

        # logging
        print(f'+ Input country or json file: {input_argument}.')

        # option 1: have a .json file as input parameter
        if os.path.isfile(input_argument):
            self.tiles = fd_fct.read_json_file(input_argument)

            # country name is the last part of the input filename
            self.country_name = os.path.split(input_argument)[1][:-5]

        # option 2: input a country as parameter, e.g. germany
        else:
            # option 2a: use Geofabrik-URL to calculate the relevant tiles
            if self.o_input_data.geofabrik_tiles:
                self.force_processing = self.o_downloader.check_and_download_geofabrik_if_needed()

                o_geofabrik = Geofabrik(input_argument)
                self.tiles = o_geofabrik.get_tiles_of_country()

            # option 2b: use static json files in the repo to calculate relevant tiles
            else:
                json_file_path = os.path.join(fd_fct.COMMON_DIR, 'json',
                                              const_fct.get_region_of_country(input_argument), input_argument + '.json')
                self.tiles = fd_fct.read_json_file(json_file_path)

            # country name is the input argument
            self.country_name = input_argument

        # Build list of countries needed
        self.border_countries = {}
        if calc_border_countries or os.path.isfile(input_argument):
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
        print(f'+ Count of Border countries: {len(self.border_countries)}')
        for country in self.border_countries:
            print(f'+ Border country: {country}')

    def filter_tags_from_country_osm_pbf_files(self):
        """
        Filter tags from country osm.pbf files
        """

        print('\n# Filter tags from country osm.pbf files')

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
                    print(f'\n+ Converting map of {key} to o5m format')
                    cmd = [self.osmconvert_path]
                    cmd.extend(['-v', '--hash-memory=2500', '--complete-ways',
                                '--complete-multipolygons', '--complete-boundaries',
                                '--drop-author', '--drop-version'])
                    cmd.append(val['map_file'])
                    cmd.append('-o='+out_file_o5m)

                    result = subprocess.run(cmd, check=True)
                    if result.returncode != 0:
                        print(f'Error in OSMConvert with country: {key}')
                        sys.exit()

                    print(
                        f'\n# Filtering unwanted map objects out of map of {key}')
                    cmd = [os.path.join(fd_fct.TOOLING_WIN_DIR, 'osmfilter')]
                    cmd.append(out_file_o5m)
                    cmd.append('--keep="' + constants.FILTERED_TAGS_WIN + '"')
                    cmd.append('--keep-tags=all type= layer= "' +
                               constants.FILTERED_TAGS_WIN + '"')
                    cmd.append('-o=' + out_file_o5m_filtered)

                    result = subprocess.run(cmd, check=True)
                    if result.returncode != 0:
                        print(f'Error in OSMFilter with country: {key}')
                        sys.exit()

                    cmd = [os.path.join(fd_fct.TOOLING_WIN_DIR, 'osmfilter')]
                    cmd.append(out_file_o5m)
                    cmd.append(
                        '--keep="' + constants.FILTERED_TAGS_WIN_NAMES + '"')
                    cmd.append('--keep-tags=all type= name= layer= "' +
                               constants.FILTERED_TAGS_WIN_NAMES + '"')
                    cmd.append('-o=' + out_file_o5m_filtered_names)

                    result = subprocess.run(cmd, check=True)
                    if result.returncode != 0:
                        print(f'Error in OSMFilter with country: {key}')
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
                    print(f'+ Create filtered country file for {key}')

                    # https://docs.osmcode.org/osmium/latest/osmium-tags-filter.html
                    cmd = ['osmium', 'tags-filter', '--remove-tags']
                    cmd.append(val['map_file'])
                    cmd.extend(constants.FILTERED_TAGS)
                    cmd.extend(['-o', out_file_o5m_filtered])
                    cmd.append('--overwrite')

                    result = subprocess.run(cmd, check=True)
                    if result.returncode != 0:
                        print(f'Error in Osmium with country: {key}')
                        sys.exit()

                    cmd = ['osmium', 'tags-filter', '--remove-tags']
                    cmd.append(val['map_file'])
                    cmd.extend(constants.FILTERED_TAGS_NAMES)
                    cmd.extend(['-o', out_file_o5m_filtered_names])
                    cmd.append('--overwrite')

                    result = subprocess.run(cmd, check=True)
                    if result.returncode != 0:
                        print(f'Error in Osmium with country: {key}')
                        sys.exit()

                val['filtered_file'] = out_file_o5m_filtered
                val['filtered_file_names'] = out_file_o5m_filtered_names

        # logging
        print('# Filter tags from country osm.pbf files: OK')

    def generate_land(self):
        """
        Generate land for all tiles
        """

        print('\n# Generate land')

        tile_count = 1
        for tile in self.tiles:
            land_file = os.path.join(fd_fct.OUTPUT_DIR,
                                     f'{tile["x"]}', f'{tile["y"]}', 'land.shp')
            out_file = os.path.join(fd_fct.OUTPUT_DIR,
                                    f'{tile["x"]}', f'{tile["y"]}', 'land')

            # create land.dbf, land.prj, land.shp, land.shx
            if not os.path.isfile(land_file) or self.force_processing is True:
                print(
                    f'+ Generate land {tile_count} of {len(self.tiles)} for Coordinates: {tile["x"]},{tile["y"]}')
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

                subprocess.run(cmd, check=True)

            # create land1.osm
            if not os.path.isfile(out_file+'1.osm') or self.force_processing is True:
                # Windows
                if platform.system() == "Windows":
                    cmd = ['python', os.path.join(fd_fct.TOOLING_DIR,
                                                  'shape2osm.py'), '-l', out_file, land_file]
                    # new shapefile for python 3 ?!
                    #   'shape2osm', 'shape2osm.py'), land_file, out_file+'1.osm']

                # Non-Windows
                else:
                    cmd = ['python3', os.path.join(fd_fct.TOOLING_DIR,
                                                   'shape2osm.py'), '-l', out_file, land_file]

                subprocess.run(cmd, check=True)
            tile_count += 1

        # logging
        print('# Generate land: OK')

    def generate_sea(self):
        """
        Generate sea for all tiles
        """

        print('\n# Generate sea')

        tile_count = 1
        for tile in self.tiles:
            out_file = os.path.join(fd_fct.OUTPUT_DIR,
                                    f'{tile["x"]}', f'{tile["y"]}', 'sea.osm')
            if not os.path.isfile(out_file) or self.force_processing is True:
                print(
                    f'+ Generate sea {tile_count} of {len(self.tiles)} for Coordinates: {tile["x"]},{tile["y"]}')
                with open(os.path.join(fd_fct.TOOLING_DIR, 'sea.osm')) as sea_file:
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
        print('# Generate sea: OK')

    def split_filtered_country_files_to_tiles(self):
        """
        Split filtered country files to tiles
        """

        print('\n# Split filtered country files to tiles')
        tile_count = 1
        for tile in self.tiles:

            for country, val in self.border_countries.items():
                print(
                    f'+ Splitting tile {tile_count} of {len(self.tiles)} for Coordinates: {tile["x"]},{tile["y"]} from map of {country}')
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

                        result = subprocess.run(cmd, check=True)
                        if result.returncode != 0:
                            print(f'Error in Osmosis with country: {country}')
                            sys.exit()

                        cmd = [self.osmconvert_path,
                               '-v', '--hash-memory=2500']
                        cmd.append('-b='+f'{tile["left"]}' + ',' + f'{tile["bottom"]}' +
                                   ',' + f'{tile["right"]}' + ',' + f'{tile["top"]}')
                        cmd.extend(
                            ['--complete-ways', '--complete-multipolygons', '--complete-boundaries'])
                        cmd.append(val['filtered_file_names'])
                        cmd.append('-o='+out_file_names)

                        result = subprocess.run(cmd, check=True)
                        if result.returncode != 0:
                            print(f'Error in Osmosis with country: {country}')
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

                        result = subprocess.run(cmd, check=True)
                        if result.returncode != 0:
                            print(f'Error in Osmium with country: {country}')
                            sys.exit()

                        cmd = ['osmium', 'extract']
                        cmd.extend(
                            ['-b', f'{tile["left"]},{tile["bottom"]},{tile["right"]},{tile["top"]}'])
                        cmd.append(val['filtered_file_names'])
                        cmd.extend(['-s', 'smart'])
                        cmd.extend(['-o', out_file_names])
                        cmd.extend(['--overwrite'])

                        # print(cmd)
                        result = subprocess.run(cmd, check=True)
                        if result.returncode != 0:
                            print(f'Error in Osmium with country: {country}')
                            sys.exit()

                        print(val['filtered_file'])

            tile_count += 1

        print('# Split filtered country files to tiles: OK')

    def merge_splitted_tiles_with_land_and_sea(self, calc_border_countries):
        """
        Merge splitted tiles with land an sea
        """

        print('\n# Merge splitted tiles with land an sea')
        tile_count = 1
        for tile in self.tiles:
            print(
                f'+ Merging tiles for tile {tile_count} of {len(self.tiles)} for Coordinates: {tile["x"]},{tile["y"]}')

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

                result = subprocess.run(cmd, check=True)
                if result.returncode != 0:
                    print(
                        f'Error in Osmosis with tile: {tile["x"]},{tile["y"]}')
                    sys.exit()

            tile_count += 1

        # logging
        print('# Merge splitted tiles with land an sea: OK')

    def sort_osm_files(self, tile):
        """
        sort land*.osm files to be in this order: nodes, then ways, then relations.
        this is mandatory for osmium-merge since:
        https://github.com/osmcode/osmium-tool/releases/tag/v1.13.2
        """

        print('\n# Sorting land* osm files')

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

        result = subprocess.run(cmd, check=True)

        if result.returncode != 0:
            print(
                f'Error in Osmosis with sorting land* osm files of tile: {tile["x"]},{tile["y"]}')
            sys.exit()

        # logging
        print('# Sorting land* osm files: OK')

    def create_map_files(self, save_cruiser, tag_wahoo_xml):
        """
        Creating .map files
        """

        print('\n# Creating .map files')

        # Number of threads to use in the mapwriter plug-in
        threads = str(multiprocessing.cpu_count() - 1)
        if int(threads) < 1:
            threads = 1

        tile_count = 1
        for tile in self.tiles:
            print(
                f'+ Creating map file for tile {tile_count} of {len(self.tiles)} for Coordinates: {tile["x"]},{tile["y"]}')
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

                result = subprocess.run(cmd, check=True)
                if result.returncode != 0:
                    print(
                        f'Error in Osmosis with country: c // tile: {tile["x"]}, {tile["y"]}')
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

                subprocess.run(cmd, check=True)

            # Create "tile present" file
            with open(out_file + '.lzma.12', 'wb') as tile_present_file:
                tile_present_file.close()

            tile_count += 1

        # logging
        print('# Creating .map files: OK')

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

        print(f'\n# Zip: {extension} files')
        print(f'+ Country: {self.country_name}')

        # Check for us/utah etc names
        try:
            res = self.country_name.index('/')
            self.country_name = self.country_name[res+1:]
        except ValueError:
            pass

        # copy the needed tiles to the country folder
        print(f'Copying {extension} tiles to output folders')
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
            except:
                print(
                    f'Error copying {extension} files of country {self.country_name}')
                sys.exit()

        if extension == '.map.lzma':
            src = src + '.12'
            dst = dst + '.12'
            if not os.path.isdir(outdir):
                os.makedirs(outdir)
            try:
                shutil.copy2(src, dst)
            except:
                print(
                    f'Error copying precense files of country {self.country_name}')
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

        subprocess.run(cmd, cwd=fd_fct.OUTPUT_DIR, check=True)

        # Keep (True) or delete (False) the country/region map folders after compression
        if keep_map_folders is False:
            try:
                shutil.rmtree(os.path.join(
                    f'{fd_fct.OUTPUT_DIR}', folder_name))
            except OSError:
                print(
                    f'Error, could not delete folder \
                        {os.path.join(fd_fct.OUTPUT_DIR, folder_name)}')

        # logging
        print('# Zip .map.lzma files: OK \n')
