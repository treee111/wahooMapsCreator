# Quickstart Guide for Anaconda on Windows and macOS <!-- omit in toc -->

#### Table of contents <!-- omit in toc -->
- [Download and Install required programs](#download-and-install-required-programs)
  - [Anaconda](#anaconda)
  - [wahooMapsCreator](#wahoomapscreator)
- [Create Anaconda Environment](#create-anaconda-environment)
- [Run wahooMapsCreator](#run-wahoomapscreator)

# Download and Install required programs

## Anaconda
1. Download `Anaconda Individual Edition` for your OS from

https://www.anaconda.com/products/individual


2. Install `Anaconda Individual Edition` with default settings

## wahooMapsCreator
Download the latest .zip file from the [Releases](https://github.com/treee111/wahooMapsCreator/releases) page and save the folder on your drive. Extract the folder.

You can also clone the repository to have the latest coding.

# Create Anaconda Environment
1. Open (or change to) the root of the extracted wahooMapsCreator folder in terminal or cmd prompt
2. Create a new Anaconda environment via
```
conda env create --prefix ./envs -f ./conda_env/enduser.yml
```
3. activate Anaconda environment with the command printed out
```
conda activate <PATH_TO_FOLDER>/wahooMapsCreator/envs
```

Additional informations: https://opensourceoptions.com/blog/how-to-install-gdal-with-anaconda/

# Run wahooMapsCreator
Run wahooMapsCreater as described in the [README](../README.md/#Run-wahooMapsCreator)