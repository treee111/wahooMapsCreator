"""
tests for the downloader file
"""
import unittest
from mock import patch


from wahoomc.constants_functions import translate_country_input_to_geofabrik
from wahoomc.constants_functions import translate_tags_to_keep


class TestTranslateCountries(unittest.TestCase):
    """
    tests for translating country-constants between geofabrik and other formats
    """

    def test_translated_countries_to_china(self):
        """
        Test countries which have no own geofabrik country but are included in china
        """

        expected = 'china'

        transl_c = translate_country_input_to_geofabrik('hong_kong')
        self.assertEqual(expected, transl_c)

        transl_c = translate_country_input_to_geofabrik('macao')
        self.assertEqual(expected, transl_c)

        transl_c = translate_country_input_to_geofabrik('paracel_islands')
        self.assertEqual(expected, transl_c)

    def test_translated_countries_no_mapping(self):
        """
        Test countries which have no own geofabrik country but are included in china
        """

        expected = 'germany'

        transl_c = translate_country_input_to_geofabrik('germany')
        self.assertEqual(expected, transl_c)


tags_universal_simple = {
    'access': '',
    'area': 'yes'
}

tags_universal_adv = {
    'access': '',
    'area': 'yes',
    'bicycle': '',
    'bridge': '',
    'foot': ['ft_yes', 'foot_designated']
}

tags_universal_full = {
    'access': '',
    'area': 'yes',
    'bicycle': '',
    'bridge': '',
    'foot': ['ft_yes', 'foot_designated'],
    'highway': ['abandoned', 'bus_guideway', 'disused', 'bridleway', 'byway', 'construction', 'cycleway', 'footway', 'living_street', 'motorway', 'motorway_link', 'path', 'pedestrian', 'primary', 'primary_link', 'residential', 'road', 'secondary', 'secondary_link', 'service', 'steps', 'tertiary', 'tertiary_link', 'track', 'trunk', 'trunk_link', 'unclassified'],
    'natural': ['coastline', 'nosea', 'sea', 'beach', 'land', 'scrub', 'water', 'wetland', 'wood'],
    'leisure': ['park', 'nature_reserve'],
    'railway': ['abandoned', 'bus_guideway', 'disused', 'funicular', 'light_rail', 'miniature', 'narrow_gauge', 'preserved', 'rail', 'subway', 'tram'],
    'surface': '',
    'tracktype': '',
    'tunnel': '',
    'waterway': ['canal', 'drain', 'river', 'riverbank'],
    'wood': 'deciduous'
}

name_tags_universal_full = {
    'admin_level': '2',
    'area': 'yes',
    'mountain_pass': '',
    'natural': '',
    'place': ['city', 'hamlet', 'island', 'isolated_dwelling', 'islet', 'locality', 'suburb', 'town', 'village', 'country']
}


class TestTranslateTags(unittest.TestCase):
    """
    tests for translating tags-constants between the universal format and OS-specific formats
    """

    @patch('wahoomc.constants.TAGS_TO_KEEP_UNIVERSAL', tags_universal_simple)
    def test_translate_tags_to_keep_simple_macos(self):
        """
        Test translating tags to keep from universal format to macOS
        """
        tags = ['access', 'area=yes']

        transl_tags = translate_tags_to_keep()
        self.assertEqual(tags, transl_tags)

    @patch('wahoomc.constants.TAGS_TO_KEEP_UNIVERSAL', tags_universal_simple)
    def test_translate_tags_to_keep_simple_win(self):
        """
        Test translating tags to keep from universal format to Windows
        """
        tags_win = 'access= area=yes'

        transl_tags = translate_tags_to_keep(sys_platform='Windows')
        self.assertEqual(tags_win, transl_tags)

    @patch('wahoomc.constants.TAGS_TO_KEEP_UNIVERSAL', tags_universal_adv)
    def test_translate_tags_to_keep_adv_macos(self):
        """
        Test translating tags to keep from universal format to macOS
        """
        tags = ['access', 'area=yes', 'bicycle',
                'bridge', 'foot=ft_yes, foot_designated']

        transl_tags = translate_tags_to_keep()
        self.assertEqual(tags, transl_tags)

    @patch('wahoomc.constants.TAGS_TO_KEEP_UNIVERSAL', tags_universal_adv)
    def test_translate_tags_to_keep_adv_win(self):
        """
        Test translating tags to keep from universal format to Windows
        """
        tags_win = 'access= area=yes bicycle= bridge= foot=ft_yes =foot_designated'

        transl_tags = translate_tags_to_keep(sys_platform='Windows')
        self.assertEqual(tags_win, transl_tags)

    # @patch('wahoomc.constants.TAGS_TO_KEEP_UNIVERSAL', tags_universal_full)
    def test_translate_tags_to_keep_full_macos(self):
        """
        Test translating tags to keep from universal format to macOS // all "tags to keep"
        """
        tags = ['access', 'area=yes', 'bicycle', 'bridge', 'foot=ft_yes, foot_designated',
                'amenity=fuel, cafe, drinking_water', 'shop=bakery',
                'highway=abandoned, bus_guideway, disused, bridleway, byway, construction, cycleway, footway, living_street, motorway, motorway_link, path, pedestrian, primary, primary_link, residential, road, secondary, secondary_link, service, steps, tertiary, tertiary_link, track, trunk, trunk_link, unclassified',
                'natural=coastline, nosea, sea, beach, land, scrub, water, wetland, wood',
                'landuse=forest',
                'leisure=park, nature_reserve', 'railway=abandoned, bus_guideway, disused, funicular, light_rail, miniature, narrow_gauge, preserved, rail, subway, tram',
                'surface', 'tracktype', 'tunnel', 'waterway=canal, drain, river, riverbank', 'wood=deciduous']

        transl_tags = translate_tags_to_keep()
        self.assertEqual(tags, transl_tags)

    # @patch('wahoomc.constants.TAGS_TO_KEEP_UNIVERSAL', tags_universal_full)
    def test_translate_tags_to_keep_full_win(self):
        """
        Test translating tags to keep from universal format to Windows // all "tags to keep"
        """
        tags_win = 'access= area=yes bicycle= bridge= foot=ft_yes =foot_designated amenity=fuel =cafe =drinking_water shop=bakery highway=abandoned =bus_guideway =disused =bridleway =byway =construction =cycleway =footway =living_street =motorway =motorway_link =path =pedestrian =primary =primary_link =residential =road =secondary =secondary_link =service =steps =tertiary =tertiary_link =track =trunk =trunk_link =unclassified natural=coastline =nosea =sea =beach =land =scrub =water =wetland =wood landuse=forest leisure=park =nature_reserve railway=abandoned =bus_guideway =disused =funicular =light_rail =miniature =narrow_gauge =preserved =rail =subway =tram surface= tracktype= tunnel= waterway=canal =drain =river =riverbank wood=deciduous'

        transl_tags = translate_tags_to_keep(sys_platform='Windows')
        self.assertEqual(tags_win, transl_tags)

    # @patch('wahoomc.constants.NAME_TAGS_TO_KEEP_UNIVERSAL', name_tags_universal_full)
    def test_translate_name_tags_to_keep_full_macos(self):
        """
        Test translating name tags to keep from universal format to Windows // all "name tags to keep"
        """
        names_tags = ['admin_level=2', 'area=yes', 'mountain_pass', 'natural',
                      'place=city, hamlet, island, isolated_dwelling, islet, locality, suburb, town, village, country']

        transl_tags = translate_tags_to_keep(name_tags=True)
        self.assertEqual(names_tags, transl_tags)

    # @patch('wahoomc.constants.NAME_TAGS_TO_KEEP_UNIVERSAL', name_tags_universal_full)
    def test_translate_name_tags_to_keep_full_win(self):
        """
        Test translating name tags to keep from universal format to macOS // all "name tags to keep"
        """

        names_tags_win = 'admin_level=2 area=yes mountain_pass= natural= place=city =hamlet =island =isolated_dwelling =islet =locality =suburb =town =village =country'

        transl_tags = translate_tags_to_keep(
            name_tags=True, sys_platform='Windows')
        self.assertEqual(names_tags_win, transl_tags)


if __name__ == '__main__':
    unittest.main()
