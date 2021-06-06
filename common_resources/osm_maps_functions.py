#!/usr/bin/python

# import official python packages
import glob
import os
import os.path
import requests
import subprocess
import sys
import time
import zipfile
import platform

# import custom python packages
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from common_resources import file_directory_functions
from common_resources import constants

class OSM_Maps:
    "This is a OSM data class"


    def __init__(self, input_country, Max_Days_Old, Force_Processing):
        self.input_country = input_country
        self.region = self.getRegionOfCountry(input_country)
        self.Max_Days_Old = Max_Days_Old
        self.Force_Processing = Force_Processing
        self.country = []
        self.border_countries = {}
   

    def getRegionOfCountry(self, county):
        region = ''
        if county in constants.africa :
            region = 'africa'
        if county in constants.antarctica :
            region = 'antarctica'
        if county in constants.asia :
            region = 'asia'
        if county in constants.europe :
            region = 'europe'
        if county in constants.northamerica :
            region = 'north-america'
        if county in constants.oceania :
            region = 'oceania'
        if county in constants.southamerica :
            region = 'south-america'
        if county in constants.unitedstates :
            region = 'united-states'

        return region


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


    def checkAndDownloadLandPoligonsFile(self):
        pathCommon = os.path.join(os.getcwd(), 'common_resources')
        land_polygons_file = os.path.join(os.getcwd(), 'common_resources', 'land-polygons-split-4326/land_polygons.shp')

        print('\n\n# check land_polygons.shp file')
        # Check for expired land polygons file and delete it
        now = time.time()
        To_Old = now - 60 * 60 * 24 * self.Max_Days_Old
        try:
            FileCreation = os.path.getctime(land_polygons_file)
            if FileCreation < To_Old:
                print (f'# Deleting old land polygons file')
                os.remove(land_polygons_file)
                Force_Processing = 1
        except:
            Force_Processing = 1

        if not os.path.exists(land_polygons_file) or not os.path.isfile(land_polygons_file) or self.Force_Processing == 1:
            print('# Downloading land polygons file')
            url = 'https://osmdata.openstreetmap.de/download/land-polygons-split-4326.zip'
            r = requests.get(url, allow_redirects=True, stream = True)
            if r.status_code != 200:
                print(f'failed to find or download land polygons file')
                sys.exit()
            Download=open(os.path.join (pathCommon, 'land-polygons-split-4326.zip'), 'wb')
            for chunk in r.iter_content(chunk_size=1024*100):
                Download.write(chunk)
            Download.close()
            # unpack it
            # should work on macOS and Windows
            self.unzip(os.path.join (pathCommon, 'land-polygons-split-4326.zip'), pathCommon)
            # Windows-Version
            # cmd = ['7za', 'x', '-y', os.path.join (pathCommon, 'land-polygons-split-4326.zip')]
            #print(cmd)
            # result = subprocess.run(cmd)
            os.remove(os.path.join (pathCommon, 'land-polygons-split-4326.zip'))
            # if result.returncode != 0:
            #     print(f'Error unpacking land polygons file')
            #     sys.exit()

        # Check if land polygons file exists
        if not os.path.isfile(land_polygons_file):
            print(f'! failed to find {land_polygons_file}')
            sys.exit()
        
        # logging
        print('# check land_polygons.shp file: OK')


    def createEmptyDirectories(self):
        for tile in self.country:
            outdir = os.path.join(file_directory_functions.OUT_PATH, f'{tile["x"]}', f'{tile["y"]}')
            if not os.path.isdir(outdir):
                os.makedirs(outdir)

    def checkAndDownloadOsmPbfFile(self):
        print('\n\n# check countries .osm.pbf files')
        # Build list of countries needed
        border_countries = {}
        for tile in self.country:
            for c in tile['countries']:
                if c not in border_countries:
                    border_countries[c] = {'map_file':c}

        print (f'{border_countries}')
        # time.sleep(60)

        # Check for expired maps and delete them
        print(f'+ Checking for old maps and remove them')
        now = time.time()
        To_Old = now - 60 * 60 * 24 * self.Max_Days_Old
        for c in border_countries:
            map_files = glob.glob(f'{file_directory_functions.MAP_PATH}/{c}*.osm.pbf')
            if len(map_files) != 1:
                map_files = glob.glob(f'{file_directory_functions.MAP_PATH}/**/{c}*.osm.pbf')
            if len(map_files) == 1 and os.path.isfile(map_files[0]):
                FileCreation = os.path.getctime(map_files[0])
                if FileCreation < To_Old or self.Force_Processing == 1:
                    print (f'# Deleting old map of {c}')
                    os.remove(map_files[0])
                    self.Force_Processing = 1

        print('+ deleted files')
        # time.sleep(60)

        self.createEmptyDirectories()

        border_countries = {}
        for tile in self.country:

        # search for user entered country name in translated (to geofabrik). if match continue with matched else continue with user entered country
        # search for country match in geofabrik tables to determine region to use for map download 
            for c in tile['countries']:
                if c not in border_countries:
                    print(f'+ Checking mapfile for {c}')
                    map_files = glob.glob(f'{file_directory_functions.MAP_PATH}/{c}*.osm.pbf')
                    if len(map_files) != 1:
                        map_files = glob.glob(f'{file_directory_functions.MAP_PATH}/**/{c}*.osm.pbf')
                    if len(map_files) != 1 or not os.path.isfile(map_files[0]):
                        try:
                            c_translated = constants.Translate_Country[f'{c}']
                        except:
                            c_translated = c
                        region = ''
                        if c_translated in constants.africa_geofabrik :
                            region = 'africa'
                        if c_translated in constants.antarctica_geofabrik :
                            region = 'antarctica'
                        if c_translated in constants.asia_geofabrik :
                            region = 'asia'
                        if c_translated in constants.australiaoceania_geofabrik :
                            region = 'australia-oceania'
                        if c_translated in constants.centralamerica_geofabrik :
                            region = 'central-america'
                        if c_translated in constants.europe_geofabrik :
                            region = 'europe'
                        if c_translated in constants.northamerica_geofabrik :
                            region = 'north-america'
                        if c_translated in constants.southamerica_geofabrik :
                            region = 'south-america'
                        if c_translated in constants.germany_subregions_geofabrik :
                            region = 'europe\\germany'
                        if c_translated in constants.noregion_geofabrik :
                            region = 'no'                    
                        if region == '':
                            print(f'\n\n! No Geofabrik region match for country: {c_translated}')
                            sys.exit()
                        print(f'+ Trying to download missing map of {c}.')
                        try:
                            self.Translate_Country[f'{c}']
                            if region != 'no':
                                url = 'https://download.geofabrik.de/'+ region + '/' + self.Translate_Country[f'{c}'] + '-latest.osm.pbf'
                            else:
                                url = 'https://download.geofabrik.de/' + self.Translate_Country[f'{c}'] + '-latest.osm.pbf'
                        except:
                            if region != 'no':
                                url = 'https://download.geofabrik.de/'+ region + f'/{c}' + '-latest.osm.pbf'
                            else:
                                url = 'https://download.geofabrik.de/' + f'/{c}' + '-latest.osm.pbf'
                        r = requests.get(url, allow_redirects=True, stream = True)
                        if r.status_code != 200:
                            print(f'! failed to find or download country: {c}')
                            sys.exit()
                        Download=open(os.path.join (file_directory_functions.MAP_PATH, f'{c}' + '-latest.osm.pbf'), 'wb')
                        for chunk in r.iter_content(chunk_size=1024*100):
                            Download.write(chunk)
                        Download.close()
                        map_files = [os.path.join (file_directory_functions.MAP_PATH, f'{c}' + '-latest.osm.pbf')]
                        print(f'+ Map of {c} downloaded.')
                    self.border_countries[c] = {'map_file':map_files[0]}

                    # logging
                    print(f'+ Border countries of json file: {len(border_countries)}')
                    for c in border_countries:
                        print(f'+ Border country: {c}')
                    print('# Check countries .osm.pbf files: OK')
    
    def filterTagsFromCountryOsmPbdFiles(self):

        print('\n\n# Filter tags from country osm.pbf files')

        # Windows
        # if os.name == "nt":
        if platform.system() == "Windows":
            print('\n\n# filter tags from country osm.pbf files')
            for key, val in self.border_countries.items():
            # print(key, val)
                outFile = os.path.join(file_directory_functions.OUT_PATH, f'filtered-{key}.osm.pbf')
                outFileo5m = os.path.join(file_directory_functions.OUT_PATH, f'outFile-{key}.o5m')
                outFileo5mFiltered = os.path.join(file_directory_functions.OUT_PATH, f'outFileFiltered-{key}.o5m')
                
                # print(outFile)
                if not os.path.isfile(outFile) or self.Force_Processing == 1:
                    #print('! create filtered country file(s)')
                    print(f'\n\n# Converting map of {key} to o5m format')
                    cmd = ['osmconvert']
                    cmd.extend(['-v', '--hash-memory=2500', '--complete-ways', '--complete-multipolygons', '--complete-boundaries', '--drop-author', '--drop-version'])
                    cmd.append(val['map_file'])
                    cmd.append('-o='+outFileo5m)
                    # print(cmd)
                    result = subprocess.run(cmd)
                    if result.returncode != 0:
                        # ToDo: check: key was c before ?!
                        print(f'Error in OSMConvert with country: {key}')
                        sys.exit()
                            
                    print(f'\n\n# Filtering unwanted map objects out of map of {key}')
                    cmd = ['osmfilter']
                    cmd.append(outFileo5m)
                    cmd.append('--keep="' + constants.filtered_tags + '"')
                    cmd.append('-o=' + outFileo5mFiltered)
                    # print(cmd)
                    result = subprocess.run(cmd)
                    if result.returncode != 0:
                        # ToDo: check: key was c before ?!
                        print(f'Error in OSMFilter with country: {key}')
                        sys.exit()
                                            
                    print(f'\n\n# Converting map of {key} back to osm.pbf format')
                    cmd = ['osmconvert', '-v', '--hash-memory=2500', outFileo5mFiltered]
                    cmd.append('-o='+outFile)
                    # print(cmd)
                    result = subprocess.run(cmd)
                    if result.returncode != 0:
                        # ToDo: check: key was c before ?!
                        print(f'Error in OSMConvert with country: {key}')
                        sys.exit()

                    os.remove(outFileo5m)
                    os.remove(outFileo5mFiltered)
                    
                self.border_countries[key]['filtered_file'] = outFile
        
        # Non-Windows
        else:
            for key, val  in self.border_countries.items():
                ## print(key, val)
                outFile = os.path.join(file_directory_functions.OUT_PATH, f'filtered-{key}.osm.pbf')
                ## print(outFile)
                if not os.path.isfile(outFile):
                    print(f'+ Create filtered country file for {key}')    

                    cmd = ['osmium', 'tags-filter']
                    cmd.append(val['map_file'])
                    cmd.extend(constants.filtered_tags)
                    cmd.extend(['-o', outFile])
                    # print(cmd)
                    subprocess.run(cmd)
                self.border_countries[key]['filtered_file'] = outFile

        # logging
        print('# Filter tags from country osm.pbf files: OK')

    def generateLand(self):
        print('\n\n# Generate land')

        TileCount = 1
        for tile in self.country:
            landFile = os.path.join(file_directory_functions.OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'land.shp')
            outFile = os.path.join(file_directory_functions.OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'land')

            if not os.path.isfile(landFile) or self.Force_Processing == 1:
                print(f'+ Generate land {TileCount} of {len(self.country)} for Coordinates: {tile["x"]} {tile["y"]}')
                cmd = ['ogr2ogr', '-overwrite', '-skipfailures']
                cmd.extend(['-spat', f'{tile["left"]-0.1:.6f}',
                            f'{tile["bottom"]-0.1:.6f}',
                            f'{tile["right"]+0.1:.6f}',
                            f'{tile["top"]+0.1:.6f}'])
                cmd.append(landFile)
                cmd.append(file_directory_functions.land_polygons_file)
                #print(cmd)
                subprocess.run(cmd)

            if not os.path.isfile(outFile+'1.osm') or self.Force_Processing == 1:
                cmd = ['python3', os.path.join(file_directory_functions.COMMON_PATH, 'shape2osm.py'), '-l', outFile, landFile]
                #print(cmd)
                subprocess.run(cmd)
            TileCount += 1

        # logging
        print('# Generate land: OK')

    def generateSea(self):
        print('\n\n# Generate sea')

        TileCount = 1
        for tile in self.country:
            outFile = os.path.join(file_directory_functions.OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'sea.osm')
            if not os.path.isfile(outFile) or self.Force_Processing == 1:
                print(f'+ Generate sea {TileCount} of {len(self.country)} for Coordinates: {tile["x"]} {tile["y"]}')
                with open(os.path.join(file_directory_functions.COMMON_PATH, 'sea.osm')) as f:
                    sea_data = f.read()

                    sea_data = sea_data.replace('$LEFT', f'{tile["left"]-0.1:.6f}')
                    sea_data = sea_data.replace('$BOTTOM',f'{tile["bottom"]-0.1:.6f}')
                    sea_data = sea_data.replace('$RIGHT',f'{tile["right"]+0.1:.6f}')
                    sea_data = sea_data.replace('$TOP',f'{tile["top"]+0.1:.6f}')

                    with open(outFile, 'w') as of:
                        of.write(sea_data)
            TileCount += 1

        # logging
        print('# Generate sea: OK')

    def splitFilteredCountryFilesToTiles(self):
        print('\n\n# Split filtered country files to tiles')
        TileCount = 1
        for tile in self.country:

            for c in tile['countries']:
                print(f'+ Split filtered country {c}')
                print(f'+ Splitting tile {TileCount} of {len(self.country)} for Coordinates: {tile["x"]},{tile["y"]} from map of {c}')
                outFile = os.path.join(file_directory_functions.OUT_PATH, f'{tile["x"]}', f'{tile["y"]}', f'split-{c}.osm.pbf')
                if not os.path.isfile(outFile) or self.Force_Processing == 1:
                    # Windows
                    if platform.system() == "Windows":
                        #cmd = ['.\\osmosis\\bin\\osmosis.bat', '--rbf',border_countries[c]['filtered_file'],'workers='+workers, '--buffer', 'bufferCapacity=12000', '--bounding-box', 'completeWays=yes', 'completeRelations=yes']
                        #cmd.extend(['left='+f'{tile["left"]}', 'bottom='+f'{tile["bottom"]}', 'right='+f'{tile["right"]}', 'top='+f'{tile["top"]}', '--buffer', 'bufferCapacity=12000', '--wb'])
                        #cmd.append('file='+outFile)
                        #cmd.append('omitmetadata=true')
                        cmd = ['osmconvert', '-v', '--hash-memory=2500']
                        cmd.append('-b='+f'{tile["left"]}' + ',' + f'{tile["bottom"]}' + ',' + f'{tile["right"]}' + ',' + f'{tile["top"]}')
                        cmd.extend(['--complete-ways', '--complete-multipolygons', '--complete-boundaries'])
                        cmd.append(self.border_countries[c]['filtered_file'])
                        cmd.append('-o='+outFile)

                        # print(cmd)
                        result = subprocess.run(cmd)
                        if result.returncode != 0:
                            print(f'Error in Osmosis with country: {c}')
                            sys.exit()            
                        # print(border_countries[c]['filtered_file'])

                    # Non-Windows
                    else:
                        cmd = ['osmium', 'extract']
                        cmd.extend(['-b',f'{tile["left"]},{tile["bottom"]},{tile["right"]},{tile["top"]}'])
                        cmd.append(self.border_countries[c]['filtered_file'])
                        cmd.extend(['-s', 'smart'])
                        cmd.extend(['-o', outFile])
                        # print(cmd)
                        subprocess.run(cmd)
                        print(self.border_countries[c]['filtered_file'])
            
            TileCount += 1

            # logging
            print('# Split filtered country files to tiles: OK')