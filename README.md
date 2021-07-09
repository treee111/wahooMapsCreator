<div align="center">
    <img src="https://github.com/treee111/wahooMapsCreator/blob/develop/docs/wahoo_elemnt_bolt.png" alt="wahooMapsCreator Logo" width=20%>
    <p>
        <a href="https://img.shields.io/badge/python-v3.6+-blue.svg" alt="Python">
            <img src="https://img.shields.io/badge/python-v3.6+-blue.svg" /></a>
        <a href="https://github.com/treee111/wahooMapsCreator/issues" alt="GitHub issues">
            <img src="https://img.shields.io/github/issues/treee111/wahooMapsCreator" /></a>
        <a href="#sponsors" alt="Contributions welcome">
            <img src="https://img.shields.io/badge/contributions-welcome-orange.svg" /></a>
    </p>
    <h1>Wahoo Maps Creator</h1>
</div>
A tool to create up-to-date maps for your Wahoo ELEMNT BOLT and Wahoo ELEMNT!

# Basic Overview
WahooMapsCreator is a tool to create updated maps for Wahoo ELEMNT BOLT and Wahoo ELEMNT devices for your country.
The maps of your device may be old because Wahoo did not release a newer version in the last years. OSM maps are constantly updated and with this program, the updated maps can be used on our Wahoo bike-computers.

## Get it running
The instructens are intended to be suitable for beginners.
If anything is unclear or just wrong, write an issue!

### Overview of the steps
The steps for both OS are similar:
- Download and Install required programs
- Sownload a release of wahooMapsCreator or clone Repository
- Run wahooMapsCreator for your country
- copy the map-files to your device

### Download and Install required programs
The initial setup takes some minutes but is only a one-timer!

Follow the Quick Start guide depending on your OS:
- [Quick Start Guide for Windows](docs/QUICKSTART_WINDOWS.md)
- [Quick Start Guide for macOS](docs/QUICKSTART_MACOS.md)

### Get wahooMapsCreator
Download the latest Release from the ["Releases" Section](https://github.com/treee111/wahooMapsCreator/releases) and Save the folder on your drive. You can also clone the repository and have the latest coding.

### Run wahooMapsCreator for your country
It might be a good idea to run wahooMapsCreator first for a small country e.g. Malta to check if everything is running fine.
In a next step you can run it for your own country.

#### macOS and Windows
From the `root` folder of wahooMapsCreator, run:
- `python3 wahoo_map_creator.py <country_name>` or
- `python wahoo_map_creator.py <country_name>`

Examples:
- for Malta: `python3 wahoo_map_creator.py malta`
- for Ireland: `python3 wahoo_map_creator.py ireland`

### Copy the map-files to your device
When file-creation is finished copy the map-files to your device:
-  [Copy maps files to Wahoo](docs/COPY_TO_WAHOO.md)

## Contribution
You are welcome to provide input via Pull Requests, Issues or in any other way!
Discussion goes on:
- in this telegram channel: https://t.me/joinchat/TaMhjouxlsAzNWZk
- in this google group: https://groups.google.com/g/wahoo-elemnt-users/c/PSrdapfWLUE

More details can be found here: [CONTRIBUTING](.github/CONTRIBUTING.md#Contributing-to-wahooMapsCreator)

## Thanks to
@Intyre/Hank for the initial version of the script

@Higli and @ebo for the Windows- port