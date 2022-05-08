# Copy Maps files to Wahoo Device <!-- omit in toc -->

#### Table of contents <!-- omit in toc -->
- [Steps to carry out](#steps-to-carry-out)
  - [Location of the generated maps](#location-of-the-generated-maps)
  - [Install adb](#install-adb)
  - [Authorize Wahoo device](#authorize-wahoo-device)
  - [Copy map files](#copy-map-files)
    - [Simplified usage with MTP-tranfer (under Windows)](#simplified-usage-with-mtp-tranfer-under-windows)
  - [Copy device theme](#copy-device-theme)
- [POIs](#pois)
  - [Copy relevant files for POIs](#copy-relevant-files-for-pois)
  - [Activate VTM rendering](#activate-vtm-rendering)
- [Delete temp-files and Clear Cache](#delete-temp-files-and-clear-cache)
- [Troubleshooting](#troubleshooting)

# Steps to carry out
## Location of the generated maps
The generated maps are saved in the user directory in folder: `$user_directory/wahooMapsCreatorData`.

There is a folder per country or for the X/Y combination with the relevant tiles.

## Install adb
You can download the lates adb-tools (included in the SDK Platform Tools) for your OS here:
https://developer.android.com/studio/releases/platform-tools

## Authorize Wahoo device
The Wahoo device must be authorized for adb to be reachable from Windows and macOS. Adb authorization works different per Wahoo device and is decribed now.

1. disconnect device from your computer
2. turn the device on
3. press keys on device
   * **BOLT v1 and ROAM**
     * press the power button (you enter the settings menu)
     * press the power button again (you return to the normal screen)
   * **BOLT v2**
     * press the power, up and down buttons at the same time
4. connect the device to your pc

Successful authorization can be tested via terminal / cmd:
```
adb devices
```

## Copy map files
copy map folders per tile to \ELEMNT-BOLT\USB storage\maps\tiles\8\

These tools can be helpful if you want to copy the files with a GUI and not via CLI:
- Windows: https://github.com/hexadezi/adbGUI
- macOS: https://www.android.com/filetransfer/

### Simplified usage with MTP-tranfer (under Windows)
According to [the Wahoo documentation](https://support.wahoofitness.com/hc/en-us/articles/115000127910-Connecting-ELEMNT-BOLT-ROAM-to-Desktop-or-Laptop-Computers) the device is able to connect via MTP. On windows you can navigate to the maps folder and drag new map files onto the folder called `maps\8`. The system will ask if you want to overwrite existing files. Don't forget to [delete temp-files and Clear Cache](#delete-temp-files-and-clear-cache). You can simply reboot to clear the cache.

## Copy device theme
In this repo, device themes are stored in folder `device_themes`. There are initial versions and adjusted versions. Both can be further changed to your requirements!

The following table shows the file per device and the location where the device theme needs to be copied to.

| device | file                 | location                                 |
| ------ | -------------------- | ---------------------------------------- |
| BOLTv2 | `vtm-elemnt.xml`     | `maps/vtm-elemnt/vtm-elemnt.xml`         |
| ROAM   | `mapsforge-roam.xml` | `maps/mapsforge-roam/mapsforge-roam.xml` |
| BOLTv1 | `mapsforge-bolt.xml` | `maps/mapsforge-bolt/mapsforge-bolt.xml` |
| ELEMNT | `mapsforge-bolt.xml` | `maps/mapsforge-bolt/mapsforge-bolt.xml` |

Device themes are described [here](TAGS_ON_MAP_AND_DEVICE.md#Device-Theme)

# POIs
## Copy relevant files for POIs
For having POIs displayed on your device, you need to copy the icons and a corresponding device theme on your device.
These are the steps to follow:
- create folder `maps/vtm-elemnt`
- copy the content of  `device_themes/vtm_theme_poi` into  `maps/vtm-elemnt`.

## Activate VTM rendering
If you have a ROAM or BOLTv2, VTM is already the default rendering theme.
For e.g. a BOLTv1, you need to activete VTM rendering first.

- Create a empty file with this name `cfg_BHomeActivity_VtmMaps`
- Copy that file to the root-folder. It should be on the same level as the `maps` and `factory` folder.

# Delete temp-files and Clear Cache
- delete all files from \ELEMNT-BOLT\USB storage\maps\temp\
- to clear the cache and load the new maps on the Bolt:
1. `adb shell am broadcast -a com.wahoofitness.bolt.service.BMapManager.PURGE`
2. `adb shell am broadcast -a com.wahoofitness.bolt.service.BMapManager.RELOAD_MAP`

# Troubleshooting
If adb does seam to not work with your PC and Wahoo:
- try to do the [Authorization](#authorize-bolt-to-connect-to-windows--macos) multiple times
- try another USB cable. Some cables do not support adb / file transfer
