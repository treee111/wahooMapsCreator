#!/usr/bin/python

# import official python packages
import os
import subprocess
import zipfile


def getGitRoot():
    return subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')

# script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir)) #os.getcwd() #getGitRoot()
COMMON_DIR = os.path.join(ROOT_DIR, 'common_resources')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output')
MAPS_DIR = os.path.join(COMMON_DIR, 'maps')
LAND_POLYGONS_PATH = os.path.join(COMMON_DIR, 'land-polygons-split-4326', 'land_polygons.shp')


def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
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
            if(member.filename.split('/').pop()): member.filename = member.filename.split('/').pop()
            zf.extract(member, path)


def createEmptyDirectories(tilesFromJson):
    for tile in tilesFromJson:
        outdir = os.path.join(OUTPUT_DIR, f'{tile["x"]}', f'{tile["y"]}')
        if not os.path.isdir(outdir):
            os.makedirs(outdir)