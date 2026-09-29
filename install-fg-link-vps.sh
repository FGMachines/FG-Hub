#!/usr/bin/env bash
set -euo pipefail

VERSION="1.6.11"
BASE_URL="https://raw.githubusercontent.com/FGMachines/FG-Hub/main/server/${VERSION}"

if [ "${EUID}" -ne 0 ]; then
  echo "Run as root: sudo bash install-fg-link-vps.sh"
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y ca-certificates curl

WORKDIR="/tmp/fg-link-vps-$$"
PACKAGE_DIR="$WORKDIR/FG-Link-Server-$VERSION"
mkdir -p "$PACKAGE_DIR/app"
trap 'rm -rf "$WORKDIR"' EXIT

FILES=(
  "Caddyfile"
  "Dockerfile"
  "README.md"
  "backup.sh"
  "docker-compose.yml"
  "install-vps.sh"
  "requirements.txt"
  "app/__init__.py"
  "app/database.py"
  "app/main.py"
  "app/models.py"
  "app/panel.html"
)

echo "Downloading FG Link Server ${VERSION}..."
for FILE in "${FILES[@]}"; do
  mkdir -p "$PACKAGE_DIR/$(dirname "$FILE")"
  curl -fL --retry 3 --connect-timeout 15     "$BASE_URL/$FILE"     -o "$PACKAGE_DIR/$FILE"
done

chmod +x "$PACKAGE_DIR/install-vps.sh" "$PACKAGE_DIR/backup.sh"

echo
echo "FG Link Server ${VERSION} downloaded successfully."
echo "Starting installer/updater..."
echo
bash "$PACKAGE_DIR/install-vps.sh" </dev/tty
