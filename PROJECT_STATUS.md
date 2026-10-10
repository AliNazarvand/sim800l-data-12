# PROJECT STATUS - SIM800L Knowledge Base

**ماژول هدف:** SIM800L (فقط)
**فرمت داده:** YAML کانونیک (JSON legacy حذف شده)
**Schema:** JSON Schema draft-07 در قالب YAML
**تعداد فایل:** < 500

## خلاصه وضعیت

| # | دیتاست | status | منبع |
|---|--------|--------|------|
| dat_01 | AT Command DB | complete | SIM800 AT Manual V1.01 |
| dat_02 | URC DB | complete | SIM800 AT Manual V1.01 |
| dat_03 | Error Code DB | complete | SIM800 AT Manual V1.01 |
| dat_04 | Timing & Timeout | complete | V2.02 + V1.00 |
| dat_05 | State Machine | complete | V2.02 + V1.00 |
| dat_06 | Init Sequence | complete | V2.02 + V1.00 |
| dat_07 | Hardware Reference | complete | V2.02 + V1.00 |
| dat_08 | Firmware Compatibility | inferred (پذیرش مستند) | Public history |
| dat_09 | SMS DB | complete | SIM800 AT Manual V1.01 |
| dat_10 | GPRS/Data | complete | TCP/IP Manual |
| dat_11 | HTTP/FTP/SSL | complete | HTTP/FTP/SSL Manuals |
| dat_12 | Audio | complete | Audio Manual |
| dat_13 | SIM Management | complete | SIM800 AT Manual V1.01 |
| dat_14 | Operator/APN | external | mcc-mnc.com |
| dat_15 | Power Management | complete | V2.02 + V1.00 |
| dat_16 | Board/EVB | inferred (پذیرش مستند) | Public photos |
| dat_17 | Certificate/Key Store | inferred (پذیرش مستند) | Public SSL family |
| dat_18 | Certification | inferred (پذیرش مستند) | Public claims |

## قواعد حاکم

- R1: فقط SIM800L
- R2: هیچ رکورد بدون source
- R4: inferred با confidence ≤ 0.5
- R6: هیچ synthetic
- R7: V2.02 > V1.00
- R21: هیچ example-only در data/

## تصمیمات کلیدی (D6-D12)

- D6: حذف figures/tables/ocr از git
- D7: فیلتر ابعاد/حجم/hash در extract_figures
- D8: فیلتر ردیف/ستون در extract_tables
- D9: پذیرش نهایی inferred برای dat_08/16/17/18
- D10: یکپارچه‌سازی به YAML
- D11: حذف tools/
- D12: حذف raw/
