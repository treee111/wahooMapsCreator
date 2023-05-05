"""
functions and object for checking for up-to-date & downloading land_polygons file and OSM maps
"""
#!/usr/bin/python

# import official python packages
import glob
import os
import os.path
import sys
import time
import logging
import platform
import zipfile
import requests

# import custom python packages
from wahoomc.constants_functions import get_tooling_win_path
from wahoomc.geofabrik_json import GeofabrikJson

from wahoomc.constants import USER_DL_DIR
from wahoomc.constants import USER_MAPS_DIR
from wahoomc.constants import LAND_POLYGONS_PATH
from wahoomc.constants import GEOFABRIK_PATH
from wahoomc.constants import OSMOSIS_WIN_FILE_PATH
from wahoomc.constants import USER_TOOLING_WIN_DIR
from wahoomc.constants import USER_DIR

log = logging.getLogger('main-logger')


def older_than_x_days(file_creation_timestamp, max_days_old):
    """
    check if given timestamp is older that given days
    """
    to_old_timestamp = time.time() - 60 * 60 * 24 * max_days_old

    return bool(file_creation_timestamp < to_old_timestamp)


def download_file(target_filepath, url, target_dir=""):
    """
    download given file and eventually unzip it
    """
    logging_filename = target_filepath.split(os.sep)[-1]
    log.info('-' * 80)
    log.info('# Downloading %s file', logging_filename)
    if url.split('.')[-1] == 'zip':
        # build target-filepath based on last element of URL
        last_part = url.rsplit('/', 1)[-1]
        dl_file_path = os.path.join(USER_DL_DIR, last_part)
        # download URL to file
        download_url_to_file(url, dl_file_path)

        # if a target directory is given --> extract into that folder
        if target_dir:
            target_path = target_dir
        else:
            target_path = USER_DL_DIR

        # unpack it
        unzip(dl_file_path, target_path)

        os.remove(dl_file_path)
    else:
        # no zipping --> directly download to given target filepath
        download_url_to_file(url, target_filepath)
    # Check if file exists (if target file exists)
    if not os.path.isfile(target_filepath):
        log.error('! failed to find %s', target_filepath)
        sys.exit()
    else:
        log.info('+ Downloaded: %s', target_filepath)


def build_osm_pbf_filepath(country_translated):
    """
    build download filepath to countries' OSM file
    replace / to have no problem with directories
    """
    # build path to downloaded file with translated geofabrik country
    map_file_path = os.path.join(
        USER_MAPS_DIR, f'{country_translated.replace("/", "_")}' + '-latest.osm.pbf')

    # return download filepath
    return map_file_path


def download_url_to_file(url, map_file_path):
    """
    download the content of a ULR to file
    """
    # set timeout to 30 minutes (per file)
    request_geofabrik = requests.get(
        url, allow_redirects=True, stream=True, timeout=1800)
    if request_geofabrik.status_code != 200:
        log.error('! failed download URL: %s', url)
        sys.exit()

    # write content to file
    write_to_file(map_file_path, request_geofabrik)


def download_tooling():
    """
    Windows
    - check for Windows tooling
    - download if Windows tooling is not available
    --> this is done to bring down the filesize of the python module

    macOS
    - check for mapwriter plugin and download if not existing
    """

    mapwriter_plugin_url = 'https://search.maven.org/remotecontent?filepath=org/mapsforge/mapsforge-map-writer/0.18.0/mapsforge-map-writer-0.18.0-jar-with-dependencies.jar'

    # Windows
    if platform.system() == "Windows":
        os.makedirs(USER_TOOLING_WIN_DIR, exist_ok=True)

        if not os.path.isfile(OSMOSIS_WIN_FILE_PATH):
            log.info('# Need to download Osmosis application for Windows')
            download_file(OSMOSIS_WIN_FILE_PATH,
                          'https://github.com/openstreetmap/osmosis/releases/download/0.48.3/osmosis-0.48.3.zip',
                          get_tooling_win_path('Osmosis', in_user_dir=True))

        if not os.path.isfile(get_tooling_win_path('osmfilter.exe', in_user_dir=True)):
            log.info('# Need to download osmfilter application for Windows')

            download_file(get_tooling_win_path('osmfilter.exe', in_user_dir=True),
                          'http://m.m.i24.cc/osmfilter.exe')

        mapwriter_plugin_path = os.path.join(USER_TOOLING_WIN_DIR,
                                             'Osmosis', 'lib', 'default', 'mapsforge-map-writer-0.18.0-jar-with-dependencies.jar')

    # Non-Windows
    else:
        mapwriter_plugin_path = os.path.join(
            str(USER_DIR), '.openstreetmap', 'osmosis', 'plugins', 'mapsforge-map-writer-0.18.0-jar-with-dependencies.jar')

    if not os.path.isfile(mapwriter_plugin_path):
        log.info('# Need to download Osmosis mapwriter plugin')
        # create plugins directory
        os.makedirs(os.path.dirname(mapwriter_plugin_path), exist_ok=True)
        download_file(mapwriter_plugin_path, mapwriter_plugin_url)

    # download geofabrik json as this will be needed always
    # because of the .json file replacement by geofabrik
    download_geofabrik_file_if_not_existing()


def download_geofabrik_file_if_not_existing():
    """
    check geofabrik file if not existing
    if the file does not exist, download geofabrik file
    """
    if not os.path.isfile(GEOFABRIK_PATH):
        log.info('# Need to download geofabrik file')
        download_file(GEOFABRIK_PATH,
                      'https://download.geofabrik.de/index-v1.json')


def get_latest_pypi_version():
    """
    get latest wahoomc version available on PyPI
    """
    try:
        response = requests.get(
            'https://pypi.org/pypi/wahoomc/json', timeout=1)
        return response.json()['info']['version']
    except (requests.ConnectionError, requests.Timeout):
        return None


def write_to_file(file_path, request):
    """
    write content of request into given file path
    """
    with open(file_path, mode='wb') as file_handle:
        for chunk in request.iter_content(chunk_size=1024*100):
            file_handle.write(chunk)


def unzip(source_filename, dest_dir):
    """
    unzip the given file into the given directory
    """
    with zipfile.ZipFile(source_filename, 'r') as zip_ref:
        zip_ref.extractall(dest_dir)


class Downloader:
    """
    This is the class to check and download maps / artifacts"
    """

    def __init__(self, max_days_old, force_download, border_countries=None):
        self.max_days_old = max_days_old
        self.force_download = force_download
        self.border_countries = border_countries

        # safety net if geofabrik file is not there
        # OsmData=>process_input_of_the_tool does it "correctly"
        download_geofabrik_file_if_not_existing()

        self.o_geofabrik_json = GeofabrikJson()

        self.need_to_dl = []

    def should_geofabrik_file_be_downloaded(self):
        """
        check geofabrik file if not existing or is not up-to-date

        # if geofabrik file needs to be downloaded, force-processing is set because there might be
        # a change in the geofabrik file
        """
        if self.check_file(GEOFABRIK_PATH) is True or \
                self.force_download is True:
            log.info('# Need to download geofabrik file')

            return True

        return False

    def download_geofabrik_file(self):
        """
        download geofabrik file
        """
        download_file(GEOFABRIK_PATH,
                      'https://download.geofabrik.de/index-v1.json')

        log.info('+ download geofabrik.json file: OK')

    def check_land_polygons_file(self):
        """
        check land_polygons file if not existing or are not up-to-date
        """

        if self.check_file(LAND_POLYGONS_PATH) is True or \
                self.force_download is True:
            log.info('+ Need to download land polygons file')
            self.need_to_dl.append('land_polygons')

    def download_files_if_needed(self):
        """
        check land_polygons and OSM map files if not existing or are not up-to-date
        and download if needed
        """
        if 'land_polygons' in self.need_to_dl:
            download_file(LAND_POLYGONS_PATH,
                          'https://osmdata.openstreetmap.de/download/land-polygons-split-4326.zip')

        # log.info('+ download land_polygons.shp file: OK')

        if 'osm_pbf' in self.need_to_dl:
            self.download_osm_pbf_file()

    def check_file(self, target_filepath):
        """
        check if given file is up-to-date
        """

        need_to_download = False
        logging_filename = target_filepath.rsplit('/', 1)[-1]

        log.info('-' * 80)
        log.info('# check %s file', logging_filename)

        # Check for expired file and delete it
        try:
            if self.should_file_be_downloaded(target_filepath):
                log.info('+ Deleting old %s file', logging_filename)
                os.remove(target_filepath)
                need_to_download = True

        except FileNotFoundError:
            need_to_download = True

        # if file does not exists --> download
        if not os.path.exists(target_filepath) or \
                not os.path.isfile(target_filepath):
            need_to_download = True

            log.info('+ %s file needs to be downloaded', logging_filename)

        return need_to_download

    def check_osm_pbf_file(self):
        """
        check if the relevant countries' OSM files are up-to-date
        """

        log.info('-' * 80)
        log.info('# check countries .osm.pbf files')

        # Check for expired maps and delete them
        log.info('+ Checking for old maps and remove them')

        for country in self.border_countries:
            # check for already existing .osm.pbf file
            map_file_path = glob.glob(
                f'{USER_MAPS_DIR}/{country}-latest.osm.pbf')
            if len(map_file_path) != 1:
                map_file_path = glob.glob(
                    f'{USER_MAPS_DIR}/**/{country}-latest.osm.pbf')

            # delete .osm.pbf file if out of date
            if len(map_file_path) == 1 and os.path.isfile(map_file_path[0]):
                if self.should_file_be_downloaded(map_file_path[0]):
                    log.info(
                        '+ mapfile for %s: deleted.', country)
                    os.remove(map_file_path[0])
                    self.need_to_dl.append('osm_pbf')
                else:
                    self.border_countries[country] = {
                        'map_file': map_file_path[0]}
                    log.info(
                        '+ mapfile for %s: up-to-date.', country)

            # mark country .osm.pbf file for download if there exists no file or it is no file
            map_file_path = self.border_countries[country].get('map_file')
            if map_file_path is None or (not os.path.isfile(map_file_path) or self.force_download):
                self.border_countries[country]['download'] = True
                self.need_to_dl.append('osm_pbf')

    def download_osm_pbf_file(self):
        """
        download countries' OSM files
        """
        for country, item in self.border_countries.items():
            try:
                if item['download'] is True:
                    # build path to downloaded file with translated geofabrik country
                    map_file_path = build_osm_pbf_filepath(country)
                    # fetch the geofabrik download url to countries' OSM file
                    url = self.o_geofabrik_json.get_geofabrik_url(country)
                    download_file(map_file_path, url)
                    self.border_countries[country] = {
                        'map_file': map_file_path}
            except KeyError:
                pass

    def should_file_be_downloaded(self, file_path):
        """
        check if given file should be downloaded
        - older that max_days old OR
        - force_download is set
        """

        chg_time = os.path.getmtime(file_path)

        return bool(older_than_x_days(chg_time, self.max_days_old) or self.force_download is True)
