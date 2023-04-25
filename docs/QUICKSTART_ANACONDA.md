# Quickstart Guide for Anaconda on Windows and macOS <!-- omit in toc -->

#### Table of contents <!-- omit in toc -->
- [Download and Install required programs](#download-and-install-required-programs)
  - [Anaconda](#anaconda)
  - [Java](#java)
    - [Oracle Java:](#oracle-java)
    - [OpenJDK:](#openjdk)
  - [macOS, Linux only](#macos-linux-only)
    - [homebrew](#homebrew)
    - [OSM-tools](#osm-tools)
- [wahooMapsCreator](#wahoomapscreator)
  - [Create Anaconda environment](#create-anaconda-environment)
  - [Install wahooMapsCreator into Anaconda environment](#install-wahoomapscreator-into-anaconda-environment)
    - [Update wahooMapsCreator](#update-wahoomapscreator)
  - [Additional programs for generating contour lines](#additional-programs-for-generating-contour-lines)
    - [Install phyghtmap](#install-phyghtmap)
    - [Verify phyghtmap](#verify-phyghtmap)
    - [Free account for USGS](#free-account-for-usgs)
- [Run wahooMapsCreator](#run-wahoomapscreator)
- [Additional information](#additional-information)

# Download and Install required programs
Using Anaconda to setup a virtual Python environment is the fastest way to get wahooMapsCreator running!

## Anaconda
1. Download `Anaconda Individual Edition` for your OS

Click *Download* on top right to download `Anaconda Distribution` for your OS:

https://www.anaconda.com/products/individual


2. Install `Anaconda Individual Edition` with default settings

## Java
Java needs to be installed for every OS (Windows, macOS, Linux). You can use Oracle Java or OpenJDK.

### Oracle Java:
1. Download `Java Runtime Environment` for your OS from:

https://www.java.com/de/download/

2. Install `Java Runtime Environment` with default settings

### OpenJDK:
1. Download `OpenJDK` build file for your OS and unzip

https://jdk.java.net/19/

2. Move the folder to the appropriate directory
* macOS: `/Library/Java/JavaVirtualMachines/`
* Windows: `C:\Program Files\Java\`
* Linux: `/usr/java`

3. Set environment variable
* macOS: nothing to do
* Windows: https://javatutorial.net/set-java-home-windows-10/
* Linux: https://www.cyberciti.biz/faq/linux-unix-set-java_home-path-variable/

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

# wahooMapsCreator
## Create Anaconda environment
1. Open terminal (macOS/Linux) or **Anaconda Prompt** (Windows, via Startmenu)
2. Create a new Anaconda environment with needed packages
```
conda create -n gdal-user python=3.10 geojson=2.5 gdal=3.4 requests=2.28 shapely=1.8 bs4=4.11 lxml=4.9 matplotlib=3.4.3 pip --channel conda-forge --override-channels
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

## Additional programs for generating contour lines
For integrating contour lines into the generated maps, some additional steps need to be taken.
An additional Python packages has to be installed and you need an free account for USGS to query contour lines from.

### Install phyghtmap
1. Download and unpack http://katze.tfiu.de/projects/phyghtmap/phyghtmap_2.23.orig.tar.gz
2. Enter your Anaconda environment and go to the unpacked folder
3. Install phyghtmap into your Anaconda environment

macOS / Linux
```
sudo python setup.py install
```

Windows
```
python setup.py install
```

### Verify phyghtmap
You can verify the installation of phyghtmap and dependant python packages if you enter the following into your Anaconda shell.
```
phyghtmap
```

If there is a output, phyghtmap was installed and recognized successfully

### Free account for USGS
1. Enter https://ers.cr.usgs.gov/ and create a free account. It's straight forward.
2. Remember your username and password.

# Run wahooMapsCreator
Run wahooMapsCreater as described in the [README](../README.md/#Run-wahooMapsCreator)

# Additional information
Additional information: https://opensourceoptions.com/blog/how-to-install-gdal-with-anaconda/
