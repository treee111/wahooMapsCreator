"""
constants, functions and object for file-system operations
"""
#!/usr/bin/python

# import official python packages
import json
import os
from os.path import isfile, join
import subprocess
import sys
import zipfile
import logging
from pathlib import Path

# import custom python packages
import requests

log = logging.getLogger('main-logger')


def get_git_root():
    """
    get the root directory of the git repository
    """
    return subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                            stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')

# script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
# alternatives for ROOT_DIR: #os.getcwd() #getGitRoot()


# wahooMapsCreator directory
WAHOO_MC_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

WAHOO_MC_USER = os.path.join(str(Path.home()), 'wahooMapsCreator')

# PAR_DIR = os.path.abspath(os.path.join(os.path.join(
#     os.path.dirname(__file__), os.pardir), os.pardir))
COMMON_DIR = os.path.join(WAHOO_MC_DIR, 'resources')
USER_DL_DIR = os.path.join(WAHOO_MC_USER, '_download')
USER_OUTPUT_DIR = os.path.join(WAHOO_MC_USER, '_tiles')
MAPS_DIR = os.path.join(USER_DL_DIR, 'maps')
TOOLING_DIR = os.path.join(ROOT_DIR, 'tooling')
TOOLING_WIN_DIR = os.path.join(WAHOO_MC_DIR, 'tooling_win')
LAND_POLYGONS_PATH = os.path.join(
    USER_DL_DIR, 'land-polygons-split-4326', 'land_polygons.shp')
GEOFABRIK_PATH = os.path.join(USER_DL_DIR, 'geofabrik.json')


def unzip(source_filename, dest_dir):
    """
    unzip the given file into the given directory
    """
    with zipfile.ZipFile(source_filename) as zip_file:
        for member in zip_file.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                while True:
                    drive, word = os.path.splitdrive(word)
                    head, word = os.path.split(  # pylint: disable=unused-variable
                        word)
                    if not drive:
                        break
                if word in (os.curdir, os.pardir, ''):
                    continue
                path = os.path.join(path, word)
            if member.filename.split('/').pop():
                member.filename = member.filename.split('/').pop()
            zip_file.extract(member, path)


def initialize_work_directories():
    """
    Initialize work directories
    """

    # USER_DIR = os.path.join(str(Path.home()), 'gitcommon')

    os.makedirs(WAHOO_MC_USER, exist_ok=True)

    os.makedirs(USER_DL_DIR, exist_ok=True)
    os.makedirs(MAPS_DIR, exist_ok=True)
    os.makedirs(USER_OUTPUT_DIR, exist_ok=True)


def create_empty_directories(tiles_from_json):
    """
    create empty directory for the files
    """
    for tile in tiles_from_json:
        outdir = os.path.join(USER_OUTPUT_DIR, f'{tile["x"]}', f'{tile["y"]}')
        if not os.path.isdir(outdir):
            os.makedirs(outdir)


def read_json_file(json_file_path):
    """
    read the tiles from the given json file
    """

    log.debug('-' * 80)
    log.debug('# Read json file')

    with open(json_file_path, encoding="utf-8") as json_file:
        tiles_from_json = json.load(json_file)
        json_file.close()
    if tiles_from_json == '':
        log.error('! Json file could not be opened.')
        sys.exit()

    log.debug(
        '+ Use json file %s with %s tiles', json_file.name, len(tiles_from_json))
    log.debug('+ Read json file: OK')

    return tiles_from_json


def download_url_to_file(url, map_file_path):
    """
    download the content of a ULR to file
    """
    request_geofabrik = requests.get(url, allow_redirects=True, stream=True)
    if request_geofabrik.status_code != 200:
        log.error('! failed download URL: %s', url)
        sys.exit()

    # write content to file
    write_to_file(map_file_path, request_geofabrik)


def write_to_file(file_path, request):
    """
    write content of request into given file path
    """
    with open(file_path, mode='wb') as file_handle:
        for chunk in request.iter_content(chunk_size=1024*100):
            file_handle.write(chunk)


def get_folders_in_folder(folder):
    """
    return foldernames of given folder without path as list
    """
    onlyfolders = [f for f in os.listdir(
        folder) if not isfile(join(folder, f))]

    return onlyfolders


def get_files_in_folder(folder):
    """
    return filenames of given folder without path as list
    """
    onlyfiles = [f for f in os.listdir(folder) if isfile(join(folder, f))]

    return onlyfiles


def get_filenames_of_jsons_in_folder(folder):
    """
    return json-file filenames of given folder without path as list
    """
    json_files = []

    for file in get_files_in_folder(folder):
        if file.endswith('.json'):
            # filename = file.split('.')[0]
            filename = os.path.splitext(file)[0]
            json_files.extend([filename])

    return json_files
