"""
functions and object for managing OSM maps
"""
#!/usr/bin/python

# import official python packages
import glob
import os
import subprocess
import sys
import platform

# import custom python packages
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common_resources import file_directory_functions as fdf
from common_resources import constants
from common_resources import constants_functions

from common_resources.downloader import Downloader


class OsmMaps:
    """
    This is a OSM data class
    """

    def __init__(self, Force_Processing, workers, Save_Cruiser):
        # input parameters
        self.force_processing = Force_Processing
        self.workers = workers
        self.save_cruiser = Save_Cruiser

        self.tiles = []
        self.border_countries = {}
        self.country_name = ''


    def process_input(self, input_argument):
        """
        get relevant tiles for given input and calc border countries of these tiles
        """

        # option 1: have a .json file as input parameter
        if os.path.isfile(input_argument):
            self.tiles = fdf.read_json_file(input_argument)
        # option 2: input a country as parameter, e.g. germany
        else:
            json_file_path = os.path.join (fdf.COMMON_DIR,
                'json', constants_functions.get_region_of_country(input_argument), input_argument + '.json')
            self.tiles = fdf.read_json_file(json_file_path)

        # country name is the input argument or the last part of the input filename
        self.country_name = input_argument
        if self.country_name == '':
            self.country_name = os.path.split(input_argument)[1][:-5]

        # Build list of countries needed
        self.calc_border_countries()


    def check_and_download_files(self, max_days_old, force_download):
        """
        trigger check of land_poligons and OSM map files if not existing or are not up-to-date
        """

        o_downloader = Downloader(max_days_old, force_download, self.tiles, self.border_countries)

        force_processing = o_downloader.check_and_download_files_if_needed()
        if force_processing is True:
            self.force_processing = force_processing


    def calc_border_countries(self):
        """
        calculate relevant border countries for the given tiles
        """

        # Build list of countries needed
        self.border_countries = {}
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
            # print(key, val)
                out_file = os.path.join(fdf.OUTPUT_DIR,
                 f'filtered-{key}.osm.pbf')
                out_file_o5m = os.path.join(fdf.OUTPUT_DIR,
                 f'outFile-{key}.o5m')
                out_file_o5m_filtered = os.path.join(fdf.OUTPUT_DIR,
                 f'outFileFiltered-{key}.o5m')

                if not os.path.isfile(out_file) or self.force_processing is True:
                    print(f'\n+ Converting map of {key} to o5m format')
                    cmd = [os.path.join(fdf.TOOLING_WIN_DIR, 'osmconvert')]
                    cmd.extend(['-v', '--hash-memory=2500', '--complete-ways', '--complete-multipolygons', '--complete-boundaries', '--drop-author', '--drop-version'])
                    cmd.append(val['map_file'])
                    cmd.append('-o='+out_file_o5m)
                    # print(cmd)
                    result = subprocess.run(cmd, check=True)
                    if result.returncode != 0:
                        print(f'Error in OSMConvert with country: {key}')
                        sys.exit()

                    print(f'\n# Filtering unwanted map objects out of map of {key}')
                    cmd = [os.path.join(fdf.TOOLING_WIN_DIR, 'osmfilter')]
                    cmd.append(out_file_o5m)
                    cmd.append('--keep="' + constants.FILTERED_TAGS_WIN + '"')
                    cmd.append('-o=' + out_file_o5m_filtered)
                    # print(cmd)
                    result = subprocess.run(cmd, check=True)
                    if result.returncode != 0:
                        print(f'Error in OSMFilter with country: {key}')
                        sys.exit()

                    print(f'\n# Converting map of {key} back to osm.pbf format')
                    cmd = [os.path.join(fdf.TOOLING_WIN_DIR, 'osmconvert'), '-v', '--hash-memory=2500', out_file_o5m_filtered]
                    cmd.append('-o='+out_file)
                    # print(cmd)
                    result = subprocess.run(cmd, check=True)
                    if result.returncode != 0:
                        print(f'Error in OSMConvert with country: {key}')
                        sys.exit()

                    os.remove(out_file_o5m)
                    os.remove(out_file_o5m_filtered)

                self.border_countries[key]['filtered_file'] = out_file

        # Non-Windows
        else:
            for key, val  in self.border_countries.items():
                ## print(key, val)
                out_file = os.path.join(fdf.OUTPUT_DIR,
                 f'filtered-{key}.osm.pbf')
                ## print(outFile)
                if not os.path.isfile(out_file):
                    print(f'+ Create filtered country file for {key}')

                    cmd = ['osmium', 'tags-filter']
                    cmd.append(val['map_file'])
                    cmd.extend(constants.filtered_tags)
                    cmd.extend(['-o', out_file])
                    # print(cmd)
                    subprocess.run(cmd, check=True)
                self.border_countries[key]['filtered_file'] = out_file

        # logging
        print('# Filter tags from country osm.pbf files: OK')


    def generate_land(self):
        """
        Generate land for all tiles
        """

        print('\n# Generate land')

        tile_count = 1
        for tile in self.tiles:
            land_file = os.path.join(fdf.OUTPUT_DIR,
             f'{tile["x"]}', f'{tile["y"]}', 'land.shp')
            out_file = os.path.join(fdf.OUTPUT_DIR,
             f'{tile["x"]}', f'{tile["y"]}', 'land')

            if not os.path.isfile(land_file) or self.force_processing is True:
                print(f'+ Generate land {tile_count} of {len(self.tiles)} for Coordinates: {tile["x"]} {tile["y"]}')
                cmd = ['ogr2ogr', '-overwrite', '-skipfailures']
                cmd.extend(['-spat', f'{tile["left"]-0.1:.6f}',
                            f'{tile["bottom"]-0.1:.6f}',
                            f'{tile["right"]+0.1:.6f}',
                            f'{tile["top"]+0.1:.6f}'])
                cmd.append(land_file)
                cmd.append(fdf.LAND_POLYGONS_PATH)
                #print(cmd)
                subprocess.run(cmd, check=True)

            if not os.path.isfile(out_file+'1.osm') or self.force_processing is True:
                # Windows
                if platform.system() == "Windows":
                    cmd = ['python', os.path.join(fdf.COMMON_DIR,
                     'shape2osm.py'), '-l', out_file, land_file]
                # Non-Windows
                else:
                    cmd = ['python3', os.path.join(fdf.COMMON_DIR,
                     'shape2osm.py'), '-l', out_file, land_file]
                #print(cmd)
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
            out_file = os.path.join(fdf.OUTPUT_DIR,
             f'{tile["x"]}', f'{tile["y"]}', 'sea.osm')
            if not os.path.isfile(out_file) or self.force_processing is True:
                print(f'+ Generate sea {tile_count} of {len(self.tiles)} for Coordinates: {tile["x"]} {tile["y"]}')
                with open(os.path.join(fdf.COMMON_DIR, 'sea.osm')) as sea_file:
                    sea_data = sea_file.read()

                    sea_data = sea_data.replace('$LEFT', f'{tile["left"]-0.1:.6f}')
                    sea_data = sea_data.replace('$BOTTOM',f'{tile["bottom"]-0.1:.6f}')
                    sea_data = sea_data.replace('$RIGHT',f'{tile["right"]+0.1:.6f}')
                    sea_data = sea_data.replace('$TOP',f'{tile["top"]+0.1:.6f}')

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

            for country in tile['countries']:
                print(f'+ Split filtered country {country}')
                print(f'+ Splitting tile {tile_count} of {len(self.tiles)} for Coordinates: {tile["x"]},{tile["y"]} from map of {country}')
                out_file = os.path.join(fdf.OUTPUT_DIR,
                 f'{tile["x"]}', f'{tile["y"]}', f'split-{country}.osm.pbf')
                if not os.path.isfile(out_file) or self.force_processing is True:
                    # Windows
                    if platform.system() == "Windows":
                        #cmd = ['.\\osmosis\\bin\\osmosis.bat', '--rbf',border_countries[c]['filtered_file'],'workers='+workers, '--buffer', 'bufferCapacity=12000', '--bounding-box', 'completeWays=yes', 'completeRelations=yes']
                        #cmd.extend(['left='+f'{tile["left"]}', 'bottom='+f'{tile["bottom"]}', 'right='+f'{tile["right"]}', 'top='+f'{tile["top"]}', '--buffer', 'bufferCapacity=12000', '--wb'])
                        #cmd.append('file='+outFile)
                        #cmd.append('omitmetadata=true')
                        cmd = [os.path.join(fdf.TOOLING_WIN_DIR, 'osmconvert'), '-v', '--hash-memory=2500']
                        cmd.append('-b='+f'{tile["left"]}' + ',' + f'{tile["bottom"]}' + ',' + f'{tile["right"]}' + ',' + f'{tile["top"]}')
                        cmd.extend(['--complete-ways', '--complete-multipolygons', '--complete-boundaries'])
                        cmd.append(self.border_countries[country]['filtered_file'])
                        cmd.append('-o='+out_file)

                        # print(cmd)
                        result = subprocess.run(cmd, check=True)
                        if result.returncode != 0:
                            print(f'Error in Osmosis with country: {country}')
                            sys.exit()
                        # print(border_countries[c]['filtered_file'])

                    # Non-Windows
                    else:
                        cmd = ['osmium', 'extract']
                        cmd.extend(['-b',f'{tile["left"]},{tile["bottom"]},{tile["right"]},{tile["top"]}'])
                        cmd.append(self.border_countries[country]['filtered_file'])
                        cmd.extend(['-s', 'smart'])
                        cmd.extend(['-o', out_file])
                        # print(cmd)
                        subprocess.run(cmd, check=True)
                        print(self.border_countries[country]['filtered_file'])

            tile_count += 1

            # logging
            print('# Split filtered country files to tiles: OK')


    def merge_splitted_tiles_with_land_and_sea(self):
        """
        Merge splitted tiles with land an sea
        """

        print('\n# Merge splitted tiles with land an sea')
        tile_count = 1
        for tile in self.tiles:
            print(f'+ Merging tiles for tile {tile_count} of {len(self.tiles)} for Coordinates: {tile["x"]},{tile["y"]}')
            out_file = os.path.join(fdf.OUTPUT_DIR,
             f'{tile["x"]}', f'{tile["y"]}', 'merged.osm.pbf')
            if not os.path.isfile(out_file) or self.force_processing is True:
                # Windows
                if platform.system() == "Windows":
                    cmd = [os.path.join (fdf.COMMON_DIR,
                     'Osmosis', 'bin', 'osmosis.bat')]
                    loop=0
                    for country in tile['countries']:
                        cmd.append('--rbf')
                        cmd.append(os.path.join(fdf.OUTPUT_DIR,
                         f'{tile["x"]}', f'{tile["y"]}', f'split-{country}.osm.pbf'))
                        cmd.append('workers='+ self.workers)
                        if loop > 0:
                            cmd.append('--merge')
                        loop+=1
                    land_files = glob.glob(os.path.join(fdf.OUTPUT_DIR,
                     f'{tile["x"]}', f'{tile["y"]}', 'land*.osm'))
                    for land in land_files:
                        cmd.extend(['--rx', 'file='+os.path.join(fdf.OUTPUT_DIR,
                         f'{tile["x"]}', f'{tile["y"]}', f'{land}'), '--s', '--m'])
                    cmd.extend(['--rx', 'file='+os.path.join(fdf.OUTPUT_DIR,
                     f'{tile["x"]}', f'{tile["y"]}', 'sea.osm'), '--s', '--m'])
                    cmd.extend(['--tag-transform', 'file=' + os.path.join (fdf.COMMON_DIR, 'tunnel-transform.xml'), '--wb', out_file, 'omitmetadata=true'])

                # Non-Windows
                else:
                    cmd = ['osmium', 'merge', '--overwrite']
                    for country in tile['countries']:
                        cmd.append(os.path.join(fdf.OUTPUT_DIR,
                         f'{tile["x"]}', f'{tile["y"]}', f'split-{country}.osm.pbf'))

                    cmd.append(os.path.join(fdf.OUTPUT_DIR,
                     f'{tile["x"]}', f'{tile["y"]}', 'land1.osm'))
                    cmd.append(os.path.join(fdf.OUTPUT_DIR,
                     f'{tile["x"]}', f'{tile["y"]}', 'sea.osm'))
                    cmd.extend(['-o', out_file])

                #print(cmd)
                result = subprocess.run(cmd, check=True)
                if result.returncode != 0:
                    print(f'Error in Osmosis with tile: {tile["x"]},{tile["y"]}')
                    sys.exit()

            tile_count += 1

        # logging
        print('# Merge splitted tiles with land an sea: OK')


    def create_map_files(self, threads):
        """
        Creating .map files
        """

        print('\n# Creating .map files')
        tile_count = 1
        for tile in self.tiles:
            print(f'+ Creating map file for tile {tile_count} of {len(self.tiles)} for Coordinates: {tile["x"]}, {tile["y"]}')
            out_file = os.path.join(fdf.OUTPUT_DIR,
             f'{tile["x"]}', f'{tile["y"]}.map')
            if not os.path.isfile(out_file+'.lzma') or self.force_processing is True:
                merged_file = os.path.join(fdf.OUTPUT_DIR,
                 f'{tile["x"]}', f'{tile["y"]}', 'merged.osm.pbf')

                # Windows
                if platform.system() == "Windows":
                    cmd = [os.path.join (fdf.COMMON_DIR, 'Osmosis', 'bin', 'osmosis.bat'), '--rbf', merged_file, 'workers=' + self.workers, '--mw', 'file='+out_file]
                # Non-Windows
                else:
                    cmd = ['osmosis', '--rb', merged_file, '--mw', 'file='+out_file]

                cmd.append(f'bbox={tile["bottom"]:.6f},{tile["left"]:.6f},{tile["top"]:.6f},{tile["right"]:.6f}')
                cmd.append('zoom-interval-conf=10,0,17')
                cmd.append('threads='+ threads)
                # should work on macOS and Windows
                cmd.append(f'tag-conf-file={os.path.join(fdf.COMMON_DIR, "tag-wahoo.xml")}')
                # print(cmd)
                result = subprocess.run(cmd, check=True)
                if result.returncode != 0:
                    print(f'Error in Osmosis with country: c // tile: {tile["x"]}, {tile["y"]}')
                    sys.exit()

                # Windows
                if platform.system() == "Windows":
                    cmd = [os.path.join(fdf.TOOLING_WIN_DIR, 'lzma'), 'e', out_file, out_file+'.lzma', f'-mt{threads}', '-d27', '-fb273', '-eos']
                # Non-Windows
                else:
                    cmd = ['lzma', out_file]

                    # --keep: do not delete source file
                    if self.save_cruiser:
                        cmd.append('--keep')

                # print(cmd)
                subprocess.run(cmd, check=True)
            tile_count += 1

        # logging
        print('# Creating .map files: OK')


    def zip_map_files(self):
        """
        Zip .map.lzma files
        """

        print('\n# Zip .map.lzma files')
        print(f'+ Country: {self.country_name}')

        # Make Wahoo zip file
        # Windows
        if platform.system() == "Windows":
            path_7za = os.path.join(fdf.TOOLING_WIN_DIR, '7za')
            cmd = [path_7za, 'a', '-tzip', '-m0=lzma', '-mx9', '-mfb=273', '-md=1536m', self.country_name + '.zip']
            #cmd = ['7za', 'a', '-tzip', '-m0=lzma', countryName[1] + '.zip']
        # Non-Windows
        else:
            cmd = ['zip', '-r', self.country_name + '.zip']

        for tile in self.tiles:
            cmd.append(os.path.join(f'{tile["x"]}', f'{tile["y"]}.map.lzma'))
        #print(cmd)
        subprocess.run(cmd, cwd=fdf.OUTPUT_DIR, check=True)

        # logging
        print('# Zip .map.lzma files: OK \n')


    def make_cruiser_files(self):
        """
        Make Cruiser map files zip file
        """

        # Make Cruiser map files zip file
        if self.save_cruiser == 1:
            # Windows
            if platform.system() == "Windows":
                cmd = [os.path.join(fdf.TOOLING_WIN_DIR, '7za'), 'a', '-tzip', '-m0=lzma', self.country_name + '-maps.zip']
            # Non-Windows
            else:
                cmd = ['zip', '-r', self.country_name + '-maps.zip']

            for tile in self.tiles:
                cmd.append(os.path.join(f'{tile["x"]}', f'{tile["y"]}.map'))
            #print(cmd)
            subprocess.run(cmd, cwd=fdf.OUTPUT_DIR, check=True)
