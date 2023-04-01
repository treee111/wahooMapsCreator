"""
functions and object for managing OSM maps
"""
#!/usr/bin/python
# pylint: skip-file

# import official python packages
import sys
import math
import logging
from shapely.geometry import Polygon, shape

# import custom python packages
from wahoomc.constants import special_regions, block_download
from wahoomc.geofabrik_json import CountyIsNoGeofabrikCountry, GeofabrikJson

log = logging.getLogger('main-logger')


class XYCombinationHasNoCountries(Exception):
    """Raised when no tile is found for x/y combination"""

    def __init__(self, xy_coordinate):
        message = f"Given XY coordinate '{xy_coordinate}' consists of no countries. Please check if your input is valid."
        super().__init__(message)


class InformalGeofabrikInterface:
    """Informal class for Geofabrik processing"""
    wanted_maps = []
    tiles = []
    border_countries = {}
    output = {}

    o_geofabrik_json = None

    def get_tiles_of_wanted_map_single(self, wanted_map) -> str:
        """Get the relevant tiles for ONE wanted country or X/Y coordinate"""
        pass

    def get_tiles_of_wanted_map(self) -> list:
        """
        calculates tiles of all input wanted-maps
        :returns: list of tiles
        """

        tiles_of_input = []

        for wanted_map in self.wanted_maps:
            try:
                tiles_of_input.extend(
                    self.get_tiles_of_wanted_map_single(wanted_map))
            except XYCombinationHasNoCountries as exception:
                # this exception is actually only raised in class XYGeofabrik
                raise exception

        return tiles_of_input

    def find_needed_countries(self, bbox_tiles, wanted_map, wanted_region_polygon) -> dict:
        """find needed countries for requested country or X/Y combination"""
        pass

    def compose_bouding_box(self, bounds) -> dict:
        """calculate bounding box based on geometry or X/Y combination"""
        pass

    def log_tile(self, counter, all):
        """
        unified status logging for this class
        """
        log.info(
            '(+ tile %s of %s) Find needed countries ', counter, all)

    def split_input_to_list(input_value) -> list:
        """split the input to single values in a list"""
        pass


class CountryGeofabrik(InformalGeofabrikInterface):
    """Geofabrik processing for countries"""

    def __init__(self, input_countries):
        """
        :param input: string with countries: 'malta' or 'malta, switzerland'
        :returns: object for country geofabrik processing
        """
        self.o_geofabrik_json = GeofabrikJson()
        self.wanted_maps = []

        # input parameters
        self.wanted_maps = self.split_input_to_list(input_countries)

    def get_tiles_of_wanted_map_single(self, wanted_map):
        """Overrides InformalGeofabrikInterface.get_tiles_of_wanted_map_single()"""
        # Check if wanted_map is in the json file and if so get the polygon (shape)
        wanted_map_geom = self.o_geofabrik_json.get_geofabrik_geometry(
            wanted_map)

        # convert to shape (multipolygon)
        wanted_region = shape(wanted_map_geom)

        # calc bounding box - the whole area to be created
        bbox = self.compose_bouding_box(wanted_region.bounds)

        # Build bounding box list of tiles - several X/Y combinations making up the area
        bbox_tiles = calc_bounding_box_tiles(bbox)

        # get all infos of these bounding box tiles
        tiles_of_input = self.find_needed_countries(
            bbox_tiles, wanted_map, wanted_region)

        return tiles_of_input

    def find_needed_countries(self, bbox_tiles, wanted_map, wanted_region_polygon) -> list:
        """Overrides InformalGeofabrikInterface.find_needed_countries()"""
        output = []

        geofabrik_regions = self.o_geofabrik_json.geofabrik_regions

        # itterate through tiles and find Geofabrik regions that are in the tiles
        counter = 1
        for tile in bbox_tiles:
            # Do progress indicator every 50 tiles
            if counter % 50 == 0:
                self.log_tile(counter, len(bbox_tiles)+1)
            counter += 1

            parent_added = 0
            force_added = 0

            # example contents of tile: {'index': 0, 'x': 130, 'y': 84, 'tile_left': 2.8125,
            # 'tile_top': 52.48278022207821, 'tile_right': 4.21875, 'tile_bottom': 51.6180165487737}
            # convert tile x/y to tile polygon lon/lat
            poly = Polygon([(tile["tile_left"], tile["tile_top"]), (tile["tile_right"],
                                                                    tile["tile_top"]), (tile["tile_right"], tile["tile_bottom"]),
                            (tile["tile_left"], tile["tile_bottom"]), (tile["tile_left"],
                                                                       tile["tile_top"])])

            # (re)initialize list of needed maps and their url's
            must_download_maps = []
            must_download_urls = []

            # itterate through countries/regions in the geofabrik json file
            for region, value in self.o_geofabrik_json.geofabrik_overview.items():
                regionname = region
                try:
                    parent = value['parent']
                except KeyError:
                    parent = ''
                rurl = value['pbf_url']
                rshape = shape(value['geometry'])

                # for debugging
                # if tile["x"] == 137 and (region == "denmark" or region == "germany" or region == "sweden"):
                #     print("stop for debugging")
                # if not xy_mode:

                # print (f'Processing region: {regionname}')

                # check if the region we are processing is needed for the tile we are processing

                # If currently processing country/region IS the desired country/region
                if regionname == wanted_map:
                    # Check if it is part of the tile we are processing
                    if rshape.intersects(poly):  # if so
                        # catch special_regions like (former) colonies where the map of the region is not fysically in the map of the parent country.
                        # example Guadeloupe, it's parent country is France but Guadeloupe is not located within the region covered by the map of France
                        if wanted_map not in special_regions:
                            # If we are proseccing a sub-region add the parent of this sub-region
                            # to the must download list.
                            # This to prevent downloading several small regions AND it's containing region
                            # we are processing a sub-regiongo find the parent region:
                            if parent not in geofabrik_regions and regionname not in geofabrik_regions:
                                # we are processing a sub-regiongo find the parent region
                                x_value = 0
                                # handle sub-sub-regions like unterfranken->bayern->germany
                                while parent not in geofabrik_regions:
                                    parent, child = self.o_geofabrik_json.get_geofabrik_parent_country(
                                        parent)
                                    if parent in geofabrik_regions:
                                        parent = child
                                        break
                                    if x_value > 10:  # prevent endless loop
                                        log.error(
                                            'Can not find parent map of region: %s', regionname)
                                        sys.exit()
                                    x_value += 1
                                if parent not in must_download_maps:
                                    must_download_maps.append(parent)
                                    must_download_urls.append(
                                        self.o_geofabrik_json.get_geofabrik_url(parent))
                                    # parent_added = 1
                            else:
                                if regionname not in must_download_maps:
                                    must_download_maps.append(regionname)
                                    must_download_urls.append(rurl)
                        else:
                            # wanted_map is a special region like Guadeloupe, France
                            if regionname not in must_download_maps:
                                must_download_maps.append(regionname)
                                must_download_urls.append(rurl)
                        # if there is an intersect, force the tile to be put in the output
                        force_added = 1
                    else:  # currently processing tile does not contain, a part of, the desired region
                        continue

                # currently processing country/region is NOT the desired country/region but might be
                # in the tile (neighbouring country)
                if regionname != wanted_map:
                    # check if we are processing a country or a sub-region.
                    # For countries only process other countries. also block special geofabrik sub regions
                    if parent in geofabrik_regions and regionname not in block_download:
                        # processing a country and no special sub-region
                        # check if rshape is subset of desired region. If so discard it
                        if wanted_region_polygon.contains(rshape):
                            # print (f'\t{regionname} is a subset of {wanted_map}, discard it')
                            continue
                        # check if rshape is a superset of desired region. if so discard it
                        if rshape.contains(wanted_region_polygon):
                            # print (f'\t{regionname} is a superset of {wanted_map}, discard it')
                            # if regionname not in must_download_maps:
                            #    must_download_maps.append (regionname)
                            #    must_download_urls.append (rurl)
                            #    parent_added = 1
                            continue
                        # Check if rshape is a part of the tile
                        if rshape.intersects(poly):
                            # print(f'\tintersecting tile: {regionname} tile={tile}')
                            if regionname not in must_download_maps:
                                must_download_maps.append(regionname)
                                must_download_urls.append(rurl)

            # If this tile contains the desired region, add it to the output
            # print (f'map= {wanted_map}\tmust_download= {must_download_maps}\tparent_added= {parent_added}\tforce_added= {force_added}')
            if wanted_map in must_download_maps or parent_added == 1 or force_added == 1:
                # first replace any forward slashes with underscores (us/texas to us_texas)
                must_download_maps = [sub.replace(
                    '/', '_') for sub in must_download_maps]
                output.append({'x': tile['x'], 'y': tile['y'], 'left': tile['tile_left'], 'top': tile['tile_top'],
                               'right': tile['tile_right'], 'bottom': tile['tile_bottom'], 'countries': must_download_maps, 'urls': must_download_urls})

        return output

    def compose_bouding_box(self, bounds):
        """Overrides InformalGeofabrikInterface.calc_bouding_box()"""
        # get bounding box
        (bbox_left, bbox_bottom, bbox_right, bbox_top) = bounds

        # convert bounding box to list of tiles at zoom level 8
        (top_x, top_y) = deg2num(bbox_top, bbox_left)
        (bot_x, bot_y) = deg2num(bbox_bottom, bbox_right)

        # and stay within the allowed tilenumber range!
        if top_x < 0:
            top_x = 0
        if top_x > 255:
            top_x = 255
        if top_y < 0:
            top_y = 0
        if top_y > 255:
            top_y = 255
        if bot_x < 0:
            bot_x = 0
        if bot_x > 255:
            bot_x = 255
        if bot_y < 0:
            bot_y = 0
        if bot_y > 255:
            bot_y = 255

        return {'top_x': top_x, 'top_y': top_y, 'bot_x': bot_x, 'bot_y': bot_y}

    @staticmethod
    def split_input_to_list(input_value) -> list:
        """
        extract/split x/y combinations by given X/Y coordinates.
        input should be "188/88" or for multiple values "188/88,100/10,109/99".
        returns a list of x/y combinations as integers
        """
        countries = []
        o_geofabrik_json = GeofabrikJson()

        try:
            # split by "," first for multiple x/y combinations, then by "/" for x and y value
            for country in input_value.split(","):
                countries.append(o_geofabrik_json.translate_id_no_to_geofabrik(
                    country))
        except CountyIsNoGeofabrikCountry as exception:
            raise exception

        return countries


class XYGeofabrik(InformalGeofabrikInterface):
    """Geofabrik processing for X/Y coordinates"""

    def __init__(self, input_xy_coordinates):
        """
        :param input: string with xy-coordinates: 133/88 or 133/88,134/88
        :returns: object for xy geofabrik processing
        """
        self.o_geofabrik_json = GeofabrikJson()

        # use Geofabrik-URL to get the relevant tiles
        self.wanted_maps = self.split_input_to_list(input_xy_coordinates)

    def get_tiles_of_wanted_map_single(self, wanted_map):
        """Overrides InformalGeofabrikInterface.get_tiles_of_wanted_map_single()"""
        # calc bounding box - the whole area to be created
        bbox = self.compose_bouding_box(wanted_map)

        # Build bounding box list of tiles - several X/Y combinations making up the area
        bbox_tiles = calc_bounding_box_tiles(bbox)

        # convert X/Y combination to shape (multipolygon)
        wanted_region = self.compose_shape(bbox_tiles)

        # get all infos of these bounding box tiles
        tiles_of_input = self.find_needed_countries(
            bbox_tiles, wanted_map, wanted_region)

        if len(tiles_of_input[0]['countries']) == 0:
            raise XYCombinationHasNoCountries(
                f'{wanted_map["x"]}/{wanted_map["y"]}')

        return tiles_of_input

    def find_needed_countries(self, bbox_tiles, wanted_map, wanted_region_polygon) -> dict:
        """Overrides InformalGeofabrikInterface.find_needed_countries()"""
        output = []

        geofabrik_regions = self.o_geofabrik_json.geofabrik_regions

        log.info('Searching for needed maps, this can take a while.')

        # itterate through tiles and find Geofabrik regions that are in the tiles
        counter = 1
        for tile in bbox_tiles:
            # Do progress indicator every 50 tiles
            if counter % 50 == 0:
                self.log_tile(counter, len(bbox_tiles)+1)
            counter += 1

            parent_added = 0
            force_added = 0

            # example contents of tile: {'index': 0, 'x': 130, 'y': 84, 'tile_left': 2.8125,
            # 'tile_top': 52.48278022207821, 'tile_right': 4.21875, 'tile_bottom': 51.6180165487737}
            # convert tile x/y to tile polygon lon/lat
            poly = Polygon([(tile["tile_left"], tile["tile_top"]), (tile["tile_right"],
                                                                    tile["tile_top"]), (tile["tile_right"], tile["tile_bottom"]),
                            (tile["tile_left"], tile["tile_bottom"]), (tile["tile_left"],
                                                                       tile["tile_top"])])

            # (re)initialize list of needed maps and their url's
            must_download_maps = []
            must_download_urls = []

            # itterate through countries/regions in the geofabrik json file
            for region, value in self.o_geofabrik_json.geofabrik_overview.items():
                regionname = region
                try:
                    parent = value['parent']
                except KeyError:
                    parent = ''
                rurl = value['pbf_url']
                rshape = shape(value['geometry'])

                if parent in geofabrik_regions and regionname not in block_download:
                    # processing a country and no special sub-region
                    # check if rshape is subset of desired region. If so discard it
                    if wanted_region_polygon.contains(rshape):
                        # print (f'\t{regionname} is a subset of {wanted_map}, discard it')
                        continue
                    # check if rshape is a superset of desired region. if so discard it
                    if rshape.contains(wanted_region_polygon):
                        # print (f'\t{regionname} is a superset of {wanted_map}, discard it')
                        continue
                    # Check if rshape is a part of the tile / XY
                    if rshape.intersects(poly):
                        # print(f'\tintersecting tile: {regionname} tile={tile}')
                        if regionname not in must_download_maps:
                            must_download_maps.append(regionname)
                            must_download_urls.append(rurl)

        # If this tile contains the desired region, add it to the output
        # print (f'map= {wanted_map}\tmust_download= {must_download_maps}\tparent_added= {parent_added}\tforce_added= {force_added}')
        # if wanted_map in must_download_maps or parent_added == 1 or force_added == 1 or xy_mode is True:
        # first replace any forward slashes with underscores (us/texas to us_texas)
        must_download_maps = [sub.replace(
            '/', '_') for sub in must_download_maps]
        output.append({'x': tile['x'], 'y': tile['y'], 'left': tile['tile_left'], 'top': tile['tile_top'],
                       'right': tile['tile_right'], 'bottom': tile['tile_bottom'], 'countries': must_download_maps, 'urls': must_download_urls})

        return output

    def compose_bouding_box(self, xy_combination):
        """Overrides InformalGeofabrikInterface.calc_bouding_box()"""

        return {'top_x': xy_combination["x"], 'bot_x': xy_combination["x"],
                'top_y': xy_combination["y"], 'bot_y': xy_combination["y"]}

    def compose_shape(self, bbox_tiles):
        coords = [(bbox_tiles[0]["tile_top"], bbox_tiles[0]["tile_left"]), (bbox_tiles[0]["tile_top"], bbox_tiles[0]["tile_right"]),
                  (bbox_tiles[0]["tile_bottom"], bbox_tiles[0]["tile_right"]), (bbox_tiles[0]["tile_bottom"], bbox_tiles[0]["tile_left"])]
        coords_polygon = Polygon(coords)
        wanted_region = shape(coords_polygon)
        return wanted_region

    @staticmethod
    def split_input_to_list(input_value) -> list:
        """
        extract/split x/y combinations by given X/Y coordinates.
        input should be "188/88" or for multiple values "188/88,100/10,109/99".
        returns a list of x/y combinations as integers
        """
        xy_combinations = []

        # split by "," first for multiple x/y combinations, then by "/" for x and y value
        for xy_coordinate in input_value.split(","):
            splitted = xy_coordinate.split("/")

            if len(splitted) == 2:
                xy_combinations.append(
                    {"x": int(splitted[0]), "y": int(splitted[1])})

        return xy_combinations


def calc_bounding_box_tiles(bbox):
    bbox_tiles = []
    for x_value in range(bbox['top_x'], bbox['bot_x'] + 1):
        for y_value in range(bbox['top_y'], bbox['bot_y'] + 1):
            (tile_top, tile_left) = num2deg(x_value, y_value)
            (tile_bottom, tile_right) = num2deg(x_value+1, y_value+1)
            if tile_left < -180:
                tile_left = -180
            if tile_left > 180:
                tile_left = 180
            if tile_right < -180:
                tile_right = -180
            if tile_right > 180:
                tile_right = 180
            if tile_top < -90:
                tile_top = -90
            if tile_top > 90:
                tile_top = 90
            if tile_bottom < -90:
                tile_bottom = -90
            if tile_bottom > 90:
                tile_bottom = 90
            bbox_tiles.append({'x': x_value, 'y': y_value, 'tile_left': tile_left,
                               'tile_top': tile_top, 'tile_right': tile_right,
                               'tile_bottom': tile_bottom})

    return bbox_tiles


def deg2num(lat_deg, lon_deg, zoom=8):
    """
    Convert on./lat. to tile numbers
    """
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def num2deg(xtile, ytile, zoom=8):
    """
    Convert tile numbers to lon./lat.
    """
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)
