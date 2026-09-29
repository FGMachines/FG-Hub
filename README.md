# FG Link

Official FG Machines distribution repository for **FG Link**.

## Current release track

- Product: FG Link
- Android package: `com.fgmachines.rck`
- Public release target: **1.6.12**
- Publisher: **FG Machines**
- Distribution model: official compiled Android APK
- Source code is not published in this repository.

The public APK will be accompanied by a SHA-256 checksum so users can verify that the file is the official FG Machines build.

## Security

Do not trust repackaged or re-signed copies distributed by third parties. Verify the package name, version and published SHA-256 checksum before installation.

FG Machines signing material, build secrets and private engineering material are never stored in this public repository.


## الاستخدام

- [دليل الاستخدام بالعربية](docs/USER-GUIDE-AR.md)
- [بنية الخادم الاختياري والحماية](docs/SERVER-ARCHITECTURE-AR.md)

سيتم إضافة لقطات شاشة حقيقية من الإصدار النهائي داخل `docs/images/` بعد نجاح Build النهائي؛ لن نستخدم صورًا تجريبية.

## مبدأ التشغيل

FG Link يعمل محليًا أولًا، مع خادم VPS فعّال للإدارة والتحكم عن بُعد. التطبيق يعرض بصمة هاتف مكوّنة من 64 خانة؛ تُستخدم البصمة لإنشاء API مرتبط بهذا الهاتف بدل كتابة أسماء العملاء. يظل LAN وZeroTier متاحين ولا يعتمد التشغيل المحلي على الخادم. تعرض لوحة VPS زرًا واحدًا لكل مخرج: أخضر عند التشغيل، أحمر عند الإغلاق، كهرماني أثناء تنفيذ الأمر، ورمادي عندما لم تصل حالة موثوقة بعد.

إصدار الخادم الحالي: **1.6.12** داخل `server/1.6.12/`.
