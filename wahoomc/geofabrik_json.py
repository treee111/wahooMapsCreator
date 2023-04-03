"""
Object for accessing Geofabrik .json file
"""
#!/usr/bin/python

# import official python packages
import geojson  # pylint: disable=import-error

# import custom python packages
from wahoomc.constants import GEOFABRIK_PATH


class CountyIsNoGeofabrikCountry(Exception):
    """Raised when actual country is not a geofabrik country"""

    def __init__(self, country):
        message = f"Entered country '{country}' is not a geofabrik country. \
                \nPlease check this URL for possible countries: https://download.geofabrik.de/index.html"
        super().__init__(message)


class GeofabrikJson:
    """
    This is a Geofabrik .json processing class for constants in the Geofabrik .json file
    """
    raw_json = None
    geofabrik_overview = {}
    geofabrik_region_overview = {}
    geofabrik_regions = []

    def __init__(self):
        # read geofabrik .json file and fill class-attributes // access is only once
        if GeofabrikJson.raw_json is None and not GeofabrikJson.geofabrik_overview \
                and not GeofabrikJson.geofabrik_region_overview and not GeofabrikJson.geofabrik_regions:
            GeofabrikJson.raw_json, GeofabrikJson.geofabrik_overview, GeofabrikJson.geofabrik_region_overview, GeofabrikJson.geofabrik_regions = self.read_geofabrik_json_file()

    def read_geofabrik_json_file(self):
        """
        read geofabrik .json file and fill class-attributes

        geofabrik_regions as i defined them are the ones without parent
        geofabrik_overview contain all entries, with and without parent
        """
        raw_json = []
        geofabrik_overview = {}
        geofabrik_region_overview = {}
        geofabrik_regions = []

        with open(GEOFABRIK_PATH, encoding='utf8') as file_handle:
            raw_json = geojson.load(file_handle)
        file_handle.close()

        # create a dict with information easy to access because they are often needed
        for feature in raw_json.features:
            props = feature.properties
            id_no = props['id']
            pbf_url = props['urls']['pbf']

            try:
                parent = props['parent']

                geofabrik_overview[id_no] = {
                    'parent': parent,
                    'pbf_url': pbf_url,
                    'geometry': feature.geometry}
            except KeyError:
                geofabrik_overview[id_no] = {
                    'pbf_url': pbf_url,
                    'geometry': feature.geometry}
                geofabrik_region_overview[id_no] = {
                    'pbf_url': pbf_url}
                geofabrik_regions.append(id_no)

        return raw_json, geofabrik_overview, geofabrik_region_overview, geofabrik_regions

    def get_geofabrik_parent_country(self, id_no):
        """
        Get the parent map/region of a country from the already loaded json data
        """
        try:
            entry = self.geofabrik_overview[id_no]
            if 'parent' in entry:
                return (entry['parent'], id_no)

            return ('', id_no)
        except KeyError as exception:
            raise CountyIsNoGeofabrikCountry(id_no) from exception

    def get_geofabrik_url(self, id_no):
        """
        Get the map download url from a country/region with the already loaded json data
        """
        try:
            entry = self.geofabrik_overview[id_no]
            if 'pbf_url' in entry:
                return entry['pbf_url']
        except KeyError:
            pass

        return None

    def get_geofabrik_geometry(self, id_no):
        """
        Get the geometry from a country/region with the already loaded json data
        """
        try:
            entry = self.geofabrik_overview[id_no]
            if 'geometry' in entry:
                return entry['geometry']
        except KeyError:
            pass

        return None

    def is_input_a_geofabrik_id_no(self, id_no):
        """
        check if the given input is a geofabrik id number
        """
        if id_no in self.geofabrik_overview:
            return True

        return False

    def translate_id_no_to_geofabrik(self, country):
        """
        get geofabrik id by country .json filename
        """

        if country in self.geofabrik_overview:
            return country

        if country.replace('_', '-') in self.geofabrik_overview:
            return country.replace('_', '-')

        if 'us/'+country.replace('_', '-') in self.geofabrik_overview:
            return 'us/'+country.replace('_', '-')

        # if none of them got triggert --> exception
        raise CountyIsNoGeofabrikCountry(country)
