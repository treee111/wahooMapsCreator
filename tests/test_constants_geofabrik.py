"""
tests for the constants geofabrik & geofabrik file
"""
import os
import unittest

# import custom python packages
from wahoomc import file_directory_functions as fd_fct
from wahoomc.downloader import Downloader
from wahoomc.downloader import get_osm_pbf_filepath_url
from wahoomc import constants
from wahoomc.constants_functions import GeofabrikJson
from wahoomc.constants_functions import get_geofabrik_region_of_country, CountyIsNoGeofabrikCountry

# json countries with no geofabrik id partner
json_file_countries_without_geofabrik_id = ['clipperton_island', 'saint_pierre_and_miquelon', 'trinidad_and_tobago',
                                            'curacao', 'bonaire_saint_eustatius_and_saba', 'falkland_islands', 'french_guiana',
                                            'aruba', 'united_states_minor_outlying_islands', 'french_polynesia',
                                            'norfolk_island', 'wallis_and_futuna', 'northern_mariana_islands', 'paracel_islands', 'united_arab_emirates', 'kuwait', 'qatar', 'spratly_islands', 'singapore', 'brunei', 'bahrain', 'macao', 'cocos_islands', 'christmas_island', 'palestina', 'malaysia', 'saudi_arabia', 'british_indian_ocean_territory', 'israel', 'oman', 'hong_kong', 'south_georgia_and_the_south_sandwich_islands', 'bouvet_island', 'heard_island_and_mcdonald_islands', 'guam', 'commonwealth_of_the_northern_mariana_islands',
                                            'american_samoa', 'united_states_virgin_islands', 'svalbard_and_jan_mayen', 'united_kingdom', 'åland', 'gibraltar', 'san_marino', 'vatican_city', 'ireland', 'bosnia_and_herzegovina', 'jersey', 'guernsey', 'montserrat', 'bermuda', 'virgin_islands_u.s.', 'dominica', 'saint-barthélemy', 'barbados', 'grenada', 'saint_vincent_and_the_grenadines', 'anguilla', 'saint-martin', 'cayman_islands', 'sint_maarten', 'haiti', 'saint_lucia', 'british_virgin_islands', 'saint_kitts_and_nevis', 'dominican_republic', 'turks_and_caicos_islands', 'antigua_and_barbuda', 'gambia', 'saint_helena', 'cote_d_ivoire', 'western_sahara', 'comoros', 'republic_of_congo', 'democratic_republic_of_the_congo', 'senegal', 'french_southern_territories']

# json countries with no geofabrik region defined in constants.py
no_geofabrik_region_assigned = ['guyana', 'solomon_islands', 'marshall_islands', 'pitcairn_islands', 'cook_islands', 'new_caledonia',
                                'new_zealand', 'alaska', 'oklahoma', 'puerto_rico', 'oregon', 'panama',
                                'martinique', 'costa_rica', 'guadeloupe', 'el_salvador', 'mayotte',
                                'sierra_leone', 'central_african_republic', 'sao_tome_and_principe',
                                'equatorial_guinea', 'reunion']


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
            child = self.get_geofabrik_id_by_json_file_country(country)

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

        # check against (new) raw representation of geofabrik json
        for feature in self.o_geofabrik_json.raw_json.features:
            try:
                feature.properties['parent']
            except KeyError:
                id_with_no_parent_geofabrik.append(feature.properties['id'])

        geofabrik_regions_w_russia = constants.geofabrik_regions
        geofabrik_regions_w_russia.append(
            'russia')

        self.assertCountEqual(geofabrik_regions_w_russia,
                              id_with_no_parent_geofabrik)

        # also check against (new) created dict
        for region in self.o_geofabrik_json.geofabrik_region_overview:
            regions_geofabrik.append(region)
        self.assertCountEqual(geofabrik_regions_w_russia,
                              regions_geofabrik)

    def test_geofabrik_region_against_get_region(self):
        """
        go through all files in the wahoo_mc/resources/json directory
        - compare the region from get_geofabrik_region_of_country against the geofabrik json file
        - some countries are skipped because
            - there is no get_geofabrik_region_of_country region
            - get_geofabrik_region_of_country returns false region
        """
        for country in self.relevant_countries:
            get_region = ''
            parent = ''

            try:
                get_region = get_geofabrik_region_of_country(country)
            except SystemExit:
                # if there is no get_region, everything else is better ;-)
                self.assertIn(country, no_geofabrik_region_assigned)
                continue

            id_no = self.get_geofabrik_id_by_json_file_country(country)
            parent, child = self.o_geofabrik_json.get_geofabrik_parent_country(
                id_no)

            # these are own continents without region/parent.
            if country in ['antarctica', 'russia']:
                self.assertEqual(parent, '')
            # these get false routed via get_region. compare against correct parent
            elif country == 'papua_new_guinea':
                self.assertEqual(parent, 'australia-oceania')
            elif country == 'georgia':
                self.assertEqual(parent, 'europe')
            else:
                # "normal" check
                # one geofabrik region in constsants.py has north-america/us
                self.assertTrue(
                    get_region in [parent, parent + '/us'], 'country: '+country)

    def test_gofabrik_url_against_built_url(self):
        """
        go through all files in the wahoo_mc/resources/json directory
        - compare the built URL via existing coding with the url out of the geofabrik json file
        - some countries are skipped because they do not exist in geofabrik
        - in addition
            - skip countries if there is a geofabrik URL (because this URL is different to the built one)
            - skip countries which do not have a direct geofabrik json entry, mostly they are in another country/region
        """
        for country in self.relevant_countries:
            built_url = None
            geofabrik_url = None

            # build URL with existing coding
            try:
                map_file_path, built_url = get_osm_pbf_filepath_url(country)
            except SystemExit:
                pass

            # grab URL from geofabrik json
            geofabrik_url = self.o_geofabrik_json.get_geofabrik_url(country)

            if not geofabrik_url:
                # check with replaced _ by -
                geofabrik_url = self.o_geofabrik_json.get_geofabrik_url(
                    country.replace('_', '-'))
                if not geofabrik_url:
                    # check with replaced _ by - AND prefix us/
                    geofabrik_url = self.o_geofabrik_json.get_geofabrik_url(
                        'us/'+country.replace('_', '-'))

            skip_countries_built_url_is_false = [
                'papua_new_guinea', 'east_timor',
                'antarctica',  # built url is false
                'georgia'  # will issue north-america/us but europe is right. Reason: order in get_geofabrik_region_of_country
            ]

            # skip_countries_for_url_comparison = [
            #     'united_arab_emirates', 'kuwait', 'qatar', 'bahrain', 'saudi_arabia', 'oman',  # gcc-states
            #     'malaysia', 'singapore', 'brunei',  # malaysia-singapore-brunei
            #     'christmas_island',  # indonesia
            #     'paracel_islands', 'spratly_islands', 'british_indian_ocean_territory',  # asia
            #     'macao', 'hong_kong',  # china
            #     'palestina', 'israel',  # israel-and-palestine
            #     'northern_mariana_islands', 'cocos_islands', 'commonwealth_of_the_northern_mariana_islands', 'american_samoa',  # australia
            #     'antarctica',  # built url is false
            #     'georgia',  # will issue north-america/us but europe is right because of the order in get_geofabrik_region_of_country
            #     'united_kingdom', 'åland', 'gibraltar', 'san_marino', 'san_marino', 'vatican_city', 'ireland',  # europe
            #     'bosnia_and_herzegovina', 'jersey', 'guernsey', 'svalbard_and_jan_mayen',  # europe
            #     'saint_helena', 'cote_d_ivoire', 'western_sahara', 'democratic_republic_of_the_congo']  # africa

            if built_url != geofabrik_url:
                # # either it is a country to skip
                # if (country in skip_countries_for_url_comparison_if_geofabrik_url and geofabrik_url) \
                #         or country in skip_countries_for_url_comparison:
                #     continue

                # or there is no built url but a geofabrik one - ok!
                # for some countries the built url is false
                if built_url is None or \
                        country in skip_countries_built_url_is_false:
                    self.assertTrue(geofabrik_url, msg='country: '+country)
                    continue

            # "normal" compare, also if both are empty/ None
            self.assertEqual(built_url, geofabrik_url,
                             msg='country: '+country)

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

    def get_geofabrik_id_by_json_file_country(self, country):
        """
        get geofabrik id by country .json filename
        """
        # get geofabrik id by country .json filename
        # 1. raw
        # parent, child = self.o_geofabrik_json.find_geofbrik_parent(
        #     country)
        # if not child:

        # get geofabrik id by country .json filename
        # 1. '_' replaced by '-'
        child = self.o_geofabrik_json.get_geofabrik_parent_country(
            country.replace('_', '-'))[1]
        if child:
            return child

        # 2. 'us/' prefix and '_' replaced by '-'
        child = self.o_geofabrik_json.get_geofabrik_parent_country(
            'us/'+country.replace('_', '-'))[1]

        if child:
            return child

        return None


if __name__ == '__main__':
    unittest.main()
