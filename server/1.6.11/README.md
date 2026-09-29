# FG Link Private Server

Private backend for the optional FG Link relay and administration panel.

## Current capabilities

- One phone = one account, enforced at database level.
- One account = one active phone binding.
- Fingerprint-first phone provisioning: the Android app exposes a privacy-reduced 64-character phone fingerprint, and the admin issues an API token bound to that fingerprint.
- High-entropy API token generation and rotation; only HMAC hashes are stored.
- Admin-only phone transfer/unbind.
- Controller heartbeat and online/offline status.
- VPS control panel can queue ON/OFF actions for each of the four outlets; the bound Android phone receives them over outbound HTTPS and applies them locally through the MTTL controller.
- Pseudonymous strip inventory/status sync; raw MAC addresses are not stored. Each strip receives a random opaque per-installation control reference.
- Activity log.
- Dark FG Machines web panel under `/panel`.
- PostgreSQL, FastAPI, Caddy HTTPS, Docker Compose.
- No Wi-Fi passwords, ZeroTier secrets, Android private keys, or direct MTTL relay-control secrets on the VPS.

## Deployment

Target: Ubuntu 24.04 or Debian 12.

1. Point a DNS A/AAAA record to the VPS.
2. Copy the `server` directory to the VPS.
3. Run:

```bash
sudo bash install-vps.sh
```

The installer creates random PostgreSQL, token-pepper and internal panel secrets, then prints the one-time admin password.

Panel:

```text
https://YOUR_DOMAIN/panel
```

Health check:

```text
https://YOUR_DOMAIN/healthz
```

## Security model

Caddy protects the panel with HTTPS + Basic Auth. It also injects a random internal panel token that FastAPI validates, providing a second barrier against direct panel API access.

Client API keys are never stored in plaintext. A raw API key is shown only when the admin provisions a phone fingerprint or rotates its key.

Phone fingerprints and local strip references are HMAC-SHA256 pseudonyms generated with a server-side pepper. The server never stores the raw fingerprint/reference.

A VPS compromise can still expose account names, hashed identifiers and operational status metadata. The design intentionally keeps local-control secrets and electrical-control authority outside the VPS.

## Backup

```bash
sudo bash /opt/fg-link-server/backup.sh
```

Backups default to `/opt/fg-link-backups` and retain 14 days unless `FG_LINK_BACKUP_KEEP_DAYS` is changed.
