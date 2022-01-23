FOLDER_NAME_MAC="wahooMapsCreator-"${GITHUB_REF_VARIABLE}"-macOS-Linux"
FOLDER_NAME_WIN="wahooMapsCreator-"${GITHUB_REF_VARIABLE}"-Windows"

echo "Github-Ref: ${GITHUB_REF_VARIABLE}"

# delete folder with content and create top-level folder
rm -rf dist
mkdir -p dist
# create OS-specific folders
mkdir -p dist/${FOLDER_NAME_MAC}
mkdir -p dist/${FOLDER_NAME_WIN}
# navigate into mac folder
cd dist/${FOLDER_NAME_MAC}

# create empty sub-folders
mkdir -p ./common_python
mkdir -p ./common_resources
mkdir -p ./conda_env
mkdir -p ./tooling

# copy files into dist-folder
cp -a ../../common_python/*.py ./common_python/

cp -a ../../common_resources/*.xml ./common_resources/
cp -a ../../common_resources/json/ ./common_resources/json
cp -a ../../common_resources/tag_wahoo_adjusted/ ./common_resources/tag_wahoo_adjusted
cp -a ../../common_resources/tag_wahoo_initial/ ./common_resources/tag_wahoo_initial

cp -a ../../docs ./docs
cp -a ../../tooling/*.osm ../../tooling/*.py ./tooling/
cp -a ../../wahoo_map_creator.py ../../CHANGELOG.md ../../README.md ./

# zip cruiser stuff
zip -r ./tooling/cruiser.zip ../../tooling/cruiser/*

# file for virtual environments / legacy pip install
cp -a ../../conda_env/enduser.yml ./conda_env/
cp -a ../../conda_env/requirements.txt ./conda_env/

# navigate one dir up into "dist" folder and copy content from Mac to Win
cd ..
cp -R ${FOLDER_NAME_MAC}/* ${FOLDER_NAME_WIN}

# add Win specific stuff
cp -a ../tooling_windows ./${FOLDER_NAME_WIN}/tooling_windows

# zip content into .zip file
zip -r ${FOLDER_NAME_MAC}.zip ${FOLDER_NAME_MAC}/*
zip -r ${FOLDER_NAME_WIN}.zip ${FOLDER_NAME_WIN}/*