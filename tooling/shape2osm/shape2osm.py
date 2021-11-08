#! /usr/bin/env python

# shape2osm.py
# ============
#
# this is a single purpose program to convert POINT shapefiles to .OSM
# files. Do not feed it anything else.
#
# Setup
# =====
# Prerequisites:
# * [pyshp](http://code.google.com/p/pyshp/) (included)
# * [progress_bar](http://coreygoldberg.blogspot.com/2010/01/python-command-line-progress-bar-with.html) (included)
# * [elementtree](http://effbot.org/zone/xml-writer.htm)
# * [argparse](http://code.google.com/p/argparse/) (included in python 2.7 and later)
# Install these, chmod 0755 shape2osm.py and you should be good to go. 
# 
# Usage
# ===== 
# shape2osm.py [-h] INFILE OUTFILE
#
# License
# =======
# Copyright (c) 2012 Martijn van Exel
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the 
# "Software"), to deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject 
# to the following conditions:
# 
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS 
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN 
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#
# Changelog
# 0.1   initial release
# 0.2   added upload=false to xml

__version__ = 0.2

import shapefile
import argparse
# from progress_bar import ProgressBar
# from elementtree.SimpleXMLWriter import XMLWriter
from xml.etree import ElementTree
from datetime import datetime

API_VERSION = "0.6"

parser = argparse.ArgumentParser(description='Convert a ESRI Shapefile (POINT only) to .OSM')
parser.add_argument('INFILE', help='The path to the input ESRI shapefile, will append .shp if omitted')
parser.add_argument('OUTFILE', type=argparse.FileType('w'), default='out.osm', help='The path to the output OSM XML file')
parser.add_argument('--quiet', action='store_true', default=False)
args = parser.parse_args()

osm_id = 0
dt = datetime.now()

sf = shapefile.Reader(args.INFILE)
fields = sf.fields
num_shapes = len(sf.shapes())

root = ElementTree.Element("osm", {"generator": "shape2osm " + str(__version__), "version": API_VERSION, "upload": "false"})

for shape in sf.shapeRecords():
    osm_id -= 1
    print(shape.shape.points)
    # (x,y) = shape.shape.points[0]
#     node = ElementTree.SubElement(root, "node", {"id": str(osm_id), "timestamp": dt.isoformat(), "version": "1", "visible": "true", "lon": str(x), "lat": str(y)})
#     for i in range(1,len(fields)):
#         tag = ElementTree.SubElement(node, "tag", "", {"k": str(fields[i][0]), "v": str(shape.record[i-1])})

# with open(args.OUTFILE) as f:
#     f.write(ElementTree.tostring(root))

# if not args.quiet:
#     print("\nfinished.")
