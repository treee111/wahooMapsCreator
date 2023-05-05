"""
tests for the constants geofabrik & geofabrik file
"""
import os
import unittest

import geojson  # pylint: disable=import-error

# import custom python packages
from wahoomc.downloader import Downloader
from wahoomc import constants
from wahoomc.geofabrik_json import GeofabrikJson
from wahoomc.geofabrik_json import CountyIsNoGeofabrikCountry


class TestConstantsGeofabrik(unittest.TestCase):
    """
    tests for constants in geofabrik context
    """

    def setUp(self):
        if not os.path.isfile(constants.GEOFABRIK_PATH):
            o_downloader = Downloader(24, False)
            o_downloader.download_geofabrik_file()

        self.o_geofabrik_json = GeofabrikJson()

        self.relevant_countries = []

        # calc relevant countries in constructor. these should be valid for the whole class
        with open(constants.GEOFABRIK_PATH, encoding='utf8') as file_handle:
            raw_json = geojson.load(file_handle)
        file_handle.close()

        for entry in raw_json.features:
            id_no = entry.properties['id']
            self.relevant_countries.append(id_no)

    def test_if_json_countries_exist_in_geofabrik(self):
        """
        go through all files in the wahoo_mc/resources/json directory
        - check if each country does also exist in geofabrik
        - some countries are skipped because they do not exist in geofabrik
        """
        for country in self.relevant_countries:
            child = self.o_geofabrik_json.translate_id_no_to_geofabrik(country)

            self.assertIn(child, {country.replace(
                '_', '-'), 'us/'+country.replace('_', '-')})

    def test_regions_of_geofabrik(self):
        """
        go through all files in the wahoo_mc/resources/json directory
        - check if each country does also exist in geofabrik
        - some countries are skipped because they do not exist in geofabrik
        """

        id_with_no_parent_geofabrik = []
        regions_geofabrik = []

        geofabrik_regions = ['africa', 'antarctica', 'asia', 'australia-oceania',
                             'central-america', 'europe', 'north-america', 'south-america', 'russia']

        # check against (new) raw representation of geofabrik json
        for feature in self.o_geofabrik_json.raw_json.features:
            try:
                feature.properties['parent']
            except KeyError:
                id_with_no_parent_geofabrik.append(feature.properties['id'])

        self.assertCountEqual(geofabrik_regions,
                              id_with_no_parent_geofabrik)

        # also check against (new) created dict
        for region in self.o_geofabrik_json.geofabrik_region_overview:
            regions_geofabrik.append(region)
        self.assertCountEqual(geofabrik_regions,
                              regions_geofabrik)

    def test_reading_geofabrik_parent(self):
        """
        go through all files in the wahoo_mc/resources/json directory
        - compare the built URL via existing coding with the url out of the geofabrik json file
        - some countries are skipped because they do not exist in geofabrik
        - in addition
            - skip countries if there is a geofabrik URL (because this URL is different to the built one)
            - skip countries which do not have a direct geofabrik json entry, mostly they are in another country/region
        """
        parent, child = self.o_geofabrik_json.get_geofabrik_parent_country(
            'germany')
        self.assertTrue(parent == 'europe' and child == 'germany')

        parent, child = self.o_geofabrik_json.get_geofabrik_parent_country(
            'baden-wuerttemberg')
        self.assertTrue(parent == 'germany' and child == 'baden-wuerttemberg')

        parent, child = self.o_geofabrik_json.get_geofabrik_parent_country(
            'malta')
        self.assertTrue(parent == 'europe' and child == 'malta')

        parent, child = self.o_geofabrik_json.get_geofabrik_parent_country(
            'asia')
        self.assertTrue(parent == '' and child == 'asia')

        with self.assertRaises(CountyIsNoGeofabrikCountry):
            parent, child = self.o_geofabrik_json.get_geofabrik_parent_country(
                'xy')

    def test_if_input_is_geofabrik_id(self):
        """
        check if the input is a id of the geofabrik file
        """
        self.assertTrue(
            self.o_geofabrik_json.is_input_a_geofabrik_id_no('germany'))

        self.assertTrue(
            self.o_geofabrik_json.is_input_a_geofabrik_id_no('baden-wuerttemberg'))

        self.assertTrue(
            self.o_geofabrik_json.is_input_a_geofabrik_id_no('asia'))
        self.assertFalse(
            self.o_geofabrik_json.is_input_a_geofabrik_id_no('xy'))

        self.assertFalse(self.o_geofabrik_json.is_input_a_geofabrik_id_no('*'))

    def test_tranlation_id_to_geofabrik_id(self):
        """
        get geofabrik id by country .json filename
        """
        transl_country = self.o_geofabrik_json.translate_id_no_to_geofabrik(
            'malta')
        self.assertEqual('malta', transl_country)

        transl_country = self.o_geofabrik_json.translate_id_no_to_geofabrik(
            'solomon_islands')
        self.assertEqual('solomon-islands', transl_country)

        transl_country = self.o_geofabrik_json.translate_id_no_to_geofabrik(
            'nebraska')
        self.assertEqual('us/nebraska', transl_country)


if __name__ == '__main__':
    unittest.main()
