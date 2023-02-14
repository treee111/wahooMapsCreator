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
from wahoomc.constants_functions import translate_country_input_to_geofabrik

skip_countries_for_geofabrik = [
    'clipperton_island', 'saint_pierre_and_miquelon', 'trinidad_and_tobago',
    'curacao', 'bonaire_saint_eustatius_and_saba', 'falkland_islands', 'french_guiana',
    'aruba', 'united_states_minor_outlying_islands', 'french_polynesia',
    'norfolk_island', 'wallis_and_futuna',
    'south_georgia_and_the_south_sandwich_islands', 'bouvet_island', 'heard_island_and_mcdonald_islands',
    'guam', 'montserrat', 'bermuda', 'dominica', 'saint-barthélemy', 'barbados', 'grenada', 'saint_vincent_and_the_grenadines',
            'cayman_islands', 'haiti', 'saint_lucia', 'saint_kitts_and_nevis', 'dominican_republic',
            'turks_and_caicos_islands', 'antigua_and_barbuda', 'comoros', 'french_southern_territories']


class TestConstantsGeofabrik(unittest.TestCase):
    """
    tests for constants in geofabrik context
    """

    def setUp(self):
        if not os.path.isfile(constants.GEOFABRIK_PATH):
            o_downloader = Downloader(24, False)
            o_downloader.download_geofabrik_file()

        self.o_geofabrik_json = GeofabrikJson()

    def test_if_json_countries_exist_in_geofabrik(self):
        """
        go through all files in the wahoo_mc/resources/json directory
        - check if each country does also exist in geofabrik
        - some countries are skipped because they do not exist in geofabrik
        """
        for folder in fd_fct.get_folders_in_folder(os.path.join(constants.RESOURCES_DIR, 'json')):
            for file in fd_fct.get_files_in_folder(os.path.join(constants.RESOURCES_DIR, 'json', folder)):
                country = os.path.splitext(file)[0]
                if country in skip_countries_for_geofabrik:
                    continue

                parent, child = self.o_geofabrik_json.find_geofbrik_parent(
                    country)
                if not child:
                    parent, child = self.o_geofabrik_json.find_geofbrik_parent(
                        translate_country_input_to_geofabrik(country))

                    if not child:
                        country = country.replace('_', '-')
                        parent, child = self.o_geofabrik_json.find_geofbrik_parent(
                            country)

                        if not child:
                            parent, child = self.o_geofabrik_json.find_geofbrik_parent(
                                'us/'+country)

                            if not child:
                                self.assertEqual(country, child)

                else:
                    self.assertEqual(country, child)

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


if __name__ == '__main__':
    unittest.main()
