"""
tests for the osm maps file
"""
import os
# import sys
import unittest

# import custom python packages
from wahoomc.osm_maps_functions import CountryOsmData, XYOsmData
from wahoomc.osm_maps_functions import OsmMaps
# from wahoomc.osm_maps_functions import TileNotFoundError
from wahoomc.input import InputData
from wahoomc import file_directory_functions as fd_fct
from wahoomc import constants


class TestOsmMapsCalculation(unittest.TestCase):
    """
    tests for the OSM maps file
    """

    # def setUp(self):

    def test_calc_border_countries_input_country(self):
        """
        Test initialized border countries
        - of malta
        - of germany
        """

        # malta
        self.process_and_check_border_countries(
            'malta', True, {'italy': {}, 'malta': {}}, 'country')

        # germany
        expected_result = {'czech-republic': {}, 'germany': {}, 'austria': {}, 'liechtenstein': {},
                           'switzerland': {}, 'italy': {}, 'netherlands': {}, 'belgium': {},
                           'luxembourg': {}, 'france': {}, 'poland': {}, 'denmark': {}, 'sweden': {}}
        self.process_and_check_border_countries(
            'germany', True, expected_result, 'country')

        # germany,malta
        expected_result = {'czech-republic': {}, 'germany': {}, 'austria': {}, 'liechtenstein': {},
                           'switzerland': {}, 'italy': {}, 'netherlands': {}, 'belgium': {},
                           'luxembourg': {}, 'france': {}, 'poland': {}, 'denmark': {}, 'sweden': {}, 'malta': {}}
        self.process_and_check_border_countries(
            'germany,malta', True, expected_result, 'country')

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

        # malta,liechtenstein
        self.process_and_check_border_countries(
            'malta,liechtenstein', False, {'malta': {}, 'liechtenstein': {}}, 'country')

        # malta,tunisia
        self.process_and_check_border_countries(
            'malta,tunisia', False, {'malta': {}, 'tunisia': {}}, 'country')

    def test_calc_without_border_countries_xy_coordinates_1tile(self):
        """
        Test initialized countries without border countries
        - of one tile
        """

        # one tile - france and germany
        expected_result = {'france': {}, 'germany': {}}
        self.process_and_check_border_countries(
            "133/88", False, expected_result, 'xy_coordinate')

    def test_calc_without_border_countries_xy_coordinates_2tiles(self):
        """
        Test initialized countries without border countries
        - of two tiles
        """

        # two tiles - germany
        expected_result = {'germany': {}}
        self.process_and_check_border_countries(
            "134/87,134/88", False, expected_result, 'xy_coordinate')

    def process_and_check_border_countries(self, inp_val, calc_border_c, exp_result, inp_mode):
        """
        helper method to process a country or json file and check the calculated border countries
        """

        o_input_data = InputData()
        o_input_data.process_border_countries = calc_border_c

        if inp_mode == 'country':
            o_input_data.country = inp_val
            o_osm_data = CountryOsmData(o_input_data)
        elif inp_mode == 'xy_coordinate':
            o_input_data.xy_coordinates = inp_val
            o_osm_data = XYOsmData(o_input_data)

        o_osm_data.process_input_of_the_tool()

        result = o_osm_data.border_countries

        # delete the path to the file, here, only the correct border countries are checked
        for res in result:
            result[res] = {}

        self.assertEqual(result, exp_result)


class TestOSMMapsInput(unittest.TestCase):
    """
    tests for input of OsmData
    """

    def test_input_country_malta(self):
        """
        Test "malta" as input to the wahooMapsCreator
        check, if the given input-parameter is saved to the OsmMaps instance
        """
        o_osm_data = self.get_osm_data_instance('malta')

        self.assertEqual(o_osm_data.country_name, 'malta')

    def test_folder_name_many_countries(self):
        """
        Test a very long list of countries as input to the wahooMapsCreator
        check, if the list of countries is cutted down to 100 chars and that is saved to the OsmMaps instance
        """
        o_osm_data = self.get_osm_data_instance('albania,alps,andorra,austria,azores,belarus,belgium,bosnia-herzegovina,britain-and-ireland,bulgaria,croatia,cyprus,czech-republic,dach,denmark,estonia,faroe-islands,finland,france,georgia,germany,great-britain,greece,guernsey-jersey,hungary,iceland,ireland-and-northern-ireland,isle-of-man,italy,kosovo,latvia,liechtenstein,lithuania,luxembourg,macedonia,malta,moldova,monaco,montenegro,netherlands,norway,poland,portugal,romania,serbia,slovakia,slovenia,spain,sweden,switzerland,turkey,ukraine')

        o_osm_maps = OsmMaps(o_osm_data)
        folder_name = o_osm_maps.calculate_folder_name('.map.lzma')
        folder_name_maps = o_osm_maps.calculate_folder_name('.map')

        self.assertEqual(folder_name, 'albania_alps_andorra_austria_azores_belarus_belgiu')
        self.assertEqual(folder_name_maps, 'albania_alps_andorra_austria_azores_belarus_belgiu-maps')

    def test_encoding_open_sea_osm(self):
        """
        use static json files in the repo to calculate relevant tile
        """

        with open(os.path.join(constants.RESOURCES_DIR, 'sea.osm')) as sea_file:  # pylint: disable=unspecified-encoding
            sea_data_no_encoding = sea_file.read()
        with open(os.path.join(constants.RESOURCES_DIR, 'sea.osm'), encoding="utf-8") as sea_file:
            sea_data_utf8 = sea_file.read()

        self.assertEqual(sea_data_no_encoding, sea_data_utf8)

    def get_osm_data_instance(self, country_input):
        """
        takes given input creates OsmData instance
        """
        o_input_data = InputData()
        o_input_data.country = country_input

        o_osm_data = CountryOsmData(o_input_data)
        o_osm_data.process_input_of_the_tool()

        return o_osm_data

class TestConfigFile(unittest.TestCase):
    """
    tests for the config .json file in the "wahooMapsCreatorData/_tiles/{country}" directory
    """

    def test_version_and_tags_of_country_config_file(self):
        """
        tests, if the return value of version is OK and if the tags are the same
        """

        o_input_data = InputData()
        o_input_data.country = 'malta'
        # prevent from downloading land_polygons each time
        o_input_data.max_days_old = 1000

        o_osm_data = CountryOsmData(o_input_data)
        o_osm_data.process_input_of_the_tool()

        o_downloader = o_osm_data.get_downloader()

        # download files marked for download to fill up map_file per country to write to config
        o_downloader.download_files_if_needed()

        o_osm_maps = OsmMaps(o_osm_data)

        o_osm_maps.write_country_config_file(o_input_data.country)

        self.assertTrue(
            o_osm_maps.tags_are_identical_to_last_run(o_input_data.country))

        country_config = fd_fct.read_json_file_country_config(os.path.join(
            constants.USER_OUTPUT_DIR, o_input_data.country, ".config.json"))

        self.assertEqual(constants.VERSION, country_config["version_last_run"])


if __name__ == '__main__':
    unittest.main()
