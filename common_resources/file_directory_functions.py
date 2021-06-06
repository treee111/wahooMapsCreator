#!/usr/bin/python

# import official python packages
import os
import subprocess


def getGitRoot():
    return subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')

ROOT_PATH = getGitRoot()
COMMON_PATH = os.path.join(ROOT_PATH, 'common_resources')
OUT_PATH = os.path.join(ROOT_PATH, 'output')
MAP_PATH = os.path.join(COMMON_PATH, 'maps')
land_polygons_file = os.path.join(COMMON_PATH, 'land-polygons-split-4326/land_polygons.shp')