# create folder
mkdir -p dist
mkdir -p dist/common_resources
mkdir -p dist/common_resources/maps
mkdir -p dist/output

# copy files into dist-folder
cp -a ./common_resources/json/ ./dist/common_resources/json
cp -a ./common_resources/Osmosis/ ./dist/common_resources/Osmosis
cp -a ./common_resources/*.py ./dist/common_resources/
cp -a ./common_resources/*.xml ./dist/common_resources/
cp -a ./common_resources/*.osm ./dist/common_resources/
cp -a ./docs ./dist/docs
# cp -a ./output ./dist/output
cp -a ./tooling ./dist/tooling
cp -a ./tooling_windows ./dist/tooling_windows
cp -a ./wahoo_map_creator.py ./CHANGELOG.md ./README.md ./dist/

# zip content into .zip file
zip -r dist/wahooMapsCreator-release.zip ./dist