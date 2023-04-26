#!/usr/bin/sh
# Default Dark Mode base
echo "Merging Default Dark Mode..."
mkdir temp-dir
cp -R Default-Dark-Mode/assets temp-dir
cp Default-Dark-Mode/pack.png temp-dir

# augmenting dark mode color
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
printf "N\n" | unzip $PACK_NAME -d temp-dir
rm $PACK_NAME

# Awesome Skies merge
echo "Merging Awesome Skies..."
cp -Rn Awesome-Skies/assets temp-dir

# font configuration
if [ "$#" -gt 0 ]; then
	echo "Configuring font..."
	FONT_PATH="temp-dir/assets/minecraft/font/default.json"
	cp "$1" temp-dir/assets/minecraft/font/font.ttf
	jq --ascii-output ".providers += [$(cat font-conf.json)]" $FONT_PATH > "${FONT_PATH}.temp"
	mv "${FONT_PATH}.temp" $FONT_PATH
fi

# finalization
echo "Finalizing..."
cp pack.mcmeta temp-dir
cd temp-dir
zip -r ../pack.zip ./*
cd ..
rm -Rf temp-dir
