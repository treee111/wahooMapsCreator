"""
functions and object for constants
"""
#!/usr/bin/python

# import official python packages
import sys
import os

# import custom python packages
from common_python import constants
from common_python import file_directory_functions as fd_fct


def get_region_of_country(county):
    """
    returns the region / continent of a given country
    """
    region = ''
    if county in constants.africa:
        region = 'africa'
    if county in constants.antarctica:
        region = 'antarctica'
    if county in constants.asia:
        region = 'asia'
    if county in constants.europe:
        region = 'europe'
    if county in constants.northamerica:
        region = 'north_america'
    if county in constants.oceania:
        region = 'oceania'
    if county in constants.southamerica:
        region = 'south_america'
    if county in constants.unitedstates:
        region = 'united_states'

    return region


def get_geofabrik_region_of_country(input_county):
    """
    returns the geofabrik region / continent of a given country
    the geofabrik region is sometimes written different than the get_region_of_country() region
    """
    # search for country match in geofabrik tables to determine region to use for map download
    c_translated = translate_country_input_to_geofabrik(input_county)

    region = ''
    if c_translated in constants.africa_geofabrik:
        region = 'africa'
    if c_translated in constants.antarctica_geofabrik:
        region = 'antarctica'
    if c_translated in constants.asia_geofabrik:
        region = 'asia'
    if c_translated in constants.australiaoceania_geofabrik:
        region = 'australia-oceania'
    if c_translated in constants.centralamerica_geofabrik:
        region = 'central-america'
    if c_translated in constants.europe_geofabrik:
        region = 'europe'
    if c_translated in constants.northamerica_geofabrik:
        region = 'north-america'
    if c_translated in constants.southamerica_geofabrik:
        region = 'south-america'
    if c_translated in constants.germany_subregions_geofabrik:
        region = 'europe\\germany'
    if c_translated in constants.noregion_geofabrik:
        region = 'no'
    if region == '':
        print(f'\n! No Geofabrik region match for country: {c_translated}')
        sys.exit()

    return region


def translate_country_input_to_geofabrik(county):
    """
    translates the given country to the geofabrik country
    the geofabrik country is sometimes written different
    """
    # search for user entered country name in translated (to geofabrik). if match continue with matched else continue with user entered country

    try:
        c_translated = constants.Translate_Country[f'{county}']
    except:
        c_translated = county

    return c_translated


def get_path_to_static_tile_json(country):
    """
    return the path to the static .json file with the files for the given country
    """
    return os.path.join(fd_fct.COMMON_DIR, 'json',
                        get_region_of_country(country), country + '.json')
