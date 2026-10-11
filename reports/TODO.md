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
- [ ] dat_07 — 75/78 رکورد annotate شد؛ تعداد کل پین‌های PDF تأیید نشده
- [ ] dat_09, dat_10, dat_11, dat_12, dat_13
- [ ] dat_14 — 52 رکورد external (همه status=unknown؛ دیتاست partial چون منبع در دسترس است)
- [ ] dat_15

## محدودیت‌های استخراج dat_07 (A1)
- [ ] اسکریپت `_rebuild_dat07.py` صرفاً ۷۵ رکورد موجود را annotate کرده (جستجوی نام پین در متن PDF و ثبت source.page/quote).
- [ ] استخراج «واقعی» جدول پین‌ها (تشخیص تمام پین‌های PDF و افزودن رکوردهای جدید) انجام **نشده** است.
- [ ] بازبینی دستی جدول پین‌های V2.02 و V1.00 لازم است تا:
  - تمام پین‌های موجود در PDF در دیتاست حضور داشته باشند
  - پین‌های غایب به دیتاست اضافه شوند
- [ ] ۳ رکورد حل‌نشده در dat_07: نیازمند بازبینی دستی (بخش «بدون منبع»).

## رکوردهای بدون منبع در dat_07 (نیازمند بازبینی دستی)
- [ ] بازبینی دستی سه رکورد حل‌نشده طبق `_step2_dat07_rebuild.json`.

## خطاهای L3 پذیرفته‌شده
- ۳۰۳ خطای cross-ref — رفع در خوشه B پس از کامل شدن dat_01.

## خوشه‌های در انتظار
- [ ] خوشه A2: dat_15 Power Management
- [ ] خوشه B: pending_blocked (وابسته به dat_01)