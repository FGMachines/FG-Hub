# FG Link

> **Local-first smart power control, remote access, diagnostics, automation and device management for MTTL-W01.**  
> Official FG Machines distribution repository.

[![Android](https://img.shields.io/badge/Android-8%2B-3DDC84?logo=android&logoColor=white)](#download)
[![Release](https://img.shields.io/badge/FG%20Link-1.6.14-168BFF)](#download)
[![Build](https://img.shields.io/badge/build-43-2E3945)](#download)
[![Publisher](https://img.shields.io/badge/publisher-FG%20Machines-111827)](https://fgmachines.org)
[![VPS Direct](https://img.shields.io/badge/VPS%20Direct-testing-F59E0B)](#vps-status)

## العربية

**FG Link** منصة Android لإدارة مشتركات الطاقة الذكية المتوافقة مع **MTTL-W01**. صُمم النظام بمنهج **Local-First**: الوظائف الأساسية تعمل داخل الشبكة المحلية، ثم يمكن إضافة التحكم البعيد عبر **ZeroTier** أو عبر **FG Link VPS Relay** بدون تحويل الخادم إلى نقطة اعتماد وحيدة.

هذا المستودع هو **الصفحة الرسمية للتوزيع والتوثيق**. كود Android الهندسي، مفاتيح التوقيع، ملفات R8 mapping وأسرار البناء غير منشورة هنا.

## Download

### FG Link 1.6.14 — Build 43

- 📱 **[تحميل APK الرسمي الموقّع - FG Link 1.6.14](https://github.com/FGMachines/FG-Hub/releases/download/v1.6.14/FG-Link-1.6.14-Hardened-Signed.apk)**
- 📘 **[تحميل الكتاب العربي المصوّر](https://github.com/FGMachines/FG-Hub/releases/download/v1.6.14/FG-Link-User-Guide-AR-Illustrated-v1.6.14.pdf)**
- 🔐 **[التحقق من الأصالة والتوقيع](docs/AUTHENTICITY.md)**
- 🧾 **[سجل النشر والأصالة الرسمي](PROVENANCE.md)**
- **Package:** `com.fgmachines.rck`
- **APK 1.6.14 SHA-256:** `9b7c38657835d2f323f789494d36b57b0f12757964a1c20a3f69af91b682ee94`
- **Illustrated guide SHA-256:** `0098d5ba5567321158c93844c57cd9a50f34ab84bdeca2961912a5a6529939fb`
- **Signing certificate SHA-256:** `b9ca4a23be53f161a47b5aaf97023d2bbbeebdaf671337d2466fb74cc1f29fdf`

> نزّل النسخة فقط من صفحة FG Machines الرسمية، وراجع الـSHA-256 والتوقيع قبل التثبيت.

> **روابط التحميل المباشر:** هذه الروابط تستخدم GitHub Release Assets ولا تحتاج فتح الملف داخل واجهة المستودع أولًا. إذا كان متصفح الهاتف يمنع تنزيل APK، اختر Download / تنزيل من قائمة المتصفح.

- **[صفحة الإصدار الرسمية v1.6.14](https://github.com/FGMachines/FG-Hub/releases/tag/v1.6.14)**

## Start here

| الملف | الاستخدام |
|---|---|
| **FG-Link-1.6.14-Hardened-Signed.apk** | التطبيق الرسمي الموقّع والمصغّر/المشوّش عبر R8 |
| **الدليل العربي المصوّر - 55 صفحة** | شرح كامل بالصور والأسهم: Router، هاتف واحد، هاتفين، ZeroTier، IR، الأعطال والاستعادة الآمنة |
| **SHA256SUMS.txt** | التحقق من أن APK لم يتم تعديله |
| **AUTHENTICITY.md** | بصمة شهادة التوقيع وسجل الإصدار الرسمي |

> **VPS Direct ما زال Testing / Inspection وليس خدمة عامة.** النظام الحالي لا يعتمد عليه، وRouter/LAN/ZeroTier تظل المسارات المتاحة للمستخدمين.

## What FG Link does

| الوظيفة | الحالة |
|---|---|
| Router / LAN mode | ✅ Stable |
| One-phone mode | ✅ Available — depends on phone hotspot/Wi-Fi behavior |
| Two-phone mode | ✅ Recommended when no router is available |
| Multiple MTTL-W01 strips | ✅ |
| Outlet control + live state | ✅ |
| Power / energy / temperature telemetry | ✅ |
| Scenes, automation and history | ✅ |
| ZeroTier remote access | ✅ |
| FG Link VPS relay | ✅ |
| VPS admin control through controller phone | ✅ |
| **VPS Direct: strip → VPS without controller phone** | 🧪 Testing / not public |
| In-app VPS self-registration | 🧪 Prepared / disabled during testing |
| IR remote control | ✅ **Only when the Android device has an IR Blaster** |
| Arabic RTL + English and additional languages | ✅ |

## Architecture

FG Link uses a **Local-First** design. Local control remains independent, while remote-access layers are optional additions.

> **Private infrastructure:** VPS deployment, administration-panel installation, server source code, deployment scripts, credentials and internal backend configuration are private FG Machines engineering assets and are not published in this distribution repository.

## VPS status

VPS/Cloud capabilities are currently staged and tested separately from the public Android release. **VPS Direct remains under testing and is not a public feature yet.** Existing Router/LAN/ZeroTier modes continue to work independently.

## Three setup modes

### 1. Router Mode
الهاتف والمشترك على نفس شبكة Wi-Fi ‏2.4GHz، والهاتف يعمل كـController.

### 2. One-Phone Mode
نفس الهاتف يستخدم Hotspot ويعمل كـController. متاح، لكن سلوكه يعتمد على دعم الهاتف للتبديل بين Hotspot وشبكة الإعداد.

### 3. Two-Phone Mode
الهاتف الأول: Hotspot + Controller.  
الهاتف الثاني: يستخدم فقط لتوصيل المشترك بـTONLY_TAP وكتابة بيانات الهاتف الأول.  
هذا هو الوضع الموصى به عند عدم وجود راوتر ثابت.

## ZeroTier remote access

ZeroTier يوفّر شبكة خاصة بين هاتف الـController والهاتف البعيد بدون Port Forwarding عام. الدليل يشرح إنشاء Network، نسخ Network ID، Join، Authorize، الربط داخل FG Link وتشخيص الأعطال.

## IR Remote

FG Link يحتوي على وظائف ريموت للأجهزة المتوافقة. **إرسال أوامر الأشعة تحت الحمراء يتطلب هاتف Android مزودًا فعليًا بـIR Blaster.** وجود التطبيق وحده لا يضيف IR لهاتف لا يحتوي على الهاردوير.

## Engineering & security

الإصدار العام مبني كـ**hardened signed release**:

- R8 full-mode optimization/minification.
- Resource shrinking.
- App implementation classes are repackaged/obfuscated.
- Release build is non-debuggable.
- Android log calls are stripped from optimized release bytecode.
- R8 mapping files remain private.
- Signing keys and CI secrets are never committed.
- Wi-Fi passwords, ZeroTier secrets and local MTTL control material are not stored on the VPS.
- Public downloads include SHA-256 and signing-certificate identity.

الحماية ترفع تكلفة الهندسة العكسية ولا تجعلها مستحيلة. المرجع الحقيقي للنسخة الرسمية هو توقيع FG Machines + الـhash + سجل النشر.

Read: [Authenticity & verification](docs/AUTHENTICITY.md) • [Official provenance record](PROVENANCE.md) • [APK hardening](docs/APK-HARDENING.md) • [Security policy](SECURITY.md)

### Public distribution vs engineering source

هذا المستودع العام مخصص **للتوزيع الرسمي والتوثيق والتحقق من الإصدارات**. المصدر الهندسي، خرائط R8، مفاتيح التوقيع، أسرار CI والبنية الداخلية غير الضرورية للمستخدم لا تُنشر هنا. هذا لا يجعل الهندسة العكسية مستحيلة، لكنه يقلل سطح التسريب ويزيد تكلفة إعادة التغليف أو انتحال النسخة الرسمية.

## Documentation

- 📘 [الكتاب العربي المصوّر — PDF](https://github.com/FGMachines/FG-Hub/releases/download/v1.6.14/FG-Link-User-Guide-AR-Illustrated-v1.6.14.pdf)
- 📖 [دليل الاستخدام العربي — Markdown](docs/USER-GUIDE-AR.md)
- 🔐 [Authenticity & verification](docs/AUTHENTICITY.md)

## Official FG Machines links

- Website: https://fgmachines.org
- Facebook page: https://www.facebook.com/share/1T7r3WpH8Y/
- Developer profile: https://www.facebook.com/share/1EKVAyZZ2C/
- Email: info@fgmachines.org
- GitHub: https://github.com/FGMachines/FG-Hub

تابع الصفحة والحساب الرسميين؛ سيتم نشر **برمجيات وأدوات ومشاريع FG Machines أخرى** تباعًا.

---

**Publisher:** FG Machines  
**Android package:** `com.fgmachines.rck`  
**Current engineering build:** `1.6.14 / build 43`
