# TODO

## منابع گمشده (بلاک‌کننده)
- [ ] SIM800 Series AT Command Manual — dat_01, 02, 03, 09, 10, 11, 12, 13, 17
- [ ] SIM800 Series TCP/IP AT Command Manual — dat_10
- [ ] SIM800 Series HTTP AT Command Manual — dat_11
- [ ] SIM800 Series FTP AT Command Manual — dat_11
- [ ] SIM800 Series SSL AT Command Manual — dat_11, dat_17
- [ ] SIM800 Series Audio AT Command Manual — dat_12
- [ ] SIM800 Series SIM AT Command Manual — dat_13
- [ ] SIM800L Datasheet — مکمل سخت‌افزاری
- [ ] SIM800 Series Sleep Mode App Note — dat_15
- [ ] SIM800 Series URC App Note — dat_02
- [ ] SIM800 Series Firmware Release Notes — dat_08
- [ ] اسناد CE / FCC / GCF / PTCRB / RoHS / IC / TA / RCM / Anatel / NCC — dat_18
- [ ] منابع GSMA / ITU / mcc-mnc.com — dat_14

## کارهای بحرانی (پس از مهاجرت)
- [ ] **جایگزینی مقادیر UNMIGRATED** با منبع واقعی در رکوردهای مهاجرت‌شده (reports/MIGRATION_REPORT.md).
- [ ] **خواندن محتوای `sources/extracted/v1.00.txt` و `v2.02.txt`** و تولید رکوردهای واقعی برای dat_04, dat_05, dat_06, dat_07, dat_15.
- [ ] **اندازه‌گیری پوشش واقعی** برای dat_04/05/06 تا از `partial` به `complete` ارتقا یابند (R12).
- [ ] **به‌روزرسانی `_dataset_meta.yaml`ها** با وضعیت واقعی.

## دیتاست‌های بلاک‌شده
- [ ] dat_01, 02, 03, 08, 09, 10, 11, 12, 13, 17, 18 (دلایل در COVERAGE_MATRIX.md)

## دیتاست‌های deferred
- [ ] dat_14 — اختیاری؛ نیازمند منبع خارجی
- [ ] dat_16 — نیازمند سند رسمی EVB

## اجراهای بعدی
- [ ] `python scripts/migrate_records.py`
- [ ] `python scripts/validate.py`
- [ ] `python scripts/cross_ref.py`
- [ ] `python scripts/check_meta_consistency.py`
- [ ] به‌روزرسانی README.md و PHASE_1_REPORT.md پس از تکمیل منابع