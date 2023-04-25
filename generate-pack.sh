#!/usr/bin/sh
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
mkdir temp-dir
unzip $PACK_NAME -d temp-dir
rm $PACK_NAME
