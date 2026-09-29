#!/usr/bin/env bash
set -euo pipefail

if [ "${EUID}" -ne 0 ]; then
  echo "Run as root: sudo bash install-vps.sh"
  exit 1
fi

read -rp "FG Link domain (example: link.example.com): " DOMAIN
read -rp "ACME email: " ACME_EMAIL
read -rp "Admin panel username [admin]: " ADMIN_USER
ADMIN_USER="${ADMIN_USER:-admin}"

apt-get update
apt-get install -y ca-certificates curl openssl

if ! command -v docker >/dev/null 2>&1; then
  apt-get install -y docker.io
fi
if ! docker compose version >/dev/null 2>&1; then
  apt-get install -y docker-compose-v2 || apt-get install -y docker-compose
fi
systemctl enable --now docker

install -d -m 700 /opt/fg-link-server
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Preserve persistent credentials on upgrades/re-runs. Regenerating the
# PostgreSQL password while reusing the existing data volume breaks auth.
if [ -f /opt/fg-link-server/.env ]; then
  EXISTING_ENV="$(mktemp)"
  cp /opt/fg-link-server/.env "$EXISTING_ENV"
  cp -a "$SCRIPT_DIR"/. /opt/fg-link-server/
  cp "$EXISTING_ENV" /opt/fg-link-server/.env
  rm -f "$EXISTING_ENV"
  chmod 600 /opt/fg-link-server/.env
  cd /opt/fg-link-server
  docker compose up -d --build
  echo
  echo "FG Link server updated with existing credentials preserved."
  echo "Panel: https://$(sed -n 's/^FG_LINK_DOMAIN=//p' .env | head -n1)/panel"
  echo "Health: https://$(sed -n 's/^FG_LINK_DOMAIN=//p' .env | head -n1)/healthz"
  exit 0
fi

POSTGRES_PASSWORD="$(openssl rand -hex 32)"
TOKEN_PEPPER="$(openssl rand -hex 32)"
PANEL_TOKEN="$(openssl rand -hex 32)"
ADMIN_PASSWORD="$(openssl rand -base64 24 | tr -d '=+/\\n' | cut -c1-24)"
ADMIN_HASH="$(docker run --rm caddy:2-alpine caddy hash-password --plaintext "$ADMIN_PASSWORD")"

cp -a "$SCRIPT_DIR"/. /opt/fg-link-server/
cd /opt/fg-link-server

cat > .env <<EOF
FG_LINK_DOMAIN=$DOMAIN
FG_LINK_ACME_EMAIL=$ACME_EMAIL
FG_LINK_ADMIN_USER=$ADMIN_USER
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
FG_LINK_TOKEN_PEPPER=$TOKEN_PEPPER
FG_LINK_PANEL_TOKEN=$PANEL_TOKEN
FG_LINK_ADMIN_HASH='$ADMIN_HASH'
FG_LINK_CONTROLLER_ONLINE_SECONDS=90
FG_LINK_COMMAND_TTL_SECONDS=120
EOF
chmod 600 .env

docker compose up -d --build

echo
echo "FG Link server started."
echo "Panel: https://$DOMAIN/panel"
echo "Health: https://$DOMAIN/healthz"
echo "Admin user: $ADMIN_USER"
echo "Admin password: $ADMIN_PASSWORD"
echo
echo "Store the admin password securely. It is not written to the repository."
