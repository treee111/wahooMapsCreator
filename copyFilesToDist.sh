FOLDER_NAME_MAC="wahooMapsCreator-"${GITHUB_REF_VARIABLE}"-macOS-Linux"
FOLDER_NAME_WIN="wahooMapsCreator-"${GITHUB_REF_VARIABLE}"-Windows"
FOLDER_NAME_CRUISER="cruiser-mapviewer-"${GITHUB_REF_VARIABLE}"-macOS-Linux-Windows"

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

# navigate into mac folder
cd ../..
cd dist/${FOLDER_NAME_MAC}

# create empty sub-folders
mkdir -p ./wahoo_mc
mkdir -p ./wahoo_mc/resources
mkdir -p ./conda_env
mkdir -p ./tooling
mkdir -p ./docs
mkdir -p ./device_themes

# copy files into dist-folder
cp -a ../../wahoo_mc/*.py ./wahoo_mc/
cp -a ../../wahoo_mc/resources/*.xml ./wahoo_mc/resources/
cp -a ../../wahoo_mc/resources/*.osm ../../wahoo_mc/resources/*.py ./wahoo_mc/resources/
cp -a ../../wahoo_mc/resources/json/ ./wahoo_mc/resources/json
cp -a ../../wahoo_mc/resources/tag_wahoo_adjusted/ ./wahoo_mc/resources/tag_wahoo_adjusted
cp -a ../../wahoo_mc/resources/tag_wahoo_initial/ ./wahoo_mc/resources/tag_wahoo_initial
cp -a ../../device_themes/ ./device_themes/

cp -a ../../docs/*.md ./docs/
cp -a ../../CHANGELOG.md ../../README.md ./

# file for virtual environments / legacy pip install
cp -a ../../conda_env/gdal-user.yml ./conda_env/
cp -a ../../conda_env/requirements.txt ./conda_env/

# navigate one dir up into "dist" folder and copy content from Mac to Win
cd ..
cp -R ${FOLDER_NAME_MAC}/* ${FOLDER_NAME_WIN}

# add Win specific stuff
cp -a ../tooling_win ./${FOLDER_NAME_WIN}/tooling_win

# zip content into .zip file - by cd'ing without including root folder
cd ${FOLDER_NAME_MAC}
zip -r ../${FOLDER_NAME_MAC}.zip *

cd ..
cd ${FOLDER_NAME_WIN}
zip -r ../${FOLDER_NAME_WIN}.zip *