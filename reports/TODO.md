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
- [ ] SIM800 Series Firmware Release Notes — dat_08
- [ ] SIM800 Series Certification Documents — dat_18
- [ ] GSMA / ITU / mcc-mnc.com — dat_14 (فقط ۵۲ رکورد نمونه)

## دیتاست‌های بلاک‌شده
- [ ] dat_08 — Release Notes
- [ ] dat_15 — پارامترهای ساختاریافته Power
- [ ] dat_17 — SSL Manual
- [ ] dat_18 — اسناد رسمی

## دیتاست‌های deferred
- [ ] dat_16 — EVB document

## دیتاست‌های partial
- [ ] dat_01, dat_02, dat_03 — از AT Manual V1.01
- [ ] dat_04, dat_05, dat_06 — annotate دستی از V2.02
- [ ] dat_07 — 75/78 annotated
- [ ] dat_09, dat_10, dat_11, dat_12, dat_13
- [ ] dat_14 — 52 external records

## گام B2+B3 — نتیجه
- URC entries parsed: 0
- Error entries parsed: 0
- گزارش: reports/_step_B2B3_parsed.json

## خطاهای L3 باقی‌مانده
- L3 = 35 (پس از B2+B3)
- این‌ها commandهای تخصصی (HTTP/FTP/SSL) هستند که در AT Manual V1.01 نیستند.
- رفع در خوشه B با منابع تخصصی (B6, B7).

## خوشه‌های در انتظار
- [ ] خوشه A4: dat_16 (deferred)
- [ ] خوشه B ادامه: B4 (SMS), B5 (SIM), B6 (GPRS/Data), B7 (HTTP/FTP/SSL), B8 (Cert), B9 (Audio)