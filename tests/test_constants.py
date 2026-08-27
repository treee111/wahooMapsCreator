"""
tests for the downloader file
"""
import os
import unittest


from wahoomc.constants_functions import translate_tags_to_keep


class TestTranslateTags(unittest.TestCase):
    """
    tests for translating tags-constants between the universal format and OS-specific formats
    """

    def setUp(self):
        self.tags_to_keep = os.path.join(os.path.dirname(__file__), 'resources', 'tags-to-keep.json')

    def test_translate_tags_to_keep_full_macos(self):
        """
        Test translating tags to keep from universal format to macOS // all "tags to keep"
        """
        tags = ['access', 'area=yes', 'bicycle', 'bridge', 'foot=ft_yes, foot_designated',
                'amenity=fuel, cafe, drinking_water, shelter', 'shop=bakery, bicycle',
                'highway=abandoned, bus_guideway, disused, bridleway, byway, construction, cycleway, footway, living_street, motorway, motorway_link, path, pedestrian, primary, primary_link, residential, road, secondary, secondary_link, service, steps, tertiary, tertiary_link, track, trunk, trunk_link, unclassified',
                'natural=coastline, nosea, sea, beach, land, scrub, water, wetland, wood',
                'landuse=forest, commercial, industrial, residential, retail',
                'leisure=park, nature_reserve', 'railway=rail, tram, station, stop',
                'surface', 'tracktype', 'tunnel', 'waterway=canal, drain, river, riverbank, stream', 'wood=deciduous', 'tourism=alpine_hut']

        transl_tags = translate_tags_to_keep(self.tags_to_keep)
        self.assertEqual(tags, transl_tags)

    def test_translate_tags_to_keep_full_win(self):
        """
        Test translating tags to keep from universal format to Windows // all "tags to keep"
        """
        tags_win = 'access= area=yes bicycle= bridge= foot=ft_yes =foot_designated amenity=fuel =cafe =drinking_water =shelter shop=bakery =bicycle highway=abandoned =bus_guideway =disused =bridleway =byway =construction =cycleway =footway =living_street =motorway =motorway_link =path =pedestrian =primary =primary_link =residential =road =secondary =secondary_link =service =steps =tertiary =tertiary_link =track =trunk =trunk_link =unclassified natural=coastline =nosea =sea =beach =land =scrub =water =wetland =wood landuse=forest =commercial =industrial =residential =retail leisure=park =nature_reserve railway=rail =tram =station =stop surface= tracktype= tunnel= waterway=canal =drain =river =riverbank =stream wood=deciduous tourism=alpine_hut'

        transl_tags = translate_tags_to_keep(self.tags_to_keep, osmium=False)
        self.assertEqual(tags_win, transl_tags)

    def test_translate_name_tags_to_keep_full_macos(self):
        """
        Test translating name tags to keep from universal format to Windows // all "name tags to keep"
        """
        names_tags = ['admin_level=2', 'area=yes', 'mountain_pass', 'natural',
                      'place=city, hamlet, island, isolated_dwelling, islet, locality, suburb, town, village, country']

        transl_tags = translate_tags_to_keep(self.tags_to_keep, name_tags=True)
        self.assertEqual(names_tags, transl_tags)

    def test_translate_name_tags_to_keep_full_win(self):
        """
        Test translating name tags to keep from universal format to macOS // all "name tags to keep"
        """

        names_tags_win = 'admin_level=2 area=yes mountain_pass= natural= place=city =hamlet =island =isolated_dwelling =islet =locality =suburb =town =village =country'

        transl_tags = translate_tags_to_keep(self.tags_to_keep, name_tags=True, osmium=False)
        self.assertEqual(names_tags_win, transl_tags)


if __name__ == '__main__':
    unittest.main()
