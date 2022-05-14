"""
constants, functions and object for file-system operations
"""
#!/usr/bin/python

# import official python packages
import os
import logging

# import custom python packages
from wahoomc import file_directory_functions as fd_fct
from wahoomc import constants

log = logging.getLogger('main-logger')


def initialize_work_directories():
    """
    Initialize work directories
    """
    os.makedirs(constants.USER_WAHOO_MC, exist_ok=True)
    os.makedirs(constants.USER_DL_DIR, exist_ok=True)
    os.makedirs(constants.USER_MAPS_DIR, exist_ok=True)
    os.makedirs(constants.USER_OUTPUT_DIR, exist_ok=True)


def move_old_content_into_new_dirs():
    """
    copy files from download- and output- directory of earlier version to the new folders
    delete directory from earlier versions afterwards

    having folder on the same level as the wahooMapsCreator was introduces in release v1.1.0 with PR #93.
    This coding is only valid/needed when using the cloned version or .zip version.
    If working with a installed version via PyPI, nothing will be done because folders to copy do not exist
    """
    fd_fct.move_content('wahooMapsCreator_download', constants.USER_DL_DIR)
    fd_fct.move_content('wahooMapsCreator_output', constants.USER_OUTPUT_DIR)
