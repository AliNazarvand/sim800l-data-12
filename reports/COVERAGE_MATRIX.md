# COVERAGE_MATRIX

| دیتاست | نام | status | coverage_estimate | coverage_percent | منبع | دلیل |
|---|---|---|---|---|---|---|
| dat_01 | AT Command | partial | high | - | AT Manual V1.01 | Annotated 0 records; added 275 new commands from structured sections; manual commands found = 275 |
| dat_02 | URC | partial | low | 20% | AT Manual V1.01 | Auto-extracted; needs review |
| dat_03 | Error Code | partial | low | 20% | AT Manual V1.01 | Auto-extracted; needs review |
| dat_04 | Timing & Timeout | partial | low | 30% | V2.02/V1.00 | Structured timing section exists; annotate existing records only |
| dat_05 | State Machine | partial | low | 20% | V2.02/V1.00 | 11 inferred records present; structured table exists; annotate only |
| dat_06 | Init Sequence | partial | low | 20% | V2.02/V1.00 | 10 inferred records present; source available; annotate only |
| dat_07 | Hardware Reference | partial | medium | 96% | V2.02, V1.00 | 75/78 annotated; total pin count of PDF not verified |
| dat_08 | Firmware Compatibility | blocked | - | - | - | Release Notes not available |
| dat_09 | SMS | partial | low | 10% | AT Manual V1.01 | Auto-extracted; needs review |
| dat_10 | GPRS/Data | partial | low | 10% | AT Manual V1.01 | Auto-extracted; needs review |
| dat_11 | HTTP/FTP/SSL | partial | low | 10% | AT Manual V1.01 | Auto-extracted; needs review |
| dat_12 | Audio | partial | low | 5% | AT Manual V1.01 | Auto-extracted; needs review |
| dat_13 | SIM Management | partial | low | 10% | AT Manual V1.01 | Auto-extracted; needs review |
| dat_14 | Operator/APN | partial | low | 10% | mcc-mnc.com / external | 52 external records; source available but records incomplete |
| dat_15 | Power Management | blocked | - | - | - | Structured power parameters not extractable by auto-detection; requires manual extraction from PDF tables or Sleep Mode Application Note |
| dat_16 | Board/EVB | deferred | - | - | - | EVB document not available |
| dat_17 | Certificate/Key Store | blocked | - | - | - | SSL Manual not available |
| dat_18 | Certification | blocked | - | - | - | Certification documents not available |

## قواعد وضعیت دیتاست (طبق R22)
- مقادیر مجاز: complete | partial | blocked | deferred
- unknown فقط برای رکورد مجاز است، نه برای وضعیت دیتاست.

## قاعده D-022
- یک دیتاست blocked نباید هیچ رکوردی در فایل داده داشته باشد.
- اگر رکورد هست -> حداقل partial.
- اگر منبع در دسترس است -> حداکثر partial (نه blocked).
- blocked فقط وقتی است که منبع اصلی کل دیتاست در دسترس نباشد.