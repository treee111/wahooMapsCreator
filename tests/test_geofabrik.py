"""
tests for the downloader file
"""
import os
# import sys
import unittest

# import custom python packages
from common_resources.geofabrik import Geofabrik
from common_resources import file_directory_functions as fd_fct
from common_resources import constants_functions as const_fct
from common_resources.downloader import Downloader


class TestDownloader(unittest.TestCase):
    """
    tests for the downloader file
    """

    def setUp(self):
        self.max_days_old = 14

        if not os.path.isfile(fd_fct.GEOFABRIK_PATH):
            o_downloader = Downloader(24, False)
            o_downloader.check_and_download_geofabrik_if_needed()


    def test_tiles_via_url_malta(self):
        """
        Test the retrieval of tiles via URL
        """
        self.compare_url_and_static('malta')

    def test_tiles_via_url_germany(self):
        """
        Test the retrieval of tiles via URL
        """
        self.compare_url_and_static('germany')

    def test_tiles_via_url_ireland(self):
        """
        Test the retrieval of tiles via URL
        """
        self.compare_url_and_static('ireland-and-northern-ireland')

    def compare_url_and_static(self, input_argument):
        """
        Compare the retrieval of tiles via URL with statis json
        """
        tiles_via_geofabrik_json = self.calc_tiles_via_geofabrik_json(input_argument)

        tiles_via_static_json = self.calc_tiles_via_static_jsons(input_argument)

        self.assertEqual(tiles_via_geofabrik_json, tiles_via_static_json)

    def calc_tiles_via_geofabrik_json(self, input_argument):
        """
        calculate tiles using downloaded geofabrik file
        the "new" way of doing
        """
        o_geofabrik = Geofabrik(input_argument)
        tiles_via_geofabrik_json = o_geofabrik.get_tiles_of_country()

        return tiles_via_geofabrik_json

    def calc_tiles_via_static_jsons(self, input_argument):
        """
        calculate tiles using the json files in the repo
        the "old" way of doing
        """
        json_file_path = os.path.join (fd_fct.COMMON_DIR, 'json',
            const_fct.get_region_of_country(input_argument), input_argument + '.json')
        tiles_via_static_json = fd_fct.read_json_file(json_file_path)

        return tiles_via_static_json


if __name__ == '__main__':
    unittest.main()
