"""
tests for the constants geofabrik & geofabrik file
"""
import os
import unittest

# import custom python packages
from wahoomc import file_directory_functions as fd_fct
from wahoomc.downloader import Downloader
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
