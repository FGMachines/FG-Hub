# FG Link - APK Hardening

FG Link public Android releases are shipped as hardened, signed binaries. The goal is to raise the cost of unauthorized repackaging and casual reverse engineering while keeping the app maintainable and verifiable.

## Current release protections

The official `1.6.14 / build 43` APK uses:

- **R8 optimization + minification**
- **Resource shrinking**
- **Class repackaging/obfuscation**
- **Adapted class strings during obfuscation**
- **Release build is non-debuggable**
- **Android log calls removed from optimized bytecode**
- **Operational wire constants are runtime-decoded rather than exposed as obvious plaintext strings**
- **R8 mapping files remain private**
- **Signing keystore and signing passwords remain outside the public repository**
- **Server/API secrets are not committed**
- **Public artifact has a stable FG Machines signing identity**
- **SHA-256 checksum is published with every official APK**

## What is deliberately not published

This distribution repository does not publish:

- Android engineering source
- R8 mapping files
- signing keystores or credentials
- private CI secrets
- internal provisioning material
- customer Wi-Fi credentials
- ZeroTier secrets
- local MTTL control secrets/material

## Authenticity matters more than filenames

An attacker can copy a filename, icon, README or screenshot. They cannot create an APK that verifies under the official FG Machines private signing key.

For the current release verify:

```bash
sha256sum FG-Link-1.6.14-Hardened-Signed.apk
apksigner verify --verbose --print-certs FG-Link-1.6.14-Hardened-Signed.apk
```

Expected APK SHA-256:

```
9b7c38657835d2f323f789494d36b57b0f12757964a1c20a3f69af91b682ee94
```

Expected signing-certificate SHA-256:

```
b9ca4a23be53f161a47b5aaf97023d2bbbeebdaf671337d2466fb74cc1f29fdf
```

## Limits

No Android APK can be made impossible to reverse engineer. Obfuscation, signing, secret separation and release verification are defense-in-depth controls: they increase effort, reduce accidental exposure, make repackaged copies easier to detect, and protect the authoritative publication chain.

The canonical official record is the combination of:

1. the **FGMachines/FG-Hub** Git history,
2. the published SHA-256 values,
3. the FG Machines signing certificate,
4. the documented release version and package identity.
