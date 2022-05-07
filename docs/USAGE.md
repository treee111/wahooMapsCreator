# Usage of wahooMapsCreator <!-- omit in toc -->
#### Table of contents <!-- omit in toc -->
- [Usage of wahooMapsCreator](#usage-of-wahoomapscreator)
    - [Always activate environment first](#always-activate-environment-first)
  - [Run wahooMapsCreator for your country](#run-wahoomapscreator-for-your-country)
  - [GUI (Graphical User Interface)](#gui-graphical-user-interface)
  - [CLI (Command Line Interface)](#cli-command-line-interface)
  - [Advanced CLI-Usage](#advanced-cli-usage)
    - [Main arguments](#main-arguments)
    - [Examples](#examples)
  - [POIs - Points of Interest](#pois---points-of-interest)

# Usage of wahooMapsCreator
wahooMapsCreator can be used in two different ways:
- as [graphical window](#gui-graphical-user-interface) programm
- as [command line](#cli-command-line-interface) programm

Both ways support the same arguments to be used for the map-creation process. You can choose the arguments via GUI or as [CLI-arguments](#advanced-cli-usage).

### Always activate environment first

## Run wahooMapsCreator for your country
It might be a good idea to run wahooMapsCreator first for a small country e.g. Malta to check if everything is running fine.
In a next step you can run it for your own country.

## GUI (Graphical User Interface)

From the `root` folder of wahooMapsCreator, run:
  - `python -m wahoomc gui`

Set your arguments as required via the window:

<img src="https://github.com/treee111/wahooMapsCreator/blob/develop/docs/gui.png" alt="wahooMapsCreator GUI" width=35%>

## CLI (Command Line Interface)

From the `root` folder of wahooMapsCreator, run:
- `python -m wahoomc cli -co <country_name>`

Examples:
- for Malta: `python -m wahoomc cli -co malta`
- for Ireland: `python -m wahoomc cli -co ireland`

## Advanced CLI-Usage
The script supports many arguments via command line.
For a list of all supported arguments, run:
- `python -m wahoomc cli -h`

### Main arguments
**Create maps for a country**
- `python -m wahoomc cli -co <country>`

**Create maps for X/Y coordinates**

In particular for testing adjustments in configuration-files or coding it is helpful to create maps for only one tile or a handful of tiles!

To create maps for only one tile and not a whole country, one can use the X/Y coordinates of that tile. X/Y coordinates can be retrieved from this in zoom-level 8: [link](http://tools.geofabrik.de/map/#8/50.3079/8.8026&type=Geofabrik_Standard&grid=1). 
- `python -m wahoomc cli -xy <xy_coordinate,xy_coordinate>`

### Examples
- for Malta, download new maps if existing maps are older than 100 days and process files even if files exist
  - `python -m wahoomc cli -co malta -md 100 -fp`
- for Germany, download and process whole tiles which involves other countries than the given
  - `python -m wahoomc cli -co germany -bc`
- to create maps for only one tile
  - `python -m wahoomc cli -xy 134/88`
- for multiple tiles
  - `python -m wahoomc cli -xy 134/88,133/88`

## POIs - Points of Interest
For creating maps which include POIs and have them displayed on your Wahoo device, these steps need to be done:
1. Create custom maps including POIs
  - a) via CLI
     - `python -m wahoomc cli -co malta -tag tag-wahoo-poi.xml`
  - b) via GUI
     - `python -m wahoomc gui`
     - Fill into Advanced-->Tag wahoo XML file: `tag-wahoo-poi.xml`

By using the tag-wahoo-poi.xml file, wahooMapsCreator includes fuel stations, backeries, cafes and railway stations POI's into the generated maps. 

2. Copy POIs relevant files to your device
- [:floppy_disk: docu](COPY_TO_WAHOO.md#copy-relevant-files-for-pois)

1. Activate VTM rendering if needed
- [see here](COPY_TO_WAHOO.md#activate-vtm-rendering)
- see also: https://github.com/treee111/wahooMapsCreator/wiki/Enable-hidden-features
