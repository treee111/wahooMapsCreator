"""
functions and object for managing OSM maps
"""
#!/usr/bin/python
#pylint: skip-file

# import official python packages
import sys
import math
import logging
import geojson
from shapely.geometry import Polygon, shape

# import custom python packages
from wahoomc.constants import GEOFABRIK_PATH
from wahoomc.constants import special_regions, geofabrik_regions, block_download

log = logging.getLogger('main-logger')


class Geofabrik:
    """
    This is a Geofabrik processing class
    """

    def __init__(self, country):
        # input parameters
        self.wanted_map = country
        # replace spaces in self.wanted_map with geofabrik minuses
        self.wanted_map = self.wanted_map.replace(" ", "-")
        self.wanted_map = self.wanted_map.lower()

        self.tiles = []
        self.border_countries = {}
        self.country_name = ''

    def get_tiles_of_country(self):
        """
        Get the relevant tiles for a country
        """

        # Check if wanted_map is in the json file and if so get the polygon (shape)
        wanted_map_geom, wanted_url = geom(self.wanted_map)
        if not wanted_map_geom:
            # try to prepend us\ to the self.wanted_map
            wanted_map_geom, wanted_url = geom('us/'+self.wanted_map)
            if wanted_map_geom:
                self.wanted_map = 'us/'+self.wanted_map
            else:
                log.error(
                    'failed to find country or region %s in Geofabrik json file', self.wanted_map)
                sys.exit()

        # convert to shape (multipolygon)
        wanted_region = shape(wanted_map_geom)
        #print (f'shape = {wanted_region}')

        # get bounding box
        (bbox_left, bbox_bottom, bbox_right, bbox_top) = wanted_region.bounds

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

        # Build list of tiles from the bounding box
        bbox_tiles = []
        for x_value in range(top_x, bot_x + 1):
            for y_value in range(top_y, bot_y + 1):
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

        log.info('Searching for needed maps, this can take a while.')
        tiles_of_input = find_needed_countries(
            bbox_tiles, self.wanted_map, wanted_region)
        #print (f'Country= {country}')

        return tiles_of_input


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


def geom(wanted):
    """
    Get the Geofabrik outline of the desired country/region from the Geofabrik json file
    and the download url of the map.
    input parameter is the name of the desired country/region as use by Geofabric
    in their json file.
    """
    with open(GEOFABRIK_PATH, encoding='utf8') as file_handle:
        data = geojson.load(file_handle)
    file_handle.close()

    # loop through all entries in the json file to find the one we want
    for feature in data.features:
        props = feature.properties
        ident_no = props.get('id', '')
        if ident_no != wanted:
            continue
        #print (props.get('urls', ''))
        wurls = props.get('urls', '')
        return (feature.geometry, wurls.get('pbf', ''))
    return None, None


def find_geofbrik_parent(name, geofabrik_json):
    """
    Get the parent map/region of a region from the already loaded json data
    """
    for feature in geofabrik_json.features:
        props = feature.properties
        ident_no = props.get('id', '')
        if ident_no != name:
            continue
        return (props.get('parent', ''), props.get('id', ''))
    return None, None


def find_geofbrik_url(name, geofabrik_json):
    """
    Get the map download url from a region with the already loaded json data
    """
    for feature in geofabrik_json.features:
        props = feature.properties
        ident_no = props.get('id', '')
        if ident_no != name:
            continue
        #print (props.get('urls', ''))
        wurls = props.get('urls', '')
        return wurls.get('pbf', '')
    return None


def find_needed_countries(bbox_tiles, wanted_map, wanted_region_polygon):
    """
    Find the maps to download from Geofabrik for a given range of tiles
    arguments are
      - list of tiles of the desired region bounding box
      - name of desired region as used in Geofabrik json file
      - polygon of desired region as present in the Geofabrik json file
    """
    output = []

    with open(GEOFABRIK_PATH, encoding='utf8') as file_handle:
        geofabrik_json_data = geojson.load(file_handle)
    file_handle.close()

    # itterate through tiles and find Geofabrik regions that are in the tiles
    counter = 1
    for tile in bbox_tiles:
        # Do progress indicator every 50 tiles
        if counter % 50 == 0:
            log.info(
                'Processing tile %s of %s', counter, len(bbox_tiles)+1)
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
        for regions in geofabrik_json_data.features:
            props = regions.properties
            parent = props.get('parent', '')
            regionname = props.get('id', '')
            rurls = props.get('urls', '')
            rurl = rurls.get('pbf', '')
            rgeom = regions.geometry
            rshape = shape(rgeom)

            #print (f'Processing region: {regionname}')

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
                                parent, child = find_geofbrik_parent(
                                    parent, geofabrik_json_data)
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
                                    find_geofbrik_url(parent, geofabrik_json_data))
                                #parent_added = 1
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
                        #print (f'\t{regionname} is a subset of {wanted_map}, discard it')
                        continue
                    # check if rshape is a superset of desired region. if so discard it
                    if rshape.contains(wanted_region_polygon):
                        #print (f'\t{regionname} is a superset of {wanted_map}, discard it')
                        # if regionname not in must_download_maps:
                        #    must_download_maps.append (regionname)
                        #    must_download_urls.append (rurl)
                        #    parent_added = 1
                        continue
                    # Check if rshape is a part of the tile
                    if rshape.intersects(poly):
                        #print(f'\tintersecting tile: {regionname} tile={tile}')
                        if regionname not in must_download_maps:
                            must_download_maps.append(regionname)
                            must_download_urls.append(rurl)

        # If this tile contains the desired region, add it to the output
        #print (f'map= {wanted_map}\tmust_download= {must_download_maps}\tparent_added= {parent_added}\tforce_added= {force_added}')
        if wanted_map in must_download_maps or parent_added == 1 or force_added == 1:
            # first replace any forward slashes with underscores (us/texas to us_texas)
            must_download_maps = [sub.replace(
                '/', '_') for sub in must_download_maps]
            output.append({'x': tile['x'], 'y': tile['y'], 'left': tile['tile_left'], 'top': tile['tile_top'],
                          'right': tile['tile_right'], 'bottom': tile['tile_bottom'], 'countries': must_download_maps, 'urls': must_download_urls})
    return output
