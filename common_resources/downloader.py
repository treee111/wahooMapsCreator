"""
functions and object for checking for up-to-date & downloading land_poligons file and OSM maps
"""
#!/usr/bin/python

# import official python packages
import glob
import os
import os.path
import sys
import time

# import custom python packages
import requests
from common_resources import file_directory_functions as fd_fct
from common_resources import constants_functions as const_fct


def older_than_x_days(file_creation_timestamp, max_days_old):
    """
    check if given timestamp is older that given days
    """
    to_old_timestamp = time.time() - 60 * 60 * 24 * max_days_old

    return bool(file_creation_timestamp < to_old_timestamp)


class Downloader:
    """
    This is the class to check and download maps / artifacts"
    """

    def __init__(self, max_days_old, force_download, tiles, border_countries):
        self.max_days_old = max_days_old
        self.force_download = force_download
        self.tiles_from_json = tiles
        self.border_countries = border_countries


    def check_and_download_files_if_needed(self):
        """
        check land_poligons and OSM map files if not existing or are not up-to-date
        """
        force_processing = False

        if self.check_poligons_file() is True or self.force_download is True:
            self.download_land_poligons_file()
            force_processing = True

         # logging
        print('# check land_polygons.shp file: OK')


        if self.check_osm_pbf_file() is True or self.force_download is True:
            self.download_osm_pbf_file()
            force_processing = True

        # logging
        print('# Check countries .osm.pbf files: OK')

        # if force_processing is True:
        fd_fct.create_empty_directories(self.tiles_from_json)

        return force_processing


    def check_poligons_file(self):
        """
        check if land_poligons file is up-to-date
        """

        need_to_download = False
        print('\n# check land_polygons.shp file')

        # Check for expired land polygons file and delete it
        try:
            chg_time = os.path.getctime(fd_fct.LAND_POLYGONS_PATH)
            if older_than_x_days(chg_time, self.max_days_old):
                print ('# Deleting old land polygons file')
                os.remove(fd_fct.LAND_POLYGONS_PATH)
                need_to_download = True

        except:
            need_to_download = True

        # if land poligons file does not exists --> download
        if not os.path.exists(fd_fct.LAND_POLYGONS_PATH) or not os.path.isfile(fd_fct.LAND_POLYGONS_PATH):
            need_to_download = True
            # logging
            print('# land_polygons.shp file needs to be downloaded')

        return need_to_download


    def download_land_poligons_file(self):
        """
        download land_poligons file
        """

        print('# Downloading land polygons file')

        url = 'https://osmdata.openstreetmap.de/download/land-polygons-split-4326.zip'

        # download URL to file
        land_poligons_file_path = os.path.join (fd_fct.COMMON_DIR, 'land-polygons-split-4326.zip')
        self.download_url_to_file(url, land_poligons_file_path)

        # unpack it - should work on macOS and Windows
        fd_fct.unzip(land_poligons_file_path, fd_fct.COMMON_DIR)

        # delete .zip file
        os.remove(os.path.join (fd_fct.COMMON_DIR,
            'land-polygons-split-4326.zip'))

        # Check if land polygons file exists
        if not os.path.isfile(fd_fct.LAND_POLYGONS_PATH):
            print(f'! failed to find {fd_fct.LAND_POLYGONS_PATH}')
            sys.exit()
        else:
            print(f'+ Downloaded: {fd_fct.LAND_POLYGONS_PATH}')


    def check_osm_pbf_file(self):
        """
        check if the relevant countries' OSM files are up-to-date
        """
        need_to_download = False
        print('\n# check countries .osm.pbf files')

        # Check for expired maps and delete them
        print('+ Checking for old maps and remove them')

        for country in self.border_countries:
            # check for already existing .osm.pbf file
            map_file_path = glob.glob(f'{fd_fct.MAPS_DIR}/{country}*.osm.pbf')
            if len(map_file_path) != 1:
                map_file_path = glob.glob(f'{fd_fct.MAPS_DIR}/**/{country}*.osm.pbf')

            # delete .osm.pbf file if out of date
            if len(map_file_path) == 1 and os.path.isfile(map_file_path[0]):
                chg_time = os.path.getctime(map_file_path[0])
                if older_than_x_days(chg_time, self.max_days_old) or self.force_download is True:
                    print(f'+ mapfile for {country}: deleted')
                    os.remove(map_file_path[0])
                    need_to_download = True
                else:
                    self.border_countries[country] = {'map_file':map_file_path[0]}
                    print(f'+ mapfile for {country}: up-to-date')

            # mark country .osm.pbf file for download if there exists no file or it is no file
            map_file_path = self.border_countries[country].get('map_file')
            if map_file_path is None or (not os.path.isfile(map_file_path) or self.force_download):
                self.border_countries[country]['download'] = True
                need_to_download = True

        # self.border_countries = border_countries

        return need_to_download


    def download_osm_pbf_file(self):
        """
        trigger download of relevant countries' OSM files
        """

        for country in self.border_countries:
            try:
                if self.border_countries[country]['download'] is True:
                    map_file_path = self.download_map(country)
                    self.border_countries[country] = {'map_file':map_file_path}
            except KeyError:
                pass

    def download_map(self, country):
        """
        download a countries' OSM file
        """

        print(f'+ Trying to download missing map of {country}.')

        # get Geofabrik region of country
        translated_country = const_fct.translate_country_input_to_geofabrik(country)
        region = const_fct.get_geofabrik_region_of_country(country)

        if region != 'no':
            url = 'https://download.geofabrik.de/' + region + '/' + translated_country + '-latest.osm.pbf'
        else:
            url = 'https://download.geofabrik.de/' + translated_country + '-latest.osm.pbf'

        # download URL to file
        map_file_path = os.path.join (fd_fct.MAPS_DIR, f'{country}' + '-latest.osm.pbf')
        self.download_url_to_file(url, map_file_path)

        if not os.path.isfile(map_file_path):
            print(f'! failed to find or download country: {country}')
            sys.exit()
        else:
            print(f'+ Map of {country} downloaded.')

        return map_file_path

    def download_url_to_file(self, url, map_file_path):
        """
        download the content of a ULR to file
        """
        request_geofabrik = requests.get(url, allow_redirects = True, stream = True)
        if request_geofabrik.status_code != 200:
            print(f'! failed download URL: {url}')
            sys.exit()

        # write content to file
        self.write_to_file(map_file_path, request_geofabrik)


    def write_to_file(self, file_path, request):
        """
        write content of request into given file path
        """
        with open(file_path, 'wb') as file_handle:
            for chunk in request.iter_content(chunk_size=1024*100):
                file_handle.write(chunk)
