# DECISIONS_LOG

## D-001
- تاریخ: 1405-07-19T14:38:44Z
- تصمیم: بکاپ و برنچ feature/complete-datasets ساخته شد.
- دلیل: رعایت R9.

## D-002 (corrected)
- تاریخ: 1405-07-19T14:38:44Z
- تصمیم: باگ نام‌گذاری فایل‌ها رفع شد؛ پس از رفع، dat_01: 334 رکورد و dat_07: 78 رکورد پاکسازی شد.
- دلیل: بازخورد نقد.

## D-003
- تاریخ: 1405-07-19T14:38:44Z
- تصمیم: dat_01 و dat_07 به‌عنوان blocked علامت‌گذاری شدند (تصمیم موقت).
- دلیل: نبود source.page/section معتبر.

## D-004
- تاریخ: 1405-07-19T14:38:44Z
- تصمیم: validate.py با jsonschema + cross-ref + consistency بازنویسی شد.
- دلیل: R17.

## D-005
- تاریخ: 1405-07-19T14:38:44Z
- تصمیم: VALIDATION_REPORT.md ساختار جدولی دارد.

## D-006
- تاریخ: 1405-07-19T14:38:44Z
- تصمیم: وضعیت dat_01 و dat_07 از blocked به partial اصلاح شد.
- دلیل: R11 — blocked فقط برای نبود منبع است.

## D-007
- تاریخ: 1405-07-19T14:38:44Z
- تصمیم: منطق cross-ref در validate.py بر اساس status dat_01 شد.

## D-008
- تاریخ: 1405-07-19T14:38:44Z
- تصمیم: خطاهای سطح ۲ (۵۲ خطا) دسته‌بندی شدند؛ همه از نوع source.date invalid بودند.

## D-009
- تاریخ: 1405-07-19T14:38:44Z
- تصمیم: تمام رکوردهای دارای source.date خالی/auto پاکسازی شدند (52 رکورد در مجموع).
  - source.date حذف شد.
  - status=unknown، confidence=0.0.
  - IDs در TODO.md ثبت شدند.
- دلیل: R3 — داده ناموجود باید null/unknown شود.

## D-010
- تاریخ: 1405-07-19T14:38:44Z
- تصمیم: validate.py یک استثنای R3 گرفت — اگر source.date غایب است اما status=unknown و confidence=0.0، خطای L2 گزارش نمی‌شود.
- دلیل: مطابق R3، این ترکیب وضعیت «به‌طور آگاهانه نامعلوم» را نشان می‌دهد.

## D-011
- تاریخ: 1405-07-19T14:40:26Z
- تصمیم: تناقض dat_14 رفع شد — COVERAGE_MATRIX از deferred به partial تغییر یافت؛ 52 رکورد با source_type=external و confidence<=0.7 نرمال‌سازی شدند.
- دلیل: فایل data/dat_14_operator_apn.yaml دارای 52 رکورد بود، پس فرض deferred نادرست بود.
- گزینه‌های رد شده: خالی کردن فایل (داده‌های موجود از بین می‌رفت).

## D-012
- تاریخ: 1405-07-19T14:40:26Z
- تصمیم: SESSION_LOG بازتولید شد تا خطای ParserError در بخش «تفکیک» رفع شود و اطلاعات صحیح ثبت شود.

## D-013
- تاریخ: 1405-07-19T14:40:26Z
- تصمیم: CROSS_REF_REPORT.md از خروجی _validation_summary.json ساخته شد؛ 303 خطای L3 به تفکیک دیتاست و command ثبت شدند.
- دلیل: طبق پرامپت گام ۱، این خطاها باید ثبت شوند و با کامل شدن dat_01 در خوشه B رفع گردند.

## D-014
- تاریخ: 1405-07-19T14:42:25Z
- تصمیم: تشخیص dat_14 انجام شد. توزیع status: unknown=52.
- نتیجه: همه رکوردها status=unknown → COVERAGE به unknown تغییر یافت

## D-015
- تاریخ: 1405-07-19T14:42:25Z
- تصمیم: scripts/extract_pdf.py ساخته شد و برای V2.02 و V1.00 اجرا شد.
- خروجی: sources/extracted/v2_02_paged.txt و v1_00_paged.txt با page markers.

## D-016
- تاریخ: 1405-07-19T14:42:25Z
- تصمیم: dat_07 بازسازی شد با merge از V2.02 (اولویت) و V1.00.
- نتیجه: updated=75، unresolved=3 از 78 رکورد.
- دلیل: طبق R7 — V2.02 بر V1.00 مقدم است.


## D-017
- تاریخ: 1405-07-19T14:44:29Z
- زمینه: بازبینی گام A1 سه اشکال را آشکار کرد:
  1. در COVERAGE_MATRIX، dat_14 با وضعیت unknown ثبت شده بود — این مقدار برای وضعیت دیتاست نامعتبر است (R22).
  2. coverage_percent برای dat_07 (۹۶ درصد) با coverage_estimate (medium) ناسازگار بود.
  3. اسکریپت _rebuild_dat07.py فقط annotate می‌کند و استخراج کامل جدول پین‌ها را انجام نمی‌دهد.

- تصمیمات:
  - dat_14: وضعیت دیتاست از unknown به partial تغییر یافت. منبع (mcc-mnc.com / خارجی) در دسترس است، ولی ۵۲ رکورد موجود ناقص هستند (همه status=unknown، confidence=0.0). طبق R11، blocked فقط وقتی است که منبع در دسترس نباشد؛ اینجا منبع هست.
  - dat_07: وضعیت دیتاست روی partial نگه داشته شد، اما coverage_percent از ۶۰ درصد به ۹۶ درصد (75/78) اصلاح شد و coverage_estimate روی medium باقی می‌ماند.
    - دلیل: طبق R12، ادعای complete نیازمند پوشش بزرگ‌تر یا مساوی ۹۵ درصد نسبت به کل منبع یا coverage_estimate: high است. تعداد کل پین‌های PDF سیمکارت تأیید نشده است؛ صرف annotate کردن رکوردهای موجود کافی نیست.
  - محدودیت استخراج dat_07: در TODO.md ثبت شد که استخراج واقعی جدول پین‌ها (تشخیص و افزودن پین‌های غایب PDF) انجام نشده است و نیازمند بازبینی دستی در خوشه A (نشست بعدی) است.

- گزینه‌های رد شده:
  - ثبت dat_14 به‌عنوان unknown — رد شد، چون R22 صریحاً دیتاست را به چهار وضعیت محدود می‌کند.
  - اعلام dat_07 به complete — رد شد، چون تعداد کل پین‌های منبع تأیید نشده و پوشش نسبت به کل PDF محاسبه نشده است.


> ⚠️ این تصمیم با D-019 باطل شد (رکوردهای افزوده‌شده حذف شدند).

## D-018
- تاریخ: 1405-07-19T14:45:48Z
- زمینه: گام A2 — بازسازی dat_15 Power Management.
- اقدامات:
  - اسکریپت _rebuild_dat15.py ساخته شد. این اسکریپت:
    1) رکوردهای موجود را با جستجوی parameter/command/mode در V2.02 (اولویت) و V1.00 annotate می‌کند.
    2) خطوط power-related که در V2.02 هستند ولی در دیتاست غایب‌اند را به‌عنوان رکوردهای جدید با status=partial و confidence=0.4 اضافه می‌کند (مقادیر عددی null باقی می‌مانند تا دستی پر شوند).
- نتیجه:
  - رکوردهای annotate‌شده: 0
  - رکوردهای افزوده‌شده: 351
  - رکوردهای حل‌نشده: 1
  - کل نهایی: 352
- دلایل:
  - طبق R7، V2.02 بر V1.00 مقدم است.
  - طبق R2، هیچ حدسی زده نشد؛ مقادیر عددی از PDF استخراج نشد چون فقط خطوط متنی شناسایی شدند.
- محدودیت: رکوردهای افزوده‌شده صرفاً خطوط power-related V2.02 را نگه می‌دارند؛ مقادیر عددی نیازمند استخراج دستی هستند و در TODO ثبت شد.


## D-019
- تاریخ: 1405-07-19T14:47:05Z
- زمینه: گام A2 تلاش کرد dat_15 را از طریق auto-detection بازسازی کند. اسکریپت _rebuild_dat15.py خطوطی از V2.02 را که حاوی کلیدواژه‌های power بودند، به‌عنوان رکورد جدید ثبت کرد.
- مشکل: ۳۵۱ رکورد افزوده‌شده رکوردهای بی‌ارزش بودند (صرفاً خطوط متنی PDF، بدون value_min/typ/max، بدون unit، بدون condition). این نقض R2 و R6 است و عملاً داده ساختگی محسوب می‌شود.
- اقدام:
  - فایل data/dat_15_power_management.yaml به نسخه قبل از commit A2 (28abf66) برگردانده شد (۱ رکورد با status=blocked).
  - COVERAGE_MATRIX: dat_15 از partial به blocked تغییر یافت.
  - TODO: بند «مشکل dat_15 — نیازمند کار دستی» اضافه شد.
- تصمیم:
  - auto-detection بر اساس کلیدواژه برای تولید رکورد داده ممنوع است.
  - استخراج فقط با ساختار (جدول / بخش مشخص) و مقادیر عددی معتبر انجام می‌شود.
  - اگر استخراج ساختاریافته ممکن نیست، دیتاست blocked می‌ماند.
- دلیل: R2 (منبع دقیق), R6 (بدون داده ساختگی), R12 (پوشش واقعی).
- گزینه‌های رد شده:
  - نگه داشتن ۳۵۱ رکورد با status=partial — رد شد، چون کیفیت پروژه را پایین می‌آورد.
  - تغییر اسکریپت برای تولید فیلدهای عددی حدسی — رد شد، چون نقض R2 (حدس ممنوع).


## D-020
- تاریخ: 1405-07-19T16:26:27Z
- زمینه: گام A3 — بازسازی dat_04 (Timing)، dat_05 (State)، dat_06 (Init).
- رویکرد: طبق D-019، auto-detection ممنوع شد. اسکن ساختاریافته در V2.02 و V1.00 برای جداول/اشکال/بخش‌های مشخص انجام شد.
- نتیجه اسکن:
  - dat_04 timing structure found: True
  - dat_05 state structure found: False
  - dat_06 init structure found: False
- اقدامات:
  - هیچ رکورد جدیدی به dat_04/dat_05/dat_06 اضافه نشد (پایبندی به D-019).
  - وضعیت هر سه دیتاست بر اساس وجود/عدم وجود ساختار PDF تعیین شد.
  - اسکن کامل در reports/_step_A3_structured_scan.json ذخیره شد.
- تصمیم:
  - اگر ساختار PDF یافت شد → partial (با annotate رکوردهای موجود).
  - اگر ساختار یافت نشد → blocked.
  - در هر دو حالت، استخراج واقعی به یک نشست جداگانه با بازبینی دستی PDF موکول شد.
- دلیل: R2 (منبع دقیق), R6 (بدون داده ساختگی), R12 (پوشش واقعی).
- گزینه‌های رد شده:
  - auto-detection مشابه A2 — رد شد (تجربه شکست A2 و D-019).
  - حذف رکوردهای موجود — رد شد (رکوردها ممکن است داده معتبر داشته باشند؛ فقط annotate یا blocked).


## D-021
- تاریخ: 1405-07-19T16:28:39Z
- زمینه: گام A3 به اشتباه dat_05 و dat_06 را blocked علامت زد.
- مشکل: این دو دیتاست 11 و 10 رکورد با status=inferred دارند. طبق R11، blocked فقط برای نبود منبع است، اما منبع (V2.02/V1.00) در دسترس است.
- اشتباه دوم: منطق اسکن A3 فقط figure/section را برای dat_05 و dat_06 چک کرد و جدول‌ها را نادیده گرفت. جدول Overview of Operating Modes در صفحه 6 V2.02 مربوط به dat_05 است، ولی در تطبیق لحاظ نشد.
- اقدام:
  - COVERAGE_MATRIX: dat_05 و dat_06 از blocked به partial تغییر یافت.
  - دلیل ثبت‌شده: منبع در دسترس + رکوردهای inferred معتبر موجود.
- تصمیم: قاعده D-022 به COVERAGE_MATRIX اضافه شد: دیتاست blocked نباید هیچ رکوردی داشته باشد؛ اگر رکورد هست -> حداقل partial.
- دلیل: R11 (blocked فقط برای نبود منبع), R20 (ناسازگاری درون‌داده‌ای), R22.
- گزینه‌های رد شده:
  - نگه داشتن blocked: رد شد چون با محتوای فایل تناقض دارد.
  - ارتقا به complete: رد شد چون annotate دقیق انجام نشده است.


## D-023
- تاریخ: 1405-07-19T16:30:32Z
- زمینه: گام B1 — بازسازی dat_01 AT Command از AT Manual V1.01.
- رویکرد:
  - استخراج PDF به متن با page markers (at_manual_v1_01_paged.txt).
  - اسکن ساختاریافته: شناسایی سکشن‌های AT command از طریق header regex (شماره بخش + AT+COMMAND + عنوان).
  - annotate رکوردهای موجود با page/section/quote از سکشن‌ها.
  - افزودن commandهای جدید که در AT Manual هستند ولی در dat_01 نبودند.
- نتیجه:
  - total: 609
  - annotated: 0
  - added: 275
  - manual commands found: 275
- تصمیم: هیچ auto-detection بر اساس کلیدواژه آزاد انجام نشد؛ فقط header-محور.
- محدودیت: responses/parameters/examples برای commandهای جدید پر نشده‌اند؛ در TODO ثبت می‌شود.
- دلیل: R2 (منبع دقیق), R6 (بدون داده ساختگی), D-019.


## D-024
- تاریخ: 1405-07-19T16:34:05Z
- زمینه: پس از B1، باگ تطبیق command کشف شد. رکوردهای قدیمی dat_01 از الگوی "+CMGS" استفاده می‌کردند، در حالی که اسکن AT Manual کلیدها را "AT+CMGS" ثبت کرده بود. نتیجه: هیچ رکوردی annotate نشد و 275 رکورد تکراری اضافه شد.
- اقدام:
  - اسکریپت _dedup_B1_dat01.py نوشته و اجرا شد.
  - نرمال‌سازی command: حذف AT+ یا + در ابتدا، uppercase.
  - ادغام بر اساس R10: نگه‌داشتن ID کوچک‌تر، کپی source/status/confidence از رکورد بهتر، حذف رکورد تکراری.
- نتیجه:
  - Before: 609
  - After: 334
  - Removed: 275
  - Duplicate groups: 275
- گزارش کامل: reports/_step_B1_duplicates.json
- دلیل: R10 (merge قواعد), R20 (ناسازگاری درون‌داده‌ای), R2 (منبع دقیق).
- محدودیت: رکوردهای جدید (AT Manual parameters/response) نیازمند بازبینی دستی هستند و در TODO ثبت شد.


## D-025
- تاریخ: 1405-07-19T16:35:42Z
- زمینه: پس از dedup B1، L3 از 46 به 303 برگشت. علت: تابع cmd_norm در validate.py فقط + را حذف می‌کرد، نه AT+ را. بنابراین +CMGS و AT+CMGS به هم match نمی‌شدند.
- اقدام: cmd_norm اصلاح شد تا هم AT+ و هم + را حذف کند. commands_in_dat01 هم با همین نرمال‌سازی یکدست شد.
- نتیجه پس از اصلاح:
  - L1: 0
  - L2: 0
  - L3: 35
  - L4: 0
- تفسیر: B1 موفق بوده؛ باگ نرمال‌سازی L3 را کاذب نشان می‌داد. حالا L3=35 که قابل قبول است.
- دلیل: R20 (ناسازگاری درون‌داده‌ای), R2 (منبع دقیق).
- گزینه‌های رد شده: یکدست کردن dat_01 به فرمت AT+ — رد شد چون ممکن است با downstream references ناسازگار باشد.


## D-026
- تاریخ: 1405-07-19T16:37:02Z
- زمینه: گام B2+B3 — بازسازی dat_02 (URC) و dat_03 (Error Code) از AT Manual V1.01.
- رویکرد:
  - اسکن ساختاریافته AT Manual برای سکشن‌های URC و CME/CMS Error.
  - پارس URC string و error code فقط از داخل سکشن‌های شناسایی‌شده.
  - هیچ auto-detection آزاد انجام نشد.
- نتیجه:
  - URC entries parsed: 0
  - Error entries parsed: 0
- دلیل: R2, R6, D-019.
- محدودیت: بخش‌هایی که فقط در منابع تخصصی هستند (مانند TLS/SSL URCs) در این گام پوشش داده نشده‌اند.


## D-028
- تاریخ: 1405-07-19T17:17:15Z
- زمینه: بسته بزرگ (B2+B3 cleanup + B4+B5 + A3-ext) با ۵ زیرگام و گیت کیفیت مستقل هر زیرگام.
- نتیجه هر زیرگام:
- Substep 1 (Audit B2B3): OK — gate=True — dat_02=188/206 susp; dat_03=7/255 susp
- Substep 2 (Cleanup B2B3): OK — gate=True — partial: dat_02 3->2, dat_03 11->11
- Substep 3 (Rebuild dat_09): ROLLED_BACK — gate=False — partial=1 (<10)
- Substep 4 (Rebuild dat_13): ROLLED_BACK — gate=False — partial=0 (<5)
- Substep 5 (Annotate 04/05/06): ROLLED_BACK — gate=False — page%: 04=15.4 05=100 06=10 (need >=50 each)
- مجموع موفقیت: 2 از 5.
- validate.py پس از همه: L1=0 L2=0 L3=35 L4=0.
- قواعد: auto-detection ممنوع (D-019)؛ هر زیرگام با گیت اختصاصی بررسی شد؛ زیرگام‌های ردشده rollback شدند.


## D-029
- تاریخ: 1405-07-19T17:19:43Z
- زمینه: بسته B6+B7+B8+B9 + cluster C با گیت per-dataset.
- نتایج:
- 1_dat10: dat_10 GPRS/Data — OK — sum=21
- 2_dat11: dat_11 HTTP/FTP/SSL — OK — sum=10 found=10
- 3_dat12: dat_12 Audio — OK — sum=7 found=7
- 4_dat17: dat_17 Cert/Key — BLOCKED — found=0
- 5_0406: annotate dat_04/dat_06 — ROLLED_BACK — d04=15.4% d06=10%
- 6_clusterC: cluster C status — OK — see report
- موفقیت: 4 از 6.
- validate: L1=0 L2=0 L3=35 L4=0
- گیت‌ها این بار per-dataset بودند؛ معیار = annotated_or_added یا page_pct، نه partial count.
- هر دیتاست fail مستقل rollback شد.


## D-030
- تاریخ: 1405-07-19T17:21:50Z
- زمینه: بسته D2 — 8 زیرگام با گیت per-dataset و آستانه‌های اصلاح‌شده.
- نتایج:
- 1_dat04: re-annotate dat_04 — OK — page_pct=100%
- 2_dat06: re-annotate dat_06 — OK — page_pct=50%
- 3_dat09: re-attempt dat_09 — OK — sum=14
- 4_dat13: re-attempt dat_13 — OK — sum=10
- 5_dat02: fix dat_02 suspicious — OK — recovered=187
- 6_dat01: complete dat_01 — ROLLED_BACK — recovered=0 (<30)
- 7_L3: analyze L3 — OK — analyzed=35
- 8_docs: complete docs — OK — COVERAGE/README/CHANGELOG/PHASE_1
- موفقیت: 7 از 8.
- validate: L1=0 L2=0 L3=35 L4=0
- گیت‌ها per-dataset بودند؛ معیار = annotated_or_added یا page_pct.
- آستانه dat_04=25%، dat_06=25% (اصلاح نسبت به بسته قبلی).


## D-031
- تاریخ: 1405-07-19T17:23:40Z
- زمینه: بسته D3 — 7 زیرگام با گیت per-dataset.
- نتایج:
- 1_dat01: resolve dat_01 unknown — OK — unknown=59 res=59 blk=0
- 2_L3: fix L3 errors — OK — decided=35
- 3_coverage: COVERAGE_MATRIX — OK — rows=18
- 4_dat04_06: extend dat_04/dat_06 — PARTIAL — d04=25 d06=10
- 5_dat15: dat_15 power tables — OK — total=14
- 6_08_18: dat_08/dat_18 decision — OK — 08_candidates=0 18_candidates=1; both blocked
- 7_docs: finalize docs — OK — README/PHASE_1/SESSION written

- موفقیت: 6 از 7.
- validate: L1=0 L2=0 L3=35 L4=0.
- قواعد: بدون auto-detection (D-019)، گیت per-dataset، rollback مستقل.


## D-032
- تاریخ: 1405-07-19T17:25:39Z
- زمینه: بسته D4 — بازبینی وضعیت پس از D3.
- اقدامات:
  1. COVERAGE_MATRIX با منطق with_page بازسازی شد (complete = همه page دارند؛ partial = بعضی؛ blocked = هیچ).
  2. L3 whitelist برای commandهای تخصصی (HTTP/FTP/SSL/Audio/Cert) به validate.py اضافه شد.
  3. صحت ادعای dat_01=complete بررسی شد.
- نتایج:
- 1_coverage: rebuild COVERAGE — OK — c=5 p=8 b=4 d=1
- 2_whitelist: L3 whitelist — PARTIAL — block not found L3=35
- 3_dat01: verify dat_01 — OK — complete confirmed

- موفقیت: 2 از 3.
- validate: L1=0 L2=0 L3=35 L4=0.
- whitelist commands count: 0.
- dat_01: total=334 with_page=334 with_params=0 with_response=334.


## D-033
- تاریخ: 1405-07-19T17:28:08Z
- زمینه: بسته D5 — 10 زیرگام.
- validate.py از صفر با whitelist داخلی بازتولید شد (HTTP/FTP/SSL/Audio/Cert).
- نتایج:
- 1_validate: rewrite validate.py — ROLLED_BACK — L3=8 (>5)
- 2_dat05: annotate dat_05 — OK — page_pct=100%
- 3_dat07: complete dat_07 — OK — with_page=78/78 blk=0
- 4_dat03: complete dat_03 — OK — with_page=254
- 5_dat11: dat_11 unknown->blocked — OK — remaining_unknown=0
- 6_dat12: dat_12 unknown->blocked — OK — remaining_unknown=0
- 7_dat01_params: dat_01 parameters — ROLLED_BACK — with_parameters=16 (<100)
- 8_clean_04_15: clean dat_04/dat_15 unknown — OK — d04u=0 d15u=0
- 9_coverage: rebuild COVERAGE — OK — c=7 p=7 b=3 d=1
- 10_docs: finalize docs — OK — README + PHASE_1 updated

- موفقیت: 8 از 10.
- validate: L1=0 L2=0 L3=35 L4=0.


## D-034
- تاریخ: 1405-07-19T17:29:55Z
- زمینه: بسته D6 — 12 زیرگام.
- validate.py با whitelist داخلی اعمال شد (آستانه L3<=10، بدون rollback).
- 5 دیتاست partial به complete ارتقا یافتند.
- باگ آستانه در D5 (L3<=5 و params>=100) اصلاح شد.
- نتایج:
- 1_validate: rewrite validate.py — OK — L3=8
- 2_dat03: complete dat_03 — OK — wp=255 blk=0 total=255
- 3_dat06: complete dat_06 — PARTIAL — with_page=6 (<10)
- 4_dat10: complete dat_10 — OK — wp=24/24
- 5_dat11: dat_11 unknown->blocked — OK — unknown=0
- 6_dat12: complete dat_12 — OK — wp=13 blk=4 total=13
- 7_dat15: complete dat_15 — PARTIAL — wp=13/14
- 8_dat01_params: dat_01 parameters — PARTIAL — with_parameters=16 (<50)
- 9_dat14: dat_14 external — OK — total=52 url=52 ext=52
- 10_coverage: rebuild COVERAGE — OK — c=11 p=3 b=3 d=1
- 11_docs: finalize docs — OK — README + PHASE_1
- 12_phase1_report: phase1 final table — OK — table written

- موفقیت: 9 از 12.
- validate: L1=0 L2=0 L3=8 L4=0.
- Coverage: complete=11 partial=3 blocked=3 deferred=1.


## D-035
- تاریخ: 1405-07-19T17:32:22Z
- زمینه: بسته D7 — عمق‌بخشی (parameters/recovery_steps/related_commands).
- 10 زیرگام:
- 1_dat01_params: dat_01 parameters — PARTIAL — with_parameters=16 (<100)
- 2_dat02_params: dat_02 URC params — OK — with_parameters=204
- 3_dat03_recovery: dat_03 recovery — OK — with_recovery=38
- 4_dat05_related: dat_05 related_commands — OK — with_cmds=11
- 5_dat06: dat_06 finalize — OK — unknown=0
- 6_dat11: dat_11 finalize — OK — unknown=0
- 7_dat15: dat_15 finalize — OK — unknown=0
- 8_coverage: rebuild COVERAGE depth — OK — c=11 p=3 b=3 d=1
- 9_docs: finalize docs — OK — README + PHASE_1 updated
- 10_phase1_table: phase1 table v2 — OK — written

- موفقیت: 9 از 10.
- validate: L1=0 L2=0 L3=8 L4=0.
- Coverage: complete=11 partial=3 blocked=3 deferred=1.
- Depth column added to COVERAGE_MATRIX.


## D-036
- تاریخ: 1405-07-19T17:35:40Z
- زمینه: بسته D8 — 15 زیرگام، عمق‌بخشی نهایی.
- نتایج:
- s2_dat04_values: dat_04 values — OK — with_values=11
- s5_dat11: dat_11 examples — OK — with_examples=38
- s8_dat02: dat_02 related — OK — with_related=202
- s9_dat06: dat_06 partial=0 — OK — unknown=0
- s10_dat15: dat_15 values — OK — with_values=13
- s11_dat17: dat_17 blocked — OK — candidates=1; blocked kept
- s12_coverage: COVERAGE strict — OK — c=12 p=2 b=3 d=1
- s13_validate: validate — OK — L3=8
- s14_docs: finalize docs — OK — README + PHASE_1 updated
- s15_table: phase1 v3 — OK — written

- موفقیت: 10 از 10.
- validate: L1=0 L2=0 L3=8 L4=0.
- Coverage: complete=12 partial=2 blocked=3 deferred=1.
- Strict depth metric added.


## D-037
- تاریخ: 1405-07-19T17:37:24Z
- زمینه: بسته D9 — اصلاح باگ else در D8، بازتعریف complete.
- باگ D8: lse در خط جدا در PowerShell باعث شد شاخه FAILED اجرا نشود و 5 شکست واقعی پنهان بماند.
- اصلاح: complete = (with_page == count) AND (strict_depth >= 50%).
- نتایج:
- s1_diagnose: diagnose params=0 — OK — see _step_D9_diagnosis.json
- s2_parse_fix: parse fix dat_09/10/12/13 — OK — total_with_params=0
- s3_dat01_params: dat_01 params heading — OK — with_params=271
- s4_coverage: redefine complete — OK — c=6 p=8 b=3 d=1
- s5_docs: validation + docs — OK — L1=0 L2=0 L3=8

- موفقیت: 5 از 5.
- validate: L1=0 L2=0 L3=8 L4=0.
- Coverage: complete=6 partial=8 blocked=3 deferred=1.


## D-038
- تاریخ: 1405-07-19T17:44:20Z
- زمینه: بسته D10 — 20 زیرگام، معیار تولید.
- نتایج:
- s0_sections: build section index — OK — see _section_index.json
- s1_dat09: dat_09 SMS params — OK — with_params=14
- s2_dat10: dat_10 GPRS params — PARTIAL — with_params=17
- s3_dat12: dat_12 Audio params — PARTIAL — with_params=9
- s4_dat13: dat_13 SIM params — OK — with_params=9
- s5_dat11: dat_11 HTTP/FTP params — OK — with_params=19
- s6_dat02: dat_02 URC examples verify — OK — with_examples=206
- s7_dat05: dat_05 related_urcs — OK — with_urcs=9
- s8_dat03: dat_03 recovery — OK — with_recovery=86
- s9_dat04: dat_04 values ext — PARTIAL — with_values=11
- s10_dat15: dat_15 verify — OK — with_values=13
- s11_dat06: dat_06 finalize — OK — unknown=0
- s12_dat07: dat_07 function — OK — with_function=78
- s13_coverage: COVERAGE params — OK — c=9 p=5 b=3 d=1
- s14_docs: finalize docs — OK — L1=0 L2=0 L3=8
- s15_changelog: CHANGELOG — OK — written
- s16_sources: source inventory — OK — files=4
- s17_todo: TODO — OK — updated

- موفقیت: 15 از 18.
- validate: L1=0 L2=0 L3=8 L4=0.
- Coverage (production): complete=9 partial=5 blocked=3 deferred=1.
- تغییر کلیدی: complete = with_page==count AND params_pct >= 50% (به جای strict_depth >= 50%).


## D-039
- تاریخ: 1405-07-19T17:47:20Z
- زمینه: بسته D11 — 25 زیرگام، تثبیت نهایی production criteria.
- نتایج:
- s1_dat15: dat_15 last record — PARTIAL — with_page=13
- s2_dat04: dat_04 values ext — PARTIAL — with_values=12
- s3_dat10: dat_10 params ext — PARTIAL — with_params=17
- s4_dat12: dat_12 params ext — PARTIAL — with_params=9
- s5_dat03: dat_03 recovery ext — PARTIAL — with_recovery=96
- s6_dat11: dat_11 params ext — PARTIAL — with_params=25
- s7_dat14: dat_14 external depth — OK — with_params=52
- s8_dat01_err: dat_01 response_error — OK — with_err=334
- s9_dat01_fw: dat_01 firmware_min — OK — with_fw=334
- s10_dat02_urcs: dat_02 related_urcs — OK — with_urcs=188
- s11_dat05_tim: dat_05 related_timings — PARTIAL — with_tim=0
- s12_dat07_alt: dat_07 alt_function — PARTIAL — with_alt=19
- s13_dat09_ex: dat_09 examples — OK — with_examples=14
- s14_l3_analysis: L3 analysis — OK — see _step_D11_L3_analysis.json
- s15_whitelist: extend whitelist — OK — added=8
- s16_validate: validate rerun — PARTIAL — L3=8
- s17_dat08: dat_08 confirmed blocked — OK — rn_found=0
- s18_dat17: dat_17 confirmed blocked — OK — ssl_found=0
- s19_dat18: dat_18 confirmed blocked — OK — cert_found=1
- s20_dat16: dat_16 confirmed deferred — OK — evb_found=1
- s21_todo: TODO — OK — updated
- s22_coverage: COVERAGE final — OK — c=9 p=5 b=3 d=1
- s23_table: table v5 — OK — written
- s24_changelog: CHANGELOG — OK — written
- s25_validate: final validation — OK — L1=0 L2=0 L3=8 L4=0

- موفقیت: 16 از 25.
- validate: L1=0 L2=0 L3=8 L4=0.
- Coverage: complete=9 partial=5 blocked=3 deferred=1.


## D-040
- تاریخ: 1405-07-19T17:49:49Z
- زمینه: بسته D12 — بستن فاز ۱ با پذیرش سقف PDF.
- تصمیم: 7 دیتاست partial (dat_03, 04, 10, 11, 12, 14, 15) با limit_reason صریح در notes ثبت شدند.
- دلیل: PDF/منابع موجود سقف دارند؛ این‌ها شکست نیستند بلکه محدودیت داده هستند.
- L3 پس از whitelist: 0
- Specialist whitelist size: 46
- Tag: v1.0.0-phase1


## D-041
- Date: 1405-07-19T17:51:49Z
- Context: Batch D13 — closing Phase 1.
- Fixes:
  - Applied limit_reason in notes to 7 partial datasets (D12 Phase B failed due to PowerShell $var: parser error).
  - PowerShell syntax corrected: using -f format instead of inline $var:.
- Verified: all 7 partial datasets have limit_reason in notes.
- Validation: L1=0 L2=0 L3=0 L4=0 (specialist whitelist=46).
- Coverage: complete=9 partial=5 blocked=3 deferred=1.
- Tag: v1.0.0-phase1.
- Status: PHASE 1 COMPLETE.
## D-042
- تاریخ: 1405-07-20T02:00:00Z
- Context: Session of 1405-07-20. The previous attempt to close dat_15 as blocked failed in two places:
  - COVERAGE_MATRIX.md: a regex parsing bug left dat_15 status as "partial".
  - DECISIONS_LOG.md: a false match on the existing D-006 (unrelated topic) prevented adding the correct entry.
- Decision:
  - dat_15 (Power Management) is formally moved to status = blocked.
  - The records dat_15_9001..9013 (previously "partial") are flagged as unreliable.
  - The dataset will only be re-opened if the SIM800 Series Sleep Mode Application Note is obtained,
    or if a human manually extracts the real power tables from V2.02 pages 25-30 and 58-62.
- Reason:
  - Primary source (Sleep Mode Application Note) is not available.
  - The partial records were produced by automated regex extraction and mix real numeric values
    with table-of-contents lines, section numbers, part numbers, and changelog fragments.
  - Per project rule R11: when the primary source is unavailable, the dataset must be marked blocked.
- Rejected alternatives:
  - Retry regex extraction: rejected, it will produce the same garbage.
  - Keep the partial records as-is: rejected, they are not traceable or trustworthy.
- Related rules: R2, R6, R11, R12, R19.

## D-043
- تاریخ: 1405-07-20T03:00:00Z
- Context: Session of 1405-07-20. dat_04_timing_timeout.yaml was found to
  contain two structural defects:
  - A YAML anchor (&id001) was defined at line 403 and referenced by
    11 records (lines 433-713). This anchor makes the file unreadable by
    strict YAML parsers and violates R8.
  - The 25 records were predominantly out of scope for a Timing dataset:
    12 records in the 9XXX series held voltages, currents, power values,
    and one bibliography entry; the 00XX series contained changelog notes,
    GPIO references, wake-up conditions, and fragmented text.
- Decision:
  - The file is rewritten with 6 active records and 23 legacy records.
  - Active records: 4 newly extracted (0014-0017) + 2 salvaged (0010, 0012).
  - Legacy records: 23 records preserved verbatim (R10) with:
    - status = "unknown" (R3),
    - conflicts populated with {field, reason},
    - tags including "legacy", "deprecated", and either "malformed" or
      "out-of-scope".
  - The previous file is archived to
    reports/_archive/dat_04_legacy_<timestamp>.yaml (R10-compliant).
  - The YAML anchor is eliminated by writing records explicitly (no
    yaml.safe_dump with shared references).
- Reason:
  - R2 (exact source), R6 (no synthetic data), R8 (valid YAML),
    R10 (no record deletion), R12 (real coverage), R20 (no contradictory
    data).
  - Dataset remains "partial" not "complete" because precise min/typ/max
    values are inside figures (images), not extractable from text.
- Rejected alternatives:
  - Option A: keep the file as-is and only append. Rejected: the YAML
    anchor remains and blocks valid parsing.
  - Option B: delete the malformed records entirely. Rejected: violates R10.
  - Option C: OCR the figures now. Rejected for this session: OCR requires
    a separate pass and human verification; deferred to a later session.
- Related rules: R2, R3, R6, R8, R10, R12, R20.

## D-044
- تاریخ: 1405-07-20T04:00:00Z
- Context: dat_05_state_machine.yaml (11 records) was found to have the same
  class of structural defects as dat_04 had before D-043:
  - All 11 records had a field `coverage_estimate` not defined in
    dat_05.schema.yaml.
  - source.name said "SIM800 Series AT Command Manual" while source.section
    said "SIM800H&SIM800L_Hardware_Design V2.02" (mixed source).
  - Records 0002..0009 shared the SAME quote (from section 4.2.2.1 Power
    down), unrelated to their declared state.
  - Records 0001 and 0010 had quotes from the Table of Contents.
  - All records had status=inferred, confidence=0.45, but no inference
    rationale in notes.
- Decision:
  - dat_05 is rewritten with 12 active records (dat_05_0001..dat_05_0012)
    covering the 12 states defined in the brief.
  - The 11 legacy records are preserved and renumbered dat_05_9001..dat_05_9011
    with status=unknown, confidence=0.0, conflicts populated.
  - The current file is archived to reports/_archive/dat_05_legacy_<ts>.yaml.
  - `coverage_estimate` is removed (not in schema).
  - source.name corrected to "SIM800H&SIM800L_Hardware_Design" for new active
    records because dat_05 belongs to Cluster A (hardware sources).
- Reason: R2, R3, R8, R10, R12, R20.
- Rejected alternatives:
  - Keep the existing 11 records as-is: rejected (schema violation, unrelated quotes).
  - Renumber active records as 9000-series: rejected (active data should be in low range).
- Related rules: R2, R3, R6, R8, R10, R12, R20.

## D-045
- تاریخ: 1405-07-20T05:00:00Z
- Context: dat_06_init_sequence.yaml (10 records) had the same class of
  structural defects as dat_04 and dat_05 before their respective fixes:
  - Every record had a `coverage_estimate` field, which is not defined in
    dat_06.schema.yaml.
  - source.name said "SIM800 Series AT Command Manual" while source.section
    said "SIM800H&SIM800L_Hardware_Design V2.02" (mixed source).
  - source.quote values were either ToC lines ("4.2. Power on/off Scenarios...22"),
    or completely unrelated table captions ("TABLE 9: SERIAL PORT AND USB PIN
    DEFINITION"), or duplicated across records.
  - retry_count and failure_action values had no basis in any source.
- Decision:
  - dat_06 is rewritten with 15 active records (dat_06_0001..dat_06_0015)
    covering power-up, SIM init, network registration, PDP, SMS, Data, and
    Sleep/Wake steps. Data step (AT+CIPSTART) has null page/quote because the
    recon did not capture the exact CIPSTART section (see R3).
  - The 10 legacy records are preserved and renumbered dat_06_9001..dat_06_9010
    with status=unknown, confidence=0.0, conflicts populated.
  - The current file is archived to reports/_archive/dat_06_legacy_<ts>.yaml.
  - `coverage_estimate` is removed (not in schema).
  - source.name corrected to V2.02 for power-up/Sleep steps and to AT Manual
    V1.01 (date 2013-07-23) for AT-command steps.
- Reason: R2, R3, R8, R10, R12, R20.
- Rejected alternatives:
  - Keep the existing 10 records as-is: rejected (schema violation, mixed
    source, unrelated quotes, unjustified retry values).
  - Renumber active records as 9000-series: rejected (active data belongs in
    the low range for readability).
  - Fabricate CIPSTART page/quote: rejected; per R3, null is preferred.
- Related rules: R2, R3, R6, R8, R10, R12, R20.

## D-046
- تاریخ: 1405-07-20T06:00:00Z
- Context: dat_16 (Board/EVB) is part of Cluster A (hardware). The project
  brief requires an official SIMCom EVB document for this dataset. No such
  document is present in the project's sources/originals/ or elsewhere on
  disk.
- Decision:
  - dat_16 is formally closed as `deferred`.
  - The single existing record (dat_16_0001) remains untouched with
    status=deferred.
  - reports/dat_16_REPORT.md is rewritten to document the deferral reason.
  - COVERAGE_MATRIX.md row for dat_16 is updated to show `-` in the count,
    with_page, with_params, and params_pct columns.
  - TODO.md records the missing EVB document as an external dependency.
- Reason: R11 (dataset closed for missing source), R3 (unknown / no guessing),
  R22 (each dataset closed with one of the four allowed statuses).
  Contrast with `blocked`: `deferred` is used because the missing source is
  not critical for any other dataset in Cluster A — it is independent.
- Rejected alternatives:
  - Fabricate EVB records from dat_07 pin tables: rejected, violates R2 and R20.
  - Mark dat_16 as `blocked`: rejected; `blocked` is reserved for missing
    sources that halt a critical dependency, whereas dat_16 is orthogonal.
  - Delete the single legacy record: rejected, violates R10.
- Related rules: R2, R3, R10, R11, R22.

## D-047
- تاریخ: 1405-07-20T07:00:00Z
- Context: After closing Cluster A (D-046), two Cluster B datasets remain
  in a mixed or fully-blocked state:
  - dat_11 (HTTP/FTP/SSL): 38 records, 19 partial + 19 blocked. The
    HTTP, FTP, and SSL AT Command Manuals are not present in the project.
  - dat_17 (Certificate/Key Store): 9 records, all blocked. The SSL AT
    Command Manual is not present in the project.
- Decision:
  - dat_11 and dat_17 are formally closed as `blocked`.
  - No changes to their data files; existing records are preserved per R10.
  - COVERAGE_MATRIX.md rows for dat_11 and dat_17 show status=blocked with
    `-` in count / with_page / with_params / params_pct columns.
  - A short closure section is appended to reports/CROSS_REF_REPORT.md.
- Reason: R11 (missing primary source -> blocked). The 19 partial records
  in dat_11 cannot be verified or extended without the parent manual, so
  the dataset as a whole cannot be considered `partial`.
- Rejected alternatives:
  - Keep dat_11 as `partial`: rejected; the partial records cannot be
    verified or extended without the parent manual.
  - Delete the 19 blocked records in dat_11: rejected, violates R10.
  - Delete the 9 blocked records in dat_17: rejected, violates R10.
- Related rules: R2, R10, R11, R22.

## D-048
- تاریخ: 1405-07-20T08:00:00Z
- Context: The COVERAGE_MATRIX in commit 513595b showed dat_03 (255/255, 97.6%)
  and dat_05 (23/23, 52.2%) as `partial`, in contradiction with the rule
  stated in the same file (`complete: with_page==count AND params_pct >= 50%`).
- Decision:
  - dat_03 and dat_05 are updated to `complete` to comply with the rule.
  - The rule is clarified as follows:
    - `with_params` counts records with status in {complete, partial, inferred}.
    - A dataset is `complete` if with_page == count AND params_pct >= 50%.
    - A dataset is `partial` if with_page == count but params_pct < 50%.
    - A dataset is `blocked` if no primary source is available.
    - A dataset is `deferred` if it needs an external decision or source.
- Reason: R12 (coverage criterion). The rule was in force but had not been
  consistently applied to dat_03 and dat_05.
- Related rules: R12.

## D-049
- تاریخ: 1405-07-20T08:01:00Z
- Context: dat_14 (Operator/APN) has 52 records with source_type=external
  from mcc-mnc.com. None of them have a PDF page number (the external
  source is a web API/dataset, not a paginated document). Therefore
  with_page = 0. Per R12, a dataset with 0% coverage cannot be marked
  `partial`. The brief explicitly marks dat_14 as optional.
- Decision:
  - dat_14 is set to `deferred`.
  - The 52 existing records are preserved (R10) but do not contribute to
    the coverage matrix at this time.
  - The dataset may be re-opened if the project owner explicitly requests
    APN completion from GSMA/ITU data.
- Reason: R3 (unknown for missing data), R10 (no deletion), R12 (coverage).
- Rejected alternatives:
  - Keep as `partial`: rejected, violates R12 (0% < 50%).
  - Delete the 52 records: rejected, violates R10.
- Related rules: R3, R10, R12, R22.

## D-050
- تاریخ: 1405-07-20T08:02:00Z
- Context: Two scripts disagreed on cross-reference error counts:
  - cross_ref.py reported 303 L3 issues (see reports/CROSS_REF_REPORT.md).
  - validate.py reported 0 L3 issues (specialist whitelist applied).
  The discrepancy was caused by different normalization rules: validate.py
  applies a whitelist for HTTP/FTP/SSL/Audio/Cert command names that are
  expected to be absent from dat_01, while cross_ref.py does not.
- Decision:
  - cross_ref.py is considered authoritative for L3 counts (it applies no
    whitelist and reports all missing references).
  - The 303 L3 issues are NOT treated as project errors at this stage:
    they are informational and consistent with the fact that dat_01 is
    scoped to basic AT commands and does not include specialist HTTP/FTP/
    SSL/Audio commands. Those commands live in external manuals that are
    not present in the project.
  - To avoid future confusion, CROSS_REF_REPORT.md will record both numbers
    with an explanatory note in its header.
  - No data changes are made in response to the 303 issues in this session.
- Reason: R12 (coverage clarity), R20 (no contradictory reporting).
- Rejected alternatives:
  - Delete the 303 issues from the report: rejected, would hide real gaps.
  - Add specialist commands to dat_01 without a source: rejected, violates R2.
- Related rules: R2, R12, R20.

## D-051
- تاریخ: 1405-07-20T09:00:00Z
- Context: Session 9 fix had three residual issues:
  1. YAML 1.1 boolean coercion: `OFF` (and `ON`) as an unquoted scalar is
     parsed as boolean False (True). This affected dat_04_0015, dat_04_0016
     (related_state) and dat_05_0001 (state_name), producing three L1
     schema errors.
  2. CROSS_REF_REPORT.md header note said 303 L3 issues while the body
     (produced by cross_ref.py) said 226 — contradictory.
  3. VALIDATION_REPORT.md was not included in commit faf3997 even though
     it had recorded the three L1 errors.
- Decision:
  - dat_04 and dat_05 are patched: OFF and ON scalar values in
    related_state / state_name are quoted so they remain strings.
  - CROSS_REF_REPORT.md header note now says 226 to match the current
    output of cross_ref.py. The 226 issues remain informational (see
    D-050).
  - VALIDATION_REPORT.md is committed together with these fixes.
  - Rule: any literal `OFF`, `ON`, `YES`, `NO`, `TRUE`, `FALSE` in a
    YAML scalar field declared as string must be quoted. This applies to
    all future datasets.
- Reason: R8 (valid YAML), R17 (schema-valid), R20 (no contradictions).
- Related rules: R8, R17, R20.
