#!/usr/bin/python

# import official python packages
import glob
import os
import os.path
import requests
# import subprocess
import sys
import time
import zipfile

# import custom python packages
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from common_resources import file_directory_functions


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


def getRegionOfCountry(county):
    region = ''
    if county in africa :
        region = 'africa'
    if county in antarctica :
        region = 'antarctica'
    if county in asia :
        region = 'asia'
    if county in europe :
        region = 'europe'
    if county in northamerica :
        region = 'north-america'
    if county in oceania :
        region = 'oceania'
    if county in southamerica :
        region = 'south-america'
    if county in unitedstates :
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


def checkAndDownloadLandPoligonsFile(Max_Days_Old, Force_Processing):
    pathCommon = os.path.join(os.getcwd(), 'common_resources')
    land_polygons_file = os.path.join(os.getcwd(), 'common_resources', 'land-polygons-split-4326/land_polygons.shp')

    print('\n\n# check land_polygons.shp file')
    # Check for expired land polygons file and delete it
    now = time.time()
    To_Old = now - 60 * 60 * 24 * Max_Days_Old
    try:
        FileCreation = os.path.getctime(land_polygons_file)
        if FileCreation < To_Old:
            print (f'# Deleting old land polygons file')
            os.remove(land_polygons_file)
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
        Download=open(os.path.join (pathCommon, 'land-polygons-split-4326.zip'), 'wb')
        for chunk in r.iter_content(chunk_size=1024*100):
            Download.write(chunk)
        Download.close()
        # unpack it
        # should work on macOS and Windows
        unzip(os.path.join (pathCommon, 'land-polygons-split-4326.zip'), pathCommon)
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

def checkAndDownloadOsmPbfFile(country, Max_Days_Old, Force_Processing):
    print('\n\n# check countries .osm.pbf files')
    # Build list of countries needed
    border_countries = {}
    for tile in country:
        for c in tile['countries']:
            if c not in border_countries:
                border_countries[c] = {'map_file':c}

    print (f'{border_countries}')
    # time.sleep(60)

    # Check for expired maps and delete them
    print(f'+ Checking for old maps and remove them')
    now = time.time()
    To_Old = now - 60 * 60 * 24 * Max_Days_Old
    for c in border_countries:
        map_files = glob.glob(f'{file_directory_functions.MAP_PATH}/{c}*.osm.pbf')
        if len(map_files) != 1:
            map_files = glob.glob(f'{file_directory_functions.MAP_PATH}/**/{c}*.osm.pbf')
        if len(map_files) == 1 and os.path.isfile(map_files[0]):
            FileCreation = os.path.getctime(map_files[0])
            if FileCreation < To_Old or Force_Processing == 1:
                print (f'# Deleting old map of {c}')
                os.remove(map_files[0])
                Force_Processing = 1

    print('+ deleted files')
    # time.sleep(60)

    border_countries = {}
    for tile in country:
        outdir = os.path.join(file_directory_functions.OUT_PATH, f'{tile["x"]}', f'{tile["y"]}')
        if not os.path.isdir(outdir):
            os.makedirs(outdir)

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
                        print(f'\n\n! No Geofabrik region match for country: {c_translated}')
                        sys.exit()
                    print(f'+ Trying to download missing map of {c}.')
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
                        print(f'! failed to find or download country: {c}')
                        sys.exit()
                    Download=open(os.path.join (file_directory_functions.MAP_PATH, f'{c}' + '-latest.osm.pbf'), 'wb')
                    for chunk in r.iter_content(chunk_size=1024*100):
                        Download.write(chunk)
                    Download.close()
                    map_files = [os.path.join (file_directory_functions.MAP_PATH, f'{c}' + '-latest.osm.pbf')]
                    print(f'+ Map of {c} downloaded.')
                border_countries[c] = {'map_file':map_files[0]}

                # logging
                print(f'+ Border countries of json file: {len(border_countries)}')
                for c in border_countries:
                    print(f'+ Border country: {c}')
                print('# Check countries .osm.pbf files: OK')