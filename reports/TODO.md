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
- [ ] dat_04 — ساختار PDF یافت نشد (structure_found=True)
- [ ] dat_05 — ساختار PDF یافت نشد (structure_found=False)
- [ ] dat_06 — ساختار PDF یافت نشد (structure_found=False)
- [ ] dat_08 — Release Notes
- [ ] dat_15 — پارامترهای ساختاریافته Power قابل استخراج خودکار نیست
- [ ] dat_17 — SSL Manual
- [ ] dat_18 — اسناد رسمی CE/FCC/...

## دیتاست‌های deferred
- [ ] dat_16 — EVB document

## دیتاست‌های partial
- [ ] dat_01, dat_02, dat_03
- [ ] dat_07 — 75/78 annotated
- [ ] dat_09, dat_10, dat_11, dat_12, dat_13
- [ ] dat_14 — 52 external records

## گام A3 — نتیجه اسکن ساختاریافته
- dat_04 timing structure found: True
- dat_05 state structure found: False
- dat_06 init structure found: False
- اسکن کامل در reports/_step_A3_structured_scan.json
- **هیچ رکورد جدیدی اضافه نشد** — طبق D-019 auto-detection ممنوع است.

## خطاهای L3 پذیرفته‌شده
- ۳۰۳ خطای cross-ref — رفع در خوشه B پس از کامل شدن dat_01.

## خوشه‌های در انتظار
- [ ] خوشه A4: dat_16 Board/EVB (احتمالاً deferred)
- [ ] خوشه B: pending_blocked (وابسته به dat_01)
- [ ] بازگشت به dat_04/dat_05/dat_06 و dat_15 برای استخراج دستی (نشست جداگانه)