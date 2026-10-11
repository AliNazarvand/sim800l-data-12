# TODO

## منابع گمشده
- [ ] SIM800 Series TCP/IP AT Command Manual — dat_10
- [ ] SIM800 Series HTTP AT Command Manual — dat_11
- [ ] SIM800 Series FTP AT Command Manual — dat_11
- [ ] SIM800 Series SSL AT Command Manual — dat_11, dat_17
- [ ] SIM800 Series Audio AT Command Manual — dat_12
- [ ] SIM800 Series SIM AT Command Manual — dat_13
- [ ] SIM800L Datasheet — dat_07
- [ ] SIM800 Series Sleep Mode Application Note — dat_15
- [ ] SIM800 Series URC Application Note — dat_02
- [ ] SIM800 Series Firmware Release Notes — dat_08
- [ ] SIM800 Series Certification Documents — dat_18
- [ ] GSMA / ITU / mcc-mnc.com — dat_14 (فقط ۵۲ رکورد نمونه)

## دیتاست‌های بلاک‌شده
- [ ] dat_08 — Release Notes
- [ ] dat_17 — SSL Manual
- [ ] dat_18 — اسناد رسمی CE/FCC/...

## دیتاست‌های deferred
- [ ] dat_16 — EVB document

## دیتاست‌های partial
- [ ] dat_01, dat_02, dat_03, dat_04, dat_05, dat_06
- [ ] dat_07 — 75/78 رکورد annotate شده؛ نیازمند بازبینی جدول پین‌های PDF
- [ ] dat_09, dat_10, dat_11, dat_12, dat_13
- [ ] dat_14 — 52 رکورد external (همه status=unknown در فایل؛ دیتاست partial)
- [ ] dat_15 — annotate + افزودن خودکار خطوط power از V2.02؛ نیازمند بازبینی دستی مقادیر

## محدودیت‌های استخراج dat_07 و dat_15
### dat_07
- [ ] اسکریپت _rebuild_dat07.py صرفاً ۷۵ رکورد موجود را annotate کرده.
- [ ] استخراج واقعی جدول پین‌ها (تشخیص پین‌های غایب PDF) انجام نشده.
- [ ] بازبینی دستی جدول پین‌های V2.02 و V1.00 لازم است.
- [ ] ۳ رکورد حل‌نشده در dat_07 نیازمند بازبینی دستی.

### dat_15
- [ ] اسکریپت _rebuild_dat15.py رکوردهای موجود را annotate کرده و خطوط power جدید از V2.02 را به‌عنوان رکوردهای partial افزوده.
- [ ] مقادیر عددی (value_min/typ/max، unit) برای رکوردهای افزوده‌شده باید دستی از PDF استخراج شود.
- [ ] بازبینی دستی کامل توصیه می‌شود.

## خطاهای L3 پذیرفته‌شده
- ۳۰۳ خطای cross-ref — رفع در خوشه B پس از کامل شدن dat_01.

## خوشه‌های در انتظار
- [ ] خوشه A3: dat_04 + dat_05 + dat_06
- [ ] خوشه A4: dat_16 Board/EVB (احتمالاً deferred)
- [ ] خوشه B: pending_blocked (وابسته به dat_01)