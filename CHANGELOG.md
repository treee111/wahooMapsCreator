# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Types of changes

- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Removed` for now removed features.
- `Fixed` for any bug fixes.
- `Security` in case of vulnerabilities.

## [Unreleased]
### Added
- tag-wahoo-v12.xml which is a updated version of the current tag-wahoo-hidrive2.xml. Bus_guideways have been removed and the zoom-appear levels are copied from the original wahoo maps.
  This really should replace tag-wahoo.xml eventually when v12 maps are created.
### Changed
- Replaced the publicly available osmconvert.exe (https://wiki.openstreetmap.org/wiki/Osmconvert) 0.8.8 with a special newer version 0.8.10. 
  This version does NOT include the zlib library which enables processing of .osm.pbf files larger then 4GB on windows. The old version did have zlib which prevented processing of > 4Gb .osm.pbf files on windows. [PR38](https://github.com/treee111/wahooMapsCreator/pull/38)

## [Unreleased]
### Added
- have more different tag-wahoo-xml files and move them to folders. Modify tag-wahoo.xml to differently display some "place"-tags [PR34](https://github.com/treee111/wahooMapsCreator/issues/34)
### Changed
- move "central" download functions from downloader to file_directory_functions
- move files from common_resources into two new folders: common_download & common_python and into tooling [PR33](https://github.com/treee111/wahooMapsCreator/pull/33)
- format python files in directory common_python using "autopep8" [PR35](https://github.com/treee111/wahooMapsCreator/pull/35) [PR37](https://github.com/treee111/wahooMapsCreator/pull/37)
### Fixed
- fix bug in download handling of land polygons file which was introduced with [PR33](https://github.com/treee111/wahooMapsCreator/pull/33). [PR35](https://github.com/treee111/wahooMapsCreator/pull/35)

## [0.8.1] - 2021-09-10
### Fixed
- change dynamic access to constants-values to prevent console-errors [#29](https://github.com/treee111/wahooMapsCreator/issues/29) [PR30](https://github.com/treee111/wahooMapsCreator/issues/30)

## [0.8.0] - 2021-08-11
### Added
- download a geofabrik file only once if more countries are in the same geofabrik-country [#11](https://github.com/treee111/wahooMapsCreator/issues/11) [PR28](https://github.com/treee111/wahooMapsCreator/issues/28)
### Fixed
- `-h` and `--help` works again

## [0.7.1] - 2021-07-26
### Fixed
- Release .zip file without doubled subfolder. Directly zip content

## [0.7.0] - 2021-07-25
### Added
- GUI functionality with all relevant settings (equals CLI arguments) [#21](https://github.com/treee111/wahooMapsCreator/issues/21) [PR24](https://github.com/treee111/wahooMapsCreator/issues/24)
  - start gui via `python3 wahoo_map_creator.py` or `python wahoo_map_creator.py`
- Release .zip file will only contain relevant files for execution [PR25](https://github.com/treee111/wahooMapsCreator/issues/25)
### Fixed
- When running without calculation of border countries, ignore border countries in all steps [PR24](https://github.com/treee111/wahooMapsCreator/issues/24)
### Changed
- move contents into the correct directory [PR23](https://github.com/treee111/wahooMapsCreator/issues/23)
### Removed
- doubled / not needed files and folders [PR23](https://github.com/treee111/wahooMapsCreator/issues/23)

## [0.6.0] - 2021-07-10
### Added
- CLI arguments for relevant settings. No more editing of python files needed [#15](https://github.com/treee111/wahooMapsCreator/issues/15) [PR19](https://github.com/treee111/wahooMapsCreator/issues/19)
  - see `python3 wahoo_map_creator.py -h` or `python wahoo_map_creator.py -h` for possible arguments
### Changed
- pylint findings corrected
### Removed
- settings for processing should no longer be made in the file wahoo_map_creator.py. --> Use CLI arguments
### Fixed
- unittests run also on windows (paths are now OS-independent)

## [0.5.0] - 2021-07-04
### Added
- Parameter to control download and processing of border countries or not [PR18](https://github.com/treee111/wahooMapsCreator/issues/18)
- unittests for downloader.py and osm_maps_functions.py files [PR16](https://github.com/treee111/wahooMapsCreator/issues/16)
### Changed
- pylint findings corrected
- a lot of refactored (focus methods, constructors)
- refactor downloader-methods for testing with unittests
- correctly check force_download and force_processing against boolean
- fix pylint findings (focus documentation and imports)
- reduce (double) imported standard modules & delete unused imports
- move call of empty directories-creation

## [0.4.0] - 2021-07-01
### Added
- parameter force_download to differentiate between forcing download of new maps and force of processing maps
- enable selective download of .osm.pdf files. Only download out-of-date files

### Changed
- correct pylint findings
- unify macOS and Windows python file into one
  - the new file is: wahoo_mapcreator.py in root folder
  - deletion of tooling_mac/mac_wahoo_map_creator.py
- a lot of refactoring: move coding to class FileDir and Downloader

### Deprecated
- the tooling_mac/ and tooling_windows python files will be removed in the future

## [0.3.1] - 2021-06-17
### Added
- configuration for virtual python environment (venv)
### Changed
- correct import path for custom python package
### Removed
- unused official and custom python packages

## [0.3.0] - 2021-06-16
### Added
- README, Quick Start Guides & documentation written
- Refactoring & Renaming of .py files

## [0.2.0] - 2021-06-10
### Added
- bat file with GUI for Windows (with corresponding python file)
- automatic creation of Releases when pushing a tag with semantic version (eg. v.1.1)
- `docs` directory
### Changed
- deleted one directory level in `tooling_windows`
- move leftover common-files to `common_resources` directory
- README with picture and changed text
### Removed
- existing "single-file" program files & bat callers, mainly:
  - macOS/Unix: `tooling_mac/wahoo-map-creator-osmium-working.py`
  - Windows:    `tooling_windows/Windows-Wahoo-Map-Creator-Osmosis/wahoo-map-creator-osmosis.py`
- doubled files

## [0.1.0] - 2021-06-08
### Added
- created two files which use mainly the coding from `common_resources`:
  - macOS/Unix: `tooling_mac/wahoo-map-creator-osmium-using-common.py`
  - Windows:    `tooling_windows/Windows-Wahoo-Map-Creator-Osmosis/wahoo-map-creator-osmosis-using-common.py`
- `common_resources`: directory for common coding & resources #8
  - with folders for resources and files generally needed 
  - with extracted common coding from these two files
    - macOS/Unix: `tooling_mac/wahoo-map-creator-osmium-working.py`
    - Windows:    `tooling_windows/Windows-Wahoo-Map-Creator-Osmosis/wahoo-map-creator-osmosis.py`


[unreleased]: https://github.com/treee111/wahooMapsCreator/compare/v0.8.1...HEAD
[0.8.1]: https://github.com/treee111/wahooMapsCreator/compare/v0.8.0...v0.8.1
[0.8.0]: https://github.com/treee111/wahooMapsCreator/compare/v0.7.1...v0.8.0
[0.7.1]: https://github.com/treee111/wahooMapsCreator/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/treee111/wahooMapsCreator/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/treee111/wahooMapsCreator/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/treee111/wahooMapsCreator/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/treee111/wahooMapsCreator/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/treee111/wahooMapsCreator/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/treee111/wahooMapsCreator/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/treee111/wahooMapsCreator/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/treee111/wahooMapsCreator/releases/tag/v0.1.0