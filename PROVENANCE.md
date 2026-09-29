# FG Link - Official Release Provenance

This document records the public identity of FG Link releases distributed by **FG Machines**.

## Official Android identity

- Publisher: **FG Machines**
- Package ID: `com.fgmachines.rck`
- Official website: https://fgmachines.org
- Official distribution repository: https://github.com/FGMachines/FG-Hub
- Public release date for the 1.6.15 line: **2026-09-29**

## Official signing certificate

SHA-256 certificate fingerprint:

`b9ca4a23be53f161a47b5aaf97023d2bbbeebdaf671337d2466fb74cc1f29fdf`

Public-key SHA-256:

`b029aaa19aa3b8a5c1e62f67d4e0598554edead0c222111960a6a2ce0a018818`

An APK carrying a different signing certificate is **not** the official FG Machines release, even if its icon, package contents or screenshots look similar.

## Public-vs-private boundary

The public repository contains release binaries, checksums, documentation and high-level architecture material.

Private engineering material is intentionally not published, including:

- signing keys and passwords;
- R8 mapping files;
- private build secrets;
- private source code;
- internal credentials;
- unpublished implementation details.

## Why this document exists

Git history, checksums and the signing certificate provide a reproducible public record of which binary FG Machines distributed and when. They are more useful for release authenticity than screenshots or copied marketing text.
