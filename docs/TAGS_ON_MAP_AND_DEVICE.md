# OSM-tags during map creation and on your device <!-- omit in toc -->

#### Table of contents <!-- omit in toc -->
- [Order of generating maps](#order-of-generating-maps)
- [Zoom levels and scale](#zoom-levels-and-scale)
- [Files used in map processing](#files-used-in-map-processing)
  - [File tags-to-keep.json](#file-tags-to-keepjson)
  - [File tag-wahoo.xml](#file-tag-wahooxml)
    - [Attribute "zoom-appear"](#attribute-zoom-appear)
    - [Combination of tags-to-keep.json and tag-wahoo.xml](#combination-of-tags-to-keepjson-and-tag-wahooxml)
- [Device-Theme](#device-theme)
  - [Attribute "zoom-min"](#attribute-zoom-min)
  - [Copy the theme to the device](#copy-the-theme-to-the-device)
  - [Use the theme in cruiser](#use-the-theme-in-cruiser)
  - [Combination of tag-wahoo.xml and device-theme](#combination-of-tag-wahooxml-and-device-theme)
- [Adjustments of the device themes](#adjustments-of-the-device-themes)
  - [mapsforge-bolt.xml](#mapsforge-boltxml)


# Order of generating maps
There are mainly 4 steps to process maps from raw OSM data to the final maps for the Wahoo device. You'll find them in the following list with links to the files you can control yourself.

1. Filter relevant OSM tags from raw OSM country files - [tags-to-keep.json](#file-tags-to-keepjson)
2. Create different map increments per tile: OSM map, land and sea
3. Merge these map increments into a merged .osm.pbf file
4. Create .map file while applying tag-wahoo.xml to the merged .osm.pbf file - [tag-wahoo.xml](#file-tag-wahooxml)

For a OSM tag in the map to be displayed on your Wahoo device, it needs to be rendered using the [device theme](#device-theme).

# Zoom levels and scale
| Zoom level | Scale |
| ---------- | :---: |
| 9          | 10km  |
| 10         |  5km  |
| 11         |  2km  |
| 12         |  1km  |
| 13         | 500m  |
| 14         | 200m  |
| 15         | 100m  |

That information were derived from cruiser on macOS. It needs to be checked if the zoom level and scale on cruiser and Wahoo device is exactly the same or if there is a difference.

# Files used in map processing
## File tags-to-keep.json
The `tags-to-keep.json` file controls which tags and name-tags will stay on the map. This happens to keep the file of the generated maps low by filtering out out all other information from the downloaded OSM maps.

## File tag-wahoo.xml
The `tag-wahoo.xml` files defines how to proceed wit OSM-elements during map generation.
The OSM-tags defined in the tag-wahoo.xml are stored in the map file.

E.g. roads, locations, ...

### Attribute "zoom-appear"
Each entry has a "zoom-appear" attribute, which defines from which zoom level onwards the element will be stored in the map. If zoom-appear is set to 13, the OSM-tag will be stored in the 500m, 200m and 100m zoom levels and therefore could be rendered.

### Combination of tags-to-keep.json and tag-wahoo.xml
To bring a certain OSM tag to your generated maps they have to be included in both files. You can have a look at existing OSM tags to get 
1. `tags-to-keep.json` to not be filtered out
2. `tag-wahoo.xml` to be included in the generated maps

# Device-Theme
The device theme defines, which OSM-tags are rendered on the device. In cruiser, you can also apply the device theme to preview generated maps on your computer.

There are two types of rendering methods: VTM and non-VTM rendering. This table shows the default rendering per device:
| device | default rendering |
| ------ | :---------------: |
| ROAMv2 |        VTM        |
| BOLTv2 |        VTM        |
| ROAMv1 |      non-VTM      |
| BOLTv1 |      non-VTM      |
| ELEMNT |      non-VTM      |

You can enable the VTM rendering method on Wahoo devices other than BOLTv2/ROAMv2 by creating a empty file on the device with the name "cfg_BHomeActivity_VtmMaps" in the root folder.

The device theme is named `mapsforge-bolt.xml` or `mapsforge-roam.xml` for non-VTM rendering and `vtm-elemnt.xml` for VTM-rendering. It's content is more or less equal to the `tag-wahoo.xml` files.

## Attribute "zoom-min"
Each entry in the theme has a "zoom-min" attribute, which defines from which zoom level onwards the element will be shown. If zoom-min is set to 13, the OSM-tag will be displayed in zoom level 500m, 200m and 100m.

## Copy the theme to the device
See [here](COPY_TO_WAHOO.md#Copy-device-theme)

## Use the theme in cruiser
You should always use the corresponding theme in cruiser if you preview generated maps on your computer.
Because the theme kind of determines what you're gonna see, you want to preview what later on will be visible on the device.

## Combination of tag-wahoo.xml and device-theme
This zoom-appear in combination with the settings in the theme on the device (which can also be applied in cruiser) controls when certain elements are shown on our BOLT/ROAM etc (zoom-min).

If a element is included in the map beginning from zoom level 10 (zoom-appear in tag-wahoo.xml) but on the device only displayed beginning with zoom level 12 (zoom-min in mapsforge-bolt.xml), the element is only displayed beginning zoom level 12.

# Adjustments of the device themes
This chapter documents, which changes are done to the files in `device_themes/adjusted` in comparision to the initial device themes.

## mapsforge-bolt.xml
- render highway-secondary when zoomed out
  - from zoom 10 / 5km on (was zoom 13 / 500m before)
  - to have a overview when zoomed "out"

- render highway-road only when zoomed in
  - from zoom 14 / 200m on (was zoom 13 / 500m before)
  - to make it clearly arranged when zoomed "out" by zoom 500m
