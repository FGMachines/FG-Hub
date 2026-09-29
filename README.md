# FG Link

Official FG Machines distribution repository for **FG Link**.

## Latest Android release

**FG Link 1.6.13 — Build 42**

Package: **com.fgmachines.rck**

Publisher: **FG Machines**

Direct APK download:

https://raw.githubusercontent.com/FGMachines/FG-Hub/main/releases/1.6.13/FG-Link-1.6.13-Hardened-Signed.apk

SHA-256:

327f639f73e192c642c2fdd75af842cfd4a5825d6c26d87d3ec64ebc6dbc3824

Full Arabic usage guide:

https://github.com/FGMachines/FG-Hub/blob/main/docs/USER-GUIDE-AR.md

## الاستخدام السريع

1. ثبّت النسخة الرسمية.
2. أضف مشترك MTTL-W01 وأكمل ربطه بشبكة Wi-Fi ‏2.4 GHz.
3. افتح قسم **FG Link VPS**.
4. انسخ **بصمة الهاتف** وأرسلها إلى إدارة FG Machines.
5. تستلم API مربوطًا ببصمة الهاتف.
6. الصق الـAPI فقط داخل التطبيق.
7. لا يحتاج العميل إلى كتابة عنوان الخادم؛ العنوان ثابت داخل التطبيق:
   **https://link.fgmachines.org**
8. بعد الربط يبدأ التطبيق في مزامنة حالة الهاتف والمشتركات والمخارج مع VPS.
9. في لوحة الخادم يظهر لكل مخرج زر واحد:
   - أخضر = متصل.
   - أحمر = مغلق.
   - كهرماني = جارٍ تنفيذ الأمر.
   - رمادي = الحالة غير معروفة بعد.

## VPS architecture

FG Link يعمل محليًا أولًا مع خادم VPS فعّال للإدارة والتحكم عن بُعد. الهاتف هو طبقة التنفيذ الفعلية: يستقبل الأمر عبر HTTPS ثم ينفذه محليًا على MTTL-W01 ويرسل النتيجة للخادم.

الخادم لا يحتاج إلى تخزين كلمة مرور Wi-Fi أو أسرار ZeroTier أو MAC الخام للمشترك.

Current server package: **1.6.12**

Server files:

https://github.com/FGMachines/FG-Hub/tree/main/server/1.6.12

Server architecture:

https://github.com/FGMachines/FG-Hub/blob/main/docs/SERVER-ARCHITECTURE-AR.md

## Security

Do not trust repackaged or re-signed copies distributed by third parties.

Before installing, verify:

- Package name: **com.fgmachines.rck**
- Version: **1.6.13**
- Version code: **42**
- SHA-256: **327f639f73e192c642c2fdd75af842cfd4a5825d6c26d87d3ec64ebc6dbc3824**

FG Machines signing material, build secrets, and private engineering material are not published in this distribution repository.

## Official links

Website: https://fgmachines.org

FG Link VPS: https://link.fgmachines.org

Repository: https://github.com/FGMachines/FG-Hub
