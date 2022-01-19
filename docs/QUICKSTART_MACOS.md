

# Quick Start Guide for macOS <!-- omit in toc -->

#### Table of contents <!-- omit in toc -->
- [Download and Install required programs](#download-and-install-required-programs)
  - [Java](#java)
  - [homebrew](#homebrew)
  - [OSM-tools](#osm-tools)
  - [GDAL - The Geospatial Data Abstraction Library](#gdal---the-geospatial-data-abstraction-library)
  - [Install additional Python modules](#install-additional-python-modules)
# Download and Install required programs

## Java
https://www.oracle.com/technetwork/java/javase/downloads

## homebrew
Install using terminal
https://brew.sh/

## OSM-tools
1. Install **Osmfilter** using homebrew in terminal:
```
brew install osmfilter
```
2. Install **osmium-tool** using homebrew in terminal:
```
brew install osmium-tool
```
4. Download **Osmosis** latest version from Github
* https://github.com/openstreetmap/osmosis/releases

1. Install mapsforge-map-writer plugin (Osmosis Plugin)
* Download the [mapsforge-map-writer](https://search.maven.org/search?q=a:mapsforge-map-writer) plugin, click on "file_download" and select "jar-with-dependecies.jar".
* Put the .jar in this directory. Create it when it doesn't exist:
`~/.openstreetmap/osmosis/plugins`
* more information: https://github.com/mapsforge/mapsforge/blob/master/docs/Getting-Started-Map-Writer.md#plugin-installation
6. Install osmctools

*I'm not really sure, if this is relevant. If a error concerning osmconvert occurs while using wahooMapsCreator, install osmctools*

Install using terminal:
* with homebrew: `brew install interline-io/planetutils/osmctools` or
* `apt install osmctools` (this may only work on linux and not macOS)

* more information: https://gitlab.com/osm-c-tools/osmctools

## GDAL - The Geospatial Data Abstraction Library
Install using homebrew
```
brew install gdal
```

Wait for it to install (can take a while), and then update the “pip” Python package manager:
```
pip3 install --upgrade pip
```

After this, we can finally install GDAL for Python
```
pip3 install gdal
```

https://medium.com/@vascofernandes_13322/how-to-install-gdal-on-macos-6a76fb5e24a4

## Install additional Python modules
Move to the root-folder of wahooMapsCreator and install required Python modules:
```
pip install -r ./conda_env/requirements.txt
```
