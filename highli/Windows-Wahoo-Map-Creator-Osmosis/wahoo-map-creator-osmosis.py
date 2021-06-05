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

Translate_Country = {
    'alaska':                           'united_states_of_america',
    'anguilla':                         'central-america', 
    'bahrain':                          'gcc-states',
    'bosnia_and_herzegovina':           'bosnia-herzegovina',
    'british_virgin_islands':           'central-america', 
    'british_indian_ocean_territory':   'asia',
    'brunei':                           'malaysia-singapore-brunei',
    'burkina_faso':                     'burkina-faso',
    'cape_verde':                       'cape-verde',
    'christmas_island':                 'indonesia',
    'cocos_islands':                    'australia',
    'cote_d_ivoire':                    'ivory-coast',
    'czech_republic':                   'czech-republic',
    'democratic_republic_of_the_congo': 'congo-democratic-republic',
    'east_timor':                       'indonesia',
    'faroe_islands':                    'faroe-islands',
    'gambia':                           'senegal-and-gambia',
    'gibraltar':                        'spain',
    'guernsey':                         'guernsey-jersey',
    'hong_kong':                        'china',
    'ireland':                          'ireland-and-northern-ireland',
    'isle_of_man':                      'isle-of-man',
    'israel':                           'israel-and-palestine',
    'jersey':                           'guernsey-jersey',
    'kuwait':                           'gcc-states',
    'macao':                            'china',
    'malaysia':                         'malaysia-singapore-brunei',
    'north_korea':                      'north-korea',
    'oman':                             'gcc-states',
    'palestina':                        'israel-and-palestine',
    'papua_new_guinea':                 'asia',
    'paracel_islands':                  'china',
    'republic_of_congo':                'congo-brazzaville',
    'saint-martin':                     'central-america',
    'saint_helena':                     'saint-helena-ascension-and-tristan-da-cunha',
    'san_marino':                       'italy',
    'saudi_arabia':                     'gcc-states',
    'senegal':                          'senegal-and-gambia',
    'singapore':                        'malaysia-singapore-brunei',
    'sint_maarten':                     'central-america',
    'south_africa':                     'south-africa',
    'south_korea':                      'south-korea',
    'spratly_islands':                  'asia',
    'sri_lanka':                        'sri-lanka',
    'svalbard_and_jan_mayen':           'norway',
    'united_arab_emirates':             'gcc-states',
    'united_kingdom':                   'great-britain',
    'united_states_virgin_islands':     'central-america', 
    'vatican_city':                     'italy',
    'virgin_islands_u.s.':              'central-america', 
    'western_sahara':                   'morocco',
    'qatar':                            'gcc-states',
    'åland':                            'finland'
}

africa = ['algeria', 'angola', 'benin', 'botswana', 'burkina_faso', 'burundi',
    'cameroon', 'cape_verde', 'central_african_republic', 'chad', 'comoros',
    'cote_d_ivoire', 'democratic_republic_of_the_congo', 'djibouti', 'egypt',
    'equatorial_guinea', 'eritrea', 'ethiopia', 'french_southern_territories','gabon',
    'gambia', 'ghana', 'guinea-bissau', 'guinea', 'kenya', 'lesotho', 'liberia',
    'libya','madagascar', 'malawi', 'mali', 'mauritania', 'mauritius', 'mayotte',
    'morocco', 'mozambique', 'namibia', 'niger', 'nigeria', 'republic_of_congo',
    'reunion', 'rwanda', 'saint_helena', 'sao_tome_and_principe', 'senegal',
    'seychelles', 'sierra_leone', 'somalia', 'south_africa', 'sudan', 'swaziland',
    'tanzania', 'togo', 'tunisia', 'uganda', 'western_sahara', 'zambia', 'zimbabwe']

antarctica = ['antarctica', 'bouvet_island', 'heard_island_and_mcdonald_islands',
    'south_georgia_and_the_south_sandwich_islands']

asia = ['afghanistan', 'armenia', 'azerbaijan', 'bahrain', 'bangladesh', 'bhutan',
    'british_indian_ocean_territory', 'brunei', 'cambodia', 'china', 'christmas_island',
    'cocos_islands', 'cyprus', 'east_timor', 'hong_kong', 'india', 'indonesia',
    'iran', 'iraq', 'israel', 'japan', 'jordan', 'kazakhstan', 'kuwait',
    'kyrgyzstan', 'laos', 'lebanon', 'macao', 'malaysia', 'maldives', 'mongolia',
    'myanmar', 'nepal', 'north_korea', 'oman', 'pakistan', 'palestina',
    'paracel_islands', 'philippines', 'qatar', 'saudi_arabia', 'singapore',
    'south_korea', 'spratly_islands', 'sri_lanka', 'syria', 'taiwan', 'tajikistan',
    'thailand', 'turkey', 'turkmenistan', 'united_arab_emirates', 'uzbekistan',
    'vietnam', 'yemen']

europe = ['albania', 'andorra', 'austria', 'belarus', 'belgium', 'bosnia_and_herzegovina',
    'bulgaria', 'croatia', 'czech_republic', 'denmark', 'estonia', 'faroe_islands',
    'finland', 'france', 'germany', 'gibraltar', 'greece', 'guernsey', 'hungary',
    'iceland', 'ireland', 'isle_of_man', 'italy', 'jersey', 'latvia', 'liechtenstein',
    'lithuania', 'luxembourg', 'macedonia', 'malta', 'moldova', 'monaco', 'montenegro',
    'netherlands', 'norway', 'poland', 'portugal', 'romania', 'russia', 'san_marino',
    'serbia', 'slovakia', 'slovenia', 'spain', 'svalbard_and_jan_mayen', 'sweden',
    'switzerland', 'ukraine', 'united_kingdom', 'vatican_city', 'åland']

northamerica = ['anguilla', 'antigua_and_barbuda', 'bahamas', 'barbados', 'belize',
    'bermuda', 'british_virgin_islands', 'canada', 'cayman_islands', 'costa_rica',
    'cuba', 'dominica', 'dominican_republic', 'el_salvador', 'greenland', 'grenada',
    'guadeloupe', 'guatemala', 'haiti', 'honduras', 'jamaica', 'martinique',
    'mexico', 'montserrat', 'nicaragua', 'panama', 'saint-barth‚lemy', 'saint-martin',
    'saint_kitts_and_nevis', 'saint_lucia', 'saint_vincent_and_the_grenadines', 'sint_maarten',
    'turks_and_caicos_islands', 'virgin_islands_u.s.']

oceania = ['australia', 'cook_islands', 'fiji', 'french_polynesia', 'kiribati',
    'marshall_islands', 'micronesia', 'nauru', 'new_caledonia', 'new_zealand', 'niue',
    'norfolk_island', 'northern_mariana_islands', 'palau', 'papua_new_guinea',
    'pitcairn_islands', 'samoa', 'solomon_islands', 'tokelau', 'tonga', 'tuvalu',
    'united_states_minor_outlying_islands', 'vanuatu', 'wallis_and_futuna']

southamerica = ['australia', 'cook_islands', 'fiji', 'french_polynesia', 'kiribati',
    'marshall_islands', 'micronesia', 'nauru', 'new_caledonia', 'new_zealand', 'niue',
    'norfolk_island', 'northern_mariana_islands', 'palau', 'papua_new_guinea',
    'pitcairn_islands', 'samoa', 'solomon_islands', 'tokelau', 'tonga', 'tuvalu',
    'united_states_minor_outlying_islands', 'vanuatu', 'wallis_and_futuna']

unitedstates = ['alabama', 'alaska', 'american_samoa', 'arizona', 'arkansas',
    'california', 'colorado', 'commonwealth_of_the_northern_mariana_islands', 'connecticut',
    'delaware', 'district_of_columbia', 'florida', 'georgia', 'guam', 'hawaii',
    'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana',
    'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi',
    'missouri', 'montana', 'nebraska', 'nevada', 'new_hampshire', 'new_jersey',
    'new_mexico', 'new_york', 'north_carolina', 'north_dakota', 'ohio', 'oklahoma',
    'oregon', 'pennsylvania', 'puerto_rico', 'rhode_island', 'south_carolina',
    'south_dakota', 'tennessee', 'texas', 'united_states_virgin_islands', 'utah',
    'vermont', 'virginia', 'washington', 'west_virginia', 'wisconsin', 'wyoming']
    
africa_geofabrik = ['algeria', 'angola', 'benin', 'botswana', 'burkina-faso', 'burundi',
    'cameroon', 'Canary Islands', 'cape-verde', 'central african republic', 'chad', 'comores',
    'Congo (Republic/Brazzaville)', 'congo-democratic-republic', 'djibouti','egypt',
    'Equatorial Guinea', 'eritrea', 'ethiopia', 'gabon', 'ghana', 'guinea', 'guinea-bissau', 'ivory-coast',
    'kenya', 'lesotho', 'liberia', 'libya', 'madagascar', 'malawi', 'mali', 'mauritania', 'mauritius',
    'morocco', 'mozambique', 'namibia', 'niger','nigeria', 'rwanda', 'saint-helena-ascension-and-tristan-da-cunha',
    'Sao Tome and Principe', 'Senegal and Gambia', 'seychelles', 'Sierra Leone', 'somalia', 'south-africa',
    'South Sudan','sudan', 'swaziland', 'tanzania', 'togo', 'tunisia', 'uganda', 'zambia', 'zimbabwe']

antarctica_geofabrik = ['antarctica']

asia_geofabrik = ['afghanistan', 'armenia', 'azerbaijan', 'bangladesh', 'bhutan', 'cambodia', 'china', 'gcc-states',
    'india', 'indonesia', 'iran', 'iraq', 'israel-and-palestine', 'japan', 'jordan', 'kazakhstan', 'kyrgyzstan',
    'laos', 'lebanon', 'malaysia-singapore-brunei', 'maldives', 'mongolia', 'myanmar',
    'nepal', 'north-korea', 'pakistan', 'philippines', 'russian federation', 'south-korea', 'sri-lanka', 'syria',
    'taiwan', 'tajikistan', 'thailand', 'turkmenistan', 'uzbekistan', 'vietnam', 'yemen']

australiaoceania_geofabrik = ['american oceania', 'australia', 'cook islands', 'fiji', 'île de clipperton',
    'kiribati', 'marshall islands', 'micronesia', 'nauru', 'new caledonia', 'new zealand', 'niue', 'palau',
    'papua new guinea', 'pitcairn islands', 'polynesie-francaise', 'samoa', 'solomon islands', 'tokelau',
    'tonga', 'tuvalu', 'vanuatu', 'wallis et futuna']

centralamerica_geofabrik = ['bahamas', 'belize', 'costa rica', 'cuba', 'el salvador', 'guatemala',
    'haiti and dominican republic', 'honduras', 'jamaica', 'nicaragua']

europe_geofabrik = ['albania', 'andorra', 'austria', 'azores', 'belarus', 'belgium', 'bosnia-herzegovina',
    'bulgaria', 'croatia', 'cyprus', 'czech-republic', 'denmark', 'estonia', 'faroe-islands', 'finland',
    'france', 'georgia', 'germany', 'great-britain', 'greece', 'guernsey-jersey', 'hungary', 'iceland',
    'ireland-and-northern-ireland', 'isle-of-man', 'italy', 'kosovo', 'latvia', 'liechtenstein', 'lithuania',
    'luxembourg', 'macedonia', 'malta', 'moldova', 'monaco', 'montenegro', 'netherlands', 'norway', 'poland',
    'portugal', 'romania', 'russian federation', 'serbia', 'slovakia', 'slovenia', 'spain', 'sweden',
    'switzerland', 'turkey', 'ukraine (with crimea)']

northamerica_geofabrik = ['canada', 'greenland', 'mexico', 'us midwest', 'us northeast', 'us pacific',
    'us south', 'us west']

southamerica_geofabrik = ['argentina', 'bolivia', 'brazil', 'chile', 'colombia', 'ecuador', 'paraguay',
    'peru', 'suriname', 'uruguay', 'venezuela']

germany_subregions_geofabrik = ['baden-württemberg', 'bayern', 'berlin', 'brandenburg (mit berlin)', 'bremen', 'hamburg',
    'hessen', 'mecklenburg-vorpommern', 'niedersachsen', 'nordrhein-westfalen', 'rheinland-pfalz', 'saarland',
    'sachsen', 'sachsen-anhalt', 'schleswig-holstein', 'thüringen'] 

france_subregions_geofabrik = ['alsace', 'aquitaine', 'auvergne', 'basse-normandie', 'bourgogne', 'bretagne', 'centre',
    'champagne ardenne', 'corse', 'franche comte', 'guadeloupe', 'guyane', 'haute-normandie', 'ile-de-france',
    'languedoc-roussillon', 'limousin', 'lorraine', 'martinique', 'mayotte', 'midi-pyrenees', 'nord-pas-de-calais',
    'pays de la loire', 'picardie', 'poitou-charentes', 'provence alpes-cote-d\'azur', 'reunion', 'rhone-alpes']

#great-britain_subregions_geofabrik = ['england', 'scotland', 'wales']

italy_subregions_geofabrik = ['Centro', 'Isole', 'Nord-Est', 'Nord-Ovest', 'Sud']

noregion_geofabrik = ['russia','asia']

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} Country name part of a .json file.')
    sys.exit()

region = ''
if sys.argv[1] in africa :
    region = 'africa'
if sys.argv[1] in antarctica :
    region = 'antarctica'
if sys.argv[1] in asia :
    region = 'asia'
if sys.argv[1] in europe :
    region = 'europe'
if sys.argv[1] in northamerica :
    region = 'north-america'
if sys.argv[1] in oceania :
    region = 'oceania'
if sys.argv[1] in southamerica :
    region = 'south-america'
if sys.argv[1] in unitedstates :
    region = 'united-states'

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

print('\n\n# check land_polygons.shp file')
# Check for expired land polygons file and delete it
now = time.time()
To_Old = now - 60 * 60 * 24 * Max_Days_Old
try:
    FileCreation = os.path.getctime(land_polygons_file)
    if FileCreation < To_Old:
        print (f'# Deleting old land polygons file')
        os.remove(os.path.join (CurDir, 'land-polygons-split-4326', 'land_polygons.shp'))
        Force_Processing = 1
except:
    Force_Processing = 1

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