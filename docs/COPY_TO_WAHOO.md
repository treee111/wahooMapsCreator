# Copy Maps files to Wahoo Device <!-- omit in toc -->

#### Table of contents <!-- omit in toc -->
- [Steps to carry out](#steps-to-carry-out)
  - [Unzip Files](#unzip-files)
  - [install adb](#install-adb)
  - [Authorize Bolt to connect to Windows / macOS](#authorize-bolt-to-connect-to-windows--macos)
    - [BOLT v1](#bolt-v1)
    - [BOLT v2](#bolt-v2)
  - [Copy map files](#copy-map-files)
  - [Copy device theme](#copy-device-theme)
- [Delete temp-files and Clear Cache](#delete-temp-files-and-clear-cache)
- [Troubleshooting](#troubleshooting)

# Steps to carry out
## Unzip Files
unzip the desired country files

## install adb
You can download the lates ADB-tools (included in the SDK Platform Tools) for your OS here:
https://developer.android.com/studio/releases/platform-tools

## Authorize Bolt to connect to Windows / macOS
### BOLT v1
the Bolt must be authorized for adb (test with: adb devices):
1. disconnect Bolt from your computer
2. turn the Bolt on
3. press the power button (you enter the settings menu)
4. press the power button again (you return to the normal screen)
5. connect the Bolt to your pc

### BOLT v2
adb authorization for Bolt v2:
1. disconnect Bolt from your computer
2. turn the Bolt on
3. press the power, up and down buttons at the same time
4. connect the Bolt to your computer

## Copy map files
copy the unzipped map folders to \ELEMNT-BOLT\USB storage\maps\tiles\8\

These tools can be helpful if you want to copy the files with a GUI and not via CLI:
- Windows: https://github.com/hexadezi/adbGUI
- macOS: https://www.android.com/filetransfer/

## Copy device theme
Device themes are described [here](TAGS_ON_MAP_AND_DEVICE.md#Device-Theme)
A theme can be copied to your device like that:
- ELEMNT/BOLT 
  - copy "mapsforge-bolt.xml” of folder `common_resources/theme_adjusted` to `maps/mapsforge-bolt/mapsforge-bolt.xml` (just posted this in the google groups)
- BOLTv2
  - copy `assets/maps/vtm-elemnt/vtm-elemnt.xml` from the apk. Modify and copy the theme to `maps/vtm-elemnt/vtm-elemnt.xml`
- ROAM
  - copy `mapsforge-bolt.xml` of folder `common_resources/theme_adjusted` to `maps/mapsforge-roam/mapsforge-roam.xml`

# Delete temp-files and Clear Cache
- delete all files from \ELEMNT-BOLT\USB storage\maps\temp\
- to clear the cache and load the new maps on the Bolt:
1. `adb shell am broadcast -a com.wahoofitness.bolt.service.BMapManager.PURGE`
2. `adb shell am broadcast -a com.wahoofitness.bolt.service.BMapManager.RELOAD_MAP`

# Troubleshooting
If adb does seam to not work with your PC and Wahoo:
- try to do the [Authorization](#authorize-bolt-to-connect-to-windows--macos) multiple times
- try another USB cable. Some cables do not support adb / file transfer
