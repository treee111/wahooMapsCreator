<div align="center">
    <p>
    <img src="https://github.com/treee111/wahooMapsCreator/blob/develop/docs/wahoo_elemnt_bolt_poi1.png" alt="wahooMapsCreator Logo" width=20%>
    <img src="https://github.com/treee111/wahooMapsCreator/blob/develop/docs/wahoo_elemnt_bolt.png" alt="wahooMapsCreator Logo" width=20%>
    <img src="https://github.com/treee111/wahooMapsCreator/blob/develop/docs/wahoo_elemnt_bolt_poi2.png" alt="wahooMapsCreator Logo" width=20%>
    </p>
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
A tool to create up-to-date maps for your Wahoo BOLTv1 and BOLTv2, ROAM and ELEMNT!

It runs on Windows, macOS as well as on Linux!

## Basic Overview
WahooMapsCreator is a tool to create maps based on the latest OSM data for your Wahoo devices. You can generate maps for the countries you like and you can control which OSM-tags are included.

The maps of your device may be old because Wahoo did not release a newer version in the last years.

OSM maps are constantly updated. With this program, the updated maps can be used on our Wahoo.

# Get it running
The instructions are intended to be suitable for beginners.

If anything is unclear or seams wrong, write an [:pencil2: issue](https://github.com/treee111/wahooMapsCreator/issues)!

## Brand-New: Get POIs displayed on your Wahoo!
[:cookie: here](docs/USAGE.md#pois---points-of-interest)

## Download and Install required programs
Using Anaconda to setup a virtual Python environment is the fastest way to get wahooMapsCreator running!

[:rocket: Quick Start Guide for Anaconda](docs/QUICKSTART_ANACONDA.md#download-and-install-required-programs)

## Run wahooMapsCreator
Activate Anaconda environment
```
conda activate gdal-user
```
Run wahooMapsCreator via GUI
```
python -m wahoomc gui
```
Or run wahooMapsCreator via CLI
```
python -m wahoomc cli -co malta
```

A detailled description of the usage is documented [:computer: here](docs/USAGE.md#usage-of-wahoomapscreator)

## Copy the map-files to your device
When file-creation is finished, copy the maps files to your Wahoo device.

[:floppy_disk: docu](docs/COPY_TO_WAHOO.md#copy-maps-files-to-wahoo-device-)

## (Optional) Use a custom theme on your Wahoo
You can use a custom theme to control which OSM-tags are displayed on your device. Also in which zoom-level certain streets appear!

[:mag: docu](docs/TAGS_ON_MAP_AND_DEVICE.md#osm-tags-during-map-creation-and-on-your-device-)

## Contribution
You are welcome to provide input via Pull Requests, Issues or in any other way!
Discussion goes on:
- in this telegram channel: https://t.me/joinchat/TaMhjouxlsAzNWZk
- in this google group: https://groups.google.com/g/wahoo-elemnt-users/c/PSrdapfWLUE

More details can be found here: [CONTRIBUTING](.github/CONTRIBUTING.md#contributing-to-wahoomapscreator-)

## Thanks to
[@Intyre](https://github.com/Intyre)/Hank for the initial version of the script

[@Ebe66](https://github.com/Ebe66)/ebo for the Windows- port

[@mweirauch](https://github.com/mweirauch) for bringing in new ideas, testing and using the tool

[@zenziwerken](https://github.com/zenziwerken) for the work done for [POIs](https://github.com/zenziwerken/Bolt2-Mapsforge-Rendertheme)!

[@macdet](https://github.com/macdet) for bringing in new thoughts, testing and making this a little more public