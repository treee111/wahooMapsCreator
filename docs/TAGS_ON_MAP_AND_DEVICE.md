# OSM-tags during map creation and on your device <!-- omit in toc -->

#### Table of contents <!-- omit in toc -->
- [Zoom-Levels and metric equivalent](#zoom-levels-and-metric-equivalent)
- [File tag-wahoo.xml](#file-tag-wahooxml)
  - [Attribute "zoom-appear"](#attribute-zoom-appear)
- [Device-Theme](#device-theme)
  - [Attribute "zoom-min"](#attribute-zoom-min)
  - [Copy the theme to the device](#copy-the-theme-to-the-device)
  - [Use the theme in cruiser](#use-the-theme-in-cruiser)
- [Combination of tag-wahoo.xml and device-theme](#combination-of-tag-wahooxml-and-device-theme)


# Zoom-Levels and metric equivalent
| Zoom-Level    | Metric        |
| ------------- |:-------------:|
| 9             | 10km          |
| 10            | 5km           |
| 11            | 2km           |
| 12            | 1km           |
| 13            | 500m          |
| 14            | 200m          |
| 15            | 100m          |

# File tag-wahoo.xml
The `tag-wahoo.xml` files defines how to proceed wit OSM-elements during map generation.
The OSM-tags defined in the tag-wahoo.xml file remain on the map.

E.g. roads, locations, ...

## Attribute "zoom-appear"
Each entry has a "zoom-appear" attribute, which defines from which zoom-level onwards the element will be shown. If zoom-appear is set to 13, in 500m, 200m and 100m zoom, the OSM-tag will be displayed. 

# Device-Theme
The theme defines, which OSM-tags are shown on the device or in cruiser where the theme should be used if you preview generated maps on your computer.

The theme is named `mapsforge-bolt.xml` or `mapsforge-roam.xml` and is content-wise equal to the `tag-wahoo.xml`

## Attribute "zoom-min"
Each entry in the theme has a "zoom-min" attribute, which defines from which zoom-level onwards the element will be shown. If zoom-min is set to 13, the OSM-tag will be displayed in zoom-level 500m, 200m and 100m.

## Copy the theme to the device
A theme can be copied to your device like that:
- ELEMNT/BOLT 
  - copy "mapsforge-bolt.xml” of folder `common_resources/theme_adjusted` to `maps/mapsforge-bolt/mapsforge-bolt.xml` (just posted this in the google groups)
- BOLTv2
  - copy `assets/maps/vtm-elemnt/vtm-elemnt.xml` from the apk. Modify and copy the theme to `maps/vtm-elemnt/vtm-elemnt.xml`
- ROAM
  - copy `mapsforge-bolt.xml` of folder `common_resources/theme_adjusted` to `maps/mapsforge-roam/mapsforge-roam.xml`

## Use the theme in cruiser
You should always use the corresponding theme in cruiser if you preview generated maps on your computer.
Because the theme kind of filters out what you gonna see, you want to preview what later on will be visible on the device.

# Combination of tag-wahoo.xml and device-theme
This zoom-appear in combination with the settings in the theme on the device (which can also be applied in cruiser) controls when certain elements are shown on our BOLT/ROAM etc (zoom-min).

If a element is included in the map beginning from zoom-level 10 (zoom-apear in tag-wahoo.xml) but on the device only displayed beginning with zoom level 12 (zoom-min in mapsforge-bolt.xml), the element is only displayed beginning zoom-level 12.