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
- [ ] dat_01 — بازسازی شده از AT Manual + dedup
- [ ] dat_02, dat_03
- [ ] dat_04, dat_05, dat_06 — annotate دستی از جداول V2.02
- [ ] dat_07 — 75/78 annotated
- [ ] dat_09, dat_10, dat_11, dat_12, dat_13
- [ ] dat_14 — 52 external records

## گام B1 — نتیجه نهایی (پس از رفع باگ)
- AT Manual V1.01 به متن با page markers استخراج شد.
- اسکن ساختاریافته: 275 command.
- باگ تطبیق AT+ prefix کشف شد و 275 رکورد تکراری ادغام شدند.
- قبل: 609، بعد: N، حذف‌شده: M (طبق _step_B1_duplicates.json)
- گزارش: reports/_step_B1_duplicates.json

## محدودیت‌های B1
- رکوردهای جدید AT Manual parameters/response_success/response_error/examples ندارند (خالی هستند).
- برای تکمیل این فیلدها، بازبینی دستی هر section AT Manual لازم است (نشست جداگانه).
- source.quote و source.section برای رکوردهای ادغام‌شده باید دستی بازبینی شوند.

## خطاهای L3 باقی‌مانده
- اگر L3 بالای 40 ماند، این‌ها احتمالاً مربوط به commandهای تخصصی (HTTP, FTP, SSL) هستند که در AT Manual V1.01 نیستند.
- رفع در خوشه B با منبع تخصصی.

## خوشه‌های در انتظار
- [ ] خوشه A4: dat_16 Board/EVB (deferred)
- [ ] خوشه B: B2 (URC), B3 (Error Code), B4 (SMS), B5 (SIM), B6 (GPRS/Data), B7 (HTTP/FTP/SSL), B8 (Cert), B9 (Audio)