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
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common_python import file_directory_functions as fd_fct


class TestGeneratedFiles(unittest.TestCase):
    """
    tests for the OSM maps file
    """

    def setUp(self):
        # copy given file to download-directory
        given_osm_pbf_file = os.path.join(
            fd_fct.ROOT_DIR, 'tests/resources', 'malta-latest_2021-10-22.osm.pbf')
        map_file_path = os.path.join(
            fd_fct.MAPS_DIR, 'malta' + '-latest.osm.pbf')

        # copy file (new file takes creationdate as of now)
        shutil.copy2(given_osm_pbf_file, map_file_path)

        # run processing for malta via CLI
        if platform.system() == "Windows":
            result = os.system(
                "python wahoo_map_creator.py -tag tag-wahoo.xml -fp -c -md 100")
        else:
            result = os.system(
                "python3 wahoo_map_creator.py malta -tag tag-wahoo.xml -fp -c -md 100")

        # check if run was successful
        self.assertEqual(result, 0)

    def test_calc_output_malta(self):
        """
        Test output of countries without border countries
        - of malta

        Using given input .osm.pbf file in this repo
        Compare calculated merged.osm.pbf with merged.osm.pbf in this repo

        Files that can be possibly checked (in order of creation):
        - merged.osm.pbf
        - 100.map
        - 100.map.lzma
        """

        # malta
        # compare generated given merged.osm.pbf-file with reference-file
        # equals_merged = self.compare_test_resource_and_output(
        #     '138/100/merged.osm.pbf')
        self.compare_dir_sub_test_resource_and_output('138/100')

    def test_calc_output_iceland(self):
        """
        Test output of countries without border countries
        - of malta

        Using given input .osm.pbf file in this repo
        Compare calculated merged.osm.pbf with merged.osm.pbf in this repo

        Files that can be possibly checked (in order of creation):
        - merged.osm.pbf
        - 100.map
        - 100.map.lzma
        """

        # iceland
        self.compare_dir_sub_test_resource_and_output('110')
        self.compare_dir_sub_test_resource_and_output('111')
        self.compare_dir_sub_test_resource_and_output('112')
        self.compare_dir_sub_test_resource_and_output('113')
        self.compare_dir_sub_test_resource_and_output('114')
        self.compare_dir_sub_test_resource_and_output('115')
        self.compare_dir_sub_test_resource_and_output('116')
        self.compare_dir_sub_test_resource_and_output('117')
        self.compare_dir_sub_test_resource_and_output('118')

    def compare_test_resource_and_output(self, filename_to_compare):
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

    def compare_dir_test_resource_and_output(self, dir_to_compare):
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

    def compare_dir_sub_test_resource_and_output(self, dir_to_compare):
        """
        compare files from given directory and subdirectories for equalness.
        check the files which are in test/resources folder
        """

        path_to_dir = os.path.join(
            fd_fct.ROOT_DIR, 'tests/resources', dir_to_compare)

        # check files in subdir of given dir
        for (dirpath, dirnames, filenames) in walk(path_to_dir):
            for directory in dirnames:
                for (dirpath_2, dirnames_2, filenames_2) in walk(os.path.join(
                        dirpath, directory)):
                    for file in filenames_2:
                        given_output_file = os.path.join(
                            dirpath_2, file)
                        calculated_output_file = os.path.join(
                            fd_fct.ROOT_DIR, 'output', dir_to_compare, directory, file)

                        # is file equal?
                        self.assertTrue(filecmp.cmp(given_output_file, calculated_output_file,
                                                    shallow=False), 'You error message')

        # check files in given dir
        for (dirpath, dirnames, filenames) in walk(path_to_dir):
            for file in filenames:
                given_output_file = os.path.join(
                    dirpath, file)
                calculated_output_file = os.path.join(
                    fd_fct.ROOT_DIR, 'output', dir_to_compare, file)

                # is file equal?
                self.assertTrue(filecmp.cmp(given_output_file, calculated_output_file,
                                            shallow=False), 'You error message')


if __name__ == '__main__':
    unittest.main()
