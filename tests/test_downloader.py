"""
tests for the downloader file
"""
import os
# import sys
import unittest
import time

# import custom python packages
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common_python.downloader import older_than_x_days
from common_python.downloader import Downloader
from common_python import file_directory_functions as fd_fct


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

    def test_download_polygons_file(self):
        """
        Test the download of land poligons file via URL
        """
        path = os.path.join(fd_fct.COMMON_DL_DIR, 'land-polygons-split-4326',
                            'land_polygons.shp')
        self.o_downloader.download_file(path,
                                        'https://osmdata.openstreetmap.de/download/land-polygons-split-4326.zip', True)

    def test_download_geofabrik_file(self):
        """
        Test the download of land poligons file via URL
        """
        path = os.path.join(fd_fct.COMMON_DL_DIR, 'geofabrik.json')
        self.o_downloader.download_file(
            path, 'https://download.geofabrik.de/index-v1.json', False)


if __name__ == '__main__':
    unittest.main()
