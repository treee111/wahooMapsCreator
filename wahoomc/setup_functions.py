"""
constants, functions and object for file-system operations
"""
#!/usr/bin/python

# import official python packages
import os
import logging
import platform
import shutil
from pathlib import Path
import sys

# import custom python packages
from wahoomc.file_directory_functions import move_content
from wahoomc.constants_functions import get_tooling_win_path
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
    move_content('wahooMapsCreator_download', constants.USER_DL_DIR)
    move_content('wahooMapsCreator_output', constants.USER_OUTPUT_DIR)


def check_installation_of_required_programs():
    """
    check if required programs are installed
    """
    text_to_docu = "Please refer to the Quickstart Guide of wahooMapsCreator for instructions:\n https://github.com/treee111/wahooMapsCreator/blob/develop/docs/QUICKSTART_ANACONDA.md \
                    or create an issue:\n https://github.com/treee111/wahooMapsCreator/issues"

    if not is_program_installed("java"):
        sys.exit(
            f"Java is not installed. {text_to_docu}")

    if platform.system() == "Windows":
        if not os.path.exists(get_tooling_win_path(
                ['Osmosis', 'bin', 'osmosis.bat'])):
            sys.exit(
                f"Osmosis is not available. {text_to_docu}")

        if not os.path.exists(get_tooling_win_path(['osmconvert.exe'])):
            sys.exit(
                f"osmconvert is not available. {text_to_docu}")

        if not os.path.exists(get_tooling_win_path(['osmfilter.exe'])):
            sys.exit(
                f"osmfilter is not available. {text_to_docu}")

        if not os.path.exists(get_tooling_win_path(['7za.exe'])):
            sys.exit(
                f"7za is not available. {text_to_docu}")

    else:
        if not is_program_installed("osmium"):
            sys.exit(
                f"osmium-tool is not installed. {text_to_docu}")

        if not is_program_installed("osmosis"):
            sys.exit(
                f"Osmosis is not installed. {text_to_docu}")

        if not is_map_writer_plugin_installed():
            sys.exit(
                f"mapsforge-map-writer plugin is not installed. {text_to_docu}")


def is_program_installed(program):
    """
    check if a given program is installed
    """
    if shutil.which(program) is not None:
        return True

    return False


def is_map_writer_plugin_installed():
    """
    tests, if the mapwriter plugin is in the correct location

    Example filename for the map-writer-plugin
    mapsforge-map-writer-master-20210527.154736-408-jar-with-dependencies.jar
    """
    map_writer_path = os.path.join(
        str(Path.home()), '.openstreetmap', 'osmosis', 'plugins')

    for file in os.listdir(map_writer_path):
        if "mapsforge-map-writer" in file:
            return True

    return False
