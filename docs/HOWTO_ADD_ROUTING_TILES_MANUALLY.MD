# How to add routing tiles manually for Wahoo Elemnt ROAM
In addition to the base map tiles, routing tiles are also required to support routing/navigation features (i.e. turn by turn support for Strava route). And it seems Valhalla (https://valhalla.readthedocs.io/en/latest/api/turn-by-turn/overview/) is used by Wahoo Elemnt ROAM as routing services. Following are the detailed instructions for getting routing tiles.

## How to get routing tiles?

Different options exist to get routing tiles. Read the following information in combination with the chapter further down to get a full view on the topic.

### Option a: download pre-generated routing tiles made by the community

This might be the easiest option to get up-to-date routing tiles. Read [here](./FAQ.md#are-there-already-generated-routing-tiles-available-for-download) where to download pre-generated routing tiles and where to put it onto your Wahoo device.

### Option b: generate by using henks repo

This is a very technical option where not everything is predefined and digging into is needed.
This repository https://github.com/Intyre/valhalla-wahoo has most of whats needed to generate routing tiles on your own. Keep the [telegram channel](../README.md#contribution--questions) in mind for technical questions.

### Option c: download from wahoo update server
This is option gets the "standard" routing tiles from Wahoo which might be relatively old.

First of all, index numbers for the routing tiles of target country are required before trying to download them from wahoo update server. Since wahoo use the routing tiles ID ("routing_coordinates") instead of index in mappack-gzip.json, the python script from valhalla are required to decode the ID  into six digital index (first three are the folder name and last three are filename).

Following are the python code for the decode function. More details and full python script can be found from: https://valhalla.github.io/valhalla/tiles

```
	#!/usr/bin/env python

	LEVEL_BITS = 3 
	TILE_INDEX_BITS = 22 
	TILE_INDEX_MASK = (2**TILE_INDEX_BITS) - 1
	def get_tile_index(id): 
	  return (id >> LEVEL_BITS) & TILE_INDEX_MASK
```

After decoding the routing tile IDs into index, it is fairly easy to download all routing tiles from wahoo update server. Following are the URL:
		https://cdn.wahooligan.com/wahoo-maps/{version}/routing/tiles/{level}/000/{x}/{y}.gph.lzma
And the latest map version is 12; level is 2; x, y are both 3 digitals map tile index.

Note:
- Please use 3 digitals for x and y, and add "0" if x or y is less than 100. e.g. use "003" instead "3" when trying to download them
- Some tiles may be missing, the reason and impact are unclear. But it still can work.

## Directory hierarchy in Wahoo Elelmnt ROAM device
```
maps
   | - routing
   |      | - routing-config.json
   |      | - 2
   |          |- 000
   |              | - xxx
   |              |    |- yyy.gph.lzma
   |              |    | -  ……
   |              |    | - yyy.gph.lzma
   |              | - ……
   |              | - ……
   |              | - ……
   |              | - xxx
   |              |    | - yyy.gph.lzma
   |              |    | -  ……
   |              |    | - yyy.gph.lzma
   | - tiles
 	 | - 8
	     | - xxx
	     |    | - yyy.map.lzma
	     |    | -  ……
	     |    | - yyy.map.lzma
	     | - ……
	     | - ……
	     | - ……
	     | - xxx
	     |    | - yyy.map.lzma
	     |    | -  ……
	     |    | - yyy.map.lzma
```
