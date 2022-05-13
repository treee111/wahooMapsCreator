"""
tests for setup functions
"""
import unittest
import platform

# import custom python packages
from wahoomc.setup_functions import is_program_installed, is_map_writer_plugin_installed


class TestSetup(unittest.TestCase):
    """
    tests for the required non-python programs of the python module
    """

    def test_installed_programs_mac(self):
        """
        tests, if the mac-relevant programs are installed
        """
        self.check_installation_of_program("java")

        if platform.system() != "Windows":
            self.check_installation_of_program("osmium")
            self.check_installation_of_program("osmosis")

            result = is_map_writer_plugin_installed()
            self.assertTrue(result)

    def check_installation_of_program(self, program):
        """
        tests, if a given program is installed
        """

        result = is_program_installed(program)

        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
