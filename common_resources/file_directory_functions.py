#!/usr/bin/python

# import official python packages
import os
import subprocess


def getGitRoot():
    return subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')

# script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py

ROOT_DIR = os.getcwd() #getGitRoot()
COMMON_DIR = os.path.join(ROOT_DIR, 'common_resources')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output')
MAPS_DIR = os.path.join(COMMON_DIR, 'maps')
LAND_POLYGONS_PATH = os.path.join(COMMON_DIR, 'land-polygons-split-4326/land_polygons.shp')