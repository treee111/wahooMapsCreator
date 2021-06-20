#!/usr/bin/python

# import official python packages
import json
import os
import subprocess
import sys
import zipfile



def get_git_root():
    return subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
     stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')

# script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
# alternatives for ROOT_DIR: #os.getcwd() #getGitRoot()

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir))
COMMON_DIR = os.path.join(ROOT_DIR, 'common_resources')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output')
MAPS_DIR = os.path.join(COMMON_DIR, 'maps')
LAND_POLYGONS_PATH = os.path.join(COMMON_DIR, 'land-polygons-split-4326', 'land_polygons.shp')

def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zip_file:
        for member in zip_file.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                while True:
                    drive, word = os.path.splitdrive(word)
                    head, word = os.path.split(word)
                    if not drive:
                        break
                if word in (os.curdir, os.pardir, ''):
                    continue
                path = os.path.join(path, word)
            if(member.filename.split('/').pop()):
                member.filename = member.filename.split('/').pop()
            zip_file.extract(member, path)


def create_empty_directories(tiles_from_json):
    for tile in tiles_from_json:
        outdir = os.path.join(OUTPUT_DIR, f'{tile["x"]}', f'{tile["y"]}')
        if not os.path.isdir(outdir):
            os.makedirs(outdir)


def read_json_file(input_argument1, region):
    print('\n# Read json file')

    # option 1: have a .json file as input parameter
    if os.path.isfile(input_argument1):
        json_file_path = input_argument1
    # option 2: input a country as parameter, e.g. germany
    else:
        json_file_path = os.path.join (COMMON_DIR,
            'json', region, input_argument1 + '.json')

    with open(json_file_path) as json_file:
        tiles_from_json = json.load(json_file)
        json_file.close()
    if tiles_from_json == '' :
        print ('! Json file could not be opened.')
        sys.exit()

    # logging
    print(f'+ Use json file {json_file.name} with {len(tiles_from_json)} tiles')
    print('# Read json file: OK')

    return tiles_from_json

class FileDir:
    "This is the class to check and download maps / artifacts"

    def __init__(self, inputFile, input_region):
        self.input_argument1 = inputFile
        self.region = input_region

        self.tiles_from_json = []
