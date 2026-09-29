#!/usr/bin/env bash
set -euo pipefail

VERSION="1.6.9"
SHA256="c1664079dec09fdaddab1dcb5ab1bc1d4bb8cdcd24b2a9e8e3522583ae727d8d"
URL="https://raw.githubusercontent.com/FGMachines/FG-Hub/main/server/FG-Link-Server-1.6.9-VPS.zip"

if [ "${EUID}" -ne 0 ]; then
  echo "Run as root: sudo bash install-fg-link-vps.sh"
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y ca-certificates curl unzip openssl
if ! command -v docker >/dev/null 2>&1; then
  apt-get install -y docker.io
fi
if ! docker compose version >/dev/null 2>&1; then
  apt-get install -y docker-compose-v2 || apt-get install -y docker-compose
fi
systemctl enable --now docker

WORKDIR="/tmp/fg-link-vps-$$"
ZIP="$WORKDIR/FG-Link-Server-${VERSION}-VPS.zip"
mkdir -p "$WORKDIR"
trap 'rm -rf "$WORKDIR"' EXIT

echo "Downloading FG Link Server ${VERSION}..."
curl -fL --retry 3 --connect-timeout 15 "$URL" -o "$ZIP"

echo "${SHA256}  $ZIP" | sha256sum -c -

unzip -q "$ZIP" -d "$WORKDIR"
INSTALLER="$WORKDIR/FG-Link-Server-${VERSION}/install-vps.sh"
test -f "$INSTALLER"
chmod +x "$INSTALLER"

echo
if [ -f /opt/fg-link-server/.env ]; then
  echo "Existing FG Link installation detected. Preserving credentials..."
  SAVED_ENV="$WORKDIR/existing.env"
  cp /opt/fg-link-server/.env "$SAVED_ENV"
  cp -a "$WORKDIR/FG-Link-Server-${VERSION}"/. /opt/fg-link-server/
  cp "$SAVED_ENV" /opt/fg-link-server/.env
  chmod 600 /opt/fg-link-server/.env
  cd /opt/fg-link-server
  docker compose up -d --build
  echo "FG Link server updated. Existing credentials were preserved."
else
  echo "Package verified. Starting FG Link VPS installer..."
  echo
  bash "$INSTALLER" </dev/tty
fi
