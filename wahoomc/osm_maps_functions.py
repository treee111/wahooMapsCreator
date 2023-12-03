"""
functions and object for managing OSM maps
"""
#!/usr/bin/python

# import official python packages
from datetime import datetime
import asyncio
import glob
import multiprocessing
import os
import subprocess
import sys
import platform
import shutil
import logging

# import custom python packages
from wahoomc.file_directory_functions import read_json_file_country_config, create_empty_directories, write_json_file_generic
from wahoomc.constants_functions import translate_tags_to_keep, \
    get_tooling_win_path, get_tag_wahoo_xml_path, TagWahooXmlNotFoundError

from wahoomc.setup_functions import read_earthexplorer_credentials

from wahoomc.constants import USER_WAHOO_MC
from wahoomc.constants import USER_OUTPUT_DIR
from wahoomc.constants import RESOURCES_DIR
from wahoomc.constants import LAND_POLYGONS_PATH
from wahoomc.constants import VERSION
from wahoomc.constants import OSMOSIS_WIN_FILE_PATH
from wahoomc.constants import USER_DL_DIR

from wahoomc.timings import Timings

log = logging.getLogger('main-logger')


def run_subprocess_and_log_output(cmd, error_message, cwd=""):
    """
    run given cmd-subprocess and issue error message if wished
    """
    if not cwd:
        process = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", check=False)

    else:
        process = subprocess.run(  # pylint: disable=consider-using-with
            cmd, capture_output=True, cwd=cwd, text=True, encoding="utf-8", check=False)


    if error_message and process.returncode != 0:  # 0 means success
        log.error('subprocess error output:')
        if process.stderr:
            log.error(process.stderr)

        log.error(error_message)
        sys.exit()

    elif process.stdout:
        log.debug('subprocess debug output:')
        log.debug(process.stdout)

async def run_async_subprocess_and_log_output(semaphore, cmd, args, error_message, cwd=""):
    """
    run given cmd-subprocess and issue error message if wished
    """
    async with semaphore:
        process = await asyncio.create_subprocess_exec(
#        create_subprocess_shell,
            cmd,
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await process.communicate()

#    if not cwd:
#        process = subprocess.run(
#            cmd, capture_output=True, text=True, encoding="utf-8", check=False)
#
#    else:
#        process = subprocess.run(  # pylint: disable=consider-using-with
#            cmd, capture_output=True, cwd=cwd, text=True, encoding="utf-8", check=False)


        if error_message and process.returncode != 0:  # 0 means success
            log.error('subprocess error output:')
            if process.stderr:
                log.error(process.stderr)

            log.error(error_message)
            sys.exit()

        elif process.stdout:
            log.debug('subprocess debug output:')
            log.debug(process.stdout)


def get_timestamp_last_changed(file_path):
    """
    returns the timestamp of the last-changed datetime of the given file
    """
    chg_time = os.path.getmtime(file_path)

    return datetime.fromtimestamp(chg_time).isoformat()


class OsmMaps:
    """
    This is a OSM data class
    """

    # Number of workers for the Osmosis read binary fast function
    workers = '1'

    def __init__(self, o_osm_data):
        self.o_osm_data = o_osm_data
        self.osmconvert_path = get_tooling_win_path('osmconvert')

        create_empty_directories(
            USER_OUTPUT_DIR, self.o_osm_data.tiles, self.o_osm_data.border_countries)

    async def filter_tags_from_country_osm_pbf_files(self):  # pylint: disable=too-many-statements
        """
        Filter tags from country osm.pbf files
        """

        log.info('-' * 80)
        log.info('# Filter tags from country osm.pbf files')
        tasks = set()
        timings = Timings()
        semaphore = asyncio.Semaphore(31)
        for key, val in self.o_osm_data.border_countries.items():
            # evaluate contry directory, create if not exists
            country_dir = os.path.join(USER_OUTPUT_DIR, key)

            # set names for filtered files for WIN, later on add ".pbf" for macOS/Linux
            out_file_o5m_filtered_win = os.path.join(country_dir, 'filtered.o5m')
            out_file_o5m_filtered_names_win = os.path.join(country_dir, 'filtered_names.o5m')

            out_file_pbf_filtered_mac = f'{out_file_o5m_filtered_win}.pbf'
            out_file_pbf_filtered_names_mac = f'{out_file_o5m_filtered_names_win}.pbf'

            # filter out tags:
            # - if no filtered files exist
            # - force processing is set (this is also when new map files were dowwnloaded)
            # - the defined TAGS_TO_KEEP_UNIVERSAL constants have changed are changed (user input or new release)
            if not os.path.isfile(out_file_pbf_filtered_mac) or not os.path.isfile(out_file_pbf_filtered_names_mac) \
                     or self.o_osm_data.force_processing is True or self.tags_are_identical_to_last_run(key) is False \
                     or self.last_changed_is_identical_to_last_run(key) is False:
                log.info('+ Filtering unwanted map objects out of map of %s', key)
                        
                tags_to_keep = translate_tags_to_keep(sys_platform=platform.system())
                tags_to_keep_names = translate_tags_to_keep(name_tags=True, sys_platform=platform.system())

#                    async with asyncio.TaskGroup() as tg:                    
                log.debug('start run filtered')
                tasks.add(asyncio.create_task(self.invoke_filter_tags_osmium_linux(semaphore, key, val['map_file'], tags_to_keep, out_file_pbf_filtered_mac)))
#                        tg.create_task(self.invoke_filter_tags_osmium_linux(key, val['map_file'], tags_to_keep, out_file_pbf_filtered_mac))

                log.debug('start run filtered names')
                tasks.add(asyncio.create_task(self.invoke_filter_tags_osmium_linux(semaphore, key, val['map_file'], tags_to_keep_names, out_file_pbf_filtered_names_mac)))
#                        tg.create_task(self.invoke_filter_tags_osmium_linux(key, val['map_file'], tags_to_keep_names, out_file_pbf_filtered_names_mac))

            val['filtered_file'] = out_file_pbf_filtered_mac
            val['filtered_file_names'] = out_file_pbf_filtered_names_mac

            # write config file for country
            self.write_country_config_file(key)
            
        await asyncio.gather(*tasks)

        log.info('+ Filter tags from country osm.pbf files: OK, %s', timings.stop_and_return())

    async def invoke_filter_tags_osmium_linux(self, semaphore, country, map_file, tags_to_keep, out_filename):
        # https://docs.osmcode.org/osmium/latest/osmium-tags-filter.html
        cmd = 'osmium'
        args = ['tags-filter', '--remove-tags']
        args.append(map_file)
        args.extend(tags_to_keep)
        args.extend(['-o', out_filename])
        args.append('--overwrite')

#        log.info('osmium filter tags, %s', out_filename)
        await run_async_subprocess_and_log_output(semaphore, cmd, args, f'! Error in Osmium with country: {country}')

    async def generate_land(self):
        """
        Generate land for all tiles
        """

        log.info('-' * 80)
        log.info('# Generate land for each coordinate')
        timings = Timings()
        tile_count = 1
        semaphore = asyncio.Semaphore(60)
        land_sea_tasks = []
        land1_tasks = []
        for tile in self.o_osm_data.tiles:
            land_file = os.path.join(USER_OUTPUT_DIR, f'{tile["x"]}', f'{tile["y"]}', 'land.shp')
            out_file_land1 = os.path.join(USER_OUTPUT_DIR, f'{tile["x"]}', f'{tile["y"]}', 'land')
            timings_tile = Timings()

            # create land.dbf, land.prj, land.shp, land.shx
            if not os.path.isfile(land_file) or self.o_osm_data.force_processing is True:
#                self.log_tile_info(tile["x"], tile["y"], tile_count)
#                cmd = ['ogr2ogr', '-overwrite', '-skipfailures']
                # Try to prevent getting outside of the +/-180 and +/- 90 degrees borders. Normally the +/- 0.1 are there to prevent white lines at border borders.
                correction = 0.1
                if tile["x"] == 255 or tile["y"] == 255 or tile["x"] == 0 or tile["y"] == 0:
                    correction = 0.0

                spatLeft = f'{tile["left"]-correction:.6f}'
                spatBottom = f'{tile["bottom"]-correction:.6f}'
                spatRight = f'{tile["right"]+correction:.6f}'
                spatTop = f'{tile["top"]+correction:.6f}'
                                
                task1 = asyncio.create_task(self.invoke_create_land_and_sea_ogr2ogr_linux(semaphore, tile["x"], tile["y"], spatLeft, spatBottom, spatRight, spatTop, land_file, LAND_POLYGONS_PATH))
                land_sea_tasks.append(task1)
#                await asyncio.gather(task1)
                                
#                cmd.append(land_file)
#                cmd.append(LAND_POLYGONS_PATH)

#                run_subprocess_and_log_output(
#                    cmd, f'! Error generating land for tile: {tile["x"]},{tile["y"]}')

            # create land1.osm
            if not os.path.isfile(out_file_land1+'1.osm') or self.o_osm_data.force_processing is True:
#                # Windows
#                if platform.system() == "Windows":
#                    cmd = ['python', os.path.join(RESOURCES_DIR,
#                                                  'shape2osm.py'), '-l', out_file_land1, land_file]
#
#                # Non-Windows
#                else:
#                    cmd = ['python', os.path.join(RESOURCES_DIR,
#                                                  'shape2osm.py'), '-l', out_file_land1, land_file]

#               run_subprocess_and_log_output(
#                    cmd, f'! Error creating land.osm for tile: {tile["x"]},{tile["y"]}')
                task2 = asyncio.create_task(self.invoke_create_land1_python_linux(semaphore, tile["x"], tile["y"], land_file, out_file_land1))
                land1_tasks.append(task2)
                    
                    
            self.log_tile_debug(tile["x"], tile["y"], tile_count, timings_tile.stop_and_return())
            tile_count += 1

        log.info('start land sea')
    #    semaphore = asyncio.Semaphore(4)
#        async with semaphore:       
        await asyncio.gather(*land_sea_tasks)
        log.info('start land1')
#        async with semaphore:       
        await asyncio.gather(*land1_tasks)

        log.info('+ Generate land for each coordinate: OK, %s', timings.stop_and_return())

    async def invoke_create_land_and_sea_ogr2ogr_linux(self, semaphore, tileX, tileY, spatLeft, spatBottom, spatRight, spatTop, land_file, land_polygon_path):
        cmd = 'ogr2ogr'
        args = ['-overwrite', '-skipfailures']
        args.extend(['-spat', f'{spatLeft}', f'{spatBottom}', f'{spatRight}', f'{spatTop}'])
        args.append(land_file)
        args.append(land_polygon_path)

#        log.info('+ Generate land for each coordinate: OK, %s, %s', tileX, tileY)

        await run_async_subprocess_and_log_output(semaphore, cmd, args, f'! Error generating land for tile: {tileX},{tileY}')

    async def invoke_create_land1_python_linux(self, semaphore, tileX, tileY, land_file, out_land_file):
        cmd = 'python'
        args = [os.path.join(RESOURCES_DIR, 'shape2osm.py'), '-l', out_land_file, land_file]

        await run_async_subprocess_and_log_output(semaphore, cmd, args, f'! Error creating land1.osm for tile: {tileX},{tileY}')


    def generate_sea(self):
        """
        Generate sea for all tiles
        """

        log.info('-' * 80)
        log.info('# Generate sea for each coordinate')
        timings = Timings()
        tile_count = 1
        for tile in self.o_osm_data.tiles:
            out_file_sea = os.path.join(USER_OUTPUT_DIR,
                                        f'{tile["x"]}', f'{tile["y"]}', 'sea.osm')
            timings_tile = Timings()
            if not os.path.isfile(out_file_sea) or self.o_osm_data.force_processing is True:
#                self.log_tile_info(tile["x"], tile["y"], tile_count)
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
            self.log_tile_debug(tile["x"], tile["y"], tile_count, timings_tile.stop_and_return())
            tile_count += 1

        log.info('+ Generate sea for each coordinate: OK, %s', timings.stop_and_return())

    def generate_elevation(self, use_srtm1):
        """
        Generate contour lines for all tiles
        """
        username, password = read_earthexplorer_credentials()

        log.info('-' * 80)
        log.info('# Generate contour lines for each coordinate')

        hgt_path = os.path.join(USER_DL_DIR, 'hgt')

        tasks = set()
        timings = Timings()
        tile_count = 1
        for tile in self.o_osm_data.tiles:
            out_file_elevation = os.path.join(
                USER_OUTPUT_DIR, f'{tile["x"]}', f'{tile["y"]}', 'elevation')

            # 1) as the elevation file has a suffix, they need to be searched with glob.glob
            # example elevation filename: elevation_lon14.06_15.47lat35.46_36.60_view1,view3.osm

            # 2) use view1 as default source and srtm1 if wished by the user
            # view1 offers better quality in general apart fro some places
            # where srtm1 is the better choice
            if use_srtm1:
                # 1) search for srtm1 elevation files
                out_file_elevation_existing = glob.glob(os.path.join(
                    USER_OUTPUT_DIR, str(tile["x"]), str(tile["y"]), 'elevation*srtm1*.osm'))
                # 2) set source
                elevation_source = '--source=srtm1,view1,view3,srtm3'
            else:
                # 1) search vor view1 elevation files
                out_file_elevation_existing = glob.glob(os.path.join(
                    USER_OUTPUT_DIR, str(tile["x"]), str(tile["y"]), 'elevation*view1*.osm'))
                # 2) set source
                elevation_source = '--source=view1,view3,srtm3'

            # check for already existing elevation .osm file (the ones matched via glob)
            if not (len(out_file_elevation_existing) == 1 and os.path.isfile(out_file_elevation_existing[0])) \
                    or self.o_osm_data.force_processing is True:
                self.log_tile_info(tile["x"], tile["y"], tile_count)
                timings_tile = Timings()
                cmd = ['phyghtmap']
                cmd.append('-a ' + f'{tile["left"]}' + ':' + f'{tile["bottom"]}' +
                           ':' + f'{tile["right"]}' + ':' + f'{tile["top"]}')
                cmd.extend(['-o', f'{out_file_elevation}', '-s 10', '-c 100,50', elevation_source,
                            '--jobs=8', '--viewfinder-mask=1', '--start-node-id=20000000000',
                            '--max-nodes-per-tile=0', '--start-way-id=2000000000', '--write-timestamp',
                            '--no-zero-contour', '--hgtdir=' + hgt_path])
                cmd.append('--earthexplorer-user=' + username)
                cmd.append('--earthexplorer-password=' + password)

                run_subprocess_and_log_output(
                    cmd, f'! Error in phyghtmap with tile: {tile["x"]},{tile["y"]}. Win_macOS/elevation')
                self.log_tile_debug(tile["x"], tile["y"], tile_count, timings_tile.stop_and_return())

            tile_count += 1

        log.info('+ Generate contour lines for each coordinate: OK, %s', timings.stop_and_return())

    async def split_filtered_country_files_to_tiles(self):
        """
        Split filtered country files to tiles
        """

        log.info('-' * 80)
        log.info('# Split filtered country files to tiles')
        semaphore = asyncio.Semaphore(6)
        tasks = set()
        timings = Timings()
        tile_count = 1
        for tile in self.o_osm_data.tiles:

            for country, val in self.o_osm_data.border_countries.items():
                if country not in tile['countries']:
                    continue
#                self.log_tile_info(tile["x"], tile["y"], tile_count, country)
                timings_tile = Timings()
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
                        cmd, f'! Error in osmconvert with country: {country}. Win/out_file')

                    cmd = [self.osmconvert_path,
                           '-v', '--hash-memory=2500']
                    cmd.append('-b='+f'{tile["left"]}' + ',' + f'{tile["bottom"]}' +
                               ',' + f'{tile["right"]}' + ',' + f'{tile["top"]}')
                    cmd.extend(
                        ['--complete-ways', '--complete-multipolygons', '--complete-boundaries'])
                    cmd.append(val['filtered_file_names'])
                    cmd.append('-o='+out_file_names)

                    run_subprocess_and_log_output(
                        cmd, '! Error in osmconvert with country: {country}. Win/out_file_names')

                # Non-Windows
                else:
                    tasks.add(asyncio.create_task(self.invoke_split_country_to_tile_linux(semaphore, country, tile, val['filtered_file'], out_file)))
                    tasks.add(asyncio.create_task(self.invoke_split_country_to_tile_linux(semaphore, country, tile, val['filtered_file_names'], out_file_names)))

                self.log_tile_debug(tile["x"], tile["y"], tile_count, f'{country} {timings_tile.stop_and_return()}')

            tile_count += 1

        await asyncio.gather(*tasks)

        log.info('+ Split filtered country files to tiles: OK, %s', timings.stop_and_return())

    async def invoke_split_country_to_tile_linux(self, semaphore, country, tile, input_file, out_file):
        cmd = 'osmium'
        args = ['extract']

        args.extend(['-b', f'{tile["left"]},{tile["bottom"]},{tile["right"]},{tile["top"]}'])
        args.append(input_file)
        args.extend(['-s', 'smart'])
        args.extend(['-o', out_file])
        args.extend(['--overwrite'])

        await run_async_subprocess_and_log_output(semaphore, cmd, args, f'! Error in Osmium with country: {country}. {out_file}')

    async def merge_splitted_tiles_with_land_and_sea(self, process_border_countries, contour): # pylint: disable=too-many-locals
        """
        Merge splitted tiles with land elevation and sea
        - elevation data only if requested
        """

        log.info('-' * 80)
        log.info('# Merge splitted tiles with land, elevation, and sea')
        semaphore = asyncio.Semaphore(30)
        tasks = set()
        timings = Timings()
        tile_count = 1
        for tile in self.o_osm_data.tiles:  # pylint: disable=too-many-nested-blocks
            # sort land* osm files
            tasks.add(asyncio.create_task(self.sort_osm_files(semaphore, tile)))

        await asyncio.gather(*tasks)
        log.info('+ Sorted: OK, %s', timings.stop_and_return())

        tasks = set()
        for tile in self.o_osm_data.tiles:  # pylint: disable=too-many-nested-blocks
 #           self.log_tile_info(tile["x"], tile["y"], tile_count)
            timings_tile = Timings()

            out_tile_dir = os.path.join(USER_OUTPUT_DIR,
                                        f'{tile["x"]}', f'{tile["y"]}')
            out_file_merged = os.path.join(out_tile_dir, 'merged.osm.pbf')

            land_files = glob.glob(os.path.join(out_tile_dir, 'land*.osm'))

            elevation_files = glob.glob(
                os.path.join(out_tile_dir, 'elevation*.osm'))

            # merge splitted tiles with land and sea every time because the result is different per constants (user input)

            tasks.add(asyncio.create_task(self.invoke_merge_tile_linux(semaphore, process_border_countries, contour, tile, land_files, elevation_files, out_tile_dir, out_file_merged)))

#            self.log_tile_debug(tile["x"], tile["y"], tile_count, timings_tile.stop_and_return())
            tile_count += 1

        await asyncio.gather(*tasks)

        log.info('+ Merge splitted tiles with land, elevation, and sea: OK, %s', timings.stop_and_return())

    async def invoke_merge_tile_linux(self, semaphore, process_border_countries, contour, tile, land_files, elevation_files, out_tile_dir, out_file_merged):
        if platform.system() == "Windows":
            cmd = OSMOSIS_WIN_FILE_PATH
        # Non-Windows
        else:
            cmd = 'osmosis'

        loop = 0
        args = []
        # loop through all countries of tile, if border-countries should be processed.
        # if border-countries should not be processed, only process the "entered" country
        for country in tile['countries']:
            if process_border_countries or country in self.o_osm_data.border_countries:
                args.append('--rbf')
                args.append(os.path.join(out_tile_dir, f'split-{country}.osm.pbf'))
                args.append('workers=' + self.workers)
                if loop > 0:
                    args.append('--merge')

                args.append('--rbf')
                args.append(os.path.join(out_tile_dir, f'split-{country}-names.osm.pbf'))
                args.append('workers=' + self.workers)
                args.append('--merge')

                loop += 1

        for land in land_files:
            args.extend(
                ['--rx', 'file='+land, '--s', '--m'])

        if contour:
            for elevation in elevation_files:
                args.extend(
                    ['--rx', 'file='+elevation, '--s', '--m'])

        args.extend(['--rx', 'file='+os.path.join(out_tile_dir, 'sea.osm'), '--s', '--m'])
        args.extend(['--tag-transform', 'file=' + os.path.join(RESOURCES_DIR,
                                                                  'tunnel-transform.xml'), '--wb', out_file_merged, 'omitmetadata=true'])
        await run_async_subprocess_and_log_output(semaphore, cmd, args, f'! Error in Osmium with tile: {tile["x"]},{tile["y"]}')

    async def sort_osm_files(self, semaphore, tile):
        """
        sort land*.osm files to be in this order: nodes, then ways, then relations.
        this is mandatory for osmium-merge since:
        https://github.com/osmcode/osmium-tool/releases/tag/v1.13.2
        """

        log.debug('-' * 80)
        log.debug('# Sorting land* osm files')

        # get all land* osm files
        land_files = glob.glob(os.path.join(USER_OUTPUT_DIR,
                                            f'{tile["x"]}', f'{tile["y"]}', 'land*.osm'))

        tasks = set()
        for land in land_files:
            tasks.add(asyncio.create_task(self.invoke_sort_land_files_linux(semaphore, tile, land)))

        await asyncio.gather(*tasks)
        log.debug('+ Sorting land* osm files: OK')

    async def invoke_sort_land_files_linux(self, semaphore, tile, land):
        if platform.system() == "Windows":
            cmd = OSMOSIS_WIN_FILE_PATH
        else:
            cmd = 'osmosis'

        args = ['--read-xml', 'file='+land]
        args.append('--sort')
        args.extend(['--write-xml', 'file='+land])

        await run_async_subprocess_and_log_output(semaphore, cmd, args, f'! Error in Osmosis with sorting land* osm files of tile: {tile["x"]},{tile["y"]}')

    async def create_map_files(self, save_cruiser, tag_wahoo_xml):
        """
        Creating .map files
        """

        log.info('-' * 80)
        log.info('# Creating .map files for tiles')

        # Number of threads to use in the mapwriter plug-in
#        threads = multiprocessing.cpu_count() - 1
#        if int(threads) < 1:
#            threads = 1

        semaphore = asyncio.Semaphore(12)
        tasks = set()
        timings = Timings()
        tile_count = 1
        for tile in self.o_osm_data.tiles:
#            self.log_tile_info(tile["x"], tile["y"], tile_count)
            timings_tile = Timings()

            out_file_map = os.path.join(USER_OUTPUT_DIR, f'{tile["x"]}', f'{tile["y"]}.map')

            # apply tag-wahoo xml every time because the result is different per .xml file (user input)
            merged_file = os.path.join(USER_OUTPUT_DIR, f'{tile["x"]}', f'{tile["y"]}', 'merged.osm.pbf')

            tasks.add(asyncio.create_task(self.invoke_create_map_file_linux(semaphore, tile, tag_wahoo_xml, merged_file, out_file_map)))
            tile_count += 1

        await asyncio.gather(*tasks)

        log.info('+ Created .map files for tiles: OK, %s', timings.stop_and_return())

        semaphore = asyncio.Semaphore(30)
        tasks = set()
        tile_count = 1
        for tile in self.o_osm_data.tiles:
            timings_tile = Timings()

            out_file_map = os.path.join(USER_OUTPUT_DIR, f'{tile["x"]}', f'{tile["y"]}.map')

            tasks.add(asyncio.create_task(self.invoke_compress_map_file_linux(semaphore, tile, save_cruiser, out_file_map)))

        await asyncio.gather(*tasks)

        log.info('+ Compressed .map files for tiles: OK, %s', timings.stop_and_return())

        tile_count = 1
        for tile in self.o_osm_data.tiles:
            timings_tile = Timings()

            out_file_map = os.path.join(USER_OUTPUT_DIR, f'{tile["x"]}', f'{tile["y"]}.map')

            # Create "tile present" file
            with open(out_file_map + '.lzma.17', mode='wb') as tile_present_file:
                tile_present_file.close()

            self.log_tile_debug(tile["x"], tile["y"], tile_count, timings_tile.stop_and_return())
            tile_count += 1

        log.info('+ Creating .map files for tiles: OK, %s', timings.stop_and_return())

    async def invoke_create_map_file_linux(self, semaphore, tile, tag_wahoo_xml, merged_file, out_file_map):
        # Windows
        if platform.system() == "Windows":
            cmd = OSMOSIS_WIN_FILE_PATH
            args = ['--rbf', merged_file, 'workers=1', '--mw', 'file='+out_file_map]
        # Non-Windows
        else:
            cmd = 'osmosis'
            args = ['--rb', merged_file, '--mw', 'file='+out_file_map]

        args.append(f'bbox={tile["bottom"]:.6f},{tile["left"]:.6f},{tile["top"]:.6f},{tile["right"]:.6f}')
        args.append('zoom-interval-conf=10,0,17')
        args.append(f'threads=1')
        # add path to tag-wahoo xml file
        try:
            args.append(f'tag-conf-file={get_tag_wahoo_xml_path(tag_wahoo_xml)}')
        except TagWahooXmlNotFoundError:
            log.error('The tag-wahoo xml file was not found: ˚%s˚. Does the file exist and is your input correct?', tag_wahoo_xml)
            sys.exit()

        await run_async_subprocess_and_log_output(semaphore, cmd, args, f'! Error in creating map file via Osmosis with tile: {tile["x"]},{tile["y"]}. mapwriter plugin installed?')

    async def invoke_compress_map_file_linux(self, semaphore, tile, save_cruiser, out_file_map):
        # Windows
        if platform.system() == "Windows":
            cmd = get_tooling_win_path('lzma')
            args = ['e', out_file_map, out_file_map+'.lzma', f'-mt1', '-d27', '-fb273', '-eos']
        # Non-Windows
        else:
            # force overwrite of output file and (de)compress links
            cmd = 'lzma'
            args = [out_file_map, '-f']

            # --keep: do not delete source file
            if save_cruiser:
                cmd.append('--keep')

        await run_async_subprocess_and_log_output(semaphore, cmd, args, f'! Error creating map files for tile: {tile["x"]},{tile["y"]}')

    def make_and_zip_files(self, extension, zip_folder):
        """
        make or make and zip .map or .map.lzma files
        extension: '.map.lzma' for Wahoo tiles
        extension: '.map' for Cruiser map files
        """
        # if country_name is longer than 50 characters, cut down to 50 for the folder name
        # that preserves crashing later on when creating the output folder
        folder_name = self.calculate_folder_name(extension)

        log.info('-' * 80)
        log.info('# Create: %s files', extension)
        log.info('+ Country: %s', self.o_osm_data.country_name)
        timings = Timings()

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
                cmd = [get_tooling_win_path('7za'), 'a', '-tzip']

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

        log.info('+ Create %s files: OK, %s', extension, timings.stop_and_return())

    def calculate_folder_name(self, extension):
        """
        if country_name is longer than 50 characters, cut down to 50 for the folder name
        that preserves crashing later on when creating the output folder
        """
        # cut down to 100 (relevant if country_name is longer than 100 characters)
        if len(self.o_osm_data.country_name) > 50:
            country_name_50_chars = self.o_osm_data.country_name[:41] + '_and_more'
        else:
            country_name_50_chars = self.o_osm_data.country_name

        if extension == '.map.lzma':
            folder_name = country_name_50_chars
        else:
            folder_name = country_name_50_chars + '-maps'

        return folder_name

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
            "changed_ts_map_last_run": get_timestamp_last_changed(self.o_osm_data.border_countries[country]['map_file']),
            "tags_last_run": translate_tags_to_keep(sys_platform=platform.system()),
            "name_tags_last_run": translate_tags_to_keep(name_tags=True, sys_platform=platform.system())
        }

        write_json_file_generic(os.path.join(
            USER_OUTPUT_DIR, country, ".config.json"), configuration)

    def tags_are_identical_to_last_run(self, country):
        """
        compare tags of this run with used tags from last run stored in _tiles/{country} directory
        """
        tags_are_identical = True

        try:
            country_config = read_json_file_country_config(os.path.join(
                USER_OUTPUT_DIR, country, ".config.json"))
            if not country_config["tags_last_run"] == translate_tags_to_keep(sys_platform=platform.system()) \
                    or not country_config["name_tags_last_run"] == translate_tags_to_keep(name_tags=True, sys_platform=platform.system()):
                tags_are_identical = False
        except (FileNotFoundError, KeyError):
            tags_are_identical = False

        return tags_are_identical

    def last_changed_is_identical_to_last_run(self, country):
        """
        compare tags of this run with used tags from last run stored in _tiles/{country} directory
        """
        last_changed_is_identical = True

        try:
            country_config = read_json_file_country_config(os.path.join(
                USER_OUTPUT_DIR, country, ".config.json"))
            if not country_config["changed_ts_map_last_run"] == get_timestamp_last_changed(self.o_osm_data.border_countries[country]['map_file']):
                last_changed_is_identical = False
        except (FileNotFoundError, KeyError):
            last_changed_is_identical = False

        return last_changed_is_identical

    def log_tile_info(self, tile_x, tile_y, tile_count, additional_info=''):
        """
        log tile information at info log level
        """
        self.log_tile(tile_x, tile_y, tile_count, False, additional_info)

    def log_tile_debug(self, tile_x, tile_y, tile_count, additional_info=''):
        """
        log tile information at debug log level
        """
        self.log_tile(tile_x, tile_y, tile_count, True, additional_info)

    def log_tile(self, tile_x, tile_y, tile_count, log_level_debug, additional_info=''):  # pylint: disable=too-many-arguments
        """
        unified status logging for this class
        """
        msg = f'+ (tile {tile_count} of {len(self.o_osm_data.tiles)}) Coordinates: {tile_x},{tile_y}'
        if additional_info:
            msg = f'{msg} / {additional_info}'
        if log_level_debug:
            log.debug(msg)
        else:
            log.info(msg)
