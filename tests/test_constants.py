"""
tests for the downloader file
"""
import unittest


from common_python.constants_functions import translate_country_input_to_geofabrik
from common_python.constants_functions import translate_tags_to_keep
import common_python.constants as const


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


class TestTranslateTags(unittest.TestCase):
    """
    tests for translating tags-constants between the universal format and OS-specific formats
    """

    def setUp(self):
        self.tags_universal_simple = {
            'access': '',
            'area': 'yes'
        }

        self.tags_universal_adv = {
            'access': '',
            'area': 'yes',
            'bicycle': '',
            'bridge': '',
            'foot': ['ft_yes', 'foot_designated']
        }

        self.tags_universal_full = {
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

        self.name_tags_universal_full = {
            'admin_level': '2',
            'area': 'yes',
            'mountain_pass': '',
            'natural': '',
            'place': ['city', 'hamlet', 'island', 'isolated_dwelling', 'islet', 'locality', 'suburb', 'town', 'village', 'country']
        }

    def test_translate_tags_to_keep_simple_macos(self):
        """
        Test translating tags to keep from universal format to macOS
        """

        tags = ['access', 'area=yes']

        transl_tags = translate_tags_to_keep(self.tags_universal_simple)
        self.assertEqual(tags, transl_tags)

    def test_translate_tags_to_keep_simple_win(self):
        """
        Test translating tags to keep from universal format to Windows
        """

        tags_win = 'access= area=yes'

        transl_tags = translate_tags_to_keep(
            self.tags_universal_simple, 'Windows')
        self.assertEqual(tags_win, transl_tags)

    def test_translate_tags_to_keep_adv_macos(self):
        """
        Test translating tags to keep from universal format to macOS
        """

        tags = ['access', 'area=yes', 'bicycle',
                'bridge', 'foot=ft_yes, foot_designated']

        transl_tags = translate_tags_to_keep(self.tags_universal_adv)
        self.assertEqual(tags, transl_tags)

    def test_translate_tags_to_keep_adv_win(self):
        """
        Test translating tags to keep from universal format to Windows
        """

        tags_win = 'access= area=yes bicycle= bridge= foot=ft_yes =foot_designated'

        transl_tags = translate_tags_to_keep(
            self.tags_universal_adv, 'Windows')
        self.assertEqual(tags_win, transl_tags)

    def test_translate_tags_to_keep_full_macos(self):
        """
        Test translating tags to keep from universal format to macOS // all "tags to keep"
        """

        tags = ['access', 'area=yes', 'bicycle', 'bridge', 'foot=ft_yes, foot_designated',
                'highway=abandoned, bus_guideway, disused, bridleway, byway, construction, cycleway, footway, living_street, motorway, motorway_link, path, pedestrian, primary, primary_link, residential, road, secondary, secondary_link, service, steps, tertiary, tertiary_link, track, trunk, trunk_link, unclassified',
                'natural=coastline, nosea, sea, beach, land, scrub, water, wetland, wood',
                'leisure=park, nature_reserve', 'railway=abandoned, bus_guideway, disused, funicular, light_rail, miniature, narrow_gauge, preserved, rail, subway, tram',
                'surface', 'tracktype', 'tunnel', 'waterway=canal, drain, river, riverbank', 'wood=deciduous']

        transl_tags = translate_tags_to_keep(self.tags_universal_full)
        self.assertEqual(tags, transl_tags)

        transl_tags = translate_tags_to_keep(
            const.TAGS_TO_KEEP_UNIVERSAL)
        self.assertEqual(tags, transl_tags)

    def test_translate_tags_to_keep_full_win(self):
        """
        Test translating tags to keep from universal format to Windows // all "tags to keep"
        """

        tags_win = 'access= area=yes bicycle= bridge= foot=ft_yes =foot_designated highway=abandoned =bus_guideway =disused =bridleway =byway =construction =cycleway =footway =living_street =motorway =motorway_link =path =pedestrian =primary =primary_link =residential =road =secondary =secondary_link =service =steps =tertiary =tertiary_link =track =trunk =trunk_link =unclassified natural=coastline =nosea =sea =beach =land =scrub =water =wetland =wood leisure=park =nature_reserve railway=abandoned =bus_guideway =disused =funicular =light_rail =miniature =narrow_gauge =preserved =rail =subway =tram surface= tracktype= tunnel= waterway=canal =drain =river =riverbank wood=deciduous'

        transl_tags = translate_tags_to_keep(
            self.tags_universal_full, 'Windows')
        self.assertEqual(tags_win, transl_tags)

        transl_tags = translate_tags_to_keep(
            const.TAGS_TO_KEEP_UNIVERSAL, 'Windows')
        self.assertEqual(tags_win, transl_tags)

    def test_translate_name_tags_to_keep_full_macos(self):
        """
        Test translating name tags to keep from universal format to Windows // all "name tags to keep"
        """

        names_tags = ['admin_level=2', 'area=yes', 'mountain_pass', 'natural',
                      'place=city, hamlet, island, isolated_dwelling, islet, locality, suburb, town, village, country']

        transl_tags = translate_tags_to_keep(
            self.name_tags_universal_full)
        self.assertEqual(names_tags, transl_tags)

        transl_tags = translate_tags_to_keep(
            const.NAME_TAGS_TO_KEEP_UNIVERSAL)
        self.assertEqual(names_tags, transl_tags)

    def test_translate_name_tags_to_keep_full_win(self):
        """
        Test translating name tags to keep from universal format to macOS // all "name tags to keep"
        """

        names_tags_win = 'admin_level=2 area=yes mountain_pass= natural= place=city =hamlet =island =isolated_dwelling =islet =locality =suburb =town =village =country'

        transl_tags = translate_tags_to_keep(
            self.name_tags_universal_full, 'Windows')
        self.assertEqual(names_tags_win, transl_tags)

        transl_tags = translate_tags_to_keep(
            const.NAME_TAGS_TO_KEEP_UNIVERSAL, 'Windows')
        self.assertEqual(names_tags_win, transl_tags)


if __name__ == '__main__':
    unittest.main()
