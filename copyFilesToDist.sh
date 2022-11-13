FOLDER_NAME_DEVICE_THEMES="wahooMapsCreator-device_themes-"${GITHUB_REF_VARIABLE}

echo "Github-Ref: ${GITHUB_REF_VARIABLE}"

# delete folder with content and create top-level folder
rm -rf dist
mkdir -p dist

# zip device themes
cd device_themes
zip -r -q ../dist/${FOLDER_NAME_DEVICE_THEMES}.zip *
cd ..