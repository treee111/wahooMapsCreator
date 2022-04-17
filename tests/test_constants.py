"""
tests for the downloader file
"""
import unittest


from common_python.constants_functions import translate_country_input_to_geofabrik
from common_python.constants_functions import translate_tags_to_keep


class TestConstants(unittest.TestCase):
    """
    tests for constants and constants functions files
    """

    def setUp(self):
        self.tags_universal_simple = {
            'access': '',
            'area': 'yes'
        }

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


if __name__ == '__main__':
    unittest.main()
