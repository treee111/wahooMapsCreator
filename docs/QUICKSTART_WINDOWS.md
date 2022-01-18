# Quickstart Guide for Windows <!-- omit in toc -->

#### Table of contents <!-- omit in toc -->
- [Download and Install required programs](#download-and-install-required-programs)
  - [Python - The Python programming language interpreter](#python---the-python-programming-language-interpreter)
  - [GDAL - The Geospatial Data Abstraction Library](#gdal---the-geospatial-data-abstraction-library)
  - [Java](#java)
  - [Windows](#windows)

# Download and Install required programs

## Python - The Python programming language interpreter
1a. Download Python 3.7.9 from https://www.python.org/ftp/python/3.7.9/python-3.7.9.exe


1b. Install Python 3.7.9: 
    Check "Add Python 3.7 to PATH", select "Customize installation",
    set "Customize install location" to "C:\Python" and install.
	
1c. Reboot Windows to activate the path

1d. Install additional Python modules
    Using cmd (Windows+R, cmd), move to the root-folder of wahooMapsCreator and install required Python modules:
    `python -m pip install -r .\\conda_env\\requirements.txt`


## GDAL - The Geospatial Data Abstraction Library
2a. Download GDAL files for Python 3.7 from gisinternals
	gdal-204-1900-core.msi      from https://download.gisinternals.com/sdk/downloads/release-1900-gdal-2-4-4-mapserver-7-4-3/gdal-204-1900-core.msi
    GDAL-2.4.4.win32-py3.7.msi  from https://download.gisinternals.com/sdk/downloads/release-1900-gdal-2-4-4-mapserver-7-4-3/GDAL-2.4.4.win32-py3.7.msi
	
2b. Install gdal-204-1900-core.msi: 
    Select "Typical" setup
	
2c. Install GDAL-2.4.4.win32-py3.7.msi:
    Activate "Python from another location" and enter "C:\Python" in the textfield below. 
	Finish installation.
	

## Java
3a. Download and install Java from 
    https://javadl.oracle.com/webapps/download/AutoDL?BundleId=244582_d7fc238d0cbf4b0dac67be84580cfb4b (32 bit) or
	https://javadl.oracle.com/webapps/download/AutoDL?BundleId=244584_d7fc238d0cbf4b0dac67be84580cfb4b (64 bit)
	
	
## Windows
4a. Edit environment variables 
    by Windows search for "environ" or 
	run "rundll32.exe sysdm.cpl, EditEnvironmentVariables" from cmd
	
4b. Edit the PATH systemvariable and add ;C:\Program Files (x86)\GDAL
4c. Create new systemvariable GDAL_DATA with the value C:\Program Files (x86)\GDAL\gdal-data
4d. Create new systemvariable GDAL_DRIVER_PATH with the value C:\Program Files (x86)\GDAL\gdalplugins
4e. Create new systemvariable PROJ_LIB with the value C:\Program Files (x86)\GDAL\projlib