# Usage of wahooMapsCreator
wahooMapsCreator can be used in two different ways:
- as [graphical window](#gui-graphical-user-interface) programm
- as [command line](#cli-command-line-interface) programm

Both ways support the same arguments to be used for the map-creation process. You can choose the arguments via GUI or as [CLI-arguments](#advanced-cli-usage).

### GUI (Graphical User Interface)

From the `root` folder of wahooMapsCreator, run:
  - `python wahoo_map_creator.py`

Set your arguments as required via the window:

<img src="https://github.com/treee111/wahooMapsCreator/blob/develop/docs/gui.png" alt="wahooMapsCreator GUI" width=35%>

### CLI (Command Line Interface)

From the `root` folder of wahooMapsCreator, run:
- `python wahoo_map_creator.py <country_name>`

Examples:
- for Malta: `python wahoo_map_creator.py malta`
- for Ireland: `python wahoo_map_creator.py ireland`

### Run wahooMapsCreator for your country
It might be a good idea to run wahooMapsCreator first for a small country e.g. Malta to check if everything is running fine.
In a next step you can run it for your own country.

### Advanced CLI-Usage
The script supports many arguments.
For a list of all supported arguments, run:
- `python wahoo_map_creator.py -h`

Examples:
- for Malta, download new maps if existing maps are older than 100 days and process files even if files exist
  - `python wahoo_map_creator.py malta -md 100 -fp`
- for Germany, download and process whole tiles which involves other countries than the given
  - `python wahoo_map_creator.py germany -bc`