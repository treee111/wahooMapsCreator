

# Quick Start Guide for macOS <!-- omit in toc -->

#### Table of contents <!-- omit in toc -->

## Install Java
https://www.oracle.com/technetwork/java/javase/downloads

## Install homebrew
Install using terminal
https://brew.sh/

## Install Osmfilter
Install using homebrew in terminal:
`brew install osmfilter`

## Install Osmfilter
Install using homebrew in terminal:
`brew install osmium-tool`

## Install Osmosis
Download latest version from Github
https://github.com/openstreetmap/osmosis/releases

## Install mapsforge-map-writer plugin (Osmosis Plugin)
Download the [mapsforge-map-writer](https://search.maven.org/search?q=a:mapsforge-map-writer) plugin, click on "file_download" and select "jar-with-dependecies.jar". Put the .jar in one of these directories. Create it when it doesn't exist.

Linux/macOS ~/.openstreetmap/osmosis/plugins

https://github.com/mapsforge/mapsforge/blob/master/docs/Getting-Started-Map-Writer.md#plugin-installation

## Install osmctools
Install using terminal
`apt install osmctools`

https://gitlab.com/osm-c-tools/osmctools

## Install GDAL
Install using homebrew
`brew install gdal`

Wait for it to install (can take a while), and then update the “pip” Python package manager:
`pip3 install --upgrade pip`

After this, we can finally install GDAL for Python
`pip3 install gdal`

https://medium.com/@vascofernandes_13322/how-to-install-gdal-on-macos-6a76fb5e24a4