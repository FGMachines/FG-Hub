# FG Link — سجل النشر الرسمي

مستودع التوزيع والتوثيق العام: **FGMachines/FG-Hub**. الناشر: **FG Machines**. المصدر الهندسي للتطبيق والخادم ومفاتيح التوقيع تبقى خاصة.

## الإصدار الحالي

| البيان | القيمة |
|---|---|
| الإصدار | 2.1.2 |
| versionCode | 47 |
| الحزمة | `com.fgmachines.rck` |
| Release | [v2.1.2](https://github.com/FGMachines/FG-Hub/releases/tag/v2.1.2) |
| APK | `FG-Link-2.1.2-v47.apk` |
| SHA-256 | `07c9307f9657b02c6893174a37f2a60701b0afae4c30985877599cc5abfeff0f` |
| شهادة التوقيع SHA-256 | `b9ca4a23be53f161a47b5aaf97023d2bbbeebdaf671337d2466fb74cc1f29fdf` |

[التحقق من الأصالة](docs/AUTHENTICITY.md) · [دليل الواجهة الجديدة المصوّر](docs/USER-GUIDE-AR.md) · [التغييرات](releases/2.1.2/RELEASE_NOTES.md).

إصدار 2.1.2 يدمج Direct VPS في أجهزتي ويستخدم الحساب الشخصي والصلاحيات التي يفرضها الخادم. إرسال البريد يحتاج تجهيز SMTP على الخادم. التوثيق والصور هنا لا يتضمنان بيانات عملاء ولا كلمات مرور. تاريخ GitHub Releases هو مرجع وقت النشر.

## سجل الإصدار السابق 1.6.14

المحتوى التالي محفوظ كتاريخ للإصدار السابق فقط؛ وصف Direct VPS التجريبي فيه لا يصف الإصدار الحالي.

<details>
<summary>عرض سجل 1.6.14 المؤرشف</summary>

# FG Link — Official Publication & Provenance Record

This repository is the official public distribution and documentation channel for **FG Link**, published by **FG Machines**.

## Public release identity

- Product: **FG Link**
- Publisher: **FG Machines**
- Android package: `com.fgmachines.rck`
- Public release: **1.6.14**
- Version code: **43**
- Publication date: **2026-09-29**
- Official repository: `FGMachines/FG-Hub`
- Official release tag: `v1.6.14`

## Release verification

### APK

```text
SHA-256
9b7c38657835d2f323f789494d36b57b0f12757964a1c20a3f69af91b682ee94
```

### FG Machines signing certificate

```text
Certificate SHA-256
b9ca4a23be53f161a47b5aaf97023d2bbbeebdaf671337d2466fb74cc1f29fdf
```

Certificate identity:

```text
CN=FG Machines, OU=Software Release, O=FG Machines, C=EG
```

A copied filename, icon, screenshot, repository description, or application label is not proof that an APK is official. The authoritative identity is the **FG Machines signing certificate**, together with the release hash and the publication history in this repository.

## Public distribution model

This repository deliberately publishes the **signed application, documentation, checksums and verification information** rather than the private engineering source tree.

The following remain private engineering assets:

- Android engineering source
- R8 mapping files
- signing keystore and passwords
- private CI/build secrets
- internal server deployment material
- customer credentials and local control material

The public APK is built with R8 optimization/minification, resource shrinking, class repackaging/obfuscation and a non-debuggable release configuration. These measures raise the cost of unauthorized repackaging and reverse engineering; no Android binary can be made impossible to reverse engineer.

## Documentation record

The Arabic user guide documents the supported operating modes, ZeroTier remote access, IR hardware requirements, diagnostics, safe recovery procedures, and the staged VPS roadmap.

**VPS Direct remains an engineering test feature and is not presented as a public production feature.**

## Attribution

When redistributing an unmodified official binary or documentation file, preserve the **FG Machines** publisher identification and the original verification data. Modified or re-signed APKs must not be represented as official FG Machines builds.


</details>

