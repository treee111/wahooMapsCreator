"""
functions and object for constants
"""
#!/usr/bin/python

# import official python packages
import sys
import logging
import os

# import custom python packages
from wahoomc import constants
from wahoomc.constants import RESOURCES_DIR
from wahoomc.constants import TOOLING_WIN_DIR
from wahoomc.constants import USER_WAHOO_MC
from wahoomc.file_directory_functions import read_json_file_generic

log = logging.getLogger('main-logger')


class TagWahooXmlNotFoundError(Exception):
    """Raised when the specified tag-wahoo xml file does not exist"""


class TagsToKeepNotFoundError(Exception):
    """Raised when the specified tags to keep .json file does not exist"""


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
    if c_translated in constants.northamerica_us_geofabrik:
        region = 'north-america/us'
    if c_translated in constants.southamerica_geofabrik:
        region = 'south-america'
    if c_translated in constants.germany_subregions_geofabrik:
        region = 'europe\\germany'
    if c_translated in constants.noregion_geofabrik:
        region = 'no'
    if region == '':
        log.error('! No Geofabrik region match for country: %s', c_translated)
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
    except KeyError:
        c_translated = county

    return c_translated


def translate_tags_to_keep(name_tags=False, sys_platform='', use_repo=False):
    """
    translates the given tags to format of the operating system.
    """

    if sys_platform == "Windows":
        separator = ' ='
    else:
        separator = ', '

    tags_modif = []

    # read tags-to-keep .json from user-dir in favor of python installation
    # evaluate path first: user-dir in favor of PyPI installation
    if not use_repo:
        for path in get_absolute_dir_user_or_repo('', file='tags-to-keep.json'):
            if os.path.exists(path):
                break
    # force using file from repo - used in unittests for equal output
    else:
        path = get_absolute_dir_user_or_repo(
            '', file='tags-to-keep.json')[1]

    # read the tags from the evaluated path above
    tags_from_json = read_json_file_generic(path)

    if not tags_from_json:
        raise TagsToKeepNotFoundError

    if not name_tags:
        universal_tags = tags_from_json['TAGS_TO_KEEP_UNIVERSAL']
    else:
        universal_tags = tags_from_json['NAME_TAGS_TO_KEEP_UNIVERSAL']

    for tag, value in universal_tags.items():
        to_append = transl_tag_value(sys_platform, separator, tag, value)

        tags_modif.append(to_append)

    if sys_platform == "Windows":
        tags_modif = ' '.join(tags_modif)

    return tags_modif


def get_path_to_static_tile_json(country):
    """
    return the path to the static .json file with the files for the given country
    """
    return os.path.join(RESOURCES_DIR, 'json',
                        get_region_of_country(country), country + '.json')


def transl_tag_value(sys_platform, separator, tag, value):
    """
    translates one tag with value(s) to a "common" format
    """
    if isinstance(value, list):
        for iteration, sing_val in enumerate(value):
            if iteration == 0:
                to_append = f'{tag}={sing_val}'
            else:
                to_append = f'{to_append}{separator}{sing_val}'
    elif value:
        to_append = f'{tag}={value}'
    else:
        if sys_platform == "Windows":
            to_append = f'{tag}='
        else:
            to_append = tag

    return to_append


def get_tooling_win_path(path_in_tooling_win):
    """
    return path to a tooling in the tooling_win directory and the given path
    """
    return os.path.join(TOOLING_WIN_DIR, *path_in_tooling_win)


def get_tag_wahoo_xml_path(tag_wahoo_xml):
    """
    return path to tag-wahoo xml file if the file exists
    - from the user directory "USER_WAHOO_MC/_config/tag_wahoo_adjusted/tag_wahoo_xml"
    - 2ndly from the PyPI installation: "RESOURCES_DIR/tag_wahoo_adjusted/tag_wahoo_xml"
    """

    for path in get_absolute_dir_user_or_repo("tag_wahoo_adjusted", tag_wahoo_xml):
        if os.path.exists(path):
            return path

    raise TagWahooXmlNotFoundError


def get_absolute_dir_user_or_repo(folder, file=''):
    """
    return the absolute path to the folder (and file) in this priorization
    1. user dir
    2. wahoomc package dir

    Priorization is important later on because user- should always be used in favor of repo-dir!
    """
    absolute_paths = []
    if file:
        absolute_paths.append(os.path.join(
            USER_WAHOO_MC, '_config', folder, file))
        absolute_paths.append(os.path.join(
            RESOURCES_DIR, folder, file))
    else:
        absolute_paths.append(os.path.join(USER_WAHOO_MC, folder))
        absolute_paths.append(os.path.join(
            RESOURCES_DIR, '_config', folder))

    return absolute_paths
