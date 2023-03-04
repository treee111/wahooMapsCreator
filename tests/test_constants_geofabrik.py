"""
tests for the constants geofabrik & geofabrik file
"""
import os
import unittest

# import custom python packages
from wahoomc import file_directory_functions as fd_fct
from wahoomc.downloader import Downloader
from wahoomc import constants
from wahoomc.geofabrik_json import GeofabrikJson
from wahoomc.geofabrik_json import CountyIsNoGeofabrikCountry

# json countries with no geofabrik id partner
json_file_countries_without_geofabrik_id = ['clipperton_island', 'saint_pierre_and_miquelon', 'trinidad_and_tobago',
                                            'curacao', 'bonaire_saint_eustatius_and_saba', 'falkland_islands', 'french_guiana',
                                            'aruba', 'united_states_minor_outlying_islands', 'french_polynesia',
                                            'norfolk_island', 'wallis_and_futuna', 'northern_mariana_islands', 'paracel_islands', 'united_arab_emirates', 'kuwait', 'qatar', 'spratly_islands', 'singapore', 'brunei', 'bahrain', 'macao', 'cocos_islands', 'christmas_island', 'palestina', 'malaysia', 'saudi_arabia', 'british_indian_ocean_territory', 'israel', 'oman', 'hong_kong', 'south_georgia_and_the_south_sandwich_islands', 'bouvet_island', 'heard_island_and_mcdonald_islands', 'guam', 'commonwealth_of_the_northern_mariana_islands',
                                            'american_samoa', 'united_states_virgin_islands', 'svalbard_and_jan_mayen', 'united_kingdom', 'åland', 'gibraltar', 'san_marino', 'vatican_city', 'ireland', 'bosnia_and_herzegovina', 'jersey', 'guernsey', 'montserrat', 'bermuda', 'virgin_islands_u.s.', 'dominica', 'saint-barthélemy', 'barbados', 'grenada', 'saint_vincent_and_the_grenadines', 'anguilla', 'saint-martin', 'cayman_islands', 'sint_maarten', 'haiti', 'saint_lucia', 'british_virgin_islands', 'saint_kitts_and_nevis', 'dominican_republic', 'turks_and_caicos_islands', 'antigua_and_barbuda', 'gambia', 'saint_helena', 'cote_d_ivoire', 'western_sahara', 'comoros', 'republic_of_congo', 'democratic_republic_of_the_congo', 'senegal', 'french_southern_territories']


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
        for folder in fd_fct.get_folders_in_folder(os.path.join(constants.RESOURCES_DIR, 'json')):
            for file in fd_fct.get_files_in_folder(os.path.join(constants.RESOURCES_DIR, 'json', folder)):
                country = os.path.splitext(file)[0]
                if country not in json_file_countries_without_geofabrik_id:
                    self.relevant_countries.append(country)

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
