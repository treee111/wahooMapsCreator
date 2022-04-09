"""
tests the generated files of a full-run of the tool against fixed files
"""

import filecmp
import os
from os import listdir
from os import walk
from os.path import isfile, join
import platform
import shutil
import unittest


# import custom python packages
from common_python import file_directory_functions as fd_fct

dirname_of_file = os.path.dirname(__file__)


def copy_static_maps_input_file(country, given_osm_pbf):
    """
    copy given file to download-directory
    """

    given_osm_pbf_file = os.path.join(
        dirname_of_file, 'resources', given_osm_pbf)
    copy_to_path = os.path.join(
        fd_fct.MAPS_DIR, country + '-latest.osm.pbf')

    # copy file (new file takes creationdate as of now)
    shutil.copy2(given_osm_pbf_file, copy_to_path)


def copy_static_land_polygon_input_folder(given_osm_pbf):
    """
    copy given folder to download-directory
    """

    # get parent folder of repo
    root_dir_parent = os.path.abspath(
        os.path.join(fd_fct.ROOT_DIR, os.pardir))

    static_file_path = os.path.join(
        root_dir_parent, 'unittest-files', given_osm_pbf)
    copy_to_path = os.path.dirname(fd_fct.LAND_POLYGONS_PATH)

    # delete directory if exists. copytree fails if dir exists already
    if os.path.exists(copy_to_path):
        shutil.rmtree(copy_to_path)
    # copy folder (new file takes creationdate as of now)
    shutil.copytree(static_file_path, copy_to_path)


def compare_test_resource_and_output(filename_to_compare):
    """
    compare if two files are equal.
    """

    given_output_file = os.path.join(
        fd_fct.ROOT_DIR, 'tests/resources', filename_to_compare)

    calculated_output_file = os.path.join(
        fd_fct.ROOT_DIR, 'output', filename_to_compare)

    # https://stackoverflow.com/questions/42512016/how-to-compare-two-files-as-part-of-unittest-while-getting-useful-output-in-cas
    # filecmp.clear_cache()
    files_are_equal = filecmp.cmp(given_output_file, calculated_output_file,
                                  shallow=False)

    # another possibility to compare files.
    # if open(calculated_output_file, "rb").read() == open(
    #         given_output_file, "rb").read():
    #     files_are_equal = True

    return files_are_equal


def compare_dir_test_resource_and_output(dir_to_compare):
    """
    compare if two files are equal.
    """

    path_to_dir = os.path.join(
        fd_fct.ROOT_DIR, 'tests/resources', dir_to_compare)

    onlyfiles = [f for f in listdir(
        path_to_dir) if isfile(join(path_to_dir, f))]

    for file in onlyfiles:

        given_output_file = os.path.join(
            fd_fct.ROOT_DIR, 'tests/resources', dir_to_compare, file)

        calculated_output_file = os.path.join(
            fd_fct.ROOT_DIR, 'output', dir_to_compare, file)

        # https://stackoverflow.com/questions/42512016/how-to-compare-two-files-as-part-of-unittest-while-getting-useful-output-in-cas
        # filecmp.clear_cache()
        files_are_equal = filecmp.cmp(given_output_file, calculated_output_file,
                                      shallow=False)

        # another possibility to compare files.
        # if open(calculated_output_file, "rb").read() == open(
        #         given_output_file, "rb").read():
        #     files_are_equal = True

        return files_are_equal


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

    # def setUp(self):
    #     self.copy_static_land_polygon_input_folder(
    #         'land-polygons-split-4326_2021-10-31')

    #     self.copy_static_maps_input_file(
    #         'malta', 'malta-latest_2021-10-31.osm.pbf')
    #     self.copy_static_maps_input_file(
    #         'liechtenstein', 'liechtenstein-latest_2021-10-31.osm.pbf')

    def test_1_setup(self):  # pylint: disable=no-self-use
        """
        Copy defined static land-polygons and .osm.pbf files.
        The files are used in the launch.json configs "test_2_malta" and "test_2_liech"
        """

        copy_static_land_polygon_input_folder(
            'land-polygons-split-4326_2021-10-31')

        copy_static_maps_input_file(
            'malta', 'malta-latest_2021-10-31.osm.pbf')
        copy_static_maps_input_file(
            'liechtenstein', 'liechtenstein-latest_2021-10-31.osm.pbf')

    def test_3_malta_compare_output(self):
        """
        Compare output of countries without border countries
        - of malta
        """

        # compare generated given merged.osm.pbf-file with reference-file
        self.compare_dir_sub_test_resource_and_output(
            os.path.join('138', '100'))

    def test_3_liech_compare_output(self):
        """
        Compare output of countries without border countries
        - of liechtenstein
        """

        # compare generated given merged.osm.pbf-file with reference-file
        self.compare_dir_sub_test_resource_and_output(
            os.path.join('134', '89'))

    # def test_calc_output_malta(self):
    #     """
    #     Test output of countries without border countries
    #     - of malta
    #     """

    #     # run tool for countries
    #     self.run_wahoomapscreator_cli(
    #         'malta', 'malta-latest_2021-10-31.osm.pbf')

    #     # compare generated given merged.osm.pbf-file with reference-file
    #     # equals_merged = self.compare_test_resource_and_output(
    #     #     '138/100/merged.osm.pbf')
    #     self.compare_dir_sub_test_resource_and_output(
    #         os.path.join('138', '100'))

    # def test_calc_output_liechtenstein(self):
    #     """
    #     Test output of countries without border countries
    #     - of liechtenstein
    #     """

    #     # run tool for country
    #     self.run_wahoomapscreator_cli(
    #         'liechtenstein', 'liechtenstein-latest_2021-10-31.osm.pbf')

    #     # compare generated given merged.osm.pbf-file with reference-file

    #     self.compare_dir_sub_test_resource_and_output(
    #         os.path.join('134', '89'))

    def run_wahoomapscreator_cli(self, country, given_osm_pbf):
        """
        runs wahooMapsCreator for given country and static osm.pbf file via CLI
        """
        copy_static_maps_input_file(country, given_osm_pbf)

        # run processing of input-country via CLI
        if platform.system() == "Windows":
            cli_command = "python"
        else:
            cli_command = "python3"

        result = os.system(
            f'{cli_command} wahoo_map_creator.py {country} -tag tag-wahoo.xml -fp -c -md 100')

        # check if run was successful
        self.assertEqual(result, 0)

    def compare_dir_sub_test_resource_and_output(self, dir_to_compare):
        """
        compare files from given directory and subdirectories for equalness.
        check the files which are in test/resources folder
        """

        if platform.system() == "Windows":
            path_to_dir = os.path.join(
                dirname_of_file, 'resources', 'windows', dir_to_compare)
        else:
            path_to_dir = os.path.join(
                dirname_of_file, 'resources', 'macos', dir_to_compare)

        # check files in subdir of given dir
        for (dirpath, dirnames, filenames) in walk(path_to_dir):
            for directory in dirnames:
                for (dirpath_2, dirnames_2, filenames_2) in walk(os.path.join(  # pylint: disable=unused-variable
                        dirpath, directory)):
                    for file in filenames_2:
                        given_output_file = os.path.join(
                            dirpath_2, file)
                        calculated_output_file = os.path.join(
                            fd_fct.OUTPUT_DIR, dir_to_compare, directory, file)

                        # is file equal?
                        self.assertTrue(filecmp.cmp(given_output_file, calculated_output_file,
                                                    shallow=False), f'not equal: {calculated_output_file}')

        # check files in given dir
        for (dirpath, dirnames, filenames) in walk(path_to_dir):
            for file in filenames:
                given_output_file = os.path.join(
                    dirpath, file)
                calculated_output_file = os.path.join(
                    fd_fct.OUTPUT_DIR, dir_to_compare, file)

                # is file equal?
                self.assertTrue(filecmp.cmp(given_output_file, calculated_output_file,
                                            shallow=False), f'not equal: {calculated_output_file}')


if __name__ == '__main__':
    unittest.main()
