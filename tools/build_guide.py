from pathlib import Path
from weasyprint import HTML
import hashlib

OUT = Path("docs/FG-Link-User-Guide-AR-Illustrated-v1.6.14.pdf")
HTML_OUT = Path("/tmp/fg-link-guide.html")

RAW = r"""
FG Link 1.6.14|الدليل العربي المصوّر - الإصدار المصحح|إعداد وتشغيل وحدات MTTL-W01 محليًا وبشكل آمن.~شرح Router / LAN وOne-Phone وTwo-Phone وZeroTier.~VPS طبقة تكميلية، وVPS Direct ما زال اختباريًا وغير مطلوب للتشغيل الأساسي.|Publisher: FG Machines - Android Build 43
قبل أن تبدأ|فكرة النظام باختصار|FG Link مصمم بمنهج Local-First: التحكم المحلي يعمل دون الاعتماد على خادم خارجي.~أضف ZeroTier فقط عند الحاجة للتحكم البعيد.~لا تفتح منافذ التحكم المحلية على الإنترنت العام.|المسار الموصى به: LAN أولًا، ثم ZeroTier عند الحاجة.
محتويات الدليل 1/3|التثبيت والإعداد المحلي|صفحات 6-10: التحقق من النسخة والتثبيت والأذونات وتجهيز MTTL-W01.~صفحات 11-18: Router Mode خطوة بخطوة.~صفحات 19-24: One-Phone وTwo-Phone.|-
محتويات الدليل 2/3|التحكم البعيد والتكامل|صفحات 25-29: المخارج والطاقة والحالات.~صفحات 30-36: ZeroTier.~صفحات 37-43: VPS وIR وHome Assistant.|-
محتويات الدليل 3/3|الأمان والصيانة|صفحات 44-49: الأعطال والاستعادة.~صفحات 50-52: الأمان والتحقق من الأصالة.~صفحات 53-55: قوائم الفحص وبيانات الإصدار.|احتفظ بهذا الدليل مع ملف APK الرسمي فقط.
تنزيل النسخة الرسمية|الملف الصحيح|اسم الملف: FG-Link-1.6.14-Hardened-Signed.apk~Package: com.fgmachines.rck~Version: 1.6.14 - Build 43~نزّل التطبيق من مستودع FG Machines الرسمي فقط.|-
التحقق من SHA-256|افحص الملف قبل التثبيت|القيمة الرسمية للـAPK:~9b7c38657835d2f323f789494d36b57b0f12757964a1c20a3f69af91b682ee94~اختلاف خانة واحدة يعني أن الملف ليس مطابقًا للإصدار الرسمي.|على Windows استخدم certutil -hashfile، وعلى Linux استخدم sha256sum.
تثبيت FG Link|Android 8.0 أو أحدث|افتح ملف APK الرسمي.~اسمح بالتثبيت من المصدر المستخدم إذا طلب Android ذلك.~أكمل التثبيت ثم افتح التطبيق.~لا تحتاج إلى حساب لتشغيل التحكم المحلي.|-
الأذونات المطلوبة|لماذا يطلب التطبيق أذونات؟|الشبكة وWi-Fi لاكتشاف وربط المشترك.~الإشعارات لتنبيه المستخدم بحالة الخدمة.~قد تختلف الأذونات حسب إصدار Android والشركة المصنعة.|راجع وظيفة الصفحة قبل منح أي إذن غير واضح.
تجهيز MTTL-W01|قبل الإضافة الأولى|استخدم Wi-Fi بتردد 2.4 GHz أثناء الإعداد.~ضع الوحدة في وضع الإعداد حتى تظهر شبكة TONLY_TAP_... أو ONLY_TAP_....~اجعل الهاتف قريبًا من الوحدة والراوتر.|تأكد من كلمة مرور Wi-Fi قبل البدء.
Router Mode|الوضع الأساسي والمفضل|الهاتف والـMTTL-W01 على نفس شبكة Wi-Fi 2.4 GHz.~الهاتف يعمل كـController داخل الشبكة.~لا تحتاج إلى الإنترنت لكي تعمل أوامر LAN الأساسية.|هذا الوضع هو الأسهل للصيانة والتشخيص.
Router Mode - الخطوة 1|ابدأ إضافة المشترك|من FG Link اختر إضافة مشترك / Setup.~تأكد أن الوحدة في وضع الإعداد.~ابدأ البحث عن شبكة الإعداد الخاصة بالوحدة.|-
Router Mode - الخطوة 2|اتصل بشبكة الإعداد|وافق على الانتقال إلى شبكة TONLY_TAP أو ONLY_TAP.~رسالة لا يوجد إنترنت طبيعية أثناء الإعداد.~لا تغلق التطبيق أثناء هذه المرحلة.|-
Router Mode - الخطوة 3|اختر شبكة الموقع|اختر SSID الصحيح بتردد 2.4 GHz.~اكتب كلمة المرور بدقة.~تجنب المسافات والرموز المخفية الناتجة عن النسخ.|-
Router Mode - الخطوة 4|إرسال بيانات الشبكة|يرسل FG Link بيانات الشبكة إلى MTTL-W01.~تنتقل الوحدة من شبكة الإعداد إلى شبكة الراوتر.~انتظر حتى تكتمل العملية قبل تكرارها.|-
Router Mode - الخطوة 5|عودة الهاتف للشبكة|أعد الهاتف إلى نفس Wi-Fi.~افتح FG Link وانتظر اكتشاف الوحدة.~يفترض أن تتحول الحالة إلى Online عند نجاح الربط.|-
اختبار Router Mode|لا تعتبر الإعداد ناجحًا قبل الاختبار|شغّل وأوقف كل مخرج على حدة.~راجع أن الحالة في التطبيق تطابق الحالة الفعلية.~افصل الإنترنت مع إبقاء Wi-Fi ثم أعد الاختبار للتأكد من Local-First.|إذا فشل LAN بعد قطع الإنترنت فحل الشبكة المحلية أولًا.
تسمية المشترك|اجعل الإدارة واضحة|استخدم أسماء تصف الموقع أو الحمل: مكتب، مخزن، مضخة، كاميرات.~سمِّ المخارج بأسماء الأجهزة إن كانت الواجهة تسمح.~تجنب أسماء عامة عند وجود عدة وحدات.|-
One-Phone Mode|هاتف واحد + Hotspot|نفس الهاتف ينشئ Hotspot ويعمل كـController.~نجاحه يعتمد على قدرة الهاتف على إدارة Hotspot وWi-Fi أثناء الإعداد.~إذا أوقف الهاتف Hotspot تلقائيًا استخدم Two-Phone Mode.|-
One-Phone - تجهيز Hotspot|إعدادات مقترحة|استخدم نطاق 2.4 GHz.~اختر اسم شبكة وكلمة مرور ثابتين.~أوقف التبديل الذكي للشبكات إذا كان يسبب انقطاعًا.|لا تغيّر اسم Hotspot بعد ربط الوحدة إلا إذا كنت ستعيد إعدادها.
One-Phone - حدود معروفة|لماذا قد يفشل؟|بعض الهواتف لا تسمح بـHotspot واتصال Wi-Fi في الوقت نفسه.~بعض الأنظمة تغلق Hotspot عند الانتقال لشبكة الإعداد.~توفير الطاقة قد يوقف الخدمة في الخلفية.|عند عدم الاستقرار انتقل إلى Two-Phone Mode.
Two-Phone Mode|الموصى به عند عدم وجود راوتر|الهاتف الأول: Hotspot + Controller.~الهاتف الثاني: يستخدم فقط أثناء ربط MTTL-W01 بشبكة الهاتف الأول.~بعد الإعداد يبقى الهاتف الأول Controller الأساسي.|-
Two-Phone - خطوات الربط|تسلسل عملي|فعّل Hotspot على الهاتف الأول.~من الهاتف الثاني اتصل بشبكة إعداد MTTL-W01.~أدخل SSID وكلمة مرور Hotspot للهاتف الأول.~اختبر المخارج من الهاتف الأول بعد اكتمال الربط.|-
مقارنة أوضاع الإعداد|اختر الأنسب للموقع|Router Mode الأفضل للاستقرار الدائم.~One-Phone سريع لكنه يعتمد على قيود الهاتف.~Two-Phone عملي عند غياب الراوتر وغالبًا أكثر استقرارًا.|-
إدارة المخارج الأربعة|التحكم الأساسي|كل مخرج يجب أن يملك حالة واضحة ON/OFF.~نفّذ أمرًا واحدًا ثم انتظر التأكيد بدل النقر المتكرر.~إذا ظهرت Unknown انتظر Telemetry أو أعد فتح التحكم المحلي.|-
ألوان الحالة|كيف تقرأ الواجهة|أخضر = ON.~أحمر = OFF.~كهرماني = أمر قيد التنفيذ.~رمادي = الحالة لم تصل بعد.|الحالة الرمادية لا تعني تشغيلًا ولا إيقافًا.
الطاقة والقياسات|Telemetry|قد يعرض التطبيق بيانات الطاقة والاستهلاك والحرارة حسب ما ترسله الوحدة.~تعامل مع القياس كبيانات لحظية.~غياب Telemetry لا يعني بالضرورة تعطل المخرج.|-
الأتمتة والمشاهد|استخدمها بعد ثبات الاتصال|اختبر الأوامر اليدوية أولًا.~أنشئ المشاهد بعد التأكد من تسمية المخارج.~لا تعتمد على أتمتة حرجة قبل اختبارها عدة مرات.|-
السجل والتشخيص|حدد طبقة العطل|راجع وقت آخر اتصال.~تحقق هل المشكلة في وحدة واحدة أم كل الوحدات.~إذا كان LAN يعمل وZeroTier لا يعمل فالعطل في طبقة الوصول البعيد.|-
ZeroTier|تحكم بعيد خاص|يوفر شبكة خاصة افتراضية بين الأجهزة.~يُستخدم لإبقاء مسار التحكم بعيدًا عن الإنترنت العام.~يظل LAN مستقلًا حتى لو تعطل ZeroTier.|-
ZeroTier - إنشاء Network|من لوحة ZeroTier|أنشئ Network جديدًا.~انسخ Network ID.~لا تنشر إعدادات الشبكة بلا داعٍ.|-
ZeroTier - انضمام Controller|Join|ثبّت ZeroTier على هاتف الـController.~أدخل Network ID.~فعّل الاتصال ثم انتقل للوحة لاعتماد الجهاز عند الحاجة.|-
ZeroTier - اعتماد الجهاز|Authorize|تأكد أن الهاتف ظاهر داخل الشبكة.~فعّل Authorize للجهاز الصحيح.~راجع عنوان ZeroTier بعد الاعتماد.|-
ZeroTier - الهاتف البعيد|كرر العملية|انضم لنفس Network ID.~اعتمد الهاتف الثاني.~تأكد أن الجهازين Online قبل اختبار FG Link.|-
ZeroTier - اختبار الاتصال|افصل طبقات المشكلة|تأكد أولًا أن LAN يعمل محليًا.~ثم تأكد أن ZeroTier يربط الجهازين.~بعدها اختبر FG Link عبر المسار الخاص.|إذا فشل ZeroTier فقط فلا تعِد إعداد MTTL-W01.
ZeroTier - قواعد أمان|لا تفتح TCP 18086 للعامة|استخدم LAN أو VPN/ZeroTier لمسارات التحكم المحلية.~تجنب Port Forwarding العام.~اعتمد فقط الأجهزة التي تعرفها.|-
FG Link VPS|طبقة تكميلية|VPS لا يلغي Router/LAN/ZeroTier.~يجب أن يستمر الاستخدام المحلي إذا توقف الخادم.~اختبر LAN أولًا قبل تشخيص أي مشكلة VPS.|-
VPS API وبصمة الهاتف|مبدأ الربط|التطبيق يستخدم بصمة هاتف مخففة الخصوصية للتعريف بالتثبيت.~يمكن للإدارة ربط API بالبصمة عند تفعيل الخدمة.~API المخصص لهاتف لا ينقل إلى هاتف آخر دون إعادة ربط.|-
VPS Direct|اختباري / غير عام|يعني اتصال المشترك مباشرة بالخادم دون هاتف Controller.~هذه الوظيفة ما زالت تحت الاختبار وغير مطلوبة للمستخدمين الحاليين.~لا تغيّر إعدادات الوحدة المحلية من أجل VPS Direct قبل الإعلان عن جاهزيته.|المسارات الأساسية الحالية تبقى Router/LAN/ZeroTier.
إذا تعطل VPS|استخدم المسارات المحلية|لا تعِد ضبط الوحدة.~اختبر LAN مباشرة.~إن كنت تستخدم ZeroTier اختبره كمسار بديل.~تعامل مع VPS كخدمة إضافية وليس نقطة اعتماد وحيدة.|-
IR Remote|يتطلب IR Blaster حقيقيًا|وجود التطبيق لا يضيف IR للهاتف.~إذا لم يحتوي الهاتف على IR Blaster فلن يرسل أوامر الأشعة تحت الحمراء.~اختبر الريموت على مسافة قصيرة أولًا.|-
Home Assistant|تكامل محلي اختياري|استخدم Token محلي إذا كانت النسخة تتيح التكامل.~اربط Home Assistant بعنوان FG Link المحلي أو الخاص.~بعد نجاح التكامل يمكن تمرير الكيانات لخدمات أخرى حسب إعدادك.|-
قبل ربط أي تكامل|قاعدة ذهبية|تأكد أن التحكم اليدوي يعمل أولًا.~اختبر الوحدة دون VPS أو ZeroTier أو Home Assistant.~أضف كل طبقة منفردة ثم اختبرها.|-
المشترك لا يظهر Online|تشخيص سريع|تأكد أن الهاتف والوحدة على نفس الشبكة المطلوبة.~تحقق من 2.4 GHz وكلمة المرور.~أعد تشغيل FG Link قبل إعادة ضبط الوحدة.|-
Online لكن لا يوجد تحكم|افصل بين الاتصال والأمر|اختبر مخرجًا واحدًا.~انتظر تأكيد الحالة.~أغلق التطبيق وافتحه ثم أعد الاختبار.~إذا استمرت المشكلة أعد تشغيل الوحدة بدل حذفها فورًا.|-
الحالة Unknown|متى تكون طبيعية؟|عند بدء التطبيق قبل وصول أول Telemetry.~بعد فقد الشبكة ثم عودتها.~أثناء إعادة مزامنة الحالة.|Unknown لا تعني ON ولا OFF.
فشل الإعداد من أول مرة|تسلسل الاستعادة|تأكد من كلمة مرور Wi-Fi.~أعد الوحدة لوضع الإعداد.~جرّب Router Mode بدل One-Phone.~أعد تشغيل Wi-Fi في الهاتف ثم حاول مجددًا.|-
فشل ZeroTier فقط|لا تلمس إعداد MTTL-W01|تحقق من أن الجهازين Authorized.~تأكد أن ZeroTier متصل فعليًا على الهاتفين.~اختبر LAN؛ إذا كان يعمل فالعطل ليس في المشترك.|-
الاستعادة الآمنة|تجنب فقد الإعدادات|لا تحذف كل الأجهزة كأول خطوة.~دوّن أسماء الشبكات والوحدات قبل أي إعادة ضبط.~غيّر عنصرًا واحدًا في كل مرة ثم اختبر.|-
الأمان والخصوصية|ما الذي لا يحتاجه الخادم؟|لا يحتاج إلى كلمة مرور Wi-Fi الخاصة بالعميل.~لا يحتاج إلى أسرار ZeroTier.~لا يحتاج إلى مفاتيح توقيع APK أو Android Keystore.|لا تنشر أسرار التشغيل في المستودع العام.
التحقق من شهادة التوقيع|الاسم لا يكفي|Certificate DN: CN=FG Machines, OU=Software Release, O=FG Machines, C=EG~Certificate SHA-256:~b9ca4a23be53f161a47b5aaf97023d2bbbeebdaf671337d2466fb74cc1f29fdf|أيقونة التطبيق واسم الملف وحدهما لا يثبتان الأصالة.
مبادئ الحماية|Defense in depth|R8 optimization/minification.~Resource shrinking.~Non-debuggable release.~فصل مفاتيح التوقيع والأسرار عن المستودع العام.|الحماية ترفع تكلفة العبث ولا تجعل الهندسة العكسية مستحيلة.
قائمة فحص قبل التسليم 1/2|التشغيل|APK رسمي وhash صحيح.~وحدة MTTL-W01 باسم واضح.~اختبار المخارج الأربعة.~اختبار LAN بعد فصل الإنترنت.|-
قائمة فحص قبل التسليم 2/2|الوصول البعيد والأمان|اختبر ZeroTier فقط إذا كان مطلوبًا.~لا تفتح منافذ التحكم للعامة.~وضّح أن VPS تكميلي وأن VPS Direct غير عام بعد.~سلّم المستخدم هذا الدليل.|-
بيانات الإصدار والروابط الرسمية|FG Link 1.6.14 - Build 43|Publisher: FG Machines~Website: https://fgmachines.org~GitHub: https://github.com/FGMachines/FG-Hub~Package: com.fgmachines.rck~الدليل المصحح: 55 صفحة - عربي RTL.|ابدأ دائمًا من LAN ثم أضف الطبقات الاختيارية تدريجيًا.
"""

pages = []
for line in RAW.strip().splitlines():
    title, subtitle, bullets, note = line.split("|", 3)
    pages.append((title, subtitle, bullets.split("~"), "" if note == "-" else note))
assert len(pages) == 55, len(pages)

def art(i, title):
    c = ["#2ed282", "#55a7ff", "#ffb547", "#b7c0cc"]
    labels = ["LAN", "CTRL", "LINK", "STATE"]
    if "ZeroTier" in title: labels = ["PHONE A", "ZT", "PHONE B", "PRIVATE"]
    elif "VPS" in title: labels = ["LOCAL", "API", "VPS", "OPTIONAL"]
    elif "Router" in title: labels = ["PHONE", "ROUTER", "MTTL", "OUTLETS"]
    elif "SHA" in title or "شهادة" in title or "الأمان" in title: labels = ["HASH", "SIGN", "VERIFY", "SAFE"]
    boxes = []
    for n, (lab, col) in enumerate(zip(labels, c)):
        x = 55 + n * 205
        boxes.append(f'<rect x="{x}" y="105" width="155" height="95" rx="18" fill="#142638" stroke="{col}" stroke-width="4"/>'
                     f'<text x="{x+77}" y="160" text-anchor="middle" fill="#f5f7fa" font-size="20">{lab}</text>')
    return '<svg viewBox="0 0 900 300"><rect width="900" height="300" rx="28" fill="#0d1723"/>' + "".join(boxes) +            '<path d="M210 152 L260 152 M415 152 L465 152 M620 152 L670 152" stroke="#8ca0b4" stroke-width="4" stroke-dasharray="8 8"/></svg>'

css = """
@page { size:A4; margin:0 }
* { box-sizing:border-box }
body { margin:0; font-family:"Noto Sans Arabic","DejaVu Sans",sans-serif; background:#0b1119 }
.page { width:210mm; height:297mm; overflow:hidden; position:relative; page-break-after:always; direction:rtl; background:#f7f9fc; color:#17212d }
.header { height:31mm; padding:8mm 15mm 5mm; background:#0f2031; color:white; border-bottom:1.4mm solid #55a7ff }
.brand { font-family:"Noto Kufi Arabic","Noto Sans Arabic",sans-serif; color:#7ebcff; font-size:10pt }
.title { font-family:"Noto Kufi Arabic","Noto Sans Arabic",sans-serif; font-size:20pt; margin-top:2mm; font-weight:700 }
.subtitle { color:#c8d5df; margin-top:1mm; font-size:11pt }
.body { padding:9mm 15mm 16mm }
.art { height:64mm; margin-bottom:7mm }
.art svg { width:100%; height:100% }
ul { list-style:none; margin:0; padding:0 }
li { background:white; border:.35mm solid #d8e0e8; border-right:1.3mm solid #2ed282; border-radius:3mm; padding:3.4mm 4mm; margin-bottom:3mm; line-height:1.6; font-size:12.2pt }
li:before { content:"•"; color:#168bff; font-weight:bold; margin-left:3mm }
.note { margin-top:4mm; background:#fff4d8; border:.35mm solid #efbd56; border-radius:3mm; padding:3.5mm 4mm; color:#5b430e; font-size:11pt }
.footer { position:absolute; bottom:0; left:0; right:0; height:11mm; background:#0f1c29; color:#a8bac9; display:flex; justify-content:space-between; align-items:center; padding:0 15mm; direction:ltr; font-size:9pt }
.num { color:#58adff; font-weight:bold }
.cover .header { height:48mm; padding-top:16mm }
.cover .title { font-size:30pt }
.ltr { direction:ltr; unicode-bidi:embed; text-align:left; font-family:"DejaVu Sans",sans-serif; font-size:9.5pt }
"""

parts = [f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>{css}</style></head><body>']
for i, (title, subtitle, bullets, note) in enumerate(pages, 1):
    parts.append(f'<section class="page {"cover" if i==1 else ""}"><div class="header"><div class="brand">FG Machines • FG Link</div><div class="title">{title}</div><div class="subtitle">{subtitle}</div></div><div class="body"><div class="art">{art(i,title)}</div><ul>')
    for b in bullets:
        ltr = ("http" in b or "SHA-256" in b or b.startswith("9b7c") or b.startswith("b9ca") or b.startswith("Certificate") or b.startswith("Package:"))
        parts.append(f'<li class="{"ltr" if ltr else ""}">{b}</li>')
    parts.append("</ul>")
    if note:
        parts.append(f'<div class="note">{note}</div>')
    parts.append(f'</div><div class="footer"><span>FG Link 1.6.14 - Illustrated Arabic Guide</span><span class="num">{i} / 55</span></div></section>')
parts.append("</body></html>")
HTML_OUT.write_text("".join(parts), encoding="utf-8")
OUT.parent.mkdir(parents=True, exist_ok=True)
HTML(filename=str(HTML_OUT)).write_pdf(str(OUT))
print(f"pages={len(pages)}")
print(f"size={OUT.stat().st_size}")
print("sha256=" + hashlib.sha256(OUT.read_bytes()).hexdigest())
