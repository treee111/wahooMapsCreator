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

        for feature in self.o_geofabrik_json.json_data.features:
            try:
                feature.properties['parent']
            except KeyError:
                id_with_no_parent_geofabrik.append(feature.properties['id'])

        geofabrik_regions_w_russia = constants.geofabrik_regions
        geofabrik_regions_w_russia.append(
            'russia')

        self.assertCountEqual(geofabrik_regions_w_russia,
                              id_with_no_parent_geofabrik)

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
            geofabrik_url = self.o_geofabrik_json.find_geofbrik_url(country)

            if not geofabrik_url:
                # check with replaced _ by -
                geofabrik_url = self.o_geofabrik_json.find_geofbrik_url(
                    country.replace('_', '-'))
                if not geofabrik_url:
                    # check with replaced _ by - AND prefix us/
                    geofabrik_url = self.o_geofabrik_json.find_geofbrik_url(
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
        child = self.o_geofabrik_json.find_geofbrik_parent(
            country.replace('_', '-'))[1]
        if child:
            return child

        # 2. 'us/' prefix and '_' replaced by '-'
        child = self.o_geofabrik_json.find_geofbrik_parent(
            'us/'+country.replace('_', '-'))[1]

        if child:
            return child

        return None


if __name__ == '__main__':
    unittest.main()
