# Quickstart Guide for Anaconda on Windows and macOS <!-- omit in toc -->

#### Table of contents <!-- omit in toc -->
- [Download and Install required programs](#download-and-install-required-programs)
  - [Anaconda](#anaconda)
- [Create Anaconda Environment](#create-anaconda-environment)
- [Run wahooMapsCreator](#run-wahoomapscreator)

# Download and Install required programs

## Anaconda
1a. Download `Anaconda Individual Edition` for your OS from

https://www.anaconda.com/products/individual


1b. Install `Anaconda Individual Edition` with default settings

# Create Anaconda Environment
You can have a look at this: which guides you throught 2a and 2b!

https://opensourceoptions.com/blog/how-to-install-gdal-with-anaconda/

2a. Create a new Anaconda Environment using Python 3.7 and activate the environment
```
conda create -n conda-gdal python=3.7
```

2b. install the required Anaconda Python package GDAL
```
conda install -c conda-forge gdal
```
2b. In addition to GDAL, you have to install these packages:
```
conda install -c conda-forge geojson
conda install -c conda-forge requests
conda install -c conda-forge shapely 
```
# Run wahooMapsCreator
Run wahooMapsCreater as described in the [README](../README.md/#Run-wahooMapsCreator)

You have to move to the downloaded/cloned folder via the Anaconda Prompt before or during your Anaconda environment is activated.