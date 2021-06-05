Version history:
V1.0 2021-04-09 Initial adaption from Henk's Osmium version
V1.1 2021-04-10 Switched to osmconvert for tile extraction for speed. 
V1.2 2021-04-25 Attempt at auto map downloading, changes in command line, 
                bit of error handling and working on it ;-)


Firstly, this is the windows "port" of wahoo-map-creator-osmium.py by Henk.

- Minimal usage instructions:
Run wahoo-map-creator-osmosis from the commandline like this:
python wahoo-map-creator-osmosis.py <country-name of json file>
or
python3 wahoo-map-creator-osmosis.py <country-name of jason file>
Example: python3 wahoo-map-creator-osmosis.py netherlands
or python3 wahoo-map-creator-osmosis.py united_kingdom
 
Depending on your python installation. If you need to use python3 then
you also need to edit wahoo-map-creator-osmosis.py and change line 102 from
cmd = ['python', 'shape2osm.py', '-l', outFile, landFile]
to
cmd = ['python3', 'shape2osm.py', '-l', outFile, landFile]
You need Python 3.5 or higher.

# Not nesacerry anymore but left in for reference
#To get started you need to download the .osm.pbf file for the country
#you want to create the map for from https://download.geofabrik.de/ and 
#place it in the same folder structure in the maps folder as on this site.
#For example, if you want to create the maps for The Netherlands, you 
#download it and place it in the folder maps\europe\netherlands.
#If you miss a bordering country .osm.pbf files, the program will tell you.
#
#Next, you need to copy the <country-name>.json file from the json folder 
#to the root of this folder (where wahoo-map-creator-osmosis is located)
#netherlands.json is included as an example.

That should be it for running the program itself.
Not unimportant, the output map files as well as the .map.lzma files
needed for the Wahoo devices and a zip file containing them all is
located in the output folder. 

To be able to run the program you need to have Python > 3.5 installed. 
Furthermore you need to have ogr2ogr installed. 
I downloaded gdal (which contains ogr2ogr) from:
http://www.gisinternals.com/release.php
Following the guide here: 
https://sandbox.idre.ucla.edu/sandbox/tutorials/installing-gdal-for-windows
This guide is good but misses a needed environment variable: 
PROJ_LIB "C:\Program Files\GDAL\projlib"
See: 
https://stackoverflow.com/questions/56764046/gdal-ogr2ogr-cannot-find-proj-db-error

I myself have Python 3.7.4 installed and used gdal-302-1928-core.msi 
and GDAL-3.2.1.win32-py3.7.msi 
The later looks like it whants to install Python but it is actually asking 
you for the location where Python is installed.

# Left for reference, switched to osmconvert for the tile splitting
#General note: For me the bounding-box extraction of the tiles from the 
#country.osm.pbf files is painfully slow. Maybe it's just my system, don't know.
#Maybe tomorrow I will try to do this extraction using osmconvert but for
#the moment after a week of trail and error I can't see a map tile anymore... :-)

Hope this is somewhat complete, if not, let me know here:
https://groups.google.com/g/wahoo-elemnt-users/c/PSrdapfWLUE