# FG Link — Authenticity & Verification

This page records the identity of the official FG Machines Android artifact published on **2026-09-29**.

## Official artifact

- Product: **FG Link**
- Version: **1.6.14**
- Version code: **43**
- Android package: `com.fgmachines.rck`
- Publisher: **FG Machines**
- APK SHA-256: `9b7c38657835d2f323f789494d36b57b0f12757964a1c20a3f69af91b682ee94`

## Signing identity

- Certificate DN: `CN=FG Machines, OU=Software Release, O=FG Machines, C=EG`
- Certificate SHA-256: `b9ca4a23be53f161a47b5aaf97023d2bbbeebdaf671337d2466fb74cc1f29fdf`
- Public-key SHA-256: `b029aaa19aa3b8a5c1e62f67d4e0598554edead0c222111960a6a2ce0a018818`
- Key algorithm: **RSA 4096-bit**
- APK Signature Scheme: **v2**

## Verify the download

```bash
sha256sum FG-Link-1.6.14-Hardened-Signed.apk
apksigner verify --verbose --print-certs FG-Link-1.6.14-Hardened-Signed.apk
```

A copied filename, icon or screenshot is not sufficient to establish authenticity. Verify the APK hash and the FG Machines signing certificate.

## Publication record

Git commit history, release artifacts, SHA-256 values and the stable signing certificate create a verifiable public publication record for FG Machines releases and help distinguish official builds from repackaged or re-signed copies.


## Illustrated Arabic guide

- File: `docs/FG-Link-User-Guide-AR-Illustrated-v1.6.14.pdf`
- Pages: **55**
- SHA-256: `b9579a9d8daad140de79202ecaf0b5f36f27b1c863db826c0232f537764dacb2`

The guide contains the illustrated Router, one-phone, two-phone and ZeroTier setup flows, IR remote requirements, diagnostics, developer/follow-up information, and safe credential recovery guidance. VPS Direct is explicitly marked as **testing / not public**.
