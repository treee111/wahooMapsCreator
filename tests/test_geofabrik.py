"""
tests for the downloader file
"""
import os
# import sys
import unittest

# import custom python packages
from wahoomc.geofabrik import Geofabrik
from wahoomc.downloader import Downloader
from wahoomc import constants


def calc_tiles_via_geofabrik_json(input_argument):
    """
    calculate tiles using downloaded geofabrik file
    the "new" way of doing
    """
    o_geofabrik = Geofabrik(input_argument)
    tiles_via_geofabrik_json = o_geofabrik.get_tiles_of_country()

    return tiles_via_geofabrik_json


class TestGeofabrik(unittest.TestCase):
    """
    tests for the downloader file
    """

    def setUp(self):
        self.max_days_old = 14

        if not os.path.isfile(constants.GEOFABRIK_PATH):
            o_downloader = Downloader(24, False)
            o_downloader.download_geofabrik_file()

    def test_tiles_via_geofabrik_malta(self):
        """
        Test the retrieval of tiles via geofabrik URL against hardcoded data
        """
        item_0 = {'x': 137, 'y': 100, 'left': 12.65625, 'top': 36.59788913307021,
                  'right': 14.0625, 'bottom': 35.4606699514953, 'countries': ['italy', 'malta'],
                  'urls': ['https://download.geofabrik.de/europe/italy-latest.osm.pbf',
                           'https://download.geofabrik.de/europe/malta-latest.osm.pbf']}
        item_1 = {'x': 138, 'y': 100, 'left': 14.0625, 'top': 36.59788913307021,
                  'right': 15.46875, 'bottom': 35.4606699514953, 'countries': ['italy', 'malta'],
                  'urls': ['https://download.geofabrik.de/europe/italy-latest.osm.pbf',
                           'https://download.geofabrik.de/europe/malta-latest.osm.pbf']}

        geofabrik_tiles = calc_tiles_via_geofabrik_json('malta')

        self.assertEqual(item_0, geofabrik_tiles[0])
        self.assertEqual(item_1, geofabrik_tiles[1])


if __name__ == '__main__':
    unittest.main()
