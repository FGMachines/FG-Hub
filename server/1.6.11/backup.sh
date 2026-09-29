#!/usr/bin/env bash
set -euo pipefail

DEST="${1:-/opt/fg-link-backups}"
KEEP_DAYS="${FG_LINK_BACKUP_KEEP_DAYS:-14}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$DEST"
chmod 700 "$DEST"

cd /opt/fg-link-server
docker compose exec -T db pg_dump -U fglink -d fglink -Fc > "$DEST/fglink-$STAMP.dump"
chmod 600 "$DEST/fglink-$STAMP.dump"
find "$DEST" -type f -name 'fglink-*.dump' -mtime +"$KEEP_DAYS" -delete

echo "$DEST/fglink-$STAMP.dump"
