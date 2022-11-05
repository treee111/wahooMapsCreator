FOLDER_NAME_DEVICE_THEMES="wahooMapsCreator-device_themes-"${GITHUB_REF_VARIABLE}

echo "Github-Ref: ${GITHUB_REF_VARIABLE}"

# zip device themes
cd device_themes
zip -r -q ../dist/${FOLDER_NAME_DEVICE_THEMES}.zip *
cd ..