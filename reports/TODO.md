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
- [ ] dat_01 — بازسازی اولیه از AT Manual (annotate + add)
- [ ] dat_02, dat_03
- [ ] dat_04, dat_05, dat_06 — annotate دستی از جداول V2.02 صفحات 6, 15-25
- [ ] dat_07 — 75/78 annotated
- [ ] dat_09, dat_10, dat_11, dat_12, dat_13
- [ ] dat_14 — 52 external records

## گام B1 — نتیجه بازسازی dat_01
- AT Manual V1.01 به متن با page markers استخراج شد.
- اسکن ساختاریافته: تعداد commandهای شناسایی‌شده ثبت شد.
- annotate رکوردهای موجود بر اساس command + source.page/section/quote.
- commandهای جدید از سکشن‌های ساختاریافته اضافه شدند.
- اسکن کامل: reports/_step_B1_at_manual_scan.json
- بازسازی: reports/_step_B1_dat01_rebuild.json
- auto-detection آزادانه استفاده نشد؛ فقط سکشن‌های header-محور.

## کار بعدی
- [ ] خوشه B (B2..B9): پس از تثبیت dat_01 (اگر complete شد)
- [ ] بازبینی دستی source.quote برای رکوردهای dat_01 (اختیاری، برای افزایش confidence)

## خطاهای L3 پذیرفته‌شده
- اگر پس از B1، L3 به‌طور معنادار کاهش یافت → بخش عمده رفع شده.
- باقی‌مانده در خوشه B (B2..B9) رفع می‌شوند.

## خوشه‌های در انتظار
- [ ] خوشه A4: dat_16 Board/EVB (deferred)
- [ ] خوشه B: فعال پس از B1