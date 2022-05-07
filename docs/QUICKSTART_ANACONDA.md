# Quickstart Guide for Anaconda on Windows and macOS <!-- omit in toc -->

#### Table of contents <!-- omit in toc -->
- [Download and Install required programs](#download-and-install-required-programs)
  - [Anaconda](#anaconda)
  - [Java](#java)
  - [macOS, Linux only](#macos-linux-only)
    - [homebrew](#homebrew)
    - [OSM-tools](#osm-tools)
- [wahooMapsCreator](#wahoomapscreator)
  - [Create Anaconda Environment](#create-anaconda-environment)
  - [Install wahooMapsCreator into Anaconda environment](#install-wahoomapscreator-into-anaconda-environment)
    - [Update wahooMapsCreator](#update-wahoomapscreator)
- [Run wahooMapsCreator](#run-wahoomapscreator)
- [Archive](#archive)
  - [old but still valid way to get wahooMapsCreator](#old-but-still-valid-way-to-get-wahoomapscreator)
    - [Create Anaconda Environment](#create-anaconda-environment-1)

# Download and Install required programs

## Anaconda
1. Download `Anaconda Individual Edition` for your OS from

https://www.anaconda.com/products/individual


2. Install `Anaconda Individual Edition` with default settings

## Java
Java needs to be installed for every OS (Windows, macOS, Linux)

https://www.oracle.com/technetwork/java/javase/downloads

## macOS, Linux only
The following programs are needed for macOS and Linux

### homebrew
Install using terminal
https://brew.sh/

### OSM-tools
1. Install **osmium-tool** using homebrew in terminal:
```
brew install osmium-tool
```
2. Download **Osmosis** latest version from Github
```
brew install osmosis
```

3. Install mapsforge-map-writer plugin (Osmosis Plugin)
* Download the [mapsforge-map-writer](https://search.maven.org/search?q=a:mapsforge-map-writer) plugin, click on "file_download" and select "jar-with-dependecies.jar".
* Create this directory when it doesn't exist: `~/.openstreetmap/osmosis/plugins`. For example via terminal:
```
% cd ~
% mkdir -p .openstreetmap/osmosis/plugins
```
* Put the .jar into the `plugins` directory. You may have to enable showing hidden folders in finder via `Command + Shift + . (period)`
* more information: https://github.com/mapsforge/mapsforge/blob/master/docs/Getting-Started-Map-Writer.md#plugin-installation

# wahooMapsCreator
## Create Anaconda Environment
1. Open terminal (macOS/Linux) or **Anaconda Prompt** (Windows, via Startmenu)
2. Create a new Anaconda environment with needed packages
```
conda create -n gdal-user python=3.7 geojson=2.5.* gdal=3.4.* pip --channel conda-forge
```
3. activate Anaconda environment with the command printed out (this needs to be done each time you want to use wahooMapsCreator maps)
```
conda activate gdal-user
```

## Install wahooMapsCreator into Anaconda environment
```
pip install wahoomc
```

### Update wahooMapsCreator
If you have wahooMapsCreator already installed via pip and you want to install a newer version this can be done via:
```
pip install wahoomc --upgrade
```

If you want to upgrade to a version other than the release actual one, use this command:
```
pip install wahoomc==2.0.0a5 --upgrade 
```

# Run wahooMapsCreator
Run wahooMapsCreater as described in the [README](../README.md/#Run-wahooMapsCreator)


# Archive
## old but still valid way to get wahooMapsCreator
This was the way to install wahooMapsCreator until release v1.1.1

Download the latest .zip file from the [Releases](https://github.com/treee111/wahooMapsCreator/releases) page for your OS and save the folder on your drive. Extract the folder.
You can also clone the repository to have the latest coding.

### Create Anaconda Environment
1. Open (or change to) the root of the extracted wahooMapsCreator folder in terminal (macOS/Linux) or **Anaconda Prompt** (Windows, via Startmenu)
2. Create a new Anaconda environment via

  - macOS/ Linux
```
conda env create -f ./conda_env/gdal-user.yml
```
  - Windows
```
conda env create -f .\conda_env\gdal-user.yml 
```
3. activate Anaconda environment with the command printed out (this needs to be done each time you want to create maps)
```
conda activate gdal-user
```

Additional informations: https://opensourceoptions.com/blog/how-to-install-gdal-with-anaconda/

continue with [Run wahooMapsCreator](#run-wahoomapscreator) to use wahooMapsCreator
