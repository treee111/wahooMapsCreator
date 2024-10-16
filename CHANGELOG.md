# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

A list of unreleased changes can be found [here](https://github.com/treee111/wahooMapsCreator/compare/v4.3.0...HEAD).

<a name="4.3.0"></a>
## [4.3.0] - 2024-10-16
### Features
- remove coding handling breaking changes and unused function ([#256](https://github.com/treee111/wahooMapsCreator/issues/256)) [`43e07b4`](https://github.com/treee111/wahooMapsCreator/commit/43e07b4ffb0517eed5d53b9177c0d7dd76b8e8a3)

### Bug Fixes
- make mapwriter download URL OS independent [`e5d19bd`](https://github.com/treee111/wahooMapsCreator/commit/e5d19bdc52c322910635dfb55bb6a19040cc3e63)
- **Windows:** Download Osmosis into in `Osmosis` and not into subfolder, example `Osmosis/osmosis-0.49.2` ([#261](https://github.com/treee111/wahooMapsCreator/issues/261)) [`913d12d`](https://github.com/treee111/wahooMapsCreator/commit/913d12d1248c50348543646db63abf2b2cf061e3)
- **Windows:** adjust location of mapwriter plugin ([#262](https://github.com/treee111/wahooMapsCreator/issues/262)) [`cebf925`](https://github.com/treee111/wahooMapsCreator/commit/cebf92573c429f52ee0684e06f93a29010c36b21)

### Development/Infrastructure/Test/CI
- Create LICENSE file ([#257](https://github.com/treee111/wahooMapsCreator/issues/257)) [`827f464`](https://github.com/treee111/wahooMapsCreator/commit/827f464c60652d2f3c11f47236703a9cea4f44ee)


<a name="4.2.0"></a>
## [4.2.0] - 2024-09-12
### Features
- Add logging of timing for total time, each main section and for each tile generation step ([#225](https://github.com/treee111/wahooMapsCreator/issues/225)) [`e5baae0`](https://github.com/treee111/wahooMapsCreator/commit/e5baae02758f16588fb3ced857dec1928120c149)
- Use proper tool name in error message, reference Osmium or osmconvert ([#232](https://github.com/treee111/wahooMapsCreator/issues/232)) [`41fdbf7`](https://github.com/treee111/wahooMapsCreator/commit/41fdbf7be4e18d923258b8796d16707de211e675)

### Bug Fixes
- include elevation data only if requested by the user, i.e. if `-con` is given ([#223](https://github.com/treee111/wahooMapsCreator/issues/223)) [`4b53962`](https://github.com/treee111/wahooMapsCreator/commit/4b53962cddbd3a3aa2ed1d312e3a396ff9a93489)
- Return error code of failed subprocess instead of success (which is the default) ([#254](https://github.com/treee111/wahooMapsCreator/issues/254)) [`85b8617`](https://github.com/treee111/wahooMapsCreator/commit/85b86176c7b74f5ef35ef6e147eeb2106b9c9b84)
- Draw highways/streets over paths in VTM theme ([#250](https://github.com/treee111/wahooMapsCreator/issues/250)) [`083f247`](https://github.com/treee111/wahooMapsCreator/commit/083f247ba23bfa0dfb4d283ffb3f177e87130faf)
- Fix invalid color for bolt2-track-raw-cycle ways in VTM theme ([#242](https://github.com/treee111/wahooMapsCreator/issues/242)) [`494b772`](https://github.com/treee111/wahooMapsCreator/commit/494b7728dfdc8bdce71cc7e938cb5936e0b28083)

### Development/Infrastructure/Test/CI
- Fix unittests ([#222](https://github.com/treee111/wahooMapsCreator/issues/222)) [`04f09ac`](https://github.com/treee111/wahooMapsCreator/commit/04f09ac4dcd24c26e27bba278196e66ed4918b35)
- remove deprecated linting settings ([#226](https://github.com/treee111/wahooMapsCreator/issues/226)) [`199a13e`](https://github.com/treee111/wahooMapsCreator/commit/199a13ee9cb9d5216f9bca6594d457fda9090b2a)
- move OsmData classes from osm_maps_functions.py to osm_data.py ([#233](https://github.com/treee111/wahooMapsCreator/issues/233)) [`ad2828e`](https://github.com/treee111/wahooMapsCreator/commit/ad2828edbad9e21288f8b1fc7c5edb4a5add45ec)
- Update dependencies osmosis and mapwriter plugin incl. documenation ([#236](https://github.com/treee111/wahooMapsCreator/issues/236)) [`f15aa86`](https://github.com/treee111/wahooMapsCreator/commit/f15aa860050a5d3f77af75904b20ee9ee01f56e4)
- unify logging of searching for needed maps [`26a7eaf`](https://github.com/treee111/wahooMapsCreator/commit/26a7eaf19fb4821d096464584285c3bee22ac751)
- update dependency mapwriter plugin from 0.20.0 to 0.21.0 ([#255](https://github.com/treee111/wahooMapsCreator/issues/255)) [`c39294f`](https://github.com/treee111/wahooMapsCreator/commit/c39294fe7bcf2b9c2160e16ff94b37b305b87013)
- Update osmium-tool in developer env [`d817bc7`](https://github.com/treee111/wahooMapsCreator/commit/d817bc7e54f48bd059baca977d9b4bcf1233f0ba)


<a name="4.1.1"></a>
## [4.1.1] - 2023-11-17
### Bug Fixes
- cut down folder_name to 50 to not crash when creating output folder ([#228](https://github.com/treee111/wahooMapsCreator/issues/228)) [`866bbaa`](https://github.com/treee111/wahooMapsCreator/commit/866bbaadee1ff4a8ca884f43d091911e39b1af2e)


<a name="4.1.0"></a>
## [4.1.0] - 2023-07-11
### Features
- Include amenity/shelter and tourism/alpine_hut ([#206](https://github.com/treee111/wahooMapsCreator/issues/206)) [`b8f4d16`](https://github.com/treee111/wahooMapsCreator/commit/b8f4d1635175f680aa16044088568ca3efb6aada)

### Bug Fixes
- Use process.run instead of process.Popen to avoid deadlock ([#208](https://github.com/treee111/wahooMapsCreator/issues/208)) [`5e29dc1`](https://github.com/treee111/wahooMapsCreator/commit/5e29dc1ede9138c7b4976507977b41c5a9a83d89)
- Search for existing elevation data based on requested type [`b49330a`](https://github.com/treee111/wahooMapsCreator/commit/b49330a78acb80b9d0534a9db2fcdb4ddcfdad21)
- Log calculation of border countries based on argument [`b6fd62d`](https://github.com/treee111/wahooMapsCreator/commit/b6fd62d5414b154527b14a25796e94d0b9be1de2)


<a name="4.0.2"></a>
## [4.0.2] - 2023-05-06
### Features
- **option to choose source for contour lines:** view1 (standard) and srtm1 ([#204](https://github.com/treee111/wahooMapsCreator/issues/204)) [`400dfc4`](https://github.com/treee111/wahooMapsCreator/commit/400dfc4ebf29dfe86508bcaf12961863154ac555)


<a name="4.0.1"></a>
## [4.0.1] - 2023-05-05
### Bug Fixes
- use srtm1 data to see even more contour lines + upgrade GDAL from 3.4 to 3.6 ([#203](https://github.com/treee111/wahooMapsCreator/issues/203)) [`5eec788`](https://github.com/treee111/wahooMapsCreator/commit/5eec7889d73219b128fffdf61a72a863885ef1b6)


<a name="4.0.0"></a>
## [4.0.0] - 2023-05-05
### Breaking Changes
- Upgrade required Python version to 3.11, upgrade packages GDAL to 3.6 and autopep8 to 2.0 ([#166](https://github.com/treee111/wahooMapsCreator/issues/166)) [`afb3d1e`](https://github.com/treee111/wahooMapsCreator/commit/afb3d1e6f01f351bbe2eca532b6942ee447610ee)
- X/Y input via geofabrik .json + only support processing maps via geofabrik .json, delete `wahoomc/resources/json/` files, constants and related coding ([#183](https://github.com/treee111/wahooMapsCreator/issues/183)) [`0d62840`](https://github.com/treee111/wahooMapsCreator/commit/0d62840aacdadb99e99355738b89d47e84c551e0)
- Downgrade required Python version to 3.10 ([#187](https://github.com/treee111/wahooMapsCreator/issues/187)) [`70c0395`](https://github.com/treee111/wahooMapsCreator/commit/70c0395fe1dfa60c5d336359a0903b5e84110e4e)

### Features
- update documentation ([#175](https://github.com/treee111/wahooMapsCreator/issues/175)) [`008e0b5`](https://github.com/treee111/wahooMapsCreator/commit/008e0b574db0d60b81fe470bdb5a503eda73ec84)
- **macOS:** Download mapwriter plugin during usage instead of manually copying during setup ([#177](https://github.com/treee111/wahooMapsCreator/issues/177)) [`1119db5`](https://github.com/treee111/wahooMapsCreator/commit/1119db59110a2866f387d0b664ce57ba13f4fd1a)
- Add a FAQ entry about routing tiles for device routing ([#191](https://github.com/treee111/wahooMapsCreator/issues/191)) [`ca0261a`](https://github.com/treee111/wahooMapsCreator/commit/ca0261a400461e1d11850bddac51743675308659)
- Allow processing of multiple countries via CLI ([#190](https://github.com/treee111/wahooMapsCreator/issues/190)) [`ddbe61e`](https://github.com/treee111/wahooMapsCreator/commit/ddbe61e6ed3028bd82102848d49e4a60bac67759)
- Integrate contour lines (elevation) into generated maps with argument `-con` ([#188](https://github.com/treee111/wahooMapsCreator/issues/188)) [`0078845`](https://github.com/treee111/wahooMapsCreator/commit/0078845990584a4d43a283be6e66ac3745b8a7df)
- Include waterway/canal in tag-wahoo-poi.xml ([#199](https://github.com/treee111/wahooMapsCreator/issues/199)) [`d7b771b`](https://github.com/treee111/wahooMapsCreator/commit/d7b771b503fc7ecf0ddc8192049bb29a247180aa)
- Include waterway/stream in tags-to-keep.json ([#201](https://github.com/treee111/wahooMapsCreator/issues/201)) [`f6a4b99`](https://github.com/treee111/wahooMapsCreator/commit/f6a4b997f44c075d56e42525a635a12fdb55ed04)

### Bug Fixes
- default to BOLT_2 in VTM theme. With new firmware-releases BOLTv1 act asl BOLT_2 [`16a1586`](https://github.com/treee111/wahooMapsCreator/commit/16a1586e4328c35f4c8fd46c095a06643d302e1e)
- Do not use geofabrik .json file before geofabrik .json file has been downloaded ([#192](https://github.com/treee111/wahooMapsCreator/issues/192)) [`badef50`](https://github.com/treee111/wahooMapsCreator/commit/badef5096643c566c624c325a8ba4aee2ff9084c)
- install shapely and requests via conda instead of pip. For processing geofabrik.json with shapely on Windows ([#193](https://github.com/treee111/wahooMapsCreator/issues/193)) [`c84c3e0`](https://github.com/treee111/wahooMapsCreator/commit/c84c3e011717308803ebaa52c360bd8fb5c19fc8)

### Development/Infrastructure/Test/CI
- **macOS:** Check .osm.pbf files in unittests with `osmium diff` (due to osmium-tool upgrade) ([#176](https://github.com/treee111/wahooMapsCreator/issues/176)) [`2906a56`](https://github.com/treee111/wahooMapsCreator/commit/2906a567c7084a6b604efd4c56efc4459fdd69c5)
- enable Github action to update `latest` release ([#178](https://github.com/treee111/wahooMapsCreator/issues/178)) [`f4143fc`](https://github.com/treee111/wahooMapsCreator/commit/f4143fc7bff030be48d85794f0bb7f0c1dcf8831)
- Fix unittest, add v3 to v4 migration to FAQ, delete unused class attribute (seen during implementation of release v4.0.0) ([#180](https://github.com/treee111/wahooMapsCreator/issues/180)) [`99ed025`](https://github.com/treee111/wahooMapsCreator/commit/99ed025ad50fd3a627bf5fc232139bbc0150d6e9)
- adjust dependencies by implementing pydeps adjustments ([#184](https://github.com/treee111/wahooMapsCreator/issues/184)) [`2e66c50`](https://github.com/treee111/wahooMapsCreator/commit/2e66c50f705cfcc4471d47af5aaa6170707a9fc7)
- Use geofabrik .json for countries and regions for internal processing (from former `constants.py` and `wahoomc/resources/json`) ([#182](https://github.com/treee111/wahooMapsCreator/issues/182)) [`8632fbf`](https://github.com/treee111/wahooMapsCreator/commit/8632fbf1373ff586bc66c085cc4d226c6866e4d7)
- **unittests:** compare map files with osmium in Windows, park static files, have static geofabrik .json ([#186](https://github.com/treee111/wahooMapsCreator/issues/186)) [`f400f89`](https://github.com/treee111/wahooMapsCreator/commit/f400f89df0dfa3935af64cbb1a658aa07bef6c8f)
- refactor osm_maps_functions.py like geofabrik.py - using a interface and two implementing classes ([#194](https://github.com/treee111/wahooMapsCreator/issues/194)) [`aa5b541`](https://github.com/treee111/wahooMapsCreator/commit/aa5b5416bb4503b15041075ff89d2f09943da63c)
- detail logging of subsprocesses, unify logging (tile progress, country config file) ([#195](https://github.com/treee111/wahooMapsCreator/issues/195)) [`97b4da6`](https://github.com/treee111/wahooMapsCreator/commit/97b4da6777072b643cb10dca79025b3bb6230995)
- **refactor coding:** do/remove checks, adjust exceptions, cleanup coding ([#196](https://github.com/treee111/wahooMapsCreator/issues/196)) [`0474978`](https://github.com/treee111/wahooMapsCreator/commit/04749789d68d3ce4751b78fe507f3e2eb0ef1361)

### BREAKING CHANGE

Processing is now only based on Geofabrik .json file which is downloaded both for country and X/Y input. The static country .json files and the whole implementation has been removed.
`-gt` input argument was also removed because there is only one processing method implemented.
Input should now be in Geofabrik style. The hardcoded translation to geofabrik countries has been removed.
The size of generated maps for X/Y coordinates should remain exactly the same as before. The size of generated maps for countries should roughly be the same as before.

You need to create a new Anaconda environment with Python v3.11 for this versino. These are the steps: 
1. Remove existing environment:
`conda env remove -n gdal-user`
2. Create new environment and install wahoomc:
```
conda create -n gdal-user python=3.11 geojson=2.5 gdal=3.6 pip --channel conda-forge --override-channels
conda activate gdal-user
pip install wahoomc
```


<a name="3.2.0"></a>
## [3.2.0] - 2022-11-29
### Features
- **install:** Download Osmosis and Osmfilter on Windows during first run instead of shipping with the tool ([#167](https://github.com/treee111/wahooMapsCreator/issues/167)) [`ae4eb1f`](https://github.com/treee111/wahooMapsCreator/commit/ae4eb1f6b4ff3f75aa81da4243d4ebd16c317e01)
- **install:** Check installed version against latest published version on PyPI ([#173](https://github.com/treee111/wahooMapsCreator/issues/173)) [`08e00c3`](https://github.com/treee111/wahooMapsCreator/commit/08e00c31f7029ee47f18eded00aec2a0b910538f)

### Bug Fixes
- Raise max. memory for Osmosis in Windows to 3GB ([#171](https://github.com/treee111/wahooMapsCreator/issues/171)) [`2be33bd`](https://github.com/treee111/wahooMapsCreator/commit/2be33bdbfa9519da0eeb7ed2b51d76b77e4b9729)


<a name="3.1.1"></a>
## [3.1.1] - 2022-11-15
### Bug Fixes
- publish device themes as zip [`a5afd6e`](https://github.com/treee111/wahooMapsCreator/commit/a5afd6e0edd52de741e9a1678af799f1a331a1f0)
- Include wahoomc.init module in published PyPI version ([#172](https://github.com/treee111/wahooMapsCreator/issues/172)) [`b4da480`](https://github.com/treee111/wahooMapsCreator/commit/b4da480d7f82b2a2dc2b839157568a025778a05d)


<a name="3.1.0"></a>
## [3.1.0] - 2022-11-14
### Features
- correctly integrate tunnels to maps in macOS (in the same way as in Windows) ([#165](https://github.com/treee111/wahooMapsCreator/issues/165)) [`7d5520b`](https://github.com/treee111/wahooMapsCreator/commit/7d5520b4c1fc2597e83bb6a1913053b2fdf874a4)
- possibility to verbose output with -v in CLI and GUI [`9075b43`](https://github.com/treee111/wahooMapsCreator/commit/9075b43689bdd7c034e3c221b3c0c10e47c2012a)
- save timestamp of last-changed of raw map files being processed [`a29fd99`](https://github.com/treee111/wahooMapsCreator/commit/a29fd990e0fb00dd8ed34d20ae1efede1ff6f437)
- Read tag-wahoo.xml and tags-to-keep.json from user directory first (from python module as fallback) ([#170](https://github.com/treee111/wahooMapsCreator/issues/170)) [`fd23b8a`](https://github.com/treee111/wahooMapsCreator/commit/fd23b8a6d558c2c6e9611803b18e16a8854117a6)

### Bug Fixes
- write tags per OS & include name-tags [`4ec269e`](https://github.com/treee111/wahooMapsCreator/commit/4ec269e3555c246679c849c0cf4d885465d17cd5)
- Enable canary islands processing. Mapping in constants.py and movement of .json content ([#169](https://github.com/treee111/wahooMapsCreator/issues/169)) [`88a51ec`](https://github.com/treee111/wahooMapsCreator/commit/88a51ec0cdb1f2363fd0f7994b9c1e2dd64f412c)
- Enable ukraine processing. Mapping in constants.py [`a4f94ea`](https://github.com/treee111/wahooMapsCreator/commit/a4f94eabb3f43e7b4f75f177883336eebb904c33)
- harmonize logging of "merging splitted tiles" with the rest [`5ba0c22`](https://github.com/treee111/wahooMapsCreator/commit/5ba0c223d0890343f084ab1bc9783e16042a1c88)
- correctly compare the version of last run. fix for [#161](https://github.com/treee111/wahooMapsCreator/issues/161) [`d9893d7`](https://github.com/treee111/wahooMapsCreator/commit/d9893d76a9462deef136a47eca08c816cdc85035)

### Development/Infrastructure/Test/CI
- remove copying and remove deprecated files [#148](https://github.com/treee111/wahooMapsCreator/issues/148) [`3472a25`](https://github.com/treee111/wahooMapsCreator/commit/3472a253e2f24b083f8a465fc3e9cb5cce24927c)
- remove argument `-om` [`60e0019`](https://github.com/treee111/wahooMapsCreator/commit/60e00195bd08de7aa4bdadc6d946f3e0dc4fa6f2)
- don't publish wahooMapsCreator as .zip and don't mention in docs [`24bfef9`](https://github.com/treee111/wahooMapsCreator/commit/24bfef93e63552bd4474f8049ce4eb0c80aac912)
- Fix unittests & update unittest files after changes of release v3.0.0 ([#164](https://github.com/treee111/wahooMapsCreator/issues/164)) [`b473a97`](https://github.com/treee111/wahooMapsCreator/commit/b473a975deb62c7bcea55ee2a5b6e6fc75794d78)

### BREAKING CHANGE

Users who downloaded the .zip files from the release page should migrate to the PyPI version and update the python module accordingly.


<a name="3.0.0"></a>
## [3.0.0] - 2022-11-01
### Breaking Changes
- Remove argument `-km` (keep_map_folders) ([#140](https://github.com/treee111/wahooMapsCreator/issues/140)) [`b6157ab`](https://github.com/treee111/wahooMapsCreator/commit/b6157ab338a2963778c10e08532c24440240fb97)
- Process coding that can be influenced by user-input without `-fp` - speeds up playing with tags ([#150](https://github.com/treee111/wahooMapsCreator/issues/150)) [`71161c1`](https://github.com/treee111/wahooMapsCreator/commit/71161c12ecc769a4240cd2fec6fb71673fcecd71)
- By default include POI's into generated maps ([#151](https://github.com/treee111/wahooMapsCreator/issues/151)) [`15b9e26`](https://github.com/treee111/wahooMapsCreator/commit/15b9e26365a85eb2abf8ea38b97da80e81e4372d)

### Features
- Check for required programs at wahooMapsCreator start ([#127](https://github.com/treee111/wahooMapsCreator/issues/127)) [`bcb2dc0`](https://github.com/treee111/wahooMapsCreator/commit/bcb2dc0a91983fbbf43a152740b53fa4ba7dc26d)

### Features
- Use `python` instead of `python3` to call `shape2osm.py` to be macOS Monterey/M1 compatible ([#131](https://github.com/treee111/wahooMapsCreator/issues/131)) [`c73bd8a`](https://github.com/treee111/wahooMapsCreator/commit/c73bd8addda364daa2be85394ca50fe7d9c73e93)
- Write v17 map tile indicator ([#138](https://github.com/treee111/wahooMapsCreator/issues/138)) [`58b7a12`](https://github.com/treee111/wahooMapsCreator/commit/58b7a12d303a40fefc897c20d8b1b1e41220c48a)
- Refactor getting tag-wahoo xml file, distinguish Osmosis errors, reset default logging level to INFO ([#141](https://github.com/treee111/wahooMapsCreator/issues/141)) [`1b5f89f`](https://github.com/treee111/wahooMapsCreator/commit/1b5f89f49554068cef0d0e9f2f874c939fe0c926)
- Refactor a lot to decouple and make maintenance easier (focus osm_maps_functions.py) ([#152](https://github.com/treee111/wahooMapsCreator/issues/152)) [`9810b6d`](https://github.com/treee111/wahooMapsCreator/commit/9810b6dd0b9fda6ec3f0121823091668e9b9fbf0)
- Rename variable names to make them more understandable. Restructure one for-loop ([#153](https://github.com/treee111/wahooMapsCreator/issues/153)) [`60c1c6c`](https://github.com/treee111/wahooMapsCreator/commit/60c1c6c5593fd5cc144ef861867bd7ecf95ce78d)
- Make logging uniformly and include variables into the message correctly ([#154](https://github.com/treee111/wahooMapsCreator/issues/154)) [`f59c138`](https://github.com/treee111/wahooMapsCreator/commit/f59c138d76405170d176b1f1af2f42172a408e4c)
- Filter country file if new new tags are being used // introduce country config file .config.json ([#162](https://github.com/treee111/wahooMapsCreator/issues/162)) [`9157286`](https://github.com/treee111/wahooMapsCreator/commit/91572865e55a883d924439e4e950fd528726a8f5)
- Add shop/bicycle POIs, show also "ways" POIs ([#158](https://github.com/treee111/wahooMapsCreator/issues/158)) [`30ee102`](https://github.com/treee111/wahooMapsCreator/commit/30ee1029f630ab5d77af11cac02948a75b85b6d6)

### Bug Fixes
- handle USA json country names via conversion of `_` to `-` ([#137](https://github.com/treee111/wahooMapsCreator/issues/137)) [`f235b8c`](https://github.com/treee111/wahooMapsCreator/commit/f235b8cbe8c78c1f3fb68e678e011ac6e49a96ee)
- Set timeout for file downloads to 30 minutes per file (pylint finding) ([#149](https://github.com/treee111/wahooMapsCreator/issues/149)) [`ce48d55`](https://github.com/treee111/wahooMapsCreator/commit/ce48d55dcba0b672184fcbb14d6a60edb686a0b6)
- handle threads as int and use f-typing to append it to cmd ([#147](https://github.com/treee111/wahooMapsCreator/issues/147)) [`3cdb75d`](https://github.com/treee111/wahooMapsCreator/commit/3cdb75de2c744b9baec65c51cd99b07e2d3d997e)

### Development/Infrastructure/Test/CI
- delete cruiser tooling and do not publish as .zip in a release [`a252202`](https://github.com/treee111/wahooMapsCreator/commit/a25220255cfa5227ba59a247c5494d782120f848)
- Update unittest files after changes of release v2.0.0 ([#124](https://github.com/treee111/wahooMapsCreator/issues/124)) [`e39f984`](https://github.com/treee111/wahooMapsCreator/commit/e39f9845a10e996b49eefb0381c7e532f5632a86)
- Refactor generated_files unittests ([#125](https://github.com/treee111/wahooMapsCreator/issues/125)) [`0bab7a9`](https://github.com/treee111/wahooMapsCreator/commit/0bab7a9d91b5f1728127e4df9ccdb68395d2a778)
- Refactor constants and setup functions ([#126](https://github.com/treee111/wahooMapsCreator/issues/126)) [`ce7d7a4`](https://github.com/treee111/wahooMapsCreator/commit/ce7d7a4b91d03f1a7474d093ef413c6b8a063cce)
- add FEAT commits to changelog [`ccbe03c`](https://github.com/treee111/wahooMapsCreator/commit/ccbe03c40b81c04d1e45b7ed2265446f407fc92c)
- Run pylint tests also on pull requests [`450073b`](https://github.com/treee111/wahooMapsCreator/commit/450073b641e3f479d447fc886f841623a4a30c40)
- **install:** Update python packages to latest minor release and delete unused environment files ([#148](https://github.com/treee111/wahooMapsCreator/issues/148)) [`47e0fb7`](https://github.com/treee111/wahooMapsCreator/commit/47e0fb7271cfc518f9cb585cce4da3a6fe1340f9)
- **CI/CD:** only run tests at push onto develop or PR's [`beee898`](https://github.com/treee111/wahooMapsCreator/commit/beee898b9720e88cbef728dec6792d6c08d1d563)
- **docu:** of copy-to-wahoo, installation, contribution ([#157](https://github.com/treee111/wahooMapsCreator/issues/157)) [`6ad9d6f`](https://github.com/treee111/wahooMapsCreator/commit/6ad9d6fc6a7d39a98d03fd173476adf800c59289)
- **install:** introduce config file .config.json // store python module version ([#161](https://github.com/treee111/wahooMapsCreator/issues/161)) [`00a9b92`](https://github.com/treee111/wahooMapsCreator/commit/00a9b928e6abc840bcdc3ba7f6c08e3130a86e86)
- Correct unittests of generated files for v3.0.0 changes ([#163](https://github.com/treee111/wahooMapsCreator/issues/163)) [`4aaf161`](https://github.com/treee111/wahooMapsCreator/commit/4aaf161fcffc415fd1630fb77d4d85a6020ec4df)

### BREAKING CHANGE

As most of the people use wahooMapsCreator to create maps including POI's, this is now golden standard without any arguments.

Coding that can be influenced by user-input is now processed without giving `-fp` and coding that can not be influenced is only re-procecced when issuing `-fp`. That speeds up playing with tags.

- argument `-km`, keep_map_folders does no longer exist
- either start the tool without the -zip argument or unzip the conpressed output after processing


<a name="2.0.2"></a>
## [2.0.2] - 2022-06-06
### Bug Fixes
- Use `latin-1` encoding as fallback if UnicodeDecodeError with `utf-8` ([#133](https://github.com/treee111/wahooMapsCreator/issues/133)) [`3d23b01`](https://github.com/treee111/wahooMapsCreator/commit/3d23b01f0a227616edb6a1a1ec855a5e324e4fc2)


<a name="2.0.1"></a>
## [2.0.1] - 2022-05-09
### Bug Fixes
- Correctly include directory tooling_win in .zip and via PyPI package ([#122](https://github.com/treee111/wahooMapsCreator/issues/122)) [`5779d73`](https://github.com/treee111/wahooMapsCreator/commit/5779d73b6d34b562676a80f7943a85888e880b3e)


<a name="2.0.0"></a>
## [2.0.0] - 2022-05-08
### Breaking Changes
- X/Y coordinates can be given as input parameters (e.g. for testing!) & refactoring of GUI & CLI processing ([#99](https://github.com/treee111/wahooMapsCreator/issues/99)) [`dabe117`](https://github.com/treee111/wahooMapsCreator/commit/dabe1171ddd543cada6fbf372a8a342cad720716)
- Remove primary CLI input option `-fi`, that is giving a json-file with tile(s). It is replaced by [#99](https://github.com/treee111/wahooMapsCreator/issues/99) ([#105](https://github.com/treee111/wahooMapsCreator/issues/105)) [`1ca469c`](https://github.com/treee111/wahooMapsCreator/commit/1ca469ca75455f6cf26c36cea24a4ed4ff406d72)
- default "process border countries" to yes in GUI and CLI ([#104](https://github.com/treee111/wahooMapsCreator/issues/104)) [`631b47d`](https://github.com/treee111/wahooMapsCreator/commit/631b47de395e7e540c0e9637b0cced5697e19175)

### Features
- restructure logging using logging-object, correct unittests & unittest-files ([#101](https://github.com/treee111/wahooMapsCreator/issues/101)) [`6026893`](https://github.com/treee111/wahooMapsCreator/commit/6026893467a8142072e9db8b53361dcbfe758387)
- update documentation ([#110](https://github.com/treee111/wahooMapsCreator/issues/110)) [`b09ba71`](https://github.com/treee111/wahooMapsCreator/commit/b09ba714c10d86cfcac5ba0238bcd232dc193d18)
- adjust BOLT device theme ([#111](https://github.com/treee111/wahooMapsCreator/issues/111)) [`f2337b5`](https://github.com/treee111/wahooMapsCreator/commit/f2337b5903e93b663af7db7f7cf070596516be41)
- Introduce PyPI setup to distribute python package ([#117](https://github.com/treee111/wahooMapsCreator/issues/117)) [`a947b9f`](https://github.com/treee111/wahooMapsCreator/commit/a947b9f0a52143d7d4ab9fa07cbdf9173380a97a)
- Include POIs into generated maps and diplay them with VTM rendering ([#106](https://github.com/treee111/wahooMapsCreator/issues/106)) [`b32fd86`](https://github.com/treee111/wahooMapsCreator/commit/b32fd86aee6bb8a3edf9465674521f5d80afa5be)

### Features
- Do not zip folders with generated files by default ([#118](https://github.com/treee111/wahooMapsCreator/issues/118)) [`a4feb92`](https://github.com/treee111/wahooMapsCreator/commit/a4feb92962f9904b914fb5aa48649a534212702b)
- **install:** move work-directories to the user directory (prerequisite for PyPI setup) ([#119](https://github.com/treee111/wahooMapsCreator/issues/119)) [`0dd582b`](https://github.com/treee111/wahooMapsCreator/commit/0dd582b5c6649385925ec6ffe75fb375a8beec27)

### Bug Fixes
- Adjust documentation from [#115](https://github.com/treee111/wahooMapsCreator/issues/115) and [#119](https://github.com/treee111/wahooMapsCreator/issues/119) ([#120](https://github.com/treee111/wahooMapsCreator/issues/120)) [`32f7235`](https://github.com/treee111/wahooMapsCreator/commit/32f7235c825fd1be9a652385b42a1c14cc4349e6)

### Development/Infrastructure/Test/CI
- correct pylint findings ([#103](https://github.com/treee111/wahooMapsCreator/issues/103)) [`cd8be6d`](https://github.com/treee111/wahooMapsCreator/commit/cd8be6de007e397b787274b0c2653bc0099baf94)
- multiple small corrections & unifications. pylint findings, logging,  comments, unittests ([#107](https://github.com/treee111/wahooMapsCreator/issues/107)) [`c8ecf44`](https://github.com/treee111/wahooMapsCreator/commit/c8ecf44e4f817c52604aef371de837d86a628220)
- Refactor tags constants, have universal tags and unittest it ([#108](https://github.com/treee111/wahooMapsCreator/issues/108)) [`df80946`](https://github.com/treee111/wahooMapsCreator/commit/df809469844b973a3acbe23d7176b8209b099932)
- **CI/CD:** Introduce pylint via GitHub Actions on each push ([#112](https://github.com/treee111/wahooMapsCreator/issues/112)) [`d50479c`](https://github.com/treee111/wahooMapsCreator/commit/d50479cee6177d90510adfc72d5b78d54c3c85c6)
- Change structure of repository to python module ([#115](https://github.com/treee111/wahooMapsCreator/issues/115)) [`e87ce45`](https://github.com/treee111/wahooMapsCreator/commit/e87ce45a9588d6c798ccb14cec5bb6735706dfe3)
- correct pylint findings ([#116](https://github.com/treee111/wahooMapsCreator/issues/116)) [`d85bd01`](https://github.com/treee111/wahooMapsCreator/commit/d85bd01326b8828425697377b1b5fc0453c4ce62)

### BREAKING CHANGE

The GUI and CLI of wahooMapsCreator will now be called differently than
before:
- `python wahoomc gui` and
- `python wahoomc cli -co malta`

Für CLI and GUI, the default is now to calculate border countries.
The CLI option `-bc` was therefore replaced by `-nbc`, "do not calculate border countries".

Anaconda .yml files have now a different name for creating new environments. Existing Anaconda environments can still be used without adjustments!

The GUI and CLI of wahooMapsCreator will now be called differently than
before:
- `python wahoo_map_creator.py gui` and
- `python wahoo_map_creator.py cli -co malta`

This will ensure better control over the CLI input parameters, help
messages and is more consistent now!


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


[4.3.0]: https://github.com/treee111/wahooMapsCreator/compare/v4.2.0...v4.3.0
[4.2.0]: https://github.com/treee111/wahooMapsCreator/compare/v4.1.1...v4.2.0
[4.1.1]: https://github.com/treee111/wahooMapsCreator/compare/v4.1.0...v4.1.1
[4.1.0]: https://github.com/treee111/wahooMapsCreator/compare/v4.0.2...v4.1.0
[4.0.2]: https://github.com/treee111/wahooMapsCreator/compare/v4.0.1...v4.0.2
[4.0.1]: https://github.com/treee111/wahooMapsCreator/compare/v4.0.0...v4.0.1
[4.0.0]: https://github.com/treee111/wahooMapsCreator/compare/v3.2.0...v4.0.0
[3.2.0]: https://github.com/treee111/wahooMapsCreator/compare/v3.1.1...v3.2.0
[3.1.1]: https://github.com/treee111/wahooMapsCreator/compare/v3.1.0...v3.1.1
[3.1.0]: https://github.com/treee111/wahooMapsCreator/compare/v3.0.0...v3.1.0
[3.0.0]: https://github.com/treee111/wahooMapsCreator/compare/v2.0.2...v3.0.0
[2.0.2]: https://github.com/treee111/wahooMapsCreator/compare/v2.0.1...v2.0.2
[2.0.1]: https://github.com/treee111/wahooMapsCreator/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/treee111/wahooMapsCreator/compare/v1.1.1...v2.0.0
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
