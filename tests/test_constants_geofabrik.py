"""
tests for the constants geofabrik & geofabrik file
"""
import multiprocessing
import os
import unittest
import csv

# import custom python packages
from wahoomc import file_directory_functions as fd_fct
from wahoomc.downloader import Downloader
from wahoomc import constants
from wahoomc.geofabrik import XYGeofabrik
from wahoomc.geofabrik_json import GeofabrikJson
from wahoomc.geofabrik_json import CountyIsNoGeofabrikCountry
from wahoomc.osm_maps_functions import TileNotFoundError
from wahoomc.osm_maps_functions import get_tile_by_one_xy_combination_from_jsons

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

    # def test_number_of_tiles_geofabric_vs_static(self):
    #     llist = []
    #     counter = 0
    #     for entry in self.relevant_countries:
    #         parent = self.o_geofabrik_json.get_geofabrik_parent_country(entry)[
    #             0]
    #         if parent != 'europe':
    #             continue
    #         if counter >= 50:
    #             break
    #         counter = counter + 1
    #         tiles_via_geofabrik_json = calc_tiles_via_geofabrik_json(
    #             entry)

    #         tiles_via_static_json = calc_tiles_via_static_jsons(
    #             entry)

    #         llist.append({'country': entry, 'static': len(
    #             tiles_via_static_json), 'geof': len(tiles_via_geofabrik_json), '+-%': len(tiles_via_geofabrik_json)/len(
    #             tiles_via_static_json)})

    #     print(llist)

    def test_tile_of_all_geofabric_xy_coordinates(self):
        """
        go throught all xy-combinations: x 0-255 and y 0-255 in PARALLEL
        do stuff mentioned in calc_all_xy_combination_tiles_to_x_value for all xy-combinations
        write result in .csv output file
        """
        result_list = []

        # create a process pool that uses all cpus
        with multiprocessing.Pool() as pool:
            # call the function for each item in parallel
            # from 0 to 255, because max is (with zoom = 8): pow(2, 8) - 1
            for result in pool.map(calc_all_xy_combination_tiles_to_x_value, range(255)):
                result_list.extend(result)
                print(result)

        csv_output_path = os.path.join(constants.USER_WAHOO_MC,
                                       'all_x_y_tiles_calculated_using_geofabrik.csv')

        # write content of list with dicts into .csv file
        with open(csv_output_path, 'w', newline='', encoding='utf-8') as csvfile:
            dict_writer = csv.DictWriter(csvfile, result_list[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(result_list)

    def test_tile_of_one_geofabric_xy_coordinate(self):
        """
        go throught xy-combinations beginning with the given num_y value: x given and y beginning with given
        do stuff mentioned in calc_all_xy_combination_tiles_to_x_value for all xy-combinations
        write result in .csv output file
        """
        num_x = 89
        num_y = 17

        result_list = calc_all_xy_combination_tiles_to_x_value(num_x, num_y)

        csv_output_path = os.path.join(constants.USER_WAHOO_MC,
                                       'x_y_tiles_calculated_using_geofabrik.csv')

        # write content of list with dicts into .csv file
        with open(csv_output_path, 'w', newline='', encoding='utf-8') as csvfile:
            dict_writer = csv.DictWriter(csvfile, result_list[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(result_list)


def calc_all_xy_combination_tiles_to_x_value(num_x, num_y=0):
    """
    go throught all y-combinations: 0-255 of a given x value
    evaluate the geofabric information about the tile,
    compare about static .json information
    remember which statement was used in find_needed_countries
    """
    max_y = pow(2, 8) - 1
    result_list = []
    while num_y <= max_y:
        a_list = {'x': num_x, 'y': num_y}
        one_geofabrik_tile = False
        lat_len_ok = False
        no_countries = False

        o_geofabrik = XYGeofabrik([a_list])
        tiles_via_geofabrik_json, wanted_region_contains, rhape_contains, rhape_intersects = o_geofabrik.get_tiles_of_wanted_map()

        if len(tiles_via_geofabrik_json) == 1:
            one_geofabrik_tile = True

        tile_via_geofabrik_json = tiles_via_geofabrik_json[0]

        if not tile_via_geofabrik_json['countries']:
            no_countries = True

        try:
            tile_via_static_json = get_tile_by_one_xy_combination_from_jsons(
                a_list)
        except TileNotFoundError:
            num_y = num_y + 1
            continue

        if tile_via_geofabrik_json and tile_via_static_json:
            if tile_via_geofabrik_json['x'] == tile_via_static_json['x'] \
                    and tile_via_geofabrik_json['y'] == tile_via_static_json['y'] \
                    and tile_via_geofabrik_json['left'] == tile_via_static_json['left'] \
                    and round(tile_via_geofabrik_json['top'], 6) == tile_via_static_json['top'] \
                    and tile_via_geofabrik_json['right'] == tile_via_static_json['right'] \
                    and round(tile_via_geofabrik_json['bottom'], 6) == tile_via_static_json['bottom']:
                lat_len_ok = True

        result_list.append(
            {'x': num_x, 'y': num_y, 'lat_len_ok': lat_len_ok, 'one': wanted_region_contains, 'two': rhape_contains, 'three': rhape_intersects, 'no_countries': no_countries, 'one_geofabrik_tile': one_geofabrik_tile})

        num_y = num_y + 1

    return result_list


if __name__ == '__main__':
    unittest.main()
