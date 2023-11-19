"""
functions and object for managing OSM maps
"""
#!/usr/bin/python

# import official python packages
import sys
import logging

# import custom python packages
from wahoomc.downloader import Downloader
from wahoomc.geofabrik import CountryGeofabrik, XYCombinationHasNoCountries, XYGeofabrik

log = logging.getLogger('main-logger')

class InformalOsmDataInterface:
    """
    object with all internal parameters to process maps
    """

    def __init__(self, o_input_data):
        """
        steps in constructor:
        1. take over input paramters (force_processing is changed in the function further down)
        2. check + download geofabrik file (always)
        """
        self.force_processing = False
        self.tiles = []
        self.border_countries = {}
        self.country_name = ''

        self.o_downloader = Downloader(
            o_input_data.max_days_old, o_input_data.force_download, self.border_countries)
        # takeover what is given by user first for force_processing
        self.force_processing = o_input_data.force_processing
        self.process_border_countries = o_input_data.process_border_countries

        log.info('-' * 80)

        # geofabrik file
        if self.o_downloader.should_geofabrik_file_be_downloaded():
            self.force_processing = True
            self.o_downloader.download_geofabrik_file()

    def process_input_of_the_tool(self):
        """
        Process input: get relevant tiles and if border countries should be calculated
        The three primary inputs are giving by a separate value each and have separate processing:
        1. country name
        2. x/y combinations
        """

    def calc_tiles(self):
        """
        calculate relevant tiles for input country or xy coordinate
        """

    def calc_border_countries(self):
        """
        calculate the border countries for the given tiles. i.e.
        - if CLI/GUI input by user
        - if processing x/y coordinates
        """
        log.info('# Determine involved/border countries')

        # Build list of countries needed
        for tile in self.tiles:
            for country in tile['countries']:
                if country not in self.border_countries:
                    self.border_countries[country] = {}

    def log_border_countries(self):
        """
        write calculated border countries/involved countries to log
        """
        for country in self.border_countries:
            log.info('+ Involved country: %s', country)

        # border countries should be processed. Log it.
        if self.process_border_countries:
            log.info('+ Border countries will be processed')

    def get_downloader(self):
        """
        steps in this function:
        1. Check for not existing or expired files. Mark for download, if dl is needed
        - land polygons file
        - .osm.pbf files
        2. Calculate if force_processing should be set to true
        """
        # calc force processing
        # Check for not existing or expired files. Mark for download, if dl is needed
        self.o_downloader.check_land_polygons_file()
        self.o_downloader.check_osm_pbf_file()

        # If one of the files needs to be downloaded, reprocess all files
        if self.o_downloader.need_to_dl:
            self.force_processing = True

        return self.o_downloader


class CountryOsmData(InformalOsmDataInterface):
    """
    object with all internal parameters to process maps for countries
    """

    def __init__(self, o_input_data):
        super().__init__(o_input_data)
        self.input_country = o_input_data.country

        self.o_geofabrik = CountryGeofabrik(self.input_country)

    def process_input_of_the_tool(self):
        """
        steps in this function:
        1. calculate relevant tiles for map creation
        2. calculate border countries for map creation
        3. evaluate the country-name for folder cration during processing
        """

        # calc tiles
        self.calc_tiles()

        # calc border countries
        log.info('-' * 80)
        self.calc_border_countries()
        # log border countries when and when not calculated to output the processed country(s)
        self.log_border_countries()

        # calc country name
        self.calc_country_name()

    def calc_tiles(self):
        """
        option 1: input a country as parameter, e.g. germany
        """
        log.info('# Input country: %s.', self.input_country)

        # use Geofabrik-URL to calculate the relevant tiles
        self.tiles = self.o_geofabrik.get_tiles_of_wanted_map()

    def calc_border_countries(self):
        """
        calculate the border countries for the given tiles when input is a country
        - if CLI/GUI input by user
        """
        if self.process_border_countries:
            super().calc_border_countries()
        # set the to-be-processed country as border country
        else:
            for country in self.o_geofabrik.wanted_maps:
                self.border_countries[country] = {}

    def calc_country_name(self):
        """
        country name is the country
        >1 countries are separated by underscore
        """
        for country in self.o_geofabrik.wanted_maps:
            if not self.country_name:
                self.country_name = country
            else:
                self.country_name = f'{self.country_name}_{country}'


class XYOsmData(InformalOsmDataInterface):
    """
    object with all internal parameters to process maps for XY coordinates
    """

    def __init__(self, o_input_data):
        super().__init__(o_input_data)
        self.input_xy_coordinates = o_input_data.xy_coordinates

    def process_input_of_the_tool(self):
        """
        Process input: get relevant tiles and if border countries should be calculated
        The three primary inputs are giving by a separate value each and have separate processing:
        1. country name
        2. x/y combinations

        # Check for not existing or expired files. Mark for download, if dl is needed
        # - land polygons file
        # - .osm.pbf files

        steps in this function:
        1. calculate relevant tiles for map creation
        2. calculate border countries for map creation
        3. evaluate the country-name for folder cration during processing
        """

        # calc tiles
        self.calc_tiles()

        # calc border countries
        log.info('-' * 80)
        self.calc_border_countries()
        # log border countries when and when not calculated to output the processed country(s)
        self.log_border_countries()

        # calc country name
        self.calc_country_name()

    def calc_tiles(self):
        """
        option 2: input a x/y combinations as parameter, e.g. 134/88  or 133/88,130/100
        """
        log.info(
            '# Input X/Y coordinates: %s.', self.input_xy_coordinates)

        o_geofabrik = XYGeofabrik(self.input_xy_coordinates)
        # find the tiles for  x/y combinations in the geofabrik json files
        try:
            self.tiles = o_geofabrik.get_tiles_of_wanted_map()
        except XYCombinationHasNoCountries as exception:
            # this exception is actually only raised in class XYGeofabrik
            sys.exit(exception)

    def calc_country_name(self):
        """
        country name is the X/Y combinations separated by minus
        >1 x/y combinations are separated by underscore
        """
        for tile in self.tiles:
            if not self.country_name:
                self.country_name = f'{tile["x"]}-{tile["y"]}'
            else:
                self.country_name = f'{self.country_name}_{tile["x"]}-{tile["y"]}'
