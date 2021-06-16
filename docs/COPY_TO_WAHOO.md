# Copy Maps files to Wahoo Device <!-- omit in toc -->

#### Table of contents <!-- omit in toc -->
- [Steps to carry out](#steps-to-carry-out)
  - [Unzip Files](#unzip-files)
  - [install adb](#install-adb)
  - [Authorize Bolt to connect to Windows / macOS](#authorize-bolt-to-connect-to-windows--macos)
    - [BOLT v1](#bolt-v1)
    - [BOLT v2](#bolt-v2)
  - [Copy files](#copy-files)
- [Delete temp-files and Clear Cache](#delete-temp-files-and-clear-cache)

# Steps to carry out
## Unzip Files
unzip the desired country files

## install adb
Windows: you find adb.7z in the Windows-Wahoo-Map-Creator-Osmosis folder
macOS:

## Authorize Bolt to connect to Windows / macOS
### BOLT v1
the Bolt must be authorized for adb (test with: adb devices):
a) disconnect Bolt from your computer
b) turn the Bolt on
c) press the power button (you enter the settings menu)
d) press the power button again (you return to the normal screen)
e) connect the Bolt to your pc

### BOLT v2
adb authorization for Bolt v2:
a) disconnect Bolt from your computer
b) turn the Bolt on
c) press the power, up and down buttons at the same time
d) connect the Bolt to your computer

## Copy files
copy the unzipped map folders to \ELEMNT-BOLT\USB storage\maps\tiles\8\

# Delete temp-files and Clear Cache
- delete all files from \ELEMNT-BOLT\USB storage\maps\temp\
- to clear the cache and load the new maps on the Bolt:
a) adb shell am broadcast -a com.wahoofitness.bolt.service.BMapManager.PURGE
b) adb shell am broadcast -a com.wahoofitness.bolt.service.BMapManager.RELOAD_MAP