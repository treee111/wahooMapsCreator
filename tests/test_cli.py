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

    def test_top_parser_help(self):
        """
        tests, if help of top parser can be called
        """

        result = os.system("python -h wahoomc -h")

        self.assertEqual(result, 0)

    def test_cli_help(self):
        """
        tests, if CLI help can be called
        """

        result = os.system("python -h wahoomc cli -h")

        self.assertEqual(result, 0)

    def test_gui_help(self):
        """
        tests, if GUI help can be called
        """

        result = os.system("python -h wahoomc gui -h")

        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
