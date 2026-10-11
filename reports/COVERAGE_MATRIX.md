# COVERAGE_MATRIX

| دیتاست | نام | status | coverage_estimate | منبع | دلیل |
|---|---|---|---|---|---|
| dat_01 | AT Command | partial | medium | AT Manual V1.01 | Annotated + deduplicated; unknown records reduced |
| dat_02 | URC | partial | medium | AT Manual V1.01 | URC section extracted; suspicious records marked |
| dat_03 | Error Code | partial | medium | AT Manual V1.01 | CME/CMS appendix extracted |
| dat_04 | Timing & Timeout | partial | low | V2.02/V1.00 | Structured timing section limited |
| dat_05 | State Machine | partial | medium | V2.02/V1.00 | 100% annotated |
| dat_06 | Init Sequence | partial | low | V2.02/V1.00 | Structured init section limited |
| dat_07 | Hardware Reference | partial | medium | V2.02, V1.00 | 75/78 annotated |
| dat_08 | Firmware Compatibility | blocked | - | - | Release Notes not available |
| dat_09 | SMS | partial | medium | AT Manual V1.01 | Annotated from SMS section |
| dat_10 | GPRS/Data | partial | medium | AT Manual V1.01 | 21 records annotated from GPRS section |
| dat_11 | HTTP/FTP/SSL | partial | medium | AT Manual V1.01 | 10 records annotated from HTTP/FTP/SSL sections |
| dat_12 | Audio | partial | medium | AT Manual V1.01 | 7 records annotated from Audio section |
| dat_13 | SIM Management | partial | medium | AT Manual V1.01 | Annotated from SIM section |
| dat_14 | Operator/APN | partial | low | mcc-mnc.com / external | 52 external records |
| dat_15 | Power Management | blocked | - | - | Structured power parameters not extractable |
| dat_16 | Board/EVB | deferred | - | - | EVB document not available |
| dat_17 | Certificate/Key Store | blocked | - | - | SSL Manual not available |
| dat_18 | Certification | blocked | - | - | Certification documents not available |

## قواعد
- مقادیر مجاز status دیتاست: complete | partial | blocked | deferred
- unknown فقط برای رکورد مجاز است.
- دیتاست blocked نباید هیچ رکوردی داشته باشد.