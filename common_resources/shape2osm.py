#!/usr/bin/python3
# pylint: skip-file

"""
This script is designed to act as assistance in converting shapefiles
to OpenStreetMap data. This file is optimized and tested with MassGIS
shapefiles, converted to EPSG:4326 before being passed to the script.
You can perform this conversion with 

   ogr2ogr -t_srs EPSG:4326 new_file.shp old_file.shp

It is expected that you will modify the fixed_tags, tag_mapping, and
boring_tags attributes of this script before running. You should read,
or at least skim, the code up until it says:

  DO NOT CHANGE AFTER THIS LINE.

to accomodate your own data. 

Modified to support a maximum waylength and multiple outer ways in a
multipolygon relationship

adapted by devemux86
"""

import sys
__author__ = "Christopher Schmidt <crschmidt@crschmidt.net>"
__version__ = "$Id: polyshp2osm-WaterBody.py,v 1.3 2009/03/30 20:54:13 tbook Exp $"

gdal_install = """
Installing GDAL depends on your platform. Information is available at:
   
   http://trac.osgeo.org/gdal/wiki/DownloadingGdalBinaries

For Debian-based systems:

   apt-get install python-gdal

will usually suffice. 
"""

# These tags are attached to all exterior ways. You can put any key/value pairs
# in this dictionary.

fixed_tags = {
    'natural': 'nosea',
    'layer': '-5'
}

# Here are a number of functions: These functions define tag mappings. The API
# For these functions is that they are passed the attributes from a feature,
# and they return a list of two-tuples which match to key/value pairs.

# The following Ftypes are not imported
# 46100 - Submerged Stream
ignoreField = "tile_x"
ignoreValues = []

# The following Ftypes are imported, but don't have any OSM tags attached:
# 36100 - Playa - An area from which water evaporates


def ftype(data):
    """Type of body - From NHD Ftype"""
    natural = {
        'LakePond': 'water',
        'SwampMarsh': 'wetland'
    }

    if 'ftype' in data:
        if data['ftype'] in natural:
            return [('natural', natural[data['ftype']])]
    return None


def fcode(data):
    """For features where the ftype is not specific enough"""
    landuse = {
        '43600': 'reservoir',  # Reservoir
        '43601': 'reservoir',  # Reservoir
        '43602': 'reservoir',  # Reservoir
        '43603': 'reservoir',  # Reservoir
        '43604': 'reservoir',  # Reservoir
        '43605': 'reservoir',  # Reservoir
        '43606': 'reservoir',  # Reservoir
        '43607': 'reservoir',  # Reservoir
        '43609': 'reservoir',  # Reservoir
        '43610': 'reservoir',  # Reservoir
        '43611': 'reservoir',  # Reservoir
        '43612': 'reservoir',  # Reservoir
        '43614': 'reservoir',  # Reservoir
        '43615': 'reservoir',  # Reservoir
        '43616': 'reservoir',  # Reservoir
        '43617': 'reservoir',  # Reservoir
        '43618': 'reservoir',  # Reservoir
        '43619': 'reservoir',  # Reservoir
        '43620': 'reservoir'  # Reservoir
    }

    manmade = {
        '43613': 'reservoir_covered'  # Covered Reservoir
    }

    leisure = {
        '43608': 'swimming_pool'  # Swimming Pool
    }

    if 'fcode' in data:
        keys = []
        if data['fcode'] in landuse:
            keys.append(('landuse', landuse[data['fcode']]))
        if data['fcode'] in manmade:
            keys.append(('man_made', manmade[data['fcode']]))
        if data['fcode'] in leisure:
            keys.append(('leisure', leisure[data['fcode']]))
        return keys
    return None

# The most important part of the code: define a set of key/value pairs
# to iterate over to generate keys. This is a list of two-tuples: first
# is a 'key', which is only used if the second value is a string. In
# that case, it is a map of lowercased fieldnames to OSM tag names: so
# fee_owner maps to 'owner' in the OSM output.

# if the latter is callable (has a __call__; is a function), then that
# method is called, passing in a dict of feature attributes with
# lowercased key names. Those functions can then return a list of
# two-tuples to be used as tags, or nothin' to skip the tags.


tag_mapping = [
    ('ftype', ftype),
    ('fcode', fcode),
    ('gnis_name', 'name'),
    ('gnis_id', 'gnis:feature_id'),
    ('elevation', 'ele'),
]

# These tags are not exported, even with the source data; this should be
# used for tags which are usually calculated in a GIS. AREA and LEN are
# common.

boring_tags = ['error', 'tile_x', 'tile_y']

# Namespace is used to prefix existing data attributes. If 'None', or
# '--no-source' is set, then source attributes are not exported, only
# attributes in tag_mapping.

namespace = "NHD"
#namespace = None

# Uncomment the "DONT_RUN = False" line to get started.

#DONT_RUN = True
DONT_RUN = False

# Set the maximum length of a way (in nodes) before it is split into
# shorter ways

Max_Waylength = 1500000

# =========== DO NOT CHANGE AFTER THIS LINE. ===========================
# Below here is regular code, part of the file. This is not designed to
# be modified by users.
# ======================================================================


try:
    try:
        from osgeo import ogr
    except ImportError:
        import ogr
except ImportError:
    __doc__ += gdal_install
    if DONT_RUN:
        print(__doc__)
        sys.exit(2)
    print("OGR Python Bindings not installed.\n%s" % gdal_install)
    sys.exit(1)


def close_file():
    """ Internal. Close an open file."""
    global open_file
    if not open_file.closed:
        open_file.write("</osm>")
        open_file.close()


def start_new_file():
    """ Internal. Open a new file, closing existing file if neccesary."""
    global open_file, file_counter
    file_counter += 1
    if open_file:
        close_file()
    open_file = open("%s%s.osm" % (file_name, file_counter), "w")
    print("<osm version='0.6'>", file=open_file)


def clean_attr(val):
    """Internal. Hacky way to make attribute XML safe."""
    val = str(val)
    val = val.replace("&", "&amp;").replace("'", "&quot;").replace(
        "<", "&lt;").replace(">", "&gt;").strip()
    return val


def add_ring_nodes(ring):
    """Internal. Write the outer ring nodes."""
    global open_file, id_counter
    ringways = []
    ids = []
    firstnode = id_counter
    if range(ring.GetPointCount() - 1) == 0 or ring.GetPointCount() == 0:
        print("Degenerate ring.", file=sys.stderr)
        return
    for count in range(ring.GetPointCount() - 1):
        ids.append(id_counter)
        print("<node timestamp='1969-12-31T23:59:59Z' changeset='-1' id='%s' version='1' lon='%s' lat='%s' />" %
              (id_counter, ring.GetX(count), ring.GetY(count)), file=open_file)
        id_counter += 1
        if (count > 0) and ((count % (Max_Waylength - 1)) == 0):
            ringways.append(ids)
            ids = []
            ids.append(id_counter - 1)
    ids.append(firstnode)
    ringways.append(ids)
    return ringways


def add_ring_way(ring):
    """Internal. write out the 'holes' in a polygon."""
    global open_file, id_counter
    ids = []
    ringways = []
    for count in range(ring.GetPointCount() - 1):
        ids.append(id_counter)
        print("<node timestamp='1969-12-31T23:59:59Z' changeset='-1' version='1' id='%s' lon='%s' lat='%s' />" %
              (id_counter, ring.GetX(count), ring.GetY(count)), file=open_file)
        id_counter += 1
    if len(ids) == 0:
        return None
    print("<way timestamp='1969-12-31T23:59:59Z' changeset='-1' id='%s' version='1'>" %
          id_counter, file=open_file)
    way_id = id_counter
    id_counter += 1
    count = 0
    for i in ids:
        print("<nd ref='%s' />" % i, file=open_file)
        count += 1
        if count >= Max_Waylength - 1:
            count = 0
            print("</way>", file=open_file)
            ringways.append(way_id)
            print("<way timestamp='1969-12-31T23:59:59Z' changeset='-1'id='%s' version='1'>" %
                  id_counter, file=open_file)
            way_id = id_counter
            id_counter += 1
            print("<nd ref='%s' />" % i, file=open_file)
    print("<nd ref='%s' />" % ids[0], file=open_file)
    print("</way>", file=open_file)
    ringways.append(way_id)

    return ringways


open_file = None

file_name = None

id_counter = 22951459320

file_counter = 0
counter = 0


class AppError(Exception):
    pass


def run(filename, slice_count=1, obj_count=100000000, output_location=None, no_source=False):
    """Run the converter. Requires open_file, file_name, id_counter,
    file_counter, counter to be defined in global space; not really a very good
    singleton."""
    global id_counter, file_counter, counter, file_name, open_file, namespace

    if no_source:
        namespace = None

    if output_location:
        file_name = output_location

    ds = ogr.Open(filename)
    if not ds:
        raise AppError("OGR Could not open the file %s" % filename)
    l = ds.GetLayer(0)

    max_objs_per_file = obj_count

    extent = l.GetExtent()
    if extent[0] < -180 or extent[0] > 180 or extent[2] < -90 or extent[2] > 90:
        raise AppError("Extent does not look like degrees; are you sure it is? \n(%s, %s, %s, %s)" % (
            extent[0], extent[2], extent[1], extent[3]))
    slice_width = (extent[1] - extent[0]) / slice_count

    seen = {}

    print("Running %s slices with %s base filename against shapefile %s" % (
        slice_count, file_name, filename))

    for i in range(slice_count):

        l.ResetReading()
        l.SetSpatialFilterRect(
            extent[0] + slice_width * i, extent[2], extent[0] + (slice_width * (i + 1)), extent[3])

        start_new_file()
        f = l.GetNextFeature()

        obj_counter = 0
        last_obj_split = 0

        while f:
            start_id_counter = id_counter
            if f.GetFID() in seen:
                f = l.GetNextFeature()
                continue
            seen[f.GetFID()] = True

#            done = False
#            while f.GetField(ignoreField) in ignoreValues:
#                if l.GetNextFeature() == None:
#                    done = True
#                    break
#                f = l.GetNextFeature()
#            if done == True:
#                break

            outerways = []
            innerways = []

            geom = f.GetGeometryRef()
            ring = geom.GetGeometryRef(0)

            objcount = ring.GetPointCount()
            for i in range(1, geom.GetGeometryCount()):
                objcount += geom.GetGeometryRef(i).GetPointCount()
                objcount += 1

            if (obj_counter - last_obj_split + objcount) > max_objs_per_file:
                print("Splitting file with %s objs" %
                      (obj_counter - last_obj_split))
                start_new_file()
                last_obj_split = obj_counter

            if objcount > max_objs_per_file:
                print("Warning: a feature contains %i objects which is more than the %i object limit.  It will be placed in a file by itself." % (
                    objcount, max_objs_per_file))

            ringways = add_ring_nodes(ring)
            if not ringways or len(ringways) == 0:
                f = l.GetNextFeature()
                continue
# Write out the outer ways in the relation
            for count in range(len(ringways)):
                ids = ringways[count]
                if ids and len(ids) > 1:
                    print("<way timestamp='1969-12-31T23:59:59Z' changeset='-1' id='%s' version='1'>" %
                          id_counter, file=open_file)
                    outerways.append(id_counter)
                    id_counter += 1
                    for i in ids:
                        print("<nd ref='%s' />" % i, file=open_file)
# Write out the fields for the way
                    field_count = f.GetFieldCount()
                    fields = {}
                    for field in range(field_count):
                        value = f.GetFieldAsString(field)
                        name = f.GetFieldDefnRef(field).GetName()
                        if namespace and name and value and name not in boring_tags:
                            print("<tag k='%s:%s' v='%s' />" % (namespace,
                                  name, clean_attr(value)), file=open_file)
                        fields[name.lower()] = value
                    tags = {}
# Perform the specified field mappting
                    for tag_name, map_value in tag_mapping:
                        if hasattr(map_value, '__call__'):
                            tag_values = map_value(fields)
                            if tag_values:
                                for tag in tag_values:
                                    tags[tag[0]] = tag[1]
                        else:
                            if tag_name in fields:
                                tags[map_value] = fields[tag_name].title()
                    for key, value in tags.items():
                        if key and value:
                            print("<tag k='%s' v='%s' />" %
                                  (key, clean_attr(value)), file=open_file)
# Write fixed tabs
                    for name, value in fixed_tags.items():
                        print("<tag k='%s' v='%s' />" %
                              (name, clean_attr(value)), file=open_file)
                    print("</way>", file=open_file)
            if (geom.GetGeometryCount() > 1) or (len(ringways) > 1):
                # add the inner ways
                for i in range(1, geom.GetGeometryCount()):
                    ringways = add_ring_way(geom.GetGeometryRef(i))
                    for way in ringways:
                        innerways.append(way)
                print("<relation timestamp='1969-12-31T23:59:59Z' changeset='-1' id='%s' version='1' ><tag k='type' v='multipolygon' />" %
                      id_counter, file=open_file)
                id_counter += 1
                for way in outerways:
                    print('<member type="way" ref="%s" role="outer" />' %
                          way, file=open_file)
                for way in innerways:
                    print('<member type="way" ref="%s" role="inner" />' %
                          way, file=open_file)
                print("</relation>", file=open_file)

            counter += 1
            f = l.GetNextFeature()
            obj_counter += (id_counter - start_id_counter)

        close_file()


if __name__ == "__main__":
    if DONT_RUN:
        print(__doc__)
        sys.exit(2)

    from optparse import OptionParser

    parse = OptionParser(
        usage="%prog [args] filename.shp", version=__version__)
    parse.add_option("-s", "--slice-count", dest="slice_count",
                     help="Number of horizontal slices of data", default=1,
                     action="store", type="int")
    parse.add_option("-o", "--obj-count",
                     dest="obj_count",
                     help="Maximum number of objects in a single .osm file",
                     default=1000000, type="int")
    parse.add_option("-n", "--no-source", dest="no_source",
                     help="Do not store source attributes as tags.",
                     action="store_true", default=False)
    parse.add_option("-l", "--output-location",
                     dest="output_location", help="base filepath for output files.",
                     default="poly_output")
    (options, args) = parse.parse_args()

    if not len(args):
        print("No shapefile name given!")
        parse.print_help()
        sys.exit(3)

    kw = {}
    for key in ('slice_count', 'obj_count', 'output_location', 'no_source'):
        kw[key] = getattr(options, key)

    try:
        run(args[0], **kw)
    except AppError as E:
        print("An error occurred: \n%s" % E)
