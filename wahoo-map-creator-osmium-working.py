#!/usr/bin/python

import os
import sys
import json
import getopt
import glob
import subprocess

# logging
# # means top-level command
# ! means error
# + means additional comment in a working-unit

MAP_PATH='maps'
OUT_PATH='output'
land_polygons_file='land-polygons-split-4326/land_polygons.shp'

filtered_tags=['access', 'admin_level', 'aerialway', 'aeroway', 'barrier',
               'boundary', 'bridge', 'highway', 'natural', 'oneway', 'place',
               'railway', 'tracktype', 'tunnel', 'waterway']

if len(sys.argv) != 2:
    print(f'! Usage: {sys.argv[0]} splitted.json')
    sys.exit()

print('# read json file')
with open(sys.argv[1]) as f:
    country = json.load(f)

# logging
print(f'use json file {f.name} with {len(country)} tiles\n')


print('# check land_polygons.shp file')
if not os.path.isfile(land_polygons_file):
    print(f'! failed to find {land_polygons_file}')
    sys.exit()
# else:

# logging
print('# check land_polygons.shp file: OK \n')


print('# check countries .osm.pbf files')
border_countries = {}
for tile in country:
    outdir = os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}')
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    for c in tile['countries']:
        if c not in border_countries:
            map_files = glob.glob(f'{MAP_PATH}/**/{c}*.osm.pbf')
            if len(map_files) != 1 or not os.path.isfile(map_files[0]):
                print(f'! failed to find country: {c}')
                sys.exit()
            border_countries[c] = {'map_file':map_files[0]}

# logging
print(f'# border countries of json file: {len(border_countries)}')
for c in border_countries:
    print(f'+ border country: {c}')
print('# check countries .osm.pbf files:OK \n')


print('# filter tags from country osm.pbf files')
for key, val  in border_countries.items():
    ## print(key, val)
    outFile = os.path.join(OUT_PATH, f'filtered-{key}.osm.pbf')
    ## print(outFile)
    if not os.path.isfile(outFile):
        print('+ create filtered country file')
# add country in print        

        cmd = ['osmium', 'tags-filter']
        cmd.append(val['map_file'])
        cmd.extend(filtered_tags)
        cmd.extend(['-o', outFile])
        # print(cmd)
        subprocess.run(cmd)
    border_countries[key]['filtered_file'] = outFile

# logging
print('# filter tags from country osm.pbf files: OK \n')


print('# generate land')
for tile in country:
    landFile = os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'land.shp')
    outFile = os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'land')

    if not os.path.isfile(landFile):
        print(f'+ generate land for {tile["x"]} {tile["y"]}')
        cmd = ['ogr2ogr', '-overwrite', '-skipfailures']
        cmd.extend(['-spat', f'{tile["left"]:.6f}',
                    f'{tile["bottom"]:.6f}',
                    f'{tile["right"]:.6f}',
                    f'{tile["top"]:.6f}'])
        cmd.append(landFile)
        cmd.append(land_polygons_file)
        # print(cmd)
        subprocess.run(cmd)

    if not os.path.isfile(outFile+'1.osm'):
        cmd = ['python3', 'shape2osm.py', '-l', outFile, landFile]
        # print(cmd)
        subprocess.run(cmd)

# logging
print('# generate land: OK \n')


print('# generate sea')
for tile in country:
    outFile = os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'sea.osm')
    if not os.path.isfile(outFile):
        print(f'+ generate sea for {tile["x"]} {tile["y"]}')
        with open('sea.osm') as f:
            sea_data = f.read()

            sea_data = sea_data.replace('$LEFT', f'{tile["left"]:.6f}')
            sea_data = sea_data.replace('$BOTTOM',f'{tile["bottom"]:.6f}')
            sea_data = sea_data.replace('$RIGHT',f'{tile["right"]:.6f}')
            sea_data = sea_data.replace('$TOP',f'{tile["top"]:.6f}')

            with open(outFile, 'w') as of:
                of.write(sea_data)

# logging
print('# generate sea: OK \n')


print('# split filtered countries')
for tile in country:
    print(f'+ split filtered country {c}')

    for c in tile['countries']:
        outFile = os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'split-{c}.osm.pbf')
        
        print(f'+ split filtered country {c} for {tile["x"]} {tile["y"]}')

        if not os.path.isfile(outFile):
            cmd = ['osmium', 'extract']
            cmd.extend(['-b',f'{tile["left"]},{tile["bottom"]},{tile["right"]},{tile["top"]}'])
            cmd.append(border_countries[c]['filtered_file'])
            cmd.extend(['-s', 'smart'])
            cmd.extend(['-o', outFile])
            # print(cmd)
            subprocess.run(cmd)
            print(border_countries[c]['filtered_file'])

# logging
print('# split filtered countries: OK \n')


print('# merge splitted, land an sea')
for tile in country:
    outFile = os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'merged.osm.pbf')
    if not os.path.isfile(outFile):
        cmd = ['osmium', 'merge', '--overwrite']
        for c in tile['countries']:
            cmd.append(os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'split-{c}.osm.pbf'))

        cmd.append(os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'land1.osm'))
        cmd.append(os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'sea.osm'))
        cmd.extend(['-o', outFile])
        # print(cmd)
        subprocess.run(cmd)

# logging
print('# merge splitted, land an sea: OK \n')


print('# create .map files')
for tile in country:
    outFile = os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}.map')
    if not os.path.isfile(outFile+'.lzma'):
        mergedFile = os.path.join(OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', 'merged.osm.pbf')
        cmd = ['osmosis', '--rb', mergedFile, '--mw', 'file='+outFile]
        cmd.append(f'bbox={tile["bottom"]:.6f},{tile["left"]:.6f},{tile["top"]:.6f},{tile["right"]:.6f}')
        cmd.append('zoom-interval-conf=10,0,17')
        cmd.append('tag-conf-file=tag-wahoo.xml')
        # print(cmd)
        subprocess.run(cmd)

        print('+ compress .map files')
        cmd = ['lzma', outFile]
        # print(cmd)
        subprocess.run(cmd)

# logging
print('# create .map files: OK \n')

print('# zip .map.lzma files')
countryName = os.path.split(sys.argv[1])
print(f'+ country: {countryName[1][:-5]}')
cmd = ['zip', '-r', countryName[1][:-5] + '.zip']
for tile in country:
    cmd.append(os.path.join(f'{tile["x"]}', f'{tile["y"]}.map.lzma'))
# print(cmd)
subprocess.run(cmd, cwd=OUT_PATH)

# logging
print('# zip .map.lzma files: OK \n')