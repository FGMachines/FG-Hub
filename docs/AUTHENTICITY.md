# FG Link — التحقق من النسخة الرسمية

الإصدار الحالي **2.1.2 / versionCode 47**، الناشر **FG Machines**، الحزمة `com.fgmachines.rck`.

- [تحميل APK الرسمي](https://github.com/FGMachines/FG-Hub/releases/download/v2.1.2/FG-Link-2.1.2-v47.apk)
- APK SHA-256: `07c9307f9657b02c6893174a37f2a60701b0afae4c30985877599cc5abfeff0f`
- شهادة التوقيع SHA-256: `b9ca4a23be53f161a47b5aaf97023d2bbbeebdaf671337d2466fb74cc1f29fdf`
- شهادة الناشر: `CN=FG Machines, OU=Software Release, O=FG Machines, C=EG`

```bash
sha256sum FG-Link-2.1.2-v47.apk
apksigner verify --verbose --print-certs FG-Link-2.1.2-v47.apk
```

قارن بصمة الملف وبصمة الشهادة بالقيم أعلاه. اسم الملف أو الأيقونة وحدهما لا يثبتان الأصالة. التوقيع هو نفسه المستخدم للنسخة الرسمية السابقة، مع رقم بناء أعلى، ليُثبّت كتحديث مباشر حين يكون رقم النسخة المثبتة أقل من 47.

المصدر البرمجي ومفتاح التوقيع وكلمات المرور وخرائط التشويش لا تُنشر. راجع [سجل النشر](../PROVENANCE.md) و[الدليل المصوّر](USER-GUIDE-AR.md).

## النسخة السابقة المؤرشفة

إصدار 1.6.14 / Build 43: `FG-Link-1.6.14-Hardened-Signed.apk`، SHA-256: `9b7c38657835d2f323f789494d36b57b0f12757964a1c20a3f69af91b682ee94`. [صفحة الإصدار المؤرشف](https://github.com/FGMachines/FG-Hub/releases/tag/v1.6.14). دليله القديم لا يصف واجهة Direct VPS في 2.1.2.

