"""
tests for the downloader file
"""
import unittest


from common_python.constants_functions import translate_country_input_to_geofabrik


class TestConstants(unittest.TestCase):
    """
    tests for constants and constants functions files
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


if __name__ == '__main__':
    unittest.main()
