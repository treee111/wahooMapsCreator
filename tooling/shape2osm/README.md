shape2osm.py
============

this is a single purpose program to convert POINT shapefiles to .OSM
files. Do not feed it anything else.

Setup
=====
Prerequisites:

 * [pyshp](http://code.google.com/p/pyshp/) (included)
 * [progress_bar](http://coreygoldberg.blogspot.com/2010/01/python-command-line-progress-bar-with.html) (included)
 * [elementtree](http://effbot.org/zone/xml-writer.htm)
 * [argparse](http://code.google.com/p/argparse/) (included in python 2.7 and later)

Install these, chmod 0755 shape2osm.py and you should be good to go. 

Usage
===== 
shape2osm.py [-h] INFILE OUTFILE

License
=======
Copyright (c) 2012 Martijn van Exel

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the 
"Software"), to deal in the Software without restriction, including 
without limitation the rights to use, copy, modify, merge, publish, 
distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject 
to the following conditions:

The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS 
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN 
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
