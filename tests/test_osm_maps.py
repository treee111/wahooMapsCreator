"""
tests for the downloader file
"""
import os
# import sys
import unittest

# import custom python packages
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common_python.osm_maps_functions import OsmMaps
from common_python.osm_maps_functions import get_tile_by_xy_coordinate
from common_python.osm_maps_functions import get_xy_coordinate_from_input
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

        self.file_path_test_json = os.path.join(os.getcwd(), 'tests', 'json')

    def test_input_country_malta(self):
        """
        Test "malta" as input to the wahooMapsCreator
        check, if the given input-parameter is saved to the OsmMaps instance
        """

        self.o_osm_maps.o_input_data.country = 'malta'
        self.o_osm_maps.process_input(True)

        result = self.o_osm_maps.country_name
        self.assertEqual(result, 'malta')

    def test_input_json_file(self):
        """
        Test a json file as input to the wahooMapsCreator
        check, if the given input-parameter is saved to the OsmMaps instance
        """
        json_file_path = os.path.join(
            self.file_path_test_json, 'germany-only1.json')

        self.o_osm_maps.o_input_data.tile_file = json_file_path
        self.o_osm_maps.process_input(True)

        result = self.o_osm_maps.country_name
        self.assertEqual(result, 'germany-only1')

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

    def test_calc_border_countries_input_json_file(self):
        """
        Test initialized border countries
        - of a file with 1 tile
        - of a file with 2 tiles
        """

        # one tile - france and germany
        input_file = os.path.join(
            self.file_path_test_json, 'germany-france-only1.json')
        expected_result = {'france': {}, 'germany': {}}
        self.process_and_check_border_countries(
            input_file, True, expected_result, 'json_file')

        # two tiles - germany
        input_file = os.path.join(
            self.file_path_test_json, 'germany-only2.json')
        expected_result = {'germany': {}}
        self.process_and_check_border_countries(
            input_file, True, expected_result, 'json_file')

    def test_calc_without_border_countries(self):
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

        # one tile - france and germany
        input_file = os.path.join(
            self.file_path_test_json, 'germany-france-only1.json')
        expected_result = {'france': {}, 'germany': {}}
        self.process_and_check_border_countries(
            input_file, False, expected_result, 'json_file')

        # two tiles - germany
        input_file = os.path.join(
            self.file_path_test_json, 'germany-only2.json')
        expected_result = {'germany': {}}
        self.process_and_check_border_countries(
            input_file, False, expected_result, 'json_file')

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
        elif inp_mode == 'json_file':
            self.o_osm_maps.o_input_data.tile_file = inp_val

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

    def test_splitting_of_xy_coordinate(self):
        """
        use static json files in the repo to calculate relevant tiles
        """
        x_coord, y_coord = get_xy_coordinate_from_input("133/88")

        self.assertEqual(x_coord, 133)
        self.assertEqual(y_coord, 88)

        x_coord, y_coord = get_xy_coordinate_from_input("11/92")

        self.assertEqual(x_coord, 11)
        self.assertEqual(y_coord, 92)

    def test_get_tile_via_xy_coordinate(self):
        """
        use static json files in the repo to calculate relevant tiles
        """
        tile = get_tile_by_xy_coordinate(133, 88)

        expected_result = fd_fct.read_json_file(
            '/Users/benjamin/VSCode/wahooMapsCreator/tests/json/germany-only9.json')

        self.assertEqual(tile, expected_result[3])


if __name__ == '__main__':
    unittest.main()
