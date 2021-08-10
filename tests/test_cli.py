"""
tests for the python file
"""
import os
import unittest

# import custom python packages


class TestCli(unittest.TestCase):
    """
    tests for the CLI of the python file
    """

    def test_cli_help(self):
        """
        tests, if help can be called
        """
        result =  os.system("python3 wahoo_map_creator.py -h")
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()
