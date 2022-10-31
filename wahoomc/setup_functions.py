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
import pkg_resources

# import custom python packages
from wahoomc.file_directory_functions import move_content, write_json_file_generic, \
    read_json_file_generic, delete_o5m_pbf_files_in_folder
from wahoomc.constants_functions import get_tooling_win_path

from wahoomc.constants import USER_WAHOO_MC
from wahoomc.constants import USER_DL_DIR
from wahoomc.constants import USER_MAPS_DIR
from wahoomc.constants import USER_OUTPUT_DIR
from wahoomc.constants import VERSION

log = logging.getLogger('main-logger')

config_file_path = os.path.join(USER_WAHOO_MC, ".config.json")


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
    # create directories first because initialize_work_directories is now called later
    os.makedirs(USER_DL_DIR, exist_ok=True)
    os.makedirs(USER_OUTPUT_DIR, exist_ok=True)

    move_content('wahooMapsCreator_download', USER_DL_DIR)
    move_content('wahooMapsCreator_output', USER_OUTPUT_DIR)


def adjustments_due_to_breaking_changes():
    """
    copy files from download- and output- directory of earlier version to the new folders
    """
    version_last_run = read_version_last_run()

    # file-names of filteres country files were uniformed in #153.
    # due to that old files are sometimes no longer accessed and files in the _tiles folder are deleted here.
    if version_last_run is None or \
            pkg_resources.parse_version(VERSION) > pkg_resources.parse_version('2.0.2'):
        log.info(
            'Last run was with version %s, deleting files of %s directory due to breaking changes.', version_last_run, USER_OUTPUT_DIR)
        delete_o5m_pbf_files_in_folder(USER_OUTPUT_DIR)

    # version 1.1.0 moved the directories with "processing" files out of the repo folder due to the publishing via PyPI
    # old files are moved to the new structure. Can be deleted soon (in version 3.0.x)
    if version_last_run is None or \
            pkg_resources.parse_version(VERSION) < pkg_resources.parse_version('1.1.0'):
        log.info(
            'Last run was with version %s, moving content to new directories due to breaking changes.', version_last_run)
        move_old_content_into_new_dirs()


def check_installation_of_required_programs():
    """
    check if required programs are installed
    """
    text_to_docu = "\nPlease refer to the Quickstart Guide of wahooMapsCreator for instructions:\n- https://github.com/treee111/wahooMapsCreator/blob/develop/docs/QUICKSTART_ANACONDA.md \
                    \nor create an issue:\n- https://github.com/treee111/wahooMapsCreator/issues"

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
    downloaded on 01.10.2022: mapsforge-map-writer-0.18.0-jar-with-dependencies.jar
    """
    map_writer_path = os.path.join(
        str(Path.home()), '.openstreetmap', 'osmosis', 'plugins')

    # test if the file is there
    try:
        for file in os.listdir(map_writer_path):
            if "mapsforge-map-writer" in file:
                return True
    # if there is no file in the plugins directory
    except FileNotFoundError:
        pass

    return False


def write_config_file():
    """
    Write config file of wahoomc to root directory
    """
    # Data to be written
    configuration = {
        "version_last_run": VERSION
    }

    write_json_file_generic(config_file_path, configuration)


def read_version_last_run():
    """
    Read the version of wahoomc's last run
    by reading json and access version attribute, if not set, give None
    """
    try:
        version_last_run = read_json_file_generic(config_file_path)[
            "version_last_run"]
    except (FileNotFoundError, KeyError):
        version_last_run = None

    return version_last_run
