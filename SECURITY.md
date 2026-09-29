# Security Policy

FG Link official releases are distributed by **FG Machines**.

## Verify before installing

For every public release, verify all of the following:

1. The download comes from `FGMachines/FG-Hub`.
2. The package ID is `com.fgmachines.rck`.
3. The APK SHA-256 matches the release checksum.
4. The signing certificate SHA-256 is:

   `b9ca4a23be53f161a47b5aaf97023d2bbbeebdaf671337d2466fb74cc1f29fdf`

Do not trust a copy merely because the UI or filename looks identical.

## Release protection

The public APK uses multiple defense-in-depth controls, including optimized/minified release builds, resource shrinking, implementation-name obfuscation, log removal, private build mappings and official-signature verification.

These controls are designed to make simple copying, repackaging and re-signing harder. They do not make reverse engineering mathematically impossible.

## Secrets

Signing keys, passwords, VPS credentials, API secrets, private mapping files and private engineering material must never be committed to this public repository.

## Network model

FG Link is local-first. Local Router/LAN and ZeroTier modes remain independent of the optional VPS service. VPS Direct is explicitly treated as a test feature until the direct-device test program is completed.

## Reporting a vulnerability

Please send security reports privately through an official FG Machines contact channel. Do not publish working exploit details, credentials or private customer data in a public GitHub issue.
