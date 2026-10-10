# sim800l-data

پروژه داده‌محور SIM800L.

**آخرین به‌روزرسانی**: 2026-10-10T15:24:11Z

## وضعیت ۱۸ دیتاست

| # | نام | تعداد رکورد |
|---|---|---|
| dat_01 | dat_01_at_command.yaml | 311 |
| dat_02 | dat_02_urc.yaml | 121 |
| dat_03 | dat_03_error_code.yaml | 238 |
| dat_04 | dat_04_timing_timeout.yaml | 16 |
| dat_05 | dat_05_state_machine.yaml | 11 |
| dat_06 | dat_06_init_sequence.yaml | 12 |
| dat_07 | dat_07_hardware_reference.yaml | 26 |
| dat_08 | dat_08_firmware_compatibility.yaml | 0 |
| dat_09 | dat_09_sms.yaml | 14 |
| dat_10 | dat_10_gprs_data.yaml | 21 |
| dat_11 | dat_11_http_ftp_ssl.yaml | 43 |
| dat_12 | dat_12_audio.yaml | 5 |
| dat_13 | dat_13_sim_management.yaml | 10 |
| dat_14 | dat_14_operator_apn.yaml | 52 |
| dat_15 | dat_15_power_management.yaml | 4 |
| dat_16 | dat_16_board_evb.yaml | 0 |
| dat_17 | dat_17_certificate_key_store.yaml | 0 |
| dat_18 | dat_18_certification.yaml | 0 |


## منابع
- SIM800L_Hardware_Design_V1.00.pdf
- SIM800H&SIM800L_Hardware_Design_V2.02.PDF
- SIM800 Series_AT Command Manual_V1.01.pdf

## ساختار
- `data/` — ۱۸ دیتاست YAML
- `schemas/` — ۱۸ JSON schema
- `scripts/` — اسکریپت‌های pipeline
- `sources/` — PDFهای اصلی و متن استخراج‌شده
- `reports/` — گزارش‌ها

## Pipeline
```
py scripts/extract_pdf_v3.py
py scripts/parse_sources_v2.py
py scripts/populate_v3.py
py scripts/cross_ref_v3.py
py scripts/validate_v3.py
py scripts/generate_reports_v3.py
```
