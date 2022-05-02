# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

A list of unreleased changes can be found [here](https://github.com/treee111/wahooMapsCreator/compare/v1.1.1...HEAD).

<a name="1.1.1"></a>
## [1.1.1] - 2022-05-02
### Bug Fixes
- country & regions constants and mapping ([#113](https://github.com/treee111/wahooMapsCreator/issues/113)) [`e45d89c`](https://github.com/treee111/wahooMapsCreator/commit/e45d89c204e915412fb6c7104b12e3ae275acf69)


<a name="1.1.0"></a>
## [1.1.0] - 2022-03-18
### Features
- **CI/CD:** create OS-specific .zip files during build for release .zip files, separate cruiser.zip Asset and delete unused files ([#90](https://github.com/treee111/wahooMapsCreator/issues/90)) [`c3cd530`](https://github.com/treee111/wahooMapsCreator/commit/c3cd530767931d7246cc616573cf646923846e82)
- **install:** move work-directories `common_download` and `output` to level of wahooMapsCreator to be release independent ([#93](https://github.com/treee111/wahooMapsCreator/issues/93)) [`c33fefe`](https://github.com/treee111/wahooMapsCreator/commit/c33fefedb93a4b17d76485e37110ec3fa3106ea6)

### Bug Fixes
- copy version files to map archive ([#92](https://github.com/treee111/wahooMapsCreator/issues/92)) [`e50c1b7`](https://github.com/treee111/wahooMapsCreator/commit/e50c1b791e97642908fef6ebc0f0b57a7ce6ca49)
- Release all dist/*.zip files as Assets (also cruiser!) and include moved files (corrects [#90](https://github.com/treee111/wahooMapsCreator/issues/90)) ([#97](https://github.com/treee111/wahooMapsCreator/issues/97)) [`4fb49f6`](https://github.com/treee111/wahooMapsCreator/commit/4fb49f62c3ddf8640c5a20eae509292d7849f720)
- **Windows:** use (official) 32bit or 64bit osmconvert.exe ([#91](https://github.com/treee111/wahooMapsCreator/issues/91)) [`187e4ac`](https://github.com/treee111/wahooMapsCreator/commit/187e4ac47a8f11ce4c9d35768e43acdb44ab34e4)

### Development/Infrastructure/Test/CI
- **docu:** remove not needed install steps and clarify installation (macOS/ Windows) [`9e1a00b`](https://github.com/treee111/wahooMapsCreator/commit/9e1a00b74bbfa0e1704742f5f6463f7ed29acf87)
- **docu:** Anaconde outside of repo, do not collapse in QUICKSTART_ANACONDA.md ([#98](https://github.com/treee111/wahooMapsCreator/issues/98)) [`ea732f7`](https://github.com/treee111/wahooMapsCreator/commit/ea732f7af4368e4f0b0f98dc36f1e9bd3be4e3d9)


<a name="1.0.0"></a>
## [1.0.0] - 2022-01-19
### Features
- **install:** Make Anaconda environment very easy to setup ([#82](https://github.com/treee111/wahooMapsCreator/issues/82)) [`14b9161`](https://github.com/treee111/wahooMapsCreator/commit/14b9161c8fb2db0a8a730157e01e72f89df9c5d0)
- **docu:** Update & refactor README and install-docu for setting up Anaconda environment ([#84](https://github.com/treee111/wahooMapsCreator/issues/84)) [`07dbeea`](https://github.com/treee111/wahooMapsCreator/commit/07dbeea241c2078e8fb17b6ec5333d990b9844d6)

### Development/Infrastructure/Test/CI
- **unittest:** Update unittest files for Windows and macOS after sharpening Anaconda environment ([#83](https://github.com/treee111/wahooMapsCreator/issues/83)) [`5ed0375`](https://github.com/treee111/wahooMapsCreator/commit/5ed0375f847358ac112474acb6541708564dff27)

### BREAKING CHANGE

The recommendation for the initial setup is now to create a virtual Python environment via Anaconda on Windows, macOS or Linux. Installing multiple programs manually with all setup details and problems now belongs to the past.

wahooMapsCreator can now be used much quicker and easier!


<a name="0.12.0"></a>
## [0.12.0] - 2022-01-16
### Bug Fixes
- **macOS:** Support osmosis-tool v1.13.2 by sorting land* osm files before merging ([#78](https://github.com/treee111/wahooMapsCreator/issues/78)) [`e599294`](https://github.com/treee111/wahooMapsCreator/commit/e599294b29c28bd87da310d9777c6b77baca7c6d)
- **Make paths for zip files identical on different OS:** macOS and Windows ([#79](https://github.com/treee111/wahooMapsCreator/issues/79)) [`85c8a36`](https://github.com/treee111/wahooMapsCreator/commit/85c8a361b2ea4fd40be8adbf068f2cdc3c3b7759)

### Development/Infrastructure/Test/CI
- Update and clarify README & documentation & git files ([#81](https://github.com/treee111/wahooMapsCreator/issues/81)) [`9d1c40d`](https://github.com/treee111/wahooMapsCreator/commit/9d1c40def1f666550913c0c72e744525350066b2)
- **CI/CD:** update Pre-Release workflow to create unreleased "latest" release on commit on "release-*" [`99d9102`](https://github.com/treee111/wahooMapsCreator/commit/99d91024adb4f44414cf0debb69b379c2c9d84cd)
- **CI/CD:** Add requirements.txt to build .zip [`aaf6a40`](https://github.com/treee111/wahooMapsCreator/commit/aaf6a408ffc293b035671e0eeff1f665442f852e)


<a name="0.11.0"></a>
## [0.11.0] - 2021-12-10
### Features
- Refactor downloader.py ([#66](https://github.com/treee111/wahooMapsCreator/issues/66)) [`4bb80a1`](https://github.com/treee111/wahooMapsCreator/commit/4bb80a106815e8a662ea3b5e8cc460d9cb1bd61d)
- Calculation of tiles using Geofabrik-URL instead of static json ([#68](https://github.com/treee111/wahooMapsCreator/issues/68)) [`cee0089`](https://github.com/treee111/wahooMapsCreator/commit/cee00891f1c9244cb18d6c828927472738ad68e1)
- Add Dataline checks and checks for (sub-) regions ([#69](https://github.com/treee111/wahooMapsCreator/issues/69)) [`e0773c5`](https://github.com/treee111/wahooMapsCreator/commit/e0773c5e9b2c659e81f302cfaae09f8e261ea8fa)
- Enhance GUI with tabs for all possible arguments ([#74](https://github.com/treee111/wahooMapsCreator/issues/74)) [`243aa53`](https://github.com/treee111/wahooMapsCreator/commit/243aa532ade57401430777faf65c35b31678a6d1)
- Create one function make_and_zip_files from two existing ones ([#76](https://github.com/treee111/wahooMapsCreator/issues/76)) [`4223dc1`](https://github.com/treee111/wahooMapsCreator/commit/4223dc13851cf25179456ffe654be95a7e9b570f)

### Bug Fixes
- Reflect [#44](https://github.com/treee111/wahooMapsCreator/issues/44) also in Github Release .zip file [`c03abea`](https://github.com/treee111/wahooMapsCreator/commit/c03abea286f792ef4cd75ed64367e95a22b8fd20)
- make "filter_tags" overwrite existing files on macOS [`bc7f2c3`](https://github.com/treee111/wahooMapsCreator/commit/bc7f2c39606b68e86dae1cb4724218d38be91ce0)
- Prevent initialisation of the graphical GUI on WSL ([#72](https://github.com/treee111/wahooMapsCreator/issues/72)) [`2a64a17`](https://github.com/treee111/wahooMapsCreator/commit/2a64a179c92b21384242b8d4e99ffae75fe4600c)
- Process GUI / tk coding only if running in GUI mode ([#73](https://github.com/treee111/wahooMapsCreator/issues/73)) [`3c5cbe3`](https://github.com/treee111/wahooMapsCreator/commit/3c5cbe34c020401742e23a6d3c54892c98654616)

### Development/Infrastructure/Test/CI
- Update unittest files for Windows and macOS / use defined static land_polygons / refactor unittest ([#65](https://github.com/treee111/wahooMapsCreator/issues/65)) [`8845173`](https://github.com/treee111/wahooMapsCreator/commit/8845173901ceaf3ab9b2287137089b03b0231aad)
- Setup Dev/Run environment using Anaconda ([#67](https://github.com/treee111/wahooMapsCreator/issues/67)) [`858d890`](https://github.com/treee111/wahooMapsCreator/commit/858d890b07d64da42917028679707a2f6435c370)


<a name="0.10.0"></a>
## [0.10.0] - 2021-10-30
### Features
- Add check for required input parameter for CLI and GUI ([#41](https://github.com/treee111/wahooMapsCreator/issues/41)) [`4994f13`](https://github.com/treee111/wahooMapsCreator/commit/4994f13b6ae150faaeaf4586ec7b8232fa7b095e)
- Enhance check for existing (already downloaded) polygons and .osm.pbf files ([#43](https://github.com/treee111/wahooMapsCreator/issues/43)) [`bbdedd1`](https://github.com/treee111/wahooMapsCreator/commit/bbdedd176bc119b143a55f639641367e1275533f)
- Create Wahoo tile present/version indicator files like 84.map.lzma.v12 ([#49](https://github.com/treee111/wahooMapsCreator/issues/49)) [`2b4adb0`](https://github.com/treee111/wahooMapsCreator/commit/2b4adb019295abad1c6b4096ad43ce0b1ed2310e)
- Performance improvement for .osm.pbf creation and splitting. Use 'v12' tag (keep) filters ([#46](https://github.com/treee111/wahooMapsCreator/issues/46)) [`cef537b`](https://github.com/treee111/wahooMapsCreator/commit/cef537b46bd7a6c1c4a2a824f385d17415a454a8)
- Change creation of tiles.zip and maps.zip to support very large countries ([#47](https://github.com/treee111/wahooMapsCreator/issues/47)) [`2e20d51`](https://github.com/treee111/wahooMapsCreator/commit/2e20d51e0449a26b9f7aad121607d4b06a122cf0)

### Bug Fixes
- Storing and interpretation of CLI arguments ([#48](https://github.com/treee111/wahooMapsCreator/issues/48)) [`81fe795`](https://github.com/treee111/wahooMapsCreator/commit/81fe795eb693178381b30d41624fe191fc83a6c0)
- Update osmosis distribution with official 0.48.3 version to fix osmosis permissions ([#42](https://github.com/treee111/wahooMapsCreator/issues/42)) [`9379fb1`](https://github.com/treee111/wahooMapsCreator/commit/9379fb1e32619768814dc254a5ef94d47ce6cc07)
- Clean-up and unify output logging ([#52](https://github.com/treee111/wahooMapsCreator/issues/52)) [`6a0b9eb`](https://github.com/treee111/wahooMapsCreator/commit/6a0b9eb186ba2b88f566c1ea7cc5ff6b8c955af4)
- Fix keep_map_folders CLI argument handling ([#57](https://github.com/treee111/wahooMapsCreator/issues/57)) [`b8f187c`](https://github.com/treee111/wahooMapsCreator/commit/b8f187c50ac2bb2904aca3bd4f33a5674e2d1a7b)
- uniform Windows and macOS processing in filter_tags_from_country_osm_pbf_files ([#63](https://github.com/treee111/wahooMapsCreator/issues/63)) [`1a87ce1`](https://github.com/treee111/wahooMapsCreator/commit/1a87ce189c92ec21a270400decb0758d9520cbe5)

### Development/Infrastructure/Test/CI
- Automate CHANGELOG.md creation using git-chglog ([#45](https://github.com/treee111/wahooMapsCreator/issues/45)) [`23b8927`](https://github.com/treee111/wahooMapsCreator/commit/23b8927d3cf246538640ab4346e88f41b60fe90b)
- gitignore any work directories and create them during processing if necessary ([#44](https://github.com/treee111/wahooMapsCreator/issues/44)) [`33d5821`](https://github.com/treee111/wahooMapsCreator/commit/33d5821b18cf94bf0ef2793129bbc35878f5fe39)
- Update Github templates for issues and pull requests ([#50](https://github.com/treee111/wahooMapsCreator/issues/50)) [`b68fbd2`](https://github.com/treee111/wahooMapsCreator/commit/b68fbd225d2d8542550826f2ac0452c9be7d196a)
- Define sort-sequence of CHANGELOG entries ([#54](https://github.com/treee111/wahooMapsCreator/issues/54)) [`e47947e`](https://github.com/treee111/wahooMapsCreator/commit/e47947ebb6cd52636dfb9177db32dc30fa703612)
- Unittests for malta and liechtenstein. Check output per tile for files in tests/resources ([#56](https://github.com/treee111/wahooMapsCreator/issues/56)) [`55c47db`](https://github.com/treee111/wahooMapsCreator/commit/55c47dbac9b8b77dbc097e63afa30672ab9f08e7)
- Unify zipping & integrate last bits of PR-40 ([#55](https://github.com/treee111/wahooMapsCreator/issues/55)) [`7f2108c`](https://github.com/treee111/wahooMapsCreator/commit/7f2108c0bfc5e7db68831bbfd88a936ed6de16bb)
- Have separate files for Windows and macOS for unittests output per tile / malta and liechtenstein ([#62](https://github.com/treee111/wahooMapsCreator/issues/62)) [`28787b3`](https://github.com/treee111/wahooMapsCreator/commit/28787b3009221dea7ee550895840f509272411c0)

## [0.9.0] - 2021-10-19
### Added
- have more different tag-wahoo-xml files and move them to folders. Modify tag-wahoo.xml to differently display some "place"-tags [PR34](https://github.com/treee111/wahooMapsCreator/issues/34)
- tag-wahoo-v12.xml which is a updated version of the current tag-wahoo-hidrive2.xml. Bus_guideways have been removed and the zoom-appear levels are copied from the original wahoo maps. This really should replace tag-wahoo.xml eventually when v12 maps are created. [PR38](https://github.com/treee111/wahooMapsCreator/pull/38)
- Howto doc for manually adding routing tiles [PR32](https://github.com/treee111/wahooMapsCreator/pull/32)
### Changed
- move "central" download functions from downloader to file_directory_functions
- move files from common_resources into two new folders: common_download & common_python and into tooling [PR33](https://github.com/treee111/wahooMapsCreator/pull/33)
- format python files in directory common_python using "autopep8" [PR35](https://github.com/treee111/wahooMapsCreator/pull/35) [PR37](https://github.com/treee111/wahooMapsCreator/pull/37)
- Replaced the publicly available osmconvert.exe (https://wiki.openstreetmap.org/wiki/Osmconvert) 0.8.8 with a special newer version 0.8.10. This version does NOT include the zlib library which enables processing of .osm.pbf files larger then 4GB on windows. The old version did have zlib which prevented processing of > 4Gb .osm.pbf files on windows. [PR38](https://github.com/treee111/wahooMapsCreator/pull/38)
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


[1.1.1]: https://github.com/treee111/wahooMapsCreator/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/treee111/wahooMapsCreator/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/treee111/wahooMapsCreator/compare/v0.12.0...v1.0.0
[0.12.0]: https://github.com/treee111/wahooMapsCreator/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/treee111/wahooMapsCreator/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/treee111/wahooMapsCreator/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/treee111/wahooMapsCreator/compare/v0.8.1...v0.9.0
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
