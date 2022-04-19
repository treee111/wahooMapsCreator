"""
tests for the downloader file
"""
import os
# import sys
import unittest

# import custom python packages
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common_python.osm_maps_functions import OsmMaps
from common_python.osm_maps_functions import get_tile_by_one_xy_combination_from_jsons
from common_python.osm_maps_functions import get_xy_coordinates_from_input
from common_python.osm_maps_functions import TileNotFoundError
from common_python.input import InputData
from common_python import file_directory_functions as fd_fct
from common_python import constants_functions as const_fct


class TestOsmMaps(unittest.TestCase):
    """
    tests for the OSM maps file
    """

    def setUp(self):
        o_input_data = InputData()

        self.o_osm_maps = OsmMaps(o_input_data)

    def test_input_country_malta(self):
        """
        Test "malta" as input to the wahooMapsCreator
        check, if the given input-parameter is saved to the OsmMaps instance
        """

        self.o_osm_maps.o_input_data.country = 'malta'
        self.o_osm_maps.process_input(True)

        result = self.o_osm_maps.country_name
        self.assertEqual(result, 'malta')

    def test_calc_border_countries_input_country(self):
        """
        Test initialized border countries
        - of malta
        - of germany
        """

        # malta
        self.process_and_check_border_countries(
            'malta', True, {'malta': {}}, 'country')

        # germany
        expected_result = {'czech_republic': {}, 'germany': {}, 'austria': {}, 'liechtenstein': {},
                           'switzerland': {}, 'italy': {}, 'netherlands': {}, 'belgium': {},
                           'luxembourg': {}, 'france': {}, 'poland': {}, 'denmark': {}}
        self.process_and_check_border_countries(
            'germany', True, expected_result, 'country')

    def test_calc_border_countries_input_xy_coordinates_1tile(self):
        """
        Test initialized border countries
        - of a file with 1 tile and two countries
        """

        # one tile - france and germany
        expected_result = {'france': {}, 'germany': {}}
        self.process_and_check_border_countries(
            "133/88", True, expected_result, 'xy_coordinate')

    def test_calc_border_countries_input_xy_coordinates_2tiles(self):
        """
        Test initialized border countries
        - of a file with 2 tiles and one country
        """

        # two tiles - germany
        expected_result = {'germany': {}}
        self.process_and_check_border_countries(
            "134/87,134/88", True, expected_result, 'xy_coordinate')

    def test_calc_without_border_countries_input_country(self):
        """
        Test initialized countries without border countries
        - of germany
        - of china
        - of one tile
        """

        # germany
        self.process_and_check_border_countries(
            'germany', False, {'germany': {}}, 'country')

        # china
        self.process_and_check_border_countries(
            'china', False, {'china': {}}, 'country')

    def test_calc_without_border_countries__xy_coordinates_1tile(self):
        """
        Test initialized countries without border countries
        - of one tile
        """

        # one tile - france and germany
        expected_result = {'france': {}, 'germany': {}}
        self.process_and_check_border_countries(
            "133/88", False, expected_result, 'xy_coordinate')

    def test_calc_without_border_countries__xy_coordinates_2tiles(self):
        """
        Test initialized countries without border countries
        - of two tiles
        """

        # two tiles - germany
        expected_result = {'germany': {}}
        self.process_and_check_border_countries(
            "134/87,134/88", False, expected_result, 'xy_coordinate')

    def test_tiles_via_static_json(self):
        """
        Test the retrieval of tiles via geofabrik URL against hardcoded data for germany
        """
        expected_tiles = [{'x': 138, 'y': 100, 'left': 14.0625, 'top': 36.597889,
                           'right': 15.46875, 'bottom': 35.46067, 'countries': ['malta']}]
        self.calculate_tiles_via_static_json('malta', expected_tiles)

    def process_and_check_border_countries(self, inp_val, calc_border_c, exp_result, inp_mode):
        """
        helper method to process a country or json file and check the calculated border countries
        """

        if inp_mode == 'country':
            self.o_osm_maps.o_input_data.country = inp_val
        elif inp_mode == 'xy_coordinate':
            self.o_osm_maps.o_input_data.xy_coordinates = inp_val

        self.o_osm_maps.process_input(calc_border_c)
        result = self.o_osm_maps.border_countries

        self.assertEqual(result, exp_result)

    def calculate_tiles_via_static_json(self, country, expected_result):
        """
        use static json files in the repo to calculate relevant tiles
        """

        json_file_path = os.path.join(fd_fct.COMMON_DIR, 'json',
                                      const_fct.get_region_of_country(country), country + '.json')
        tiles = fd_fct.read_json_file(json_file_path)

        self.assertEqual(tiles, expected_result)

    def test_splitting_of_single_xy_coordinate(self):
        """
        use static json files in the repo to calculate relevant tiles
        """

        xy_tuple = get_xy_coordinates_from_input("133/88")

        self.assertEqual(xy_tuple, [{"x": 133, "y": 88}])

        xy_tuple = get_xy_coordinates_from_input("11/92")

        self.assertEqual(xy_tuple, [{"x": 11, "y": 92}])

        xy_tuple = get_xy_coordinates_from_input("138/100")
        expected_result = [{"x": 138, "y": 100}]

        self.assertEqual(xy_tuple, expected_result)

    def test_splitting_of_multiple_xy_coordinate(self):
        """
        use static json files in the repo to calculate relevant tiles
        """

        xy_tuple = get_xy_coordinates_from_input("133/88,138/100")
        expected_result = [{"x": 133, "y": 88}, {"x": 138, "y": 100}]

        self.assertEqual(xy_tuple, expected_result)

    def test_get_tile_via_xy_coordinate(self):
        """
        use static json files in the repo to calculate relevant tile
        """

        tile = get_tile_by_one_xy_combination_from_jsons({"x": 133, "y": 88})

        expected_result = {
            "x": 133,
            "y": 88,
            "left": 7.03125,
            "top": 48.922499,
            "right": 8.4375,
            "bottom": 47.989922,
            "countries": [
                "france",
                "germany"
            ]
        }

        self.assertEqual(tile, expected_result)

    def test_get_tile_via_xy_coordinate_error(self):
        """
        use static json files in the repo to calculate a not-existing tile. 
        """

        with self.assertRaises(TileNotFoundError):
            get_tile_by_one_xy_combination_from_jsons({"x": 200, "y": 1})

    def test_encoding_open_sea_osm(self):
        """
        use static json files in the repo to calculate relevant tile
        """

        with open(os.path.join(fd_fct.COMMON_DIR, 'sea.osm')) as sea_file:  # pylint: disable=unspecified-encoding
            sea_data_no_encoding = sea_file.read()
        with open(os.path.join(fd_fct.COMMON_DIR, 'sea.osm'), encoding="utf-8") as sea_file:
            sea_data_utf8 = sea_file.read()

        self.assertEqual(sea_data_no_encoding, sea_data_utf8)


if __name__ == '__main__':
    unittest.main()
