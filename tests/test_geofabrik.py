"""
tests for the downloader file
"""
import os
# import sys
import unittest
from shapely.geometry import shape  # pylint: disable=import-error

# import custom python packages
from wahoomc.geofabrik import CountryGeofabrik, XYCombinationHasNoCountries, XYGeofabrik
from wahoomc.geofabrik import calc_bounding_box_tiles
from wahoomc.downloader import Downloader
from wahoomc import constants
from wahoomc.geofabrik_json import CountyIsNoGeofabrikCountry, GeofabrikJson


def calc_tiles_via_geofabrik_json(input_argument):
    """
    calculate tiles using downloaded geofabrik file
    the "new" way of doing
    """
    o_geofabrik = CountryGeofabrik(input_argument)
    tiles_via_geofabrik_json = o_geofabrik.get_tiles_of_wanted_map()

    return tiles_via_geofabrik_json


def calc_tiles_via_geofabrik_json_xy(input_argument):
    """
    calculate tiles using downloaded geofabrik file via x/y attributes as input
    the "new" way of doing
    """
    o_geofabrik = XYGeofabrik(input_argument)
    tiles_via_geofabrik_json = o_geofabrik.get_tiles_of_wanted_map()

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

    def test_tiles_via_geofabrik_malta_xy(self):
        """
        Test the retrieval of tiles via geofabrik URL against hardcoded data
        """
        item_0 = [{'x': 138, 'y': 100, 'left': 14.0625, 'top': 36.59788913307021, 'right': 15.46875, 'bottom': 35.4606699514953, 'countries': [
            'italy', 'malta'], 'urls': ['https://download.geofabrik.de/europe/italy-latest.osm.pbf', 'https://download.geofabrik.de/europe/malta-latest.osm.pbf']}]

        geofabrik_tiles = calc_tiles_via_geofabrik_json_xy('138/100')

        self.assertEqual(item_0, geofabrik_tiles)

    def test_tiles_via_geofabrik_xy(self):
        """
        Test the retrieval of tiles via geofabrik URL against hardcoded data
        """
        geofabrik_tiles_exp = [{
            "x": 133,
            "y": 88,
            "left": 7.03125,
            "top": 48.92249926375824,
            "right": 8.4375,
            "bottom": 47.98992166741417,
            "countries": [
                "france",
                "germany"
            ],
            'urls': ['https://download.geofabrik.de/europe/france-latest.osm.pbf',
                     'https://download.geofabrik.de/europe/germany-latest.osm.pbf']
        }]

        geofabrik_tiles = calc_tiles_via_geofabrik_json_xy('133/88')

        self.assertEqual(geofabrik_tiles_exp, geofabrik_tiles)

    def test_bbox_and_shape_malta(self):
        """
        Test several small steps in geofabrik processing for countries
        """
        input_country = 'malta'

        bbox_exp = {'top_x': 137, 'top_y': 100, 'bot_x': 138, 'bot_y': 100}

        bbox_tiles_exp = [{'x': 137, 'y': 100, 'tile_left': 12.65625, 'tile_top': 36.59788913307021, 'tile_right': 14.0625, 'tile_bottom': 35.4606699514953}, {
            'x': 138, 'y': 100, 'tile_left': 14.0625, 'tile_top': 36.59788913307021, 'tile_right': 15.46875, 'tile_bottom': 35.4606699514953}]

        tiles_exp = [{'x': 137, 'y': 100, 'left': 12.65625, 'top': 36.59788913307021, 'right': 14.0625, 'bottom': 35.4606699514953, 'countries': ['italy', 'malta'], 'urls': ['https://download.geofabrik.de/europe/italy-latest.osm.pbf', 'https://download.geofabrik.de/europe/malta-latest.osm.pbf']},
                     {'x': 138, 'y': 100, 'left': 14.0625, 'top': 36.59788913307021, 'right': 15.46875, 'bottom': 35.4606699514953, 'countries': ['italy', 'malta'], 'urls': ['https://download.geofabrik.de/europe/italy-latest.osm.pbf', 'https://download.geofabrik.de/europe/malta-latest.osm.pbf']}]

        wanted_region_exp = 'MULTIPOLYGON (((14 35.7517, 14 36.26791, 14.07957 36.33296, 14.39231 36.29082, 14.8561 35.98808, 14.84002 35.7246, 14.50306 35.51985, 14 35.7517)))'

        o_geofabrik = CountryGeofabrik('malta')
        o_geofabrik.get_tiles_of_wanted_map()

        o_geofabrik_json = GeofabrikJson()

        wanted_region = shape(
            o_geofabrik_json.get_geofabrik_geometry(input_country))
        self.assertEqual(wanted_region_exp, str(wanted_region))

        bbox = o_geofabrik.compose_bouding_box(wanted_region.bounds)
        self.assertEqual(bbox_exp, bbox)

        bbox_tiles = calc_bounding_box_tiles(
            bbox)
        self.assertEqual(bbox_tiles_exp, bbox_tiles)

        tiles_of_input = o_geofabrik.find_needed_countries(
            bbox_tiles, input_country, wanted_region)
        self.assertEqual(tiles_exp, tiles_of_input)

    def test_bbox_and_shape_xy(self):
        """
        Test several small steps in geofabrik processing for X/Y combination
        """
        bbox_tiles_exp = [{'x': 138, 'y': 100, 'tile_left': 14.0625,
                           'tile_top': 36.59788913307021, 'tile_right': 15.46875, 'tile_bottom': 35.4606699514953}]
        wanted_region_exp = 'POLYGON ((36.59788913307021 14.0625, 36.59788913307021 15.46875, 35.4606699514953 15.46875, 35.4606699514953 14.0625, 36.59788913307021 14.0625))'

        bbox = {'top_x': 138, 'bot_x': 138,
                'top_y': 100, 'bot_y': 100}

        bbox_tiles = calc_bounding_box_tiles(bbox)
        self.assertEqual(bbox_tiles_exp, bbox_tiles)

        o_geofabrik = XYGeofabrik('138/100')
        wanted_region_string = str(o_geofabrik.compose_shape(bbox_tiles))

        self.assertEqual(wanted_region_exp, wanted_region_string)

    def test_splitting_of_single_xy_coordinate(self):
        """
        use static json files in the repo to calculate relevant tiles
        """

        xy_tuple = XYGeofabrik.split_input_to_list("133/88")
        self.assertEqual(xy_tuple, [{"x": 133, "y": 88}])

        xy_tuple = XYGeofabrik.split_input_to_list("11/92")
        self.assertEqual(xy_tuple, [{"x": 11, "y": 92}])

        xy_tuple = XYGeofabrik.split_input_to_list("138/100")
        self.assertEqual(xy_tuple, [{"x": 138, "y": 100}])

    def test_splitting_of_multiple_xy_coordinate(self):
        """
        use static json files in the repo to calculate relevant tiles
        """

        xy_tuple = XYGeofabrik.split_input_to_list("133/88,138/100")
        expected_result = [{"x": 133, "y": 88}, {"x": 138, "y": 100}]

        self.assertEqual(xy_tuple, expected_result)

    def test_if_countrygeofabrik_raises_exception(self):
        """
        initialize CountryGeofabrik class and let the class check if the country is OK
        in other words: if the exception raised by translate_id_no_to_geofabrik
        is transported all up
        """
        CountryGeofabrik('germany')
        CountryGeofabrik('malta')
        CountryGeofabrik('malta,germany')

        with self.assertRaises(CountyIsNoGeofabrikCountry):
            CountryGeofabrik('germanyd')
        with self.assertRaises(CountyIsNoGeofabrikCountry):
            CountryGeofabrik('xy')
        with self.assertRaises(CountyIsNoGeofabrikCountry):
            CountryGeofabrik('maltad,germany')
        with self.assertRaises(CountyIsNoGeofabrikCountry):
            CountryGeofabrik('malta,tekke')

    def test_if_xy_geofabrik_raises_exception(self):
        """
        initialize XYGeofabrik class + check if xy coordinate has countries
        """
        o_geofabrik = XYGeofabrik('133/87')
        o_geofabrik.get_tiles_of_wanted_map()

        o_geofabrik = XYGeofabrik('100/138')
        o_geofabrik.get_tiles_of_wanted_map()

        o_geofabrik = XYGeofabrik('138/100')
        o_geofabrik.get_tiles_of_wanted_map()

        with self.assertRaises(XYCombinationHasNoCountries):
            o_geofabrik = XYGeofabrik('200/1')
            o_geofabrik.get_tiles_of_wanted_map()

    # def test_get_tile_via_xy_coordinate_error(self):
    #     """
    #     use static json files in the repo to calculate a not-existing tile.

    #     does not error out due to new Geofabrik Json processing. Nevertheless, the tile is not existing
    #     only +/- 180 -/+90: https://epsg.io/4326
    #     """

    #     o_geofabrik = XYGeofabrik([{"x": 200, "y": 1}])

    #     # tiles =

    #     with self.assertRaises(TileNotFoundError):
    #         o_geofabrik.get_tiles_of_wanted_map()


if __name__ == '__main__':
    unittest.main()
