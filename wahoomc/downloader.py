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

# import custom python packages
from wahoomc import file_directory_functions as fd_fct
from wahoomc import constants_functions as const_fct

log = logging.getLogger('main-logger')


def older_than_x_days(file_creation_timestamp, max_days_old):
    """
    check if given timestamp is older that given days
    """
    to_old_timestamp = time.time() - 60 * 60 * 24 * max_days_old

    return bool(file_creation_timestamp < to_old_timestamp)


def download_file(target_filepath, url, is_zip):
    """
    download given file and eventually unzip it
    """
    logging_filename = target_filepath.split(os.sep)[-1]
    log.info('-' * 80)
    log.info('+ Downloading %s file', logging_filename)
    if is_zip:
        # build target-filepath based on last element of URL
        last_part = url.rsplit('/', 1)[-1]
        dl_file_path = os.path.join(fd_fct.USER_DL_DIR, last_part)
        # download URL to file
        fd_fct.download_url_to_file(url, dl_file_path)
        # unpack it - should work on macOS and Windows
        fd_fct.unzip(dl_file_path, fd_fct.USER_DL_DIR)
        # delete .zip file
        os.remove(dl_file_path)
    else:
        # no zipping --> directly download to given target filepath
        fd_fct.download_url_to_file(url, target_filepath)
    # Check if file exists (if target file exists)
    if not os.path.isfile(target_filepath):
        log.error('! failed to find %s', target_filepath)
        sys.exit()
    else:
        log.info('+ Downloaded: %s', target_filepath)


def get_osm_pbf_filepath_url(country):
    """
    evaluate a countries' OSM file URL and download filepath
    """

    # get .osm.pbf region of country
    url = build_url_for_country_osm_pbf_download(country)
    map_file_path = os.path.join(
        fd_fct.USER_MAPS_DIR, f'{country}' + '-latest.osm.pbf')
    # return URL and download filepath
    return map_file_path, url


def build_url_for_country_osm_pbf_download(country):
    """
    build the geofabrik download url to a countries' OSM file
    """
    transl_c = const_fct.translate_country_input_to_geofabrik(country)
    region = const_fct.get_geofabrik_region_of_country(country)
    if region != 'no':
        url = 'https://download.geofabrik.de/' + region + \
            '/' + transl_c + '-latest.osm.pbf'
    else:
        url = 'https://download.geofabrik.de/' + transl_c + '-latest.osm.pbf'
    return url


class Downloader:
    """
    This is the class to check and download maps / artifacts"
    """

    def __init__(self, max_days_old, force_download):
        self.max_days_old = max_days_old
        self.force_download = force_download
        self.tiles_from_json = []
        self.border_countries = {}

    def check_and_download_geofabrik_if_needed(self):
        """
        check geofabrik file if not existing or is not up-to-date
        and download if needed
        """

        force_processing = False

        if self.check_file(fd_fct.GEOFABRIK_PATH) is True or \
                self.force_download is True:
            log.info('# Need to download geofabrik file')
            download_file(fd_fct.GEOFABRIK_PATH,
                          'https://download.geofabrik.de/index-v1.json', False)
            force_processing = True

        log.info('+ check geofabrik.json file: OK')

        return force_processing

    def check_and_download_files_if_needed(self):
        """
        check land_polygons and OSM map files if not existing or are not up-to-date
        and download if needed
        """

        force_processing = False

        if self.check_file(fd_fct.LAND_POLYGONS_PATH) is True or \
                self.force_download is True:
            log.info('# Need to download land polygons file')
            download_file(fd_fct.LAND_POLYGONS_PATH,
                          'https://osmdata.openstreetmap.de/download/land-polygons-split-4326.zip', True)
            force_processing = True

        log.info('+ check land_polygons.shp file: OK')

        if self.check_osm_pbf_file() is True or self.force_download is True:
            # trigger download of relevant countries' OSM files
            for country, item in self.border_countries.items():
                try:
                    if item['download'] is True:
                        map_file_path, url = get_osm_pbf_filepath_url(country)
                        download_file(map_file_path, url, False)
                        self.border_countries[country] = {
                            'map_file': map_file_path}
                except KeyError:
                    pass

            force_processing = True

        log.info('+ Check countries .osm.pbf files: OK')

        # if force_processing is True:
        fd_fct.create_empty_directories(self.tiles_from_json)

        return force_processing

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

        need_to_download = False
        log.info('-' * 80)
        log.info('# check countries .osm.pbf files')

        # Check for expired maps and delete them
        log.info('+ Checking for old maps and remove them')

        for country in self.border_countries:
            # get translated country (geofabrik) of country
            # do not download the same file for different countries
            # --> e.g. China, Hong Kong and Macao, see Issue #11
            transl_c = const_fct.translate_country_input_to_geofabrik(country)

            # check for already existing .osm.pbf file
            map_file_path = glob.glob(
                f'{fd_fct.USER_MAPS_DIR}/{transl_c}-latest.osm.pbf')
            if len(map_file_path) != 1:
                map_file_path = glob.glob(
                    f'{fd_fct.USER_MAPS_DIR}/**/{transl_c}-latest.osm.pbf')

            # delete .osm.pbf file if out of date
            if len(map_file_path) == 1 and os.path.isfile(map_file_path[0]):
                if self.should_file_be_downloaded(map_file_path[0]):
                    log.info(
                        '+ mapfile for %s: deleted. Input: %s.', transl_c, country)
                    os.remove(map_file_path[0])
                    need_to_download = True
                else:
                    self.border_countries[country] = {
                        'map_file': map_file_path[0]}
                    log.info(
                        '+ mapfile for %s: up-to-date. Input: %s.', transl_c, country)

            # mark country .osm.pbf file for download if there exists no file or it is no file
            map_file_path = self.border_countries[country].get('map_file')
            if map_file_path is None or (not os.path.isfile(map_file_path) or self.force_download):
                self.border_countries[country]['download'] = True
                need_to_download = True

        # self.border_countries = border_countries

        return need_to_download

    def should_file_be_downloaded(self, file_path):
        """
        check if given file should be downloaded
        - older that max_days old OR
        - force_download is set
        """

        chg_time = os.path.getmtime(file_path)

        return bool(older_than_x_days(chg_time, self.max_days_old) or self.force_download is True)
