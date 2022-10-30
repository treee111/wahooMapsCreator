"""
constants
"""
#!/usr/bin/python

import os
from pathlib import Path

# User
USER_WAHOO_MC = os.path.join(str(Path.home()), 'wahooMapsCreatorData')
USER_DL_DIR = os.path.join(USER_WAHOO_MC, '_download')
USER_MAPS_DIR = os.path.join(USER_DL_DIR, 'maps')
LAND_POLYGONS_PATH = os.path.join(
    USER_DL_DIR, 'land-polygons-split-4326', 'land_polygons.shp')
GEOFABRIK_PATH = os.path.join(USER_DL_DIR, 'geofabrik.json')
USER_OUTPUT_DIR = os.path.join(USER_WAHOO_MC, '_tiles')

# Python Package - wahooMapsCreator directory
WAHOO_MC_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(WAHOO_MC_DIR, 'resources')
TOOLING_WIN_DIR = os.path.join(WAHOO_MC_DIR, 'tooling_win')
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
VERSION = '2.0.2'

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
    'åland':                            'finland',
    'new_mexico':                       'new-mexico',
    'american_samoa':                   'samoa',
    'commonwealth_of_the_northern_mariana_islands':                   'american-oceania',
    'northern_mariana_islands':         'american-oceania',
    'new_york':                         'new-york',
    'new_hampshire':                    'new-hampshire',
    'new_jersey':                       'new-jersey',
    'rhode_island':                     'rhode-island',
    'district_of_columbia':             'district-of-columbia',
    'north_carolina':                   'north-carolina',
    'south_carolina':                   'south-carolina',
    'north_dakota':                     'north-dakota',
    'south_dakota':                     'south-dakota',
    'west_virginia':                    'west-virginia'
}

continents = ['europe', 'unitedstates', 'north-america', 'south-america', 'asia', 'oceania',
              'africa', 'antarctica']

africa = ['algeria', 'angola', 'benin', 'botswana', 'burkina_faso', 'burundi',
          'cameroon', 'cape_verde', 'central_african_republic', 'chad', 'comoros',
          'cote_d_ivoire', 'democratic_republic_of_the_congo', 'djibouti', 'egypt',
          'equatorial_guinea', 'eritrea', 'ethiopia', 'french_southern_territories', 'gabon',
          'gambia', 'ghana', 'guinea-bissau', 'guinea', 'kenya', 'lesotho', 'liberia',
          'libya', 'madagascar', 'malawi', 'mali', 'mauritania', 'mauritius', 'mayotte',
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
                'mexico', 'montserrat', 'nicaragua', 'panama', 'saint-barthélemy', 'saint-martin',
                'saint_kitts_and_nevis', 'saint_lucia', 'saint_vincent_and_the_grenadines',
                'sint_maarten', 'turks_and_caicos_islands', 'virgin_islands_u.s.']

oceania = ['australia', 'cook_islands', 'fiji', 'french_polynesia', 'kiribati',
           'marshall_islands', 'micronesia', 'nauru', 'new_caledonia', 'new_zealand', 'niue',
           'norfolk_island', 'northern_mariana_islands', 'palau', 'papua_new_guinea',
           'pitcairn_islands', 'samoa', 'solomon_islands', 'tokelau', 'tonga', 'tuvalu',
           'united_states_minor_outlying_islands', 'vanuatu', 'wallis_and_futuna']

southamerica = ['argentina', 'aruba', 'bolivia', 'bonaire_saint_eustatius_and_saba', 'brazil',
                'chile', 'clipperton_island', 'colombia', 'curacao', 'ecuador',
                'falkland_islands', 'french_guiana', 'guyana', 'paraguay', 'peru',
                'saint_pierre_and_miquelon', 'suriname', 'trinidad_and_tobago',
                'uruguay', 'venezuela']

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
                    'cameroon', 'Canary Islands', 'cape-verde', 'central african republic', 'chad',
                    'comores', 'Congo (Republic/Brazzaville)', 'congo-democratic-republic', 'djibouti',
                    'egypt', 'Equatorial Guinea', 'eritrea', 'ethiopia', 'gabon', 'ghana', 'guinea',
                    'guinea-bissau', 'ivory-coast', 'kenya', 'lesotho', 'liberia', 'libya', 'madagascar',
                    'malawi', 'mali', 'mauritania', 'mauritius', 'morocco', 'mozambique', 'namibia',
                    'niger', 'nigeria', 'rwanda', 'saint-helena-ascension-and-tristan-da-cunha',
                    'Sao Tome and Principe', 'Senegal and Gambia', 'seychelles', 'Sierra Leone',
                    'somalia', 'south-africa', 'South Sudan', 'sudan', 'swaziland', 'tanzania', 'togo',
                    'tunisia', 'uganda', 'zambia', 'zimbabwe']

antarctica_geofabrik = ['antarctica']

asia_geofabrik = ['afghanistan', 'armenia', 'azerbaijan', 'bangladesh', 'bhutan', 'cambodia',
                  'china', 'gcc-states', 'india', 'indonesia', 'iran', 'iraq', 'israel-and-palestine',
                  'japan', 'jordan', 'kazakhstan', 'kyrgyzstan', 'laos', 'lebanon',
                  'malaysia-singapore-brunei', 'maldives', 'mongolia', 'myanmar', 'nepal', 'north-korea',
                  'pakistan', 'philippines', 'russian federation', 'south-korea', 'sri-lanka', 'syria',
                  'taiwan', 'tajikistan', 'thailand', 'turkmenistan', 'uzbekistan', 'vietnam', 'yemen']

australiaoceania_geofabrik = ['american-oceania', 'australia', 'cook islands', 'fiji',
                              'île de clipperton', 'kiribati', 'marshall islands', 'micronesia', 'nauru',
                              'new caledonia', 'new zealand', 'niue', 'palau', 'papua new guinea',
                              'pitcairn islands', 'polynesie-francaise', 'samoa', 'solomon islands', 'tokelau',
                              'tonga', 'tuvalu', 'vanuatu', 'wallis et futuna']

centralamerica_geofabrik = ['bahamas', 'belize', 'costa rica', 'cuba', 'el salvador', 'guatemala',
                            'haiti and dominican republic', 'honduras', 'jamaica', 'nicaragua']

europe_geofabrik = ['albania', 'andorra', 'austria', 'azores', 'belarus', 'belgium',
                    'bosnia-herzegovina', 'bulgaria', 'croatia', 'cyprus', 'czech-republic', 'denmark',
                    'estonia', 'faroe-islands', 'finland', 'france', 'georgia', 'germany', 'great-britain',
                    'greece', 'guernsey-jersey', 'hungary', 'iceland', 'ireland-and-northern-ireland',
                    'isle-of-man', 'italy', 'kosovo', 'latvia', 'liechtenstein', 'lithuania', 'luxembourg',
                    'macedonia', 'malta', 'moldova', 'monaco', 'montenegro', 'netherlands', 'norway',
                    'poland', 'portugal', 'romania', 'russian federation', 'serbia', 'slovakia',
                    'slovenia', 'spain', 'sweden', 'switzerland', 'turkey', 'ukraine (with crimea)']

northamerica_geofabrik = ['canada', 'greenland', 'mexico', 'us midwest', 'us northeast',
                          'us pacific', 'us south', 'us west']

northamerica_us_geofabrik = ['alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado',
                             'connecticut', 'delaware', 'district-of-columbia', 'florida',
                             'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas',
                             'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts',
                             'michigan', 'minnesota', 'mississippi', 'missouri', 'montana',
                             'nebraska', 'nevada', 'new-hampshire', 'new-jersey', 'new-mexico',
                             'new-york', 'north-carolina', 'north-dakota', 'ohio', 'oklahoma'
                             'oregon', 'pennsylvania', 'puerto-rico', 'rhode-island',
                             'south-carolina', 'south-dakota', 'tennessee', 'texas',
                             'us-virgin-islands', 'utah', 'vermont', 'virginia', 'washington',
                             'west-virginia', 'wisconsin', 'wyoming']

southamerica_geofabrik = ['argentina', 'bolivia', 'brazil', 'chile', 'colombia', 'ecuador',
                          'paraguay', 'peru', 'suriname', 'uruguay', 'venezuela']

germany_subregions_geofabrik = ['baden-württemberg', 'bayern', 'berlin',
                                'brandenburg (mit berlin)', 'bremen', 'hamburg', 'hessen', 'mecklenburg-vorpommern',
                                'niedersachsen', 'nordrhein-westfalen', 'rheinland-pfalz', 'saarland', 'sachsen',
                                'sachsen-anhalt', 'schleswig-holstein', 'thüringen']

france_subregions_geofabrik = ['alsace', 'aquitaine', 'auvergne', 'basse-normandie', 'bourgogne',
                               'bretagne', 'centre', 'champagne ardenne', 'corse', 'franche comte', 'guadeloupe',
                               'guyane', 'haute-normandie', 'ile-de-france', 'languedoc-roussillon', 'limousin',
                               'lorraine', 'martinique', 'mayotte', 'midi-pyrenees', 'nord-pas-de-calais',
                               'pays de la loire', 'picardie', 'poitou-charentes', 'provence alpes-cote-d\'azur',
                               'reunion', 'rhone-alpes']
# great-britain_subregions_geofabrik = ['england', 'scotland', 'wales']

italy_subregions_geofabrik = [
    'Centro', 'Isole', 'Nord-Est', 'Nord-Ovest', 'Sud']

noregion_geofabrik = ['russia', 'asia']

geofabrik_regions = ['africa', 'antarctica', 'asia', 'australia-oceania',
                     'central-america', 'europe', 'north-america', 'south-america']

block_download = ['dach', 'alps', 'britain-and-ireland', 'south-africa-and-lesotho',
                  'us-midwest', 'us-northeast', 'us-pacific', 'us-south', 'us-west']

# Special_regions like (former) colonies where the map of the wanted region is not present in the map of the parent country.
# example Guadeloupe, it's Geofabrik parent country is France but Guadeloupe is not located within the region covered by the map of France.
special_regions = ['guadeloupe', 'guyane', 'martinique', 'mayotte', 'reunion']

# Tags to keep
TAGS_TO_KEEP_UNIVERSAL = {
    'access': '',
    'area': 'yes',
    'bicycle': '',
    'bridge': '',
    'foot': ['ft_yes', 'foot_designated'],
    'amenity': ['fuel', 'cafe', 'drinking_water'],
    'shop': 'bakery',
    'highway': ['abandoned', 'bus_guideway', 'disused', 'bridleway', 'byway', 'construction', 'cycleway', 'footway', 'living_street', 'motorway', 'motorway_link', 'path', 'pedestrian', 'primary', 'primary_link', 'residential', 'road', 'secondary', 'secondary_link', 'service', 'steps', 'tertiary', 'tertiary_link', 'track', 'trunk', 'trunk_link', 'unclassified'],
    'natural': ['coastline', 'nosea', 'sea', 'beach', 'land', 'scrub', 'water', 'wetland', 'wood'],
    'landuse': 'forest',
    'leisure': ['park', 'nature_reserve'],
    'railway': ['abandoned', 'bus_guideway', 'disused', 'funicular', 'light_rail', 'miniature', 'narrow_gauge', 'preserved', 'rail', 'subway', 'tram'],
    'surface': '',
    'tracktype': '',
    'tunnel': '',
    'waterway': ['canal', 'drain', 'river', 'riverbank'],
    'wood': 'deciduous'
}

NAME_TAGS_TO_KEEP_UNIVERSAL = {
    'admin_level': '2',
    'area': 'yes',
    'mountain_pass': '',
    'natural': '',
    'place': ['city', 'hamlet', 'island', 'isolated_dwelling', 'islet', 'locality', 'suburb', 'town', 'village', 'country']
}
