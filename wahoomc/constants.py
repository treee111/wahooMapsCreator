"""
constants
"""
#!/usr/bin/python

import os
from pathlib import Path

# User
USER_DIR = str(Path.home())
USER_WAHOO_MC = os.path.join(str(Path.home()), 'wahooMapsCreatorData')
USER_DL_DIR = os.path.join(USER_WAHOO_MC, '_download')
USER_MAPS_DIR = os.path.join(USER_DL_DIR, 'maps')
LAND_POLYGONS_PATH = os.path.join(
    USER_DL_DIR, 'land-polygons-split-4326', 'land_polygons.shp')
GEOFABRIK_PATH = os.path.join(USER_DL_DIR, 'geofabrik.json')
USER_OUTPUT_DIR = os.path.join(USER_WAHOO_MC, '_tiles')
USER_CONFIG_DIR = os.path.join(USER_WAHOO_MC, '_config')
USER_TOOLING_WIN_DIR = os.path.join(USER_DL_DIR, 'tooling_win')
OSMOSIS_WIN_FILE_PATH = os.path.join(
    USER_TOOLING_WIN_DIR, 'Osmosis', 'bin', 'osmosis.bat')

# Python Package - wahooMapsCreator directory
WAHOO_MC_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(WAHOO_MC_DIR, 'resources')
TOOLING_WIN_DIR = os.path.join(WAHOO_MC_DIR, 'tooling_win')
# location of repo / python installation - not used
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
VERSION = '4.0.0a0'


africa = ['algeria', 'angola', 'benin', 'botswana', 'burkina_faso', 'burundi',
          'cameroon', 'canary_islands', 'cape_verde', 'central_african_republic', 'chad', 'comoros',
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

block_download = ['dach', 'alps', 'britain-and-ireland', 'south-africa-and-lesotho',
                  'us-midwest', 'us-northeast', 'us-pacific', 'us-south', 'us-west']

# Special_regions like (former) colonies where the map of the wanted region is not present in the map of the parent country.
# example Guadeloupe, it's Geofabrik parent country is France but Guadeloupe is not located within the region covered by the map of France.
special_regions = ['guadeloupe', 'guyane', 'martinique', 'mayotte', 'reunion']
