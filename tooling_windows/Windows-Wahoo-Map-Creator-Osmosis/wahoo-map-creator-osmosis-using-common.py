#!/usr/bin/python
#-*- coding:utf-8 -*-

import getopt
import glob
import json
import multiprocessing
import os
import os.path
import requests
import subprocess
import sys
import time

# ToDo: This might not work - Properly import in Windows!
# import custom python packages
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from common_resources import file_directory_functions
from common_resources import osm_maps_functions

########### Configurable Parameters

# Maximum age of source maps or land shape files before they are redownloaded
Max_Days_Old = 14

# Force (re)processing of source maps and the land shape file
# If 0 use Max_Days_Old to check for expired maps
# If 1 force redownloading/processing of maps and landshape 
Force_Processing = 0

# Save uncompressed maps for Cruiser
Save_Cruiser = 0

# Number of threads to use in the mapwriter plug-in
threads = str(multiprocessing.cpu_count() - 1)
if int(threads) < 1:
    threads = 1
# Or set it manually to:
#threads = 1
#print(f'threads = {threads}/n')

# Number of workers for the Osmosis read binary fast function
workers = '1'

########### End of Configurable Parameters

CurDir = os.getcwd() # Current Directory

MAP_PATH = os.path.join (CurDir, 'Maps')
OUT_PATH = os.path.join (CurDir, 'Output')
land_polygons_file = os.path.join (CurDir, 'land-polygons-split-4326', 'land_polygons.shp')
url = ''

# Tags to keep
filtered_tags = 'access= admin_level= aerialway= aeroway= barrier= boundary= bridge= highway= natural= oneway= place= railway= tracktype= tunnel= waterway='



if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} Country name part of a .json file.')
    sys.exit()

region = osm_maps_functions.getRegionOfCountry(sys.argv[1])
if region == '' :
    print ('Invalid country name.')
    sys.exit()

print('\n\n# read json file')
with open(os.path.join ('json', region, sys.argv[1] + '.json')) as f:
    country = json.load(f)
f.close()
if country == '' :
    print ('json file could not be opened.')
    sys.exit()

# Check for expired land polygons file and download, if too old
osm_maps_functions.checkAndDownloadLandPoligonsFile(Max_Days_Old, Force_Processing)

if not os.path.exists(land_polygons_file) or not os.path.isfile(land_polygons_file) or Force_Processing == 1:
    print('# Downloading land polygons file')
    url = 'https://osmdata.openstreetmap.de/download/land-polygons-split-4326.zip'
    r = requests.get(url, allow_redirects=True, stream = True)
    if r.status_code != 200:
        print(f'failed to find or download land polygons file')
        sys.exit()
    Download=open(os.path.join (CurDir, 'land-polygons-split-4326.zip'), 'wb')
    for chunk in r.iter_content(chunk_size=1024*100):
        Download.write(chunk)
    Download.close()
    # unpack it
    cmd = ['7za', 'x', '-y', os.path.join (CurDir, 'land-polygons-split-4326.zip')]
    #print(cmd)
    result = subprocess.run(cmd)
    os.remove(os.path.join (CurDir, 'land-polygons-split-4326.zip'))
    if result.returncode != 0:
        print(f'Error unpacking land polygons file')
        sys.exit()

print('\n\n# check countries .osm.pbf files')
# Build list of countries needed
border_countries = {}
for tile in country:
    for c in tile['countries']:
        if c not in border_countries:
            border_countries[c] = {'map_file':c}

print (f'{border_countries}')
time.sleep(60)

# Check for expired maps and delete them
print(f'# Checking for old maps and remove them')
now = time.time()
To_Old = now - 60 * 60 * 24 * Max_Days_Old
for c in border_countries:
    map_files = glob.glob(f'{MAP_PATH}/{c}*.osm.pbf')
    if len(map_files) != 1:
        map_files = glob.glob(f'{MAP_PATH}/**/{c}*.osm.pbf')
    if len(map_files) == 1 and os.path.isfile(map_files[0]):
        FileCreation = os.path.getctime(map_files[0])
        if FileCreation < To_Old or Force_Processing == 1:
            print (f'# Deleting old map of {c}')
            os.remove(map_files[0])
            Force_Processing = 1

print('deleted files')
time.sleep(60)

border_countries = {}
for tile in country:
    outdir = os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}')
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

# search for user entered country name in translated (to geofabrik). if match continue with matched else continue with user entered country
# search for country match in geofabrik tables to determine region to use for map download 
    for c in tile['countries']:
        if c not in border_countries:
            print(f'# Checking mapfile for {c}')
            map_files = glob.glob(f'{MAP_PATH}/{c}*.osm.pbf')
            if len(map_files) != 1:
                map_files = glob.glob(f'{MAP_PATH}/**/{c}*.osm.pbf')
            if len(map_files) != 1 or not os.path.isfile(map_files[0]):
                try:
                    c_translated = Translate_Country[f'{c}']
                except:
                    c_translated = c
                region = ''
                if c_translated in africa_geofabrik :
                    region = 'africa'
                if c_translated in antarctica_geofabrik :
                    region = 'antarctica'
                if c_translated in asia_geofabrik :
                    region = 'asia'
                if c_translated in australiaoceania_geofabrik :
                    region = 'australia-oceania'
                if c_translated in centralamerica_geofabrik :
                    region = 'central-america'
                if c_translated in europe_geofabrik :
                    region = 'europe'
                if c_translated in northamerica_geofabrik :
                    region = 'north-america'
                if c_translated in southamerica_geofabrik :
                    region = 'south-america'
                if c_translated in germany_subregions_geofabrik :
                    region = 'europe\\germany'
                if c_translated in noregion_geofabrik :
                    region = 'no'                    
                if region == '':
                    print(f'\n\nNo Geofabrik region match for country: {c_translated}')
                    sys.exit()
                print(f'# Trying to download missing map of {c}.')
                try:
                    Translate_Country[f'{c}']
                    if region != 'no':
                        url = 'https://download.geofabrik.de/'+ region + '/' + Translate_Country[f'{c}'] + '-latest.osm.pbf'
                    else:
                        url = 'https://download.geofabrik.de/' + Translate_Country[f'{c}'] + '-latest.osm.pbf'
                except:
                    if region != 'no':
                        url = 'https://download.geofabrik.de/'+ region + f'/{c}' + '-latest.osm.pbf'
                    else:
                        url = 'https://download.geofabrik.de/' + f'/{c}' + '-latest.osm.pbf'
                r = requests.get(url, allow_redirects=True, stream = True)
                if r.status_code != 200:
                    print(f'failed to find or download country: {c}')
                    sys.exit()
                Download=open(os.path.join (MAP_PATH, f'{c}' + '-latest.osm.pbf'), 'wb')
                for chunk in r.iter_content(chunk_size=1024*100):
                    Download.write(chunk)
                Download.close()
                map_files = [os.path.join (MAP_PATH, f'{c}' + '-latest.osm.pbf')]
                print(f'# Map of {c} downloaded.')
            border_countries[c] = {'map_file':map_files[0]}

print('\n\n# filter tags from country osm.pbf files')
for key, val  in border_countries.items():
    # print(key, val)
    outFile = os.path.join(OUT_PATH, f'filtered-{key}.osm.pbf')
    outFileo5m = os.path.join(OUT_PATH, f'outFile-{key}.o5m')
    outFileo5mFiltered = os.path.join(OUT_PATH, f'outFileFiltered-{key}.o5m')
    
    # print(outFile)
    if not os.path.isfile(outFile) or Force_Processing == 1:
        #print('! create filtered country file(s)')
        print(f'\n\n# Converting map of {key} to o5m format')
        cmd = ['osmconvert']
        cmd.extend(['-v', '--hash-memory=2500', '--complete-ways', '--complete-multipolygons', '--complete-boundaries', '--drop-author', '--drop-version'])
        cmd.append(val['map_file'])
        cmd.append('-o='+outFileo5m)
        # print(cmd)
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f'Error in OSMConvert with country: {c}')
            sys.exit()
				
        print(f'\n\n# Filtering unwanted map objects out of map of {key}')
        cmd = ['osmfilter']
        cmd.append(outFileo5m)
        cmd.append('--keep="'+filtered_tags+'"')
        cmd.append('-o='+outFileo5mFiltered)
        # print(cmd)
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f'Error in OSMFilter with country: {c}')
            sys.exit()
								
        print(f'\n\n# Converting map of {key} back to osm.pbf format')
        cmd = ['osmconvert', '-v', '--hash-memory=2500', outFileo5mFiltered]
        cmd.append('-o='+outFile)
        # print(cmd)
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f'Error in OSMConvert with country: {c}')
            sys.exit()        

        os.remove(outFileo5m)
        os.remove(outFileo5mFiltered)
								
    border_countries[key]['filtered_file'] = outFile

print('\n\n# Generate land')
TileCount = 1
for tile in country:
    landFile = os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'land.shp')
    outFile = os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'land')

    if not os.path.isfile(landFile) or Force_Processing == 1:
        print(f'\n\n# Generate land {TileCount} of {len(country)} for Coordinates: {tile["x"]} {tile["y"]}')
        cmd = ['ogr2ogr', '-overwrite', '-skipfailures']
        cmd.extend(['-spat', f'{tile["left"]-0.1:.6f}',
                    f'{tile["bottom"]-0.1:.6f}',
                    f'{tile["right"]+0.1:.6f}',
                    f'{tile["top"]+0.1:.6f}'])
        cmd.append(landFile)
        cmd.append(land_polygons_file)
        #print(cmd)
        subprocess.run(cmd)

    if not os.path.isfile(outFile+'1.osm') or Force_Processing == 1:
        cmd = ['python', 'shape2osm.py', '-l', outFile, landFile]
        #print(cmd)
        subprocess.run(cmd)
    TileCount += 1

print('\n\n# Generate sea')
TileCount = 1
for tile in country:
    outFile = os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'sea.osm')
    if not os.path.isfile(outFile) or Force_Processing == 1:
        print(f'# Generate sea {TileCount} of {len(country)} for Coordinates: {tile["x"]} {tile["y"]}')
        with open('sea.osm') as f:
            sea_data = f.read()

            sea_data = sea_data.replace('$LEFT', f'{tile["left"]-0.1:.6f}')
            sea_data = sea_data.replace('$BOTTOM',f'{tile["bottom"]-0.1:.6f}')
            sea_data = sea_data.replace('$RIGHT',f'{tile["right"]+0.1:.6f}')
            sea_data = sea_data.replace('$TOP',f'{tile["top"]+0.1:.6f}')

            with open(outFile, 'w') as of:
                of.write(sea_data)
    TileCount += 1

print('\n\n# Split filtered country files to tiles')
TileCount = 1
for tile in country:
    for c in tile['countries']:
        print(f'\n\n# Splitting tile {TileCount} of {len(country)} for Coordinates: {tile["x"]},{tile["y"]} from map of {c}')
        outFile = os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'split-{c}.osm.pbf')
        if not os.path.isfile(outFile) or Force_Processing == 1:
            #cmd = ['.\\osmosis\\bin\\osmosis.bat', '--rbf',border_countries[c]['filtered_file'],'workers='+workers, '--buffer', 'bufferCapacity=12000', '--bounding-box', 'completeWays=yes', 'completeRelations=yes']
            #cmd.extend(['left='+f'{tile["left"]}', 'bottom='+f'{tile["bottom"]}', 'right='+f'{tile["right"]}', 'top='+f'{tile["top"]}', '--buffer', 'bufferCapacity=12000', '--wb'])
            #cmd.append('file='+outFile)
            #cmd.append('omitmetadata=true')
            cmd = ['osmconvert', '-v', '--hash-memory=2500']
            cmd.append('-b='+f'{tile["left"]}' + ',' + f'{tile["bottom"]}' + ',' + f'{tile["right"]}' + ',' + f'{tile["top"]}')
            cmd.extend(['--complete-ways', '--complete-multipolygons', '--complete-boundaries'])
            cmd.append(border_countries[c]['filtered_file'])
            cmd.append('-o='+outFile)
            # print(cmd)
            result = subprocess.run(cmd)
            if result.returncode != 0:
                print(f'Error in Osmosis with country: {c}')
                sys.exit()            
            # print(border_countries[c]['filtered_file'])
    TileCount += 1

print('\n\n# Merge splitted tiles with land an sea')
TileCount = 1
for tile in country:
    print(f'\n\n# Merging tiles for tile {TileCount} of {len(country)} for Coordinates: {tile["x"]},{tile["y"]}')
    outFile = os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'merged.osm.pbf')
    if not os.path.isfile(outFile) or Force_Processing == 1:
        cmd = [os.path.join (CurDir, 'Osmosis', 'bin', 'osmosis.bat')]
        loop=0
        for c in tile['countries']:
            cmd.append('--rbf')
            cmd.append(os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'split-{c}.osm.pbf'))
            cmd.append('workers='+workers)
            if loop > 0:
                cmd.append('--merge')
            loop+=1
        land_files = glob.glob(os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'land*.osm'))
        for land in land_files:
            cmd.extend(['--rx', 'file='+os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'{land}'), '--s', '--m'])
        cmd.extend(['--rx', 'file='+os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'sea.osm'), '--s', '--m'])
        cmd.extend(['--tag-transform', 'file=' + os.path.join (CurDir, 'tunnel-transform.xml'), '--wb', outFile, 'omitmetadata=true'])
        #print(cmd)
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f'Error in Osmosis with country: {c}')
            sys.exit()   
    TileCount += 1

print('\n\n# Creating .map files')
TileCount = 1
for tile in country:
    print(f'\n\nCreating map file for tile {TileCount} of {len(country)} for Coordinates: {tile["x"]}, {tile["y"]}')
    outFile = os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}.map')
    if not os.path.isfile(outFile+'.lzma') or Force_Processing == 1:
        mergedFile = os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', 'merged.osm.pbf')
        cmd = [os.path.join (CurDir, 'Osmosis', 'bin', 'osmosis.bat'), '--rbf', mergedFile, 'workers='+workers, '--mw', 'file='+outFile]
        cmd.append(f'bbox={tile["bottom"]:.6f},{tile["left"]:.6f},{tile["top"]:.6f},{tile["right"]:.6f}')
        cmd.append('zoom-interval-conf=10,0,17')
        cmd.append('threads='+threads)
        cmd.append('tag-conf-file=' + os.path.join (CurDir, 'tag-wahoo.xml'))
        #cmd.append('tag-conf-file=tag-mapping.xml')
        # print(cmd)
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f'Error in Osmosis with country: {c}')
            sys.exit()        

        print('\n# compress .map file')
        cmd = ['lzma', 'e', outFile, outFile+'.lzma', f'-mt{threads}', '-d27', '-fb273', '-eos']
        # print(cmd)
        subprocess.run(cmd)
    TileCount += 1

print('\n# zip .map.lzma files')

countryName = os.path.split(sys.argv[1])
print(countryName[1])
# Make Wahoo zip file
cmd = ['7za', 'a', '-tzip', '-m0=lzma', '-mx9', '-mfb=273', '-md=1536m', countryName[1] + '.zip']
#cmd = ['7za', 'a', '-tzip', '-m0=lzma', countryName[1] + '.zip']

for tile in country:
    cmd.append(os.path.join(f'{tile["x"]}', f'{tile["y"]}.map.lzma'))
#print(cmd)
subprocess.run(cmd, cwd=OUT_PATH)

# Make Cruiser map files zip file
if Save_Cruiser == 1:
    cmd = ['7za', 'a', '-tzip', '-m0=lzma', countryName[1] + '-maps.zip']
    for tile in country:
        cmd.append(os.path.join(f'{tile["x"]}', f'{tile["y"]}.map'))
    #print(cmd)
    subprocess.run(cmd, cwd=OUT_PATH)