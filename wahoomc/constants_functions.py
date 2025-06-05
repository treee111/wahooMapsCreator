"""
functions and object for constants
"""
#!/usr/bin/python

# import official python packages
import logging
import os
import struct

# import custom python packages
from wahoomc.constants import RESOURCES_DIR
from wahoomc.constants import TOOLING_WIN_DIR
from wahoomc.constants import USER_CONFIG_DIR
from wahoomc.constants import USER_TOOLING_WIN_DIR
from wahoomc.file_directory_functions import read_json_file_generic

log = logging.getLogger('main-logger')


class TagsToKeepNotFoundError(Exception):
    """Raised when the specified tags to keep .json file does not exist"""


def translate_tags_to_keep(name_tags=False, osmium=True, use_repo=False):
    """
    translates the given tags to format of the operating system.
    """
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
        to_append = transl_tag_value(osmium, tag, value)

        tags_modif.append(to_append)

    if not osmium:
        tags_modif = ' '.join(tags_modif)

    return tags_modif


def transl_tag_value(osmium, tag, value):
    """
    translates one tag with value(s) to a "common" format
    """
    if isinstance(value, list):
        separator = ', ' if osmium else ' ='
        for iteration, sing_val in enumerate(value):
            if iteration == 0:
                to_append = f'{tag}={sing_val}'
            else:
                to_append = f'{to_append}{separator}{sing_val}'
    elif value:
        to_append = f'{tag}={value}'
    else:
        to_append = tag if osmium else f'{tag}='

    return to_append


def get_tooling_win_path(path_in_tooling_win, in_user_dir=False):
    """
    return path to a tooling in the tooling_win directory and the given path
    OR from the user tooling_win directory
    """
    if in_user_dir:
        tooling_dir = USER_TOOLING_WIN_DIR
    else:
        tooling_dir = TOOLING_WIN_DIR

    # special for osmconvert: handle 32 and 64 bit here
    if path_in_tooling_win in ('osmconvert', 'osmconvert.exe'):
        if 8 * struct.calcsize("P") == 32:
            return os.path.join(tooling_dir, path_in_tooling_win)
        # 64 bit: replace with 64 in the end
        return os.path.join(tooling_dir, path_in_tooling_win.replace("osmconvert", "osmconvert64-0.8.8p"))

    # all other "toolings": concatenate with win tooling dir
    return os.path.join(tooling_dir, path_in_tooling_win)

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
            USER_CONFIG_DIR, folder, file))
        absolute_paths.append(os.path.join(
            RESOURCES_DIR, folder, file))
    else:
        absolute_paths.append(os.path.join(USER_CONFIG_DIR, folder))
        absolute_paths.append(os.path.join(
            RESOURCES_DIR, folder))

    return absolute_paths
