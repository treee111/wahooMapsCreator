"""
tests for the downloader file
"""
import os
# import sys
import unittest
import time
import shutil
import platform

# import custom python packages
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wahoomc.downloader import older_than_x_days
from wahoomc.downloader import download_file
from wahoomc.downloader import build_osm_pbf_filepath
from wahoomc.downloader import download_tooling
from wahoomc.downloader import Downloader
from wahoomc import constants
from wahoomc.constants_functions import get_tooling_win_path
from wahoomc.geofabrik_json import GeofabrikJson


class TestDownloader(unittest.TestCase):
    """
    tests for the downloader file
    """

    def setUp(self):
        self.max_days_old = 14

        self.o_downloader = Downloader(24, False)

    def test_outdated_timestamp(self):
        """
        Test a outdated timestamp against 14 days ago
        """

        past = time.time() - (60 * 60 * 24 * 20)

        result = older_than_x_days(past, self.max_days_old)
        self.assertTrue(result)

    def test_outdated_timestamp_2(self):
        """
        Test a outdated timestamp against 14 days ago
        """

        result = older_than_x_days(1601097377.792748, self.max_days_old)
        self.assertTrue(result)

    def test_today_timestamp(self):
        """
        Test today timestamp against 14 days ago
        """

        today = time.time()

        result = older_than_x_days(today, self.max_days_old)
        self.assertFalse(result)

    def test_future_timestamp(self):
        """
        Test a timestamp in the future against 14 days ago
        """

        future = time.time() + (60 * 60 * 24 * 20)

        result = older_than_x_days(future, self.max_days_old)
        self.assertFalse(result)

    def test_download_geofabrik_file(self):
        """
        Test the download of geofabrik file via URL
        """
        path = os.path.join(constants.USER_DL_DIR, 'geofabrik.json')
        download_file(
            path, 'https://download.geofabrik.de/index-v1.json', False)

        self.assertTrue(os.path.exists(path))

    def test_download_geofabrik_file_2(self):
        """
        Test the download of geofabrik file via URL.
        check & download via built functions of downloader class
        """
        path = os.path.join(constants.USER_DL_DIR, 'geofabrik.json')

        if os.path.exists(path):
            os.remove(path)

        self.assertTrue(
            self.o_downloader.should_geofabrik_file_be_downloaded())

        self.o_downloader.download_geofabrik_file()

        self.assertTrue(os.path.exists(path))
        self.assertFalse(
            self.o_downloader.should_geofabrik_file_be_downloaded())

    def test_building_osm_pbf_filepaths(self):
        """
        Test if composing map file path on the device is correct
        "/" to "_" is done for "us/" countries
        """
        self.check_exp_agains_composed_map_file_path(
            'us/nebraska', 'us_nebraska')

        self.check_exp_agains_composed_map_file_path(
            'us/georgia', 'us_georgia')

        self.check_exp_agains_composed_map_file_path(
            'malta', 'malta')

        self.check_exp_agains_composed_map_file_path(
            'asia', 'asia')

        self.check_exp_agains_composed_map_file_path(
            'georgia', 'georgia')

    def test_download_osm_pbf_file(self):
        """
        Test the download of geofabrik file via URL
        """
        self.check_download_osm_pbf_file('malta', os.path.join(constants.USER_DL_DIR, 'maps',
                                                               'malta' + '-latest.osm.pbf'))

        self.check_download_osm_pbf_file('us/hawaii', os.path.join(constants.USER_DL_DIR, 'maps',
                                                                   'us_hawaii' + '-latest.osm.pbf'))

        self.check_download_osm_pbf_file('solomon-islands', os.path.join(constants.USER_DL_DIR, 'maps',
                                                                         'solomon-islands' + '-latest.osm.pbf'))

    def test_delete_not_existing_file(self):
        """
        Test if the removal of a not existing file raises a exception
        """

        path = os.path.join(constants.USER_DL_DIR, 'maps',
                            'malta' + '-latest.osm.pbf')

        if os.path.exists(path):
            os.remove(path)

        with self.assertRaises(FileNotFoundError):
            os.remove(path)

    def test_check_dl_needed_geofabrik(self):
        """
        Test if geofabrik file needs to be downloaded
        """
        path = os.path.join(constants.USER_DL_DIR, 'geofabrik.json')

        if os.path.exists(path):
            os.remove(path)

        self.o_downloader.max_days_old = 24
        # self.o_downloader.check_geofabrik_file()

        self.assertTrue(
            self.o_downloader.should_geofabrik_file_be_downloaded())

    def test_download_windows_files(self):
        """
        Test if Windows tooling files download is successful
        """
        if platform.system() == "Windows":
            path = constants.USER_TOOLING_WIN_DIR

            if os.path.exists(path):
                shutil.rmtree(path)

            self.assertFalse(os.path.exists(path))

            download_tooling()

            self.assertTrue(os.path.exists(path))

            self.assertTrue(
                os.path.exists(get_tooling_win_path('osmfilter.exe', in_user_dir=True)))

    def test_download_macos_files(self):
        """
        Test if macOS tooling files download is successful
        """
        if platform.system() != "Windows":
            path = os.path.join(str(constants.USER_DIR), '.openstreetmap', 'osmosis',
                                'plugins', 'mapsforge-map-writer-0.18.0-jar-with-dependencies.jar')

            if os.path.exists(path):
                os.remove(path)

            self.assertFalse(os.path.exists(path))

            download_tooling()

            self.assertTrue(os.path.exists(path))

    def check_exp_agains_composed_map_file_path(self, country, country_map_file_path):
        """
        helper function to check a given to-be-path against the composed on based on country
        """
        exp_path = os.path.join(constants.USER_DL_DIR, 'maps',
                                f'{country_map_file_path}' + '-latest.osm.pbf')

        composed_path = build_osm_pbf_filepath(country)

        self.assertEqual(exp_path, composed_path)

    def check_download_osm_pbf_file(self, country, path):
        """
        Test if the download of a input country created the wanted map file
        """
        o_geofabrik_json = GeofabrikJson()

        if os.path.exists(path):
            os.remove(path)

        map_file_path = build_osm_pbf_filepath(country)
        url = o_geofabrik_json.get_geofabrik_url(country)
        download_file(map_file_path, url, False)

        self.assertTrue(os.path.exists(path))


if __name__ == '__main__':
    unittest.main()
