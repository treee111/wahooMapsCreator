#!/usr/usr/env python3

import argparse
import glob
import json
import sys
from xml.dom import minidom


geofabrik_names = { # TODO: find and add more
    'bosnia-and-herzegovina':           'bosnia-herzegovina',
    'cote-divoire':                     'ivory-coast',
    'democratic-republic-of-the-congo': 'congo-democratic-republic',
    'gambia':                           'senegal-and-gambia',
    'gibraltar':                        'spain',
    'israel':                           'israel-and-palestine',
    'palestina':                        'israel-and-palestine',
    'republic-of-congo':                'congo-brazzaville',
    'saint-helena':                     'saint-helena-ascension-and-tristan-da-cunha',
    'saudi-arabia':                     'gcc-states',
    'senegal':                          'senegal-and-gambia',
    'united-kingdom':                   'great-britain',
    'western-sahara':                   'morocco',
    'åland':                            'finland',
    'guernsey':                         'guernsey-jersey',
    'jersey':                           'guernsey-jersey',
    'ireland':                          'ireland-and-northern-ireland',
    'san-marino':                       'italy',
    'vatican-city':                     'italy',
    'svalbard-and-jan-mayen':           'norway',
    'anguilla':                         'central-america', # fix this?
    'virgin-islands-us':                'central-america', # too many central-america!
    'british-virgin-islands':           'central-america', # and the .osm.pbf is only 440MB
    'united-states-virgin-islands':     'central-america', # just use it for all of them
    'saint-martin':                     'central-america',
    'sint-maarten':                     'central-america',
}

def clean_country_name(name):
    name = name.lower()
    name = name.replace(' ','-')
    name = name.replace(',','')
    name = name.replace('.','')
    name = name.replace('\'','')
    name = name.replace('é','e')

    if name in geofabrik_names:
        return geofabrik_names[name]

    return name


def read_tags(path):
    """Reads tags from a .xml used for filtering"""
    tags = []
    xmldoc = minidom.parse(path)
    for s in xmldoc.getElementsByTagName('osm-tag'):
        tag = s.attributes['key'].value
        if tag not in tags:
            tags.append(tag)
    tags.sort()
    return tags

def read_mappack(path):
    packs = {}
    coords = {}

    with open(path) as f:
        data = json.load(f)

    for region in data['tile_packs']:
        for country in region['sub_packs']:
            if 'tile_sets' in country:
                pack = {
                    'id': country['id'],
                    'region': region['name'],
                    'country': country['name'],
                    'coordinates': country['tile_sets'][0]['tile_coordinates'],
                    'tiles': []}

                cname = clean_country_name(country['name'])
                for cord in pack['coordinates']:
                    nr = cord[0]<<16|cord[1]
                    if nr not in coords:
                        coords[nr] = []
                    if cname not in coords[nr]:
                        coords[nr].append(cname)

                packs[country["id"]] = pack

            else:
                for sub in country['sub_packs']:
                    pack = {
                    'id': sub['id'],
                    'region': region['name'],
                    'country': country['name'],
                    'sub': sub['name'],
                    'coordinates': sub['tile_sets'][0]['tile_coordinates'],
                    'tiles': []}

                    cname = clean_country_name(country['name'])
                    for cord in pack['coordinates']:
                        nr = cord[0]<<16|cord[1]
                        if nr not in coords:
                            coords[nr] = []
                        if cname not in coords[nr]:
                            coords[nr].append(cname)

                    packs[sub["id"]] = pack

    for pack in packs:
        packs[pack]['countries'] = []
        for cord in packs[pack]['coordinates']:
            nr = cord[0]<<16|cord[1]
            packs[pack]['tiles'].append({
                'x': cord[0],
                'y': cord[1],
                'countries': sorted(coords[nr])})
            for country in coords[nr]:
                if country not in packs[pack]['countries']:
                    packs[pack]['countries'].append(country)

    return packs


def show_list(packs):
    for pack in packs.values():
        if 'sub' not in pack:
            print('ID: {:3d} | {} | {}'.format(pack['id'], pack['region'], pack['country']))
        else:
            print('ID: {:3d} | {} | {} | {}'.format(pack['id'], pack['region'], pack['country'], pack['sub']))


def search_pack(packs, name):
    for pack in packs.values():
        if name not in pack['country'].lower():
            continue

        if 'sub' not in pack:
            print('ID: {:3d} | {} | {}'.format(pack['id'], pack['region'], pack['country']))
        else:
            print('ID: {:3d} | {} | {} | {}'.format(pack['id'], pack['region'], pack['country'], pack['sub']))


def show_info(pack):
    print('ID:          {}'.format(pack['id']))
    print('Region:      {}'.format(pack['region']))

    if 'sub' in pack:
        print('Country:     {} - {}'.format(pack['country'], pack['sub']))
    else:
        print('Country:     {}'.format(pack['country']))

    if len(pack['countries']) > 1:
        print('Border:     ', ' '.join(pack['countries']))

    print('Tiles:       {}'.format(pack['coordinates']))


def create_map(args, pack):
    tags = read_tags(args.tag_file)

    for country in pack['countries']:
        osmFile = glob.glob(args.maps_dir + '/**/' + country + '-latest.osm.pbf')
        if len(osmFile) != 1:
            print(f'OSM file not found for: {country}')
            return

    # check osm
    # filter osm
    # change tunnel layer level
    # split osm
    # create land and sea
    # merge osm, land and sea
    # create map

def main(args):
    packs = read_mappack(args.mappack_file)

    if args.list:
        show_list(packs)
    elif args.search is not None:
        search_pack(packs, args.search)
    elif args.info is not None:
        if args.info not in packs:
            print(f'No pack found with ID: {args.info}')
        else:
            show_info(packs[args.info])
    elif args.create is not None:
        if args.create not in packs:
            print(f'No pack found with ID: {args.create}')
        else:
            create_map(args, packs[args.create])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', action='store_true', help='show list of packs')
    parser.add_argument('--search', help='search pack by name')
    parser.add_argument('--info', type=int, help='show info about pack with ID')

    parser.add_argument('--create', type=int, help='create pack for ID')
    parser.add_argument('--overwrite', action='store_true', help='overwrite all files')
    parser.add_argument('--tag-file', default='tag-wahoo.xml', help='location of .xml file used for filtering and creating maps')
    parser.add_argument('--mappack-file', default='mappack-gzip.json', help='location of mappack-gzip.json')
    parser.add_argument('--land-file', default='land-polygons.shp', help='location of land-polygons.shp')
    parser.add_argument('--maps-dir', default='maps', help='maps directory')
    parser.add_argument('--output-dir', default='output', help='output directory')
    args = parser.parse_args()
    if args.mappack_file == '' or args.tag_file == '':
        parser.print_help()
        sys.exit(0)

    main(args)