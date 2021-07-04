"""
tests for the downloader file
"""
import os
import sys
import unittest

# import custom python packages
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common_resources.osm_maps_functions import OsmMaps


class TestOsmMaps(unittest.TestCase):
    """
    tests for the OSM maps file
    """

    def setUp(self):
        self.o_osm_maps = OsmMaps(False, 1, 1)

    def test_input_country_malta(self):
        """
        Test "malta" as input to the wahooMapsCreator
        """

        self.o_osm_maps.process_input('malta')

        result = self.o_osm_maps.country_name
        self.assertEqual(result, 'malta')

    def test_input_json_file(self):
        """
        Test a json file as input to the wahooMapsCreator
        """

        self.o_osm_maps.process_input('/Users/benjamin/VSCode/wahooMapsCreator/common_resources/germany-only1.json')

        result = self.o_osm_maps.country_name
        self.assertEqual(result, 'germany-only1')

    def test_empty_border_countries_malta(self):
        """
        Test initialized border countries of malta
        """

        self.o_osm_maps.process_input('malta')

        result = self.o_osm_maps.border_countries
        self.assertEqual(result, {'malta': {}})

    def test_empty_border_countries_germany(self):
        """
        Test initialized border countries of germany
        """

        self.o_osm_maps.process_input('germany')

        result = self.o_osm_maps.border_countries
        self.assertEqual(result, {'czech_republic': {}, 'germany': {}, 'austria': {}, 'liechtenstein': {}, 'switzerland': {}, 'italy': {}, 'netherlands': {}, 'belgium': {}, 'luxembourg': {}, 'france': {}, 'poland': {}, 'denmark': {}})
if __name__ == '__main__':
    unittest.main()
