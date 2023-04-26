#!/usr/bin/sh
# Default Dark Mode base
echo "Merging Default Dark Mode..."
mkdir temp-dir
cp -R Default-Dark-Mode/assets temp-dir
cp Default-Dark-Mode/pack.png temp-dir

# augmenting dark mode color
echo "Augmenting dark mode colors..."
python color-augmentation/palettize.py temp-dir

# download vanillatweaks configuration and merge it with texture pack
echo "Merging vanillatweaks..."
VANILLATWEAKS_BASE_URL="https://vanillatweaks.net"
MINECRAFT_VERSION=$(jq -r '.version' vanillatweaks-version.json)
DOWNLOAD_PATH=$(curl \
--data-urlencode "packs@vanillatweaks-settings.json" \
--data-raw "version=$MINECRAFT_VERSION" \
"https://vanillatweaks.net/assets/server/zipresourcepacks.php" \
2>/dev/null | jq -r ".link")
PACK_LINK="${VANILLATWEAKS_BASE_URL}$DOWNLOAD_PATH"
PACK_NAME="vanillatweaks.zip"
wget -O $PACK_NAME $PACK_LINK > /dev/null 2>&1
unzip -n $PACK_NAME -d temp-dir
rm $PACK_NAME

# Awesome Skies merge
echo "Merging Awesome Skies..."
cp -Rn Awesome-Skies/assets temp-dir

# font configuration
if [ "$#" -gt 0 ]; then
	echo "Configuring font..."
	FONT_DIR="temp-dir/assets/minecraft/font"
	FONT_CONFIG_PATH="$FONT_DIR/default.json"
	FONT_PATH="$FONT_DIR/font"
	cp "$1" $FONT_PATH
	jq --ascii-output ".providers += [$(cat font-conf.json)]" $FONT_CONFIG_PATH > "${FONT_CONFIG_PATH}.temp"
	mv "${FONT_CONFIG_PATH}.temp" $FONT_CONFIG_PATH
fi

# finalization
echo "Zipping..."
cp pack.mcmeta temp-dir
cd temp-dir
zip -r ../pack.zip ./*
cd ..
rm -Rf temp-dir

echo "Done."
