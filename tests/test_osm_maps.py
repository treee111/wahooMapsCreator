"""
tests for the downloader file
"""
import os
# import sys
import unittest

# import custom python packages
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common_python.osm_maps_functions import OsmMaps
from common_python.input import InputData
from common_python import file_directory_functions as fd_fct
from common_python import constants_functions as const_fct
from common_python import constants


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

        self.o_osm_maps.process_input('malta', True)

        result = self.o_osm_maps.country_name
        self.assertEqual(result, 'malta')

    def test_input_json_file(self):
        """
        Test a json file as input to the wahooMapsCreator
        check, if the given input-parameter is saved to the OsmMaps instance
        """

        json_file_path = os.path.join(
            self.file_path_test_json, 'germany-only1.json')
        self.o_osm_maps.process_input(json_file_path, True)

        result = self.o_osm_maps.country_name
        self.assertEqual(result, 'germany-only1')

    def test_calc_border_countries(self):
        """
        Test initialized border countries
        - of malta
        - of germany
        - of a file with 1 tile
        - of a file with 2 tiles
        """

        # malta
        self.process_and_check_border_countries('malta', True, {'malta': {}})

        # germany
        expected_result = {'czech_republic': {}, 'germany': {}, 'austria': {}, 'liechtenstein': {},
                           'switzerland': {}, 'italy': {}, 'netherlands': {}, 'belgium': {},
                           'luxembourg': {}, 'france': {}, 'poland': {}, 'denmark': {}}
        self.process_and_check_border_countries(
            'germany', True, expected_result)

        # one tile - france and germany
        input_file = os.path.join(
            self.file_path_test_json, 'germany-france-only1.json')
        expected_result = {'france': {}, 'germany': {}}
        self.process_and_check_border_countries(
            input_file, True, expected_result)

        # two tiles - germany
        input_file = os.path.join(
            self.file_path_test_json, 'germany-only2.json')
        expected_result = {'germany': {}}
        self.process_and_check_border_countries(
            input_file, True, expected_result)

    def test_calc_without_border_countries(self):
        """
        Test initialized countries without border countries
        - of germany
        - of china
        - of one tile
        """

        # germany
        self.process_and_check_border_countries(
            'germany', False, {'germany': {}})

        # china
        self.process_and_check_border_countries('china', False, {'china': {}})

        # one tile - france and germany
        input_file = os.path.join(
            self.file_path_test_json, 'germany-france-only1.json')
        expected_result = {'france': {}, 'germany': {}}
        self.process_and_check_border_countries(
            input_file, False, expected_result)

        # two tiles - germany
        input_file = os.path.join(
            self.file_path_test_json, 'germany-only2.json')
        expected_result = {'germany': {}}
        self.process_and_check_border_countries(
            input_file, False, expected_result)

    def process_and_check_border_countries(self, country, calc_border_countries, expected_result):
        """
        helper method to check a country without border countries
        """

        self.o_osm_maps.process_input(country, calc_border_countries)
        result = self.o_osm_maps.border_countries

        self.assertEqual(result, expected_result)


class TestStaticJsons(unittest.TestCase):
    """
    tests for static .json files
    """

    def test_tiles_via_static_json(self):
        """
        Test the retrieval of tiles via geofabrik URL against hardcoded data for germany
        """
        expected_tiles = [{'x': 138, 'y': 100, 'left': 14.0625, 'top': 36.597889,
                           'right': 15.46875, 'bottom': 35.46067, 'countries': ['malta']}]
        self.calculate_tiles_via_static_json('malta', expected_tiles)

    def calculate_tiles_via_static_json(self, country, expected_result):
        """
        use static json files in the repo to calculate relevant tiles
        """

        json_file_path = const_fct.get_path_to_static_tile_json(country)
        tiles = fd_fct.read_json_file(json_file_path)

        self.assertEqual(tiles, expected_result)

    def test_path_of_tile_via_static_json_china(self):
        """
        test function to find .json file for china against static path
        """

        country = 'china'
        exp_path = os.path.join('asia', country)

        self.calculate_path_to_static_tile_json(country, exp_path)

    def test_path_of_tile_via_static_json_malta(self):
        """
        test function to find .json file for malta against static path
        """

        country = 'malta'
        exp_path = os.path.join('europe', country)

        self.calculate_path_to_static_tile_json(country, exp_path)

    def test_path_of_tile_via_static_json_mexico(self):
        """
        test function to find .json file for mexico against static path
        """

        country = 'mexico'
        exp_path = os.path.join('north_america', country)

        self.calculate_path_to_static_tile_json(country, exp_path)

    def test_path_of_tile_via_static_json_bahamas(self):
        """
        test function to find .json file for bahamas against static path
        """

        country = 'bahamas'
        exp_path = os.path.join('north_america', country)

        self.calculate_path_to_static_tile_json(country, exp_path)

    def test_path_of_tile_via_static_json_chile(self):
        """
        test function to find .json file for chile against static path
        """

        country = 'chile'
        exp_path = os.path.join('south_america', country)

        self.calculate_path_to_static_tile_json(country, exp_path)

    def calculate_path_to_static_tile_json(self, country, exp_path):
        """
        evaluated the .json file with get_path_to_static_tile_json function
        - check against the static file path
        - check if the file exists
        """
        json_file_path = const_fct.get_path_to_static_tile_json(country)

        expected_path = os.path.join(fd_fct.COMMON_DIR, 'json',
                                     exp_path + '.json')

        self.assertEqual(json_file_path, expected_path)
        self.assertTrue(os.path.isfile(json_file_path))

    def test_go_through_folders(self):
        """
        go through all files in the common_resources/json directory
        - check if correct .json will be evaluated through get_path_to_static_tile_json function
        """
        for folder in fd_fct.get_folders_in_folder(os.path.join(fd_fct.COMMON_DIR, 'json')):
            for file in fd_fct.get_files_in_folder(os.path.join(fd_fct.COMMON_DIR, 'json', folder)):
                country = os.path.splitext(file)[0]

                self.calculate_path_to_static_tile_json(
                    country, os.path.join(folder, country))

    def test_go_through_constants(self):
        """
        go through the constant for the GUI / country .json to region assignment
        - check if correct .json will be evaluated through get_path_to_static_tile_json function
        """
        for country in constants.africa:
            self.calculate_path_to_static_tile_json(
                country, os.path.join("africa", country))

        for country in constants.antarctica:
            self.calculate_path_to_static_tile_json(
                country, os.path.join("antarctica", country))

        for country in constants.asia:
            self.calculate_path_to_static_tile_json(
                country, os.path.join("asia", country))

        for country in constants.europe:
            self.calculate_path_to_static_tile_json(
                country, os.path.join("europe", country))

        for country in constants.northamerica:
            self.calculate_path_to_static_tile_json(
                country, os.path.join('north_america', country))

        for country in constants.oceania:
            self.calculate_path_to_static_tile_json(
                country, os.path.join("oceania", country))

        for country in constants.southamerica:
            self.calculate_path_to_static_tile_json(
                country, os.path.join("south_america", country))

        for country in constants.unitedstates:
            self.calculate_path_to_static_tile_json(
                country, os.path.join("united_states", country))



if __name__ == '__main__':
    unittest.main()
