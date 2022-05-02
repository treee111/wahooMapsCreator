# Usage of wahooMapsCreator
wahooMapsCreator can be used in two different ways:
- as [graphical window](#gui-graphical-user-interface) programm
- as [command line](#cli-command-line-interface) programm

Both ways support the same arguments to be used for the map-creation process. You can choose the arguments via GUI or as [CLI-arguments](#advanced-cli-usage).

## Run wahooMapsCreator for your country
It might be a good idea to run wahooMapsCreator first for a small country e.g. Malta to check if everything is running fine.
In a next step you can run it for your own country.

## GUI (Graphical User Interface)

From the `root` folder of wahooMapsCreator, run:
  - `python -m wahoo_mc gui`

Set your arguments as required via the window:

<img src="https://github.com/treee111/wahooMapsCreator/blob/develop/docs/gui.png" alt="wahooMapsCreator GUI" width=35%>

## CLI (Command Line Interface)

From the `root` folder of wahooMapsCreator, run:
- `python -m wahoo_mc cli -co <country_name>`

Examples:
- for Malta: `python -m wahoo_mc cli -co malta`
- for Ireland: `python -m wahoo_mc cli -co ireland`

## Advanced CLI-Usage
The script supports many arguments via command line.
For a list of all supported arguments, run:
- `python -m wahoo_mc cli -h`

### Main arguments
**Create maps for a country**
- `python -m wahoo_mc cli -co <country>`

**Create maps for X/Y coordinates**

In particular for testing adjustments in configuration-files or coding it is helpful to create maps for only one tile or a handful of tiles!

To create maps for only one tile and not a whole country, one can use the X/Y coordinates of that tile. X/Y coordinates can be retrieved from this in zoom-level 8: [link](http://tools.geofabrik.de/map/#8/50.3079/8.8026&type=Geofabrik_Standard&grid=1). 
- `python -m wahoo_mc cli -xy <xy_coordinate,xy_coordinate>`

### Examples
- for Malta, download new maps if existing maps are older than 100 days and process files even if files exist
  - `python -m wahoo_mc cli -co malta -md 100 -fp`
- for Germany, download and process whole tiles which involves other countries than the given
  - `python -m wahoo_mc cli -co germany -bc`
- to create maps for only one tile
  - `python -m wahoo_mc cli -xy 134/88`
- for multiple tiles
  - `python -m wahoo_mc cli -xy 134/88,133/88`