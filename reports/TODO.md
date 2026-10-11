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
- [ ] dat_15 — پارامترهای ساختاریافته Power قابل استخراج خودکار نیست
- [ ] dat_17 — SSL Manual
- [ ] dat_18 — اسناد رسمی CE/FCC/...

## دیتاست‌های deferred
- [ ] dat_16 — EVB document

## دیتاست‌های partial
- [ ] dat_01, dat_02, dat_03
- [ ] dat_04 — annotate pending; structured timing section موجود
- [ ] dat_05 — 11 رکورد inferred؛ نیازمند annotate از جدول Overview of Operating Modes (V2.02 p6)
- [ ] dat_06 — 10 رکورد inferred؛ نیازمند annotate دستی
- [ ] dat_07 — 75/78 annotated
- [ ] dat_09, dat_10, dat_11, dat_12, dat_13
- [ ] dat_14 — 52 external records

## بازبینی دستی موردنیاز — جداول V2.02
- [ ] بازبینی دستی جداول V2.02 صفحات 6، 15-25 برای استخراج ساختاریافته timing/state/init — نشست بعدی.
- [ ] جدول Overview of Operating Modes (V2.02 p6) — مربوط به dat_05
- [ ] جدول The Current Consumption of Minimum Functionality Mode — مربوط به dat_15
- [ ] جداول Timing/Reset — مربوط به dat_04

## گام A3 — نتیجه نهایی (اصلاح‌شده)
- dat_04 timing structure found: True → partial
- dat_05 state structure found: False در اسکن A3، اما جدول مربوطه در p6 موجود است → partial
- dat_06 init structure found: False → partial (بر اساس رکوردهای inferred موجود)
- هیچ رکورد جدیدی اضافه نشد (پایبندی به D-019).
- اسکن کامل در: reports/_step_A3_structured_scan.json

## خطاهای L3 پذیرفته‌شده
- ۳۰۳ خطای cross-ref — رفع در خوشه B پس از کامل شدن dat_01.

## خوشه‌های در انتظار
- [ ] خوشه A4: dat_16 Board/EVB (احتمالاً deferred)
- [ ] خوشه B: pending_blocked (وابسته به dat_01)
- [ ] بازگشت به dat_04/dat_05/dat_06 و dat_15 برای استخراج دستی (نشست جداگانه)