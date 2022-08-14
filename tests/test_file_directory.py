"""
tests for file directory functions file
"""
import os
import unittest

from wahoomc import file_directory_functions as fd_fct
from wahoomc.file_directory_functions import TagWahooXmlNotFoundError
from wahoomc import constants


class TestFileDirectory(unittest.TestCase):
    """
    tests for file directory functions
    """

    def test_not_existing_tag_wahoo_xml(self):
        """
        check if a non-existing tag-wahoo xml file issues an exception
        """
        with self.assertRaises(TagWahooXmlNotFoundError):
            fd_fct.get_tag_wahoo_xml_path("not_existing.xml")

    def test_existing_tag_wahoo_xml(self):
        """
        check if the correct path of an existing tag-wahoo xml file is returned
        """

        expected_path = os.path.join(
            constants.RESOURCES_DIR, "tag_wahoo_adjusted", "tag-wahoo-poi.xml")
        self.assertEqual(fd_fct.get_tag_wahoo_xml_path(
            "tag-wahoo-poi.xml"), expected_path)


if __name__ == '__main__':
    unittest.main()
