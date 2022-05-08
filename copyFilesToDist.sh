FOLDER_NAME_MAC="wahooMapsCreator-"${GITHUB_REF_VARIABLE}"-macOS-Linux"
FOLDER_NAME_WIN="wahooMapsCreator-"${GITHUB_REF_VARIABLE}"-Windows"
FOLDER_NAME_CRUISER="wahooMapsCreator-cruiser-"${GITHUB_REF_VARIABLE}
FOLDER_NAME_DEVICE_THEMES="wahooMapsCreator-device_themes-"${GITHUB_REF_VARIABLE}

echo "Github-Ref: ${GITHUB_REF_VARIABLE}"

# delete folder with content and create top-level folder
rm -rf dist
mkdir -p dist
# create OS-specific folders
mkdir -p dist/${FOLDER_NAME_MAC}
mkdir -p dist/${FOLDER_NAME_WIN}

# zip cruiser stuff
cd tooling/cruiser
zip -r ../../dist/${FOLDER_NAME_CRUISER}.zip *
cd ../..

# zip device themes
cd device_themes
zip -r ../dist/${FOLDER_NAME_DEVICE_THEMES}.zip *
cd ..

# navigate into mac folder
cd dist/${FOLDER_NAME_MAC}

# create empty sub-folders
mkdir -p ./wahoomc
mkdir -p ./wahoomc/resources
mkdir -p ./conda_env
mkdir -p ./docs

# copy files into dist-folder
cp -a ../../wahoomc/*.py ./wahoomc/
cp -a ../../wahoomc/resources/*.xml ./wahoomc/resources/
cp -a ../../wahoomc/resources/*.osm ../../wahoomc/resources/*.py ./wahoomc/resources/
cp -a ../../wahoomc/resources/json/ ./wahoomc/resources/json
cp -a ../../wahoomc/resources/tag_wahoo_adjusted/ ./wahoomc/resources/tag_wahoo_adjusted
cp -a ../../wahoomc/resources/tag_wahoo_initial/ ./wahoomc/resources/tag_wahoo_initial

cp -a ../../docs/*.md ./docs/
cp -a ../../CHANGELOG.md ../../README.md ./

# file for virtual environments / legacy pip install
cp -a ../../conda_env/gdal-user.yml ./conda_env/
cp -a ../../conda_env/requirements.txt ./conda_env/

# navigate one dir up into "dist" folder and copy content from Mac to Win
cd ..
cp -R ${FOLDER_NAME_MAC}/* ${FOLDER_NAME_WIN}

# add Win specific stuff
cp -a ../wahoomc/tooling_win ./${FOLDER_NAME_WIN}/tooling_win

# zip content into .zip file - by cd'ing without including root folder
cd ${FOLDER_NAME_MAC}
zip -r ../${FOLDER_NAME_MAC}.zip *

cd ..
cd ${FOLDER_NAME_WIN}
zip -r ../${FOLDER_NAME_WIN}.zip *