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
    read_json_file_generic, delete_o5m_pbf_files_in_folder, copy_or_move_files_and_folder
from wahoomc.constants_functions import get_tooling_win_path, get_absolute_dir_user_or_repo
from wahoomc.downloader import get_latest_pypi_version

from wahoomc.constants import GEOFABRIK_PATH, USER_WAHOO_MC
from wahoomc.constants import USER_DL_DIR
from wahoomc.constants import USER_MAPS_DIR
from wahoomc.constants import USER_OUTPUT_DIR
from wahoomc.constants import USER_CONFIG_DIR
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
    os.makedirs(USER_CONFIG_DIR, exist_ok=True)


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


def adjustments_due_to_breaking_changes():
    """
    copy files from download- and output- directory of earlier version to the new folders
    """
    version_last_run = read_version_last_run()

    # file-names of filteres country files were uniformed in #153.
    # due to that old files are sometimes no longer accessed and files in the _tiles folder are deleted here.
    if version_last_run is None or \
            pkg_resources.parse_version(VERSION) <= pkg_resources.parse_version('2.0.2'):
        log.info(
            'Last run was with version %s, deleting files of %s directory due to breaking changes.', version_last_run, USER_OUTPUT_DIR)
        delete_o5m_pbf_files_in_folder(USER_OUTPUT_DIR)

    # file-names of downloaded .osm.pbf raw mapfiles was adjusted in #182 to focus on geofabrik naming
    # other existing files may therefor not be accessed anymore in the future and therefore deleted
    if version_last_run is None or \
            pkg_resources.parse_version(VERSION) < pkg_resources.parse_version('4.0.0a0'):
        log.info(
            'Last run was with version %s, deleting files of %s directory due to breaking changes.', version_last_run, USER_MAPS_DIR)
        delete_o5m_pbf_files_in_folder(USER_MAPS_DIR)
        log.info(
            'Last run was with version %s, deleting files of %s directory due to breaking changes.', version_last_run, USER_OUTPUT_DIR)
        delete_o5m_pbf_files_in_folder(USER_OUTPUT_DIR)


def check_installation_of_required_programs():
    """
    check if required programs are installed
    """
    text_to_docu = "\nPlease refer to the Quickstart Guide of wahooMapsCreator for instructions:\n- https://github.com/treee111/wahooMapsCreator/blob/develop/docs/QUICKSTART_ANACONDA.md \
                    \nor create an issue:\n- https://github.com/treee111/wahooMapsCreator/issues"

    if not is_program_installed("java"):
        sys.exit(
            f"Java is not installed. {text_to_docu}")

    if not os.path.isfile(GEOFABRIK_PATH):
        sys.exit('Geofabrik file is not downloaded. Please create an issue:\n- https://github.com/treee111/wahooMapsCreator/issues"')

    if platform.system() == "Windows":
        if not os.path.exists(get_tooling_win_path(
                os.path.join('Osmosis', 'bin', 'osmosis.bat'), in_user_dir=True)):
            sys.exit(
                f"Osmosis is not available. {text_to_docu}")

        if not os.path.exists(get_tooling_win_path('osmconvert.exe')):
            sys.exit(
                f"osmconvert is not available. {text_to_docu}")

        if not os.path.exists(get_tooling_win_path('osmfilter.exe', in_user_dir=True)):
            sys.exit(
                f"osmfilter is not available. {text_to_docu}")

        if not os.path.exists(get_tooling_win_path('7za.exe')):
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


def check_installation_of_programs_credentials_for_contour_lines():
    """
    check if additionals programs are installed
    """
    text_to_docu = "\nYou have choosen to process contour lines. That needs additional programs. \
                    \nPlease refer to the Quickstart Guide of wahooMapsCreator for instructions:\n- https://github.com/treee111/wahooMapsCreator/blob/develop/docs/QUICKSTART_ANACONDA.md#additional-programs-for-generating-contour-lines \
                    \nor create an issue:\n- https://github.com/treee111/wahooMapsCreator/issues"

    if not is_program_installed("phyghtmap"):
        sys.exit(
            f"phyghtmap is not installed. {text_to_docu}")

    username, password = read_earthexplorer_credentials()

    if not username or not password:
        username, password = ask_for_and_write_earthexplorer_credentials()


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


def write_config_file(config_to_write=''):
    """
    Write config file of wahoomc to root directory
    incorporate given content to existing file
    """
    # Data to be written
    default_config = {
        "version_last_run": VERSION
    }

    # if no config to write is given, write default config - normally at the end of main()
    if not config_to_write:
        config_to_write = default_config

    actual_content = read_json_file_generic(config_file_path)

    for key, value in config_to_write.items():
        # overwrite value or insert new item
        actual_content[key] = value

    # write changed content to disc
    write_json_file_generic(config_file_path, actual_content)


def read_version_last_run():
    """
    Read the version of wahoomc's last run
    by reading json and access version attribute, if not set, give None
    """
    try:
        version_last_run = read_json_file_generic(config_file_path)[
            "version_last_run"]
    except KeyError:
        version_last_run = None

    return version_last_run


def ask_for_and_write_earthexplorer_credentials():
    """
    Ask user for credentials for https://ers.cr.usgs.gov and save in the config file
    """
    log.warning(
        'No saved credentials found for https://ers.cr.usgs.gov. Please register and enter your credentials.')
    username = input('https://ers.cr.usgs.gov username:')
    password = input('https://ers.cr.usgs.gov password:')

    credentials_to_write = {
        'earthexplorer-user': username, 'earthexplorer-password': password}

    write_config_file(credentials_to_write)

    return username, password


def read_earthexplorer_credentials():
    """
    Read the version of wahoomc's last run
    by reading json and access version attribute, if not set, give None
    """
    try:
        username = read_json_file_generic(config_file_path)[
            "earthexplorer-user"]
        password = read_json_file_generic(config_file_path)[
            "earthexplorer-password"]
    except KeyError:
        username = None
        password = None

    return username, password


def copy_jsons_from_repo_to_user(folder, file=''):
    """
    copies files from wahoomc repo/package to the user-directory
    """
    absolute_paths = get_absolute_dir_user_or_repo(folder, file)

    log.debug('# Copy "%s" files from repo to directory if not existing: %s',
              folder, absolute_paths[0])

    # copy files of wahoomc package directory to user directory
    copy_or_move_files_and_folder(
        absolute_paths[1], absolute_paths[0], delete_from_dir=False)

    log.info('# Copy "%s" files from wahoomc installation to directory if not existing: %s : OK',
             folder, absolute_paths[0])


def check_installed_version_against_latest_pypi():
    """
    get latest wahoomc version available on PyPI and compare with locally installed version
    """
    # get latest wahoomc version available on PyPI
    latest_version = get_latest_pypi_version()

    # compare installed version against latest and issue a info if a new version is available
    if latest_version \
            and pkg_resources.parse_version(VERSION) < pkg_resources.parse_version(latest_version):
        log.info('\n\nUpdate available! \
                \nA new version of wahoomc is available: "%s". You have installed version "%s". \
                \nUpgrade wahoomc with "pip install wahoomc --upgrade". \
                \nRelease notes are here: https://github.com/treee111/wahooMapsCreator/releases/latest. \
                \n',
                 latest_version, VERSION)
