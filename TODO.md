# TODO — منابع گمشده برای نسخه‌های آینده

## منابع بحرانی گمشده

- [ ] **SIM800 Series SSL Application Note** (نسخه V1.xx)
  - **دلیل**: دستورات SSL (`+SSLSETCERT`, `+SSLCFG`, `+SSLOPEN`, ...) در SIM800 هرگز در AT Command Manual عمومی نبوده‌اند و همیشه در یک Application Note جداگانه ارائه شده‌اند.
  - **موردنیاز برای**: dat_17 (Certificate/Key Store)
  - **مسیر پیشنهادی**: درخواست مستقیم از SIMCom یا جستجو در مخازن عمومی.

- [ ] **SIM800 Series Firmware Release Notes** (نسخه‌های مختلف)
  - **موردنیاز برای**: dat_08 (Firmware Compatibility)
  - **دلیل**: اطلاعات سازگاری نسخه‌های مختلف firmware فقط در Release Notes رسمی موجود است.

- [ ] **SIM800 Series Certification Documents** (CE, FCC, GCF, PTCRB, RoHS, IC, TA, RCM, Anatel, NCC)
  - **موردنیاز برای**: dat_18 (Certification Data)
  - **دلیل**: این اسناد فقط توسط SIMCom یا نهادهای صدور گواهی ارائه می‌شوند.

- [ ] **SIM800L EVB Schematic** (نسخه رسمی)
  - **موردنیاز برای**: dat_16 (Board/EVB Definitions)
  - **دلیل**: اطلاعات دقیق pinout و jumperهای EVB فقط در schematic رسمی موجود است.

- [ ] **SIM800 Series AT Command Manual V1.09 یا بالاتر**
  - **موردنیاز برای**: تکمیل بهتر dat_01, 02, 03, 09, 10, 11, 12, 13
  - **وضعیت فعلی**: از V1.01 استفاده شده. نسخه‌های جدیدتر شامل دستورات MMS, Email, POP3/SMTP و ... هستند.

## دیتاست‌های blocked

- **dat_08** (Firmware Compatibility) — نیازمند Release Notes
- **dat_17** (Certificate/Key Store) — نیازمند SSL Application Note
- **dat_18** (Certification) — نیازمند اسناد رسمی

## دیتاست‌های deferred

- **dat_16** (Board/EVB) — نیازمند EVB Schematic

## یادداشت‌های نسخه v1.0.0

- **تاریخ release**: 1405-07-18
- **دیتاست‌های complete**: dat_07 (Hardware), dat_15 (Power)
- **دیتاست‌های partial**: dat_01, 02, 03, 04, 05, 06, 09, 10, 11, 12, 13
- **دیتاست‌های external**: dat_14
- **دیتاست‌های blocked**: dat_08, 17, 18
- **دیتاست‌های deferred**: dat_16

## منابع گمشده برای v2.0

1. SSL Application Note
2. Firmware Release Notes
3. Certification Documents
4. EVB Schematic
5. AT Command Manual V1.09+