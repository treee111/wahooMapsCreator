"""
tests for setup functions
"""
import unittest
import platform
import os

# import custom python packages
from wahoomc.setup_functions import is_program_installed
from wahoomc.setup_functions import is_map_writer_plugin_installed
from wahoomc.constants_functions import get_tooling_win_path


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
        tests, if the mac-relevant programs are installed
        """
        if platform.system() == "Windows":
            self.check_installation_of_program("java")

            self.assertTrue(os.path.exists(get_tooling_win_path(
                ['Osmosis', 'bin', 'osmosis.bat'])))
            self.assertTrue(os.path.exists(
                get_tooling_win_path(['osmconvert.exe'])))
            self.assertTrue(os.path.exists(
                get_tooling_win_path(['osmfilter.exe'])))
            self.assertTrue(os.path.exists(get_tooling_win_path(['7za.exe'])))

    def check_installation_of_program(self, program):
        """
        tests, a given program is installed
        """

        result = is_program_installed(program)

        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
