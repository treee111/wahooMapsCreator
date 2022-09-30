"""
constants, functions and object for file-system operations
"""
#!/usr/bin/python

# import official python packages
import os
import logging

# import custom python packages
from wahoomc.file_directory_functions import move_content
from wahoomc.constants import USER_WAHOO_MC
from wahoomc.constants import USER_DL_DIR
from wahoomc.constants import USER_MAPS_DIR
from wahoomc.constants import USER_OUTPUT_DIR

log = logging.getLogger('main-logger')


def initialize_work_directories():
    """
    Initialize work directories
    """
    os.makedirs(USER_WAHOO_MC, exist_ok=True)
    os.makedirs(USER_DL_DIR, exist_ok=True)
    os.makedirs(USER_MAPS_DIR, exist_ok=True)
    os.makedirs(USER_OUTPUT_DIR, exist_ok=True)


def move_old_content_into_new_dirs():
    """
    copy files from download- and output- directory of earlier version to the new folders
    delete directory from earlier versions afterwards

    having folder on the same level as the wahooMapsCreator was introduces in release v1.1.0 with PR #93.
    This coding is only valid/needed when using the cloned version or .zip version.
    If working with a installed version via PyPI, nothing will be done because folders to copy do not exist
    """
    move_content('wahooMapsCreator_download', USER_DL_DIR)
    move_content('wahooMapsCreator_output', USER_OUTPUT_DIR)
