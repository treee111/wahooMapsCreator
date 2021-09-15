"""
tests for the downloader file
"""
import os
# import sys
import unittest

# import custom python packages
from common_python.geofabrik import Geofabrik
from common_python import file_directory_functions as fd_fct
from common_python import constants_functions as const_fct
from common_python.downloader import Downloader


class TestGeofabrik(unittest.TestCase):
    """
    tests for the downloader file
    """

    def setUp(self):
        self.max_days_old = 14

        if not os.path.isfile(fd_fct.GEOFABRIK_PATH):
            o_downloader = Downloader(24, False)
            o_downloader.check_and_download_geofabrik_if_needed()


    def test_tiles_via_geofabrik_malta(self):
        """
        Test the retrieval of tiles via geofabrik URL against hardcoded data
        """
        item_0 = {'x': 137, 'y': 100, 'left': 12.65625, 'top': 36.59788913307021, 'right': 14.0625, 'bottom': 35.4606699514953, 'countries': ['italy', 'malta'], 'urls': ['https://download.geofabrik.de/europe/italy-latest.osm.pbf', 'https://download.geofabrik.de/europe/malta-latest.osm.pbf']}
        item_1 = {'x': 138, 'y': 100, 'left': 14.0625, 'top': 36.59788913307021, 'right': 15.46875, 'bottom': 35.4606699514953, 'countries': ['italy', 'malta'], 'urls': ['https://download.geofabrik.de/europe/italy-latest.osm.pbf', 'https://download.geofabrik.de/europe/malta-latest.osm.pbf']}

        geofabrik_tiles = self.calc_tiles_via_geofabrik_json('malta')

        self.assertEqual(item_0, geofabrik_tiles[0])
        self.assertEqual(item_1, geofabrik_tiles[1])        

    # def test_tiles_via_url_germany(self):
    #     """
    #     Test the retrieval of tiles via geofabrik URL against hardcoded data for germany
    #     """
    #     self.compare_url_and_static('germany')

    # def test_tiles_via_url_ireland(self):
    #     """
    #     Test the retrieval of tiles via URL
    #     """
    #     self.compare_url_and_static('ireland-and-northern-ireland')

    def compare_geofabrik_and_static(self, input_argument):
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
