FOLDER_NAME="wahooMapsCreator-"${GITHUB_REF_VARIABLE}
echo "Foldername: ${FOLDER_NAME}"
echo "Github-Ref: ${GITHUB_REF_VARIABLE}"

# create top-folders and move into given foldername-folder
mkdir -p dist
mkdir -p dist/${FOLDER_NAME}
cd dist/${FOLDER_NAME}
mkdir -p ./common_python
mkdir -p ./common_resources

# copy files into dist-folder
cp -a ../../common_python/*.py ./common_python/
cp -a ../../common_resources/*.xml ./common_resources/
cp -a ../../common_resources/*.osm ./common_resources/
cp -a ../../common_resources/json/ ./common_resources/json
cp -a ../../common_resources/tag_wahoo_adjusted/ ./common_resources/tag_wahoo_adjusted
cp -a ../../common_resources/tag_wahoo_initial/ ./common_resources/tag_wahoo_initial
cp -a ../../docs ./docs
cp -a ../../tooling ./tooling
cp -a ../../tooling_windows ./tooling_windows
cp -a ../../wahoo_map_creator.py ../../CHANGELOG.md ../../README.md ../../requirements.txt ./

# zip content into .zip file
zip -r ../${FOLDER_NAME}.zip *
echo "dist/${FOLDER_NAME}/: ls"
ls
cd ..
echo "dist/: ls"
ls