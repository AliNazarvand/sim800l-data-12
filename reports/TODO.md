# TODO

## dat_07 — کارهای باقی‌مانده (partial → complete)
- [ ] بازبینی هم‌ارزهای علامت‌گذاری‌شده در `reports/dat_07_FIX.md` (C1..C8 ↔ SIM_*) و تصمیم برای ادغام یا حفظ هر دو.
- [ ] بازبینی رکوردهای Keypad (COL/ROW/KBC/KBR) — احتمالاً مخصوص SIM800H هستند و باید در dat_07 بمانند یا حذف شوند (تصمیم مالک پروژه).
- [ ] تکمیل `voltage_min`/`voltage_typ`/`voltage_max`، `current_typ`/`current_max` از متن manual.
- [ ] تنظیم `direction` (input/output/power/ground) برای هر pin.
- [ ] تطبیق کامل با فهرست pin در V2.02 برای اطمینان از پوشش ≥ ۹۵٪.

## ۱۸ رکورد weak_at_signal در dat_01 (منتظر بازبینی دستی)
- فهرست در `reports/dat_01_APPLY_REFINE.md`.

## منابع گمشده (خارج از پروژه)
- [ ] SIM800 Series TCP/IP AT Command Manual — dat_10
- [ ] SIM800 Series HTTP AT Command Manual — dat_11
- [ ] SIM800 Series FTP AT Command Manual — dat_11
- [ ] SIM800 Series SSL AT Command Manual — dat_11, dat_17
- [ ] SIM800 Series Audio AT Command Manual — dat_12
- [ ] SIM800 Series SIM AT Command Manual — dat_13
- [ ] SIM800 Series Firmware Release Notes — dat_08
- [ ] اسناد رسمی CE/FCC/GCF — dat_18

## گام بعدی
- [ ] خوشه A، عضو A2: `dat_15` Power Management (از V2.02 و V1.00).
- [ ] سپس A3: `dat_04` + `dat_05` + `dat_06`.
- [ ] سپس A4: `dat_16` Board/EVB.