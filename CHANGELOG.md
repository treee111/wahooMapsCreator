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

## [0.5.0] - 2021-07-04
### Added
- Parameter to control download and processing of border countries or not #18
- unittests for downloader.py and osm_maps_functions.py files #16
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


[unreleased]: https://github.com/treee111/wahooMapsCreator/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/treee111/wahooMapsCreator/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/treee111/wahooMapsCreator/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/treee111/wahooMapsCreator/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/treee111/wahooMapsCreator/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/treee111/wahooMapsCreator/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/treee111/wahooMapsCreator/releases/tag/v0.1.0