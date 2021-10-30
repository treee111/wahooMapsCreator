# OSM-tags during map creation and on your device <!-- omit in toc -->

#### Table of contents <!-- omit in toc -->
- [Zoom levels and scale](#zoom-levels-and-scale)
- [File tag-wahoo.xml](#file-tag-wahooxml)
  - [Attribute "zoom-appear"](#attribute-zoom-appear)
- [Device-Theme](#device-theme)
  - [Attribute "zoom-min"](#attribute-zoom-min)
  - [Copy the theme to the device](#copy-the-theme-to-the-device)
  - [Use the theme in cruiser](#use-the-theme-in-cruiser)
- [Combination of tag-wahoo.xml and device-theme](#combination-of-tag-wahooxml-and-device-theme)


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

That information were derived from cruiser on macOS. It needs to be checked if the zoom level and scale on cruiser and Wahoo device is exaclty the same or if there is a difference.

# File tag-wahoo.xml
The `tag-wahoo.xml` files defines how to proceed wit OSM-elements during map generation.
The OSM-tags defined in the tag-wahoo.xml are stored in the map file.

E.g. roads, locations, ...

## Attribute "zoom-appear"
Each entry has a "zoom-appear" attribute, which defines from which zoom level onwards the element will be stored in the map. If zoom-appear is set to 13, the OSM-tag will be stored in the 500m, 200m and 100m zoom levels and therefore could be rendered.

# Device-Theme
The theme defines, which OSM-tags are shown on the device or in cruiser where the theme should be used if you preview generated maps on your computer.

The theme is named `mapsforge-bolt.xml` or `mapsforge-roam.xml` and is content-wise equal to the `tag-wahoo.xml`

## Attribute "zoom-min"
Each entry in the theme has a "zoom-min" attribute, which defines from which zoom level onwards the element will be shown. If zoom-min is set to 13, the OSM-tag will be displayed in zoom level 500m, 200m and 100m.

## Copy the theme to the device
See [here](COPY_TO_WAHOO.md#Copy-device-theme)

## Use the theme in cruiser
You should always use the corresponding theme in cruiser if you preview generated maps on your computer.
Because the theme kind of determines what you're gonna see, you want to preview what later on will be visible on the device.

# Combination of tag-wahoo.xml and device-theme
This zoom-appear in combination with the settings in the theme on the device (which can also be applied in cruiser) controls when certain elements are shown on our BOLT/ROAM etc (zoom-min).

If a element is included in the map beginning from zoom level 10 (zoom-apear in tag-wahoo.xml) but on the device only displayed beginning with zoom level 12 (zoom-min in mapsforge-bolt.xml), the element is only displayed beginning zoom level 12.