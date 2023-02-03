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
from wahoomc.downloader import get_osm_pbf_filepath_url
from wahoomc.downloader import download_tooling
from wahoomc.downloader import Downloader
from wahoomc import constants
from wahoomc.constants_functions import get_tooling_win_path


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

    # def test_download_polygons_file(self):
    #     """
    #     Test the download of land poligons file via URL
    #     """
    #     path = os.path.join(fd_fct.COMMON_DL_DIR, 'land-polygons-split-4326',
    #                         'land_polygons.shp')
    #     self.o_downloader.download_file(path,
    #                                     'https://osmdata.openstreetmap.de/download/land-polygons-split-4326.zip', True)

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

    def test_download_malta_osm_pbf_file(self):
        """
        Test the download of geofabrik file via URL
        """

        country = 'malta'

        path = os.path.join(constants.USER_DL_DIR, 'maps',
                            f'{country}' + '-latest.osm.pbf')

        if os.path.exists(path):
            os.remove(path)

        map_file_path, url = get_osm_pbf_filepath_url(country)
        download_file(map_file_path, url, False)

        self.assertTrue(os.path.exists(path))

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

            os.makedirs(constants.USER_TOOLING_WIN_DIR, exist_ok=True)
            download_tooling()

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

            self.assertFalse(
                os.path.exists(path))

            # os.makedirs(constants.USER_TOOLING_WIN_DIR, exist_ok=True)
            download_tooling()

            self.assertTrue(
                os.path.exists(path))


if __name__ == '__main__':
    unittest.main()
