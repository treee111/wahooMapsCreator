"""
tests for setup functions
"""
import unittest
import platform
import os
import pkg_resources

# import custom python packages
from wahoomc.setup_functions import is_program_installed, is_map_writer_plugin_installed, \
    read_version_last_run
from wahoomc.constants_functions import get_tooling_win_path
from wahoomc.constants import USER_WAHOO_MC, VERSION
from wahoomc.file_directory_functions import write_json_file_generic
from wahoomc.downloader import get_latest_pypi_version


class TestSetup(unittest.TestCase):
    """
    tests for the required non-python programs of the python module
    """

    def test_installed_programs_mac(self):
        """
        tests, if the mac-relevant programs are installed
        """
        if platform.system() != "Windows":
            self.check_installation_of_program("java")

            self.check_installation_of_program("osmium")
            self.check_installation_of_program("osmosis")

            result = is_map_writer_plugin_installed()
            self.assertTrue(result)

    def test_installed_programs_windows(self):
        """
        tests, if the windows-relevant programs are installed
        """
        if platform.system() == "Windows":
            self.check_installation_of_program("java")

            self.assertTrue(os.path.exists(get_tooling_win_path(
                os.path.join('Osmosis', 'bin', 'osmosis.bat'), in_user_dir=True)))
            self.assertTrue(os.path.exists(
                get_tooling_win_path('osmconvert.exe')))
            self.assertTrue(os.path.exists(
                get_tooling_win_path('osmfilter.exe', in_user_dir=True)))
            self.assertTrue(os.path.exists(get_tooling_win_path('7za.exe')))

    def check_installation_of_program(self, program):
        """
        tests, if a given program is installed
        """
        result = is_program_installed(program)

        self.assertTrue(result)


class TestConfigFile(unittest.TestCase):
    """
    tests for the config .json file in the "wahooMapsCreatorData" directory
    """

    config_file_path = os.path.join(USER_WAHOO_MC, ".config.json")

    def test_version_if_no_config_file_exists(self):
        """
        tests, if the return value is None if the config file is deleted
        """
        if os.path.exists(self.config_file_path):
            os.remove(self.config_file_path)

        self.assertEqual(None, read_version_last_run())

    def test_version_if_written_eq(self):
        """
        tests, if return version is the one saved
        """
        # write dictionary to config file
        write_json_file_generic(self.config_file_path, {
                                "version_last_run": '2.0.2'})

        self.assertEqual('2.0.2', read_version_last_run())

    def test_version_if_written_neq(self):
        """
        tests, if the comparison of the returned version_last_run is OK
        """
        # write dictionary to config file
        write_json_file_generic(self.config_file_path, {
                                "version_last_run": '2.0.3'})

        self.assertNotEqual('2.0.2', read_version_last_run())

    def test_version_constants_against_pypi(self):
        """
        tests, if the version of constants.py is equal to the latest available version on PyPI
        """
        latest_version = pkg_resources.parse_version(
            get_latest_pypi_version()).public

        self.assertEqual(
            VERSION, latest_version)


if __name__ == '__main__':
    unittest.main()
