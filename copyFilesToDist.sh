FOLDER_NAME="wahooMapsCreator-"${GITHUB_REF_VARIABLE}
echo "Foldername: ${FOLDER_NAME}"
echo "Github-Ref: ${GITHUB_REF_VARIABLE}"

# create folders and move into dist-folder
mkdir -p dist
cd dist
mkdir -p ${FOLDER_NAME}
mkdir -p ${FOLDER_NAME}/common_resources
mkdir -p ${FOLDER_NAME}/common_resources/maps
mkdir -p ${FOLDER_NAME}/output

# copy files into dist-folder
cp -a ../common_resources/json/ ${FOLDER_NAME}/common_resources/json
cp -a ../common_resources/Osmosis/ ${FOLDER_NAME}/common_resources/Osmosis
cp -a ../common_resources/*.py ${FOLDER_NAME}/common_resources/
cp -a ../common_resources/*.xml ${FOLDER_NAME}/common_resources/
cp -a ../common_resources/*.osm ${FOLDER_NAME}/common_resources/
cp -a ../docs ${FOLDER_NAME}/docs
# cp -a ./output ./dist/output
cp -a ../tooling ${FOLDER_NAME}/tooling
cp -a ../tooling_windows ${FOLDER_NAME}/tooling_windows
cp -a ../wahoo_map_creator.py ../CHANGELOG.md ../README.md ${FOLDER_NAME}/

# zip content into .zip file
# cd wahooMapsCreator-${GITHUB_REF_VARIABLE}
zip -r ${FOLDER_NAME}.zip ./${FOLDER_NAME}
ls