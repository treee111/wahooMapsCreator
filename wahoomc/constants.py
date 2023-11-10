"""
constants
"""
#!/usr/bin/python

import os
from pathlib import Path

# User
USER_DIR = str(Path.home())
USER_WAHOO_MC = os.path.join(str(Path.home()), 'wahooMapsCreatorData')
USER_DL_DIR = os.path.join(USER_WAHOO_MC, '_download')
USER_MAPS_DIR = os.path.join(USER_DL_DIR, 'maps')
LAND_POLYGONS_PATH = os.path.join(
    USER_DL_DIR, 'land-polygons-split-4326', 'land_polygons.shp')
GEOFABRIK_PATH = os.path.join(USER_DL_DIR, 'geofabrik.json')
USER_OUTPUT_DIR = os.path.join(USER_WAHOO_MC, '_tiles')
USER_CONFIG_DIR = os.path.join(USER_WAHOO_MC, '_config')
USER_TOOLING_WIN_DIR = os.path.join(USER_DL_DIR, 'tooling_win')
OSMOSIS_WIN_FILE_PATH = os.path.join(
    USER_TOOLING_WIN_DIR, 'Osmosis', 'bin', 'osmosis.bat')

# Python Package - wahooMapsCreator directory
WAHOO_MC_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(WAHOO_MC_DIR, 'resources')
TOOLING_WIN_DIR = os.path.join(WAHOO_MC_DIR, 'tooling_win')
# location of repo / python installation - not used
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
VERSION = '4.1.1a1'


block_download = ['dach', 'alps', 'britain-and-ireland', 'south-africa-and-lesotho',
                  'us-midwest', 'us-northeast', 'us-pacific', 'us-south', 'us-west']

# Special_regions like (former) colonies where the map of the wanted region is not present in the map of the parent country.
# example Guadeloupe, it's Geofabrik parent country is France but Guadeloupe is not located within the region covered by the map of France.
special_regions = ['guadeloupe', 'guyane', 'martinique', 'mayotte', 'reunion']
