"""
tests the generated files of a full-run of the tool against fixed files
"""

import filecmp
import os
from os import walk
import platform
import shutil
import unittest
import subprocess


# import custom python packages
from wahoomc import constants
from wahoomc.file_directory_functions import get_files_in_folder

dirname_of_file = os.path.dirname(__file__)
unittest_files_root = os.path.join(constants.USER_WAHOO_MC, '_unittest')
unittest_files_parking = os.path.join(unittest_files_root, 'parking_lot')


def copy_static_maps_input_file(mode, country, given_osm_pbf=''):
    """
    copy given file to download-directory
    """
    static_file_path = os.path.join(
        dirname_of_file, 'resources', given_osm_pbf)
    prod_path = os.path.join(
        constants.USER_MAPS_DIR, country + '-latest.osm.pbf')
    parking_path = os.path.join(
        unittest_files_parking, country + '-latest.osm.pbf')

    # these modes need the static filename to copy
    if mode in [0, 1] and given_osm_pbf == '':
        raise SystemError

    move_file_dir(mode, static_file_path, prod_path, parking_path)


def copy_static_land_polygon_input_folder(mode):
    """
    copy given folder to download-directory
    - mode 0: parking
    - mode 1: normal
    - mode 2: restore
    """
    static_file_path = os.path.join(
        unittest_files_root, 'land-polygons-split-4326_2021-10-31')
    prod_path = os.path.dirname(constants.LAND_POLYGONS_PATH)
    parking_path = os.path.join(
        unittest_files_parking, 'land-polygons-split-4326')

    move_file_dir(mode, static_file_path, prod_path, parking_path)


def copy_static_geofabrik_file(mode):
    """
    copy given file to download-directory
    - mode 0: parking
    - mode 1: normal
    - mode 2: restore
    """
    static_file_path = os.path.join(
        dirname_of_file, 'resources', 'geofabrik-2023-02-26.json')
    prod_path = os.path.join(constants.GEOFABRIK_PATH)
    parking_path = os.path.join(
        unittest_files_parking, 'geofabrik.json')

    move_file_dir(mode, static_file_path, prod_path, parking_path)


def move_file_dir(mode, static_file_path, prod_path, parking_path):
    """
    this function does the real file movements
    doing mode 0 and 1 in a while loop. Makes mostly sense together
    """
    while True:
        copy_from_path, copy_to_path = eval_from_to_paths(
            mode, static_file_path, prod_path, parking_path)

        # delete file or dir
        if os.path.isfile(copy_to_path):
            os.remove(copy_to_path)
        elif os.path.isdir(copy_to_path):
            # delete directory if exists. copytree fails if dir exists already
            shutil.rmtree(copy_to_path)
        else:  # not existing
            pass

        # copy from- to to- path file/dir
        try:
            if os.path.isfile(copy_from_path):
                # copy file
                shutil.copy2(copy_from_path, copy_to_path)
            elif os.path.isdir(copy_from_path):
                # copy folder
                shutil.copytree(copy_from_path, copy_to_path)
            else:  # not existing
                pass
        except FileNotFoundError:
            pass

        # either go another round or go out
        if mode in (1, 2):
            break
        if mode == 0:
            mode = 1


def eval_from_to_paths(mode, static_file_path, prod_path, parking_path):
    """
    evaluate from and to path for copying by given mode
    """
    if mode == 0:  # parking
        copy_from_path = prod_path
        copy_to_path = parking_path
    elif mode == 1:  # normal
        copy_from_path = static_file_path
        copy_to_path = prod_path
    elif mode == 2:  # restore
        copy_from_path = parking_path
        copy_to_path = prod_path
    else:
        raise SystemError

    return copy_from_path, copy_to_path


class TestGeneratedFiles(unittest.TestCase):
    """
    tests for the OSM maps file

    Test output of countries without border countries
    - Using given input .osm.pbf file in this repo
    - Compare content of directory tests/resources/mac /windows against directory output/

    Files that can be possibly checked (in order of creation):
    - merged.osm.pbf
    - 100.map
    - 100.map.lzma
    """

    def setUp(self):
        os.makedirs(unittest_files_parking, exist_ok=True)

        # copy actual productive files to parking lot
        # and copy static files as productive ones to have equal results each run
        copy_static_land_polygon_input_folder(mode=0)
        copy_static_geofabrik_file(mode=0)
        copy_static_maps_input_file(
            mode=0, country='malta', given_osm_pbf='malta-latest_2021-10-31.osm.pbf')
        copy_static_maps_input_file(
            mode=0, country='liechtenstein', given_osm_pbf='liechtenstein-latest_2021-10-31.osm.pbf')

    def tearDown(self):
        # copy files from parking lot back as productive
        copy_static_land_polygon_input_folder(mode=2)
        copy_static_geofabrik_file(mode=2)
        copy_static_maps_input_file(mode=2, country='malta')
        copy_static_maps_input_file(mode=2, country='liechtenstein')

    def test_calc_output_malta_and_compare(self):
        """
        Test output of countries without border countries
        - of malta
        """
        # run tool for country
        self.run_wahoomapscreator_cli('malta')

        # compare generated given merged.osm.pbf-file with reference-file
        self.compare_dir_sub_test_resource_and_output('138', 'malta')
        self.compare_dir_sub_test_resource_and_output('137', 'malta')

    def test_calc_output_liechtenstein_and_compare(self):
        """
        Test output of countries without border countries
        - of liechtenstein
        """
        # run tool for country
        self.run_wahoomapscreator_cli('liechtenstein')

        # compare generated given merged.osm.pbf-file with reference-file
        self.compare_dir_sub_test_resource_and_output('134', 'liechtenstein')

    def run_wahoomapscreator_cli(self, country):
        """
        runs wahooMapsCreator for given country and static osm.pbf file via CLI
        - without border countries
        """
        # run processing of input-country via CLI
        result = os.system(
            f'python -m wahoomc cli -co {country} -tag tag-wahoo.xml -fp -c -md 9999 -nbc')

        # check if run was successful
        self.assertEqual(result, 0)

    def test_malta_compare(self):
        """
        compare output of malta
        - of malta
        """
        # compare generated X/Y files with reference-file
        self.compare_dir_sub_test_resource_and_output('138', 'malta')
        self.compare_dir_sub_test_resource_and_output('137', 'malta')

    def test_liechtenstein_compare(self):
        """
        compare output of malta
        - of liechtenstein
        """
        # compare generated X/Y files with reference-file
        self.compare_dir_sub_test_resource_and_output('134', 'liechtenstein')

    def compare_dir_sub_test_resource_and_output(self, dir_to_compare, country):
        """
        compare files from given directory and subdirectories for equalness.
        check the files which are in test/resources folder
        """

        if platform.system() == "Windows":
            path_to_dir = os.path.join(
                dirname_of_file, 'resources', 'windows')
        else:
            path_to_dir = os.path.join(
                dirname_of_file, 'resources', 'macos')

        # check files in subdir of given dir (i.e. the X/Y directory)
        for (dirpath, dirnames, filenames) in walk(os.path.join(path_to_dir, dir_to_compare)):  # pylint: disable=unused-variable
            for directory in dirnames:
                for (dirpath_2, dirnames_2, filenames_2) in walk(os.path.join(  # pylint: disable=unused-variable
                        dirpath, directory)):
                    for file in filenames_2:
                        if file == '.DS_Store':
                            continue
                        given_output_file = os.path.join(
                            dirpath_2, file)
                        calculated_output_file = os.path.join(
                            constants.USER_OUTPUT_DIR, dir_to_compare, directory, file)

                        # are these two files equal?
                        self.compare_two_map_files(
                            given_output_file, calculated_output_file)

        # check files in given dir - {country} folder. filtered_* files
        for file in get_files_in_folder(os.path.join(path_to_dir, country)):
            if file == '.DS_Store':
                continue
            given_output_file = os.path.join(
                path_to_dir, country, file)
            calculated_output_file = os.path.join(
                constants.USER_OUTPUT_DIR, country, file)

            # are these two files equal?
            self.compare_two_map_files(
                given_output_file, calculated_output_file)

    def compare_two_map_files(self, given_file, calculated_file):
        """
        compare two given (map) files for equalness.
        macOS / Linux:
        - classic map files are compared using CLI command "osmium diff",
        - the others are compared using "filecmp.cmp"
        Windows:
        - compare all files using "filecmp.cmp".
          osmosis and osmconvert do not offer a possibility to compare with returning a errorcode
        """

        no_osmosis_file_extensions = ['shx', 'shp', 'prj']

        # some file extensions can not be comapared using osmium
        if given_file.split('.')[-1] in no_osmosis_file_extensions:
            # platform.system() == "Windows":
            self.assertTrue(filecmp.cmp(given_file, calculated_file,
                                        shallow=False), f'not equal: {calculated_file}. Using filecmp.cmp.')
        # compare map files using osmium
        else:
            cmd = ['osmium', 'diff', '-q',
                   given_file, calculated_file]
            result = subprocess.run(cmd, check=False)

            self.assertEqual(
                0, result.returncode, f'not equal: {calculated_file}. Using osmium diff.')


if __name__ == '__main__':
    unittest.main()
