"""
tests the generated files of a full-run of the tool against fixed files
"""

import filecmp
import os
from os import walk
import platform
import shutil
import unittest


# import custom python packages
from wahoomc import constants
from wahoomc.file_directory_functions import get_files_in_folder

dirname_of_file = os.path.dirname(__file__)


def copy_static_maps_input_file(country, given_osm_pbf):
    """
    copy given file to download-directory
    """
    given_osm_pbf_file = os.path.join(
        dirname_of_file, 'resources', given_osm_pbf)
    copy_to_path = os.path.join(
        constants.USER_MAPS_DIR, country + '-latest.osm.pbf')

    # copy file (new file takes creationdate as of now)
    shutil.copy2(given_osm_pbf_file, copy_to_path)


def copy_static_land_polygon_input_folder(given_osm_pbf):
    """
    copy given folder to download-directory
    """
    # get parent folder of repo
    root_dir_parent = os.path.abspath(
        os.path.join(constants.ROOT_DIR, os.pardir))

    static_file_path = os.path.join(
        root_dir_parent, 'unittest-files', given_osm_pbf)
    copy_to_path = os.path.dirname(constants.LAND_POLYGONS_PATH)

    # delete directory if exists. copytree fails if dir exists already
    if os.path.exists(copy_to_path):
        shutil.rmtree(copy_to_path)
    # copy folder (new file takes creationdate as of now)
    shutil.copytree(static_file_path, copy_to_path)


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
        copy_static_land_polygon_input_folder(
            'land-polygons-split-4326_2021-10-31')

        copy_static_maps_input_file(
            'malta', 'malta-latest_2021-10-31.osm.pbf')
        copy_static_maps_input_file(
            'liechtenstein', 'liechtenstein-latest_2021-10-31.osm.pbf')

    def test_calc_output_malta_and_compare(self):
        """
        Test output of countries without border countries
        - of malta
        """
        # run tool for country
        self.run_wahoomapscreator_cli('malta')

        # compare generated given merged.osm.pbf-file with reference-file
        self.compare_dir_sub_test_resource_and_output('138', 'malta')

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

                        # is file equal?
                        self.assertTrue(filecmp.cmp(given_output_file, calculated_output_file,
                                                    shallow=False), f'not equal: {calculated_output_file}')

        # check files in given dir
        # for file in get_files_in_folder(path_to_dir):
        #     if file == '.DS_Store':
        #         continue
        #     given_output_file = os.path.join(
        #         path_to_dir, file)
        #     calculated_output_file = os.path.join(
        #         constants.USER_OUTPUT_DIR, dir_to_compare, file)

        #     # is file equal?
        #     self.assertTrue(filecmp.cmp(given_output_file, calculated_output_file,
        #                                 shallow=False), f'not equal: {calculated_output_file}')

        # check files in given dir - {country} folder. filtered_* files
        for file in get_files_in_folder(os.path.join(path_to_dir, country)):
            if file == '.DS_Store':
                continue
            given_output_file = os.path.join(
                path_to_dir, country, file)
            calculated_output_file = os.path.join(
                constants.USER_OUTPUT_DIR, country, file)

            # is file equal?
            self.assertTrue(filecmp.cmp(given_output_file, calculated_output_file,
                                        shallow=False), f'not equal: {calculated_output_file}')


if __name__ == '__main__':
    unittest.main()
