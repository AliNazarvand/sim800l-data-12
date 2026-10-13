# COVERAGE MATRIX — sim800l-data

Generated: 2026-10-13T18:13:14Z

| Dataset | Name | Status | Real | Coverage | Reason |
|---------|------|--------|------|----------|--------|
| dat_01 | AT Command | complete | 335 | 100% | coverage=100% |
| dat_02 | URC | blocked | 0 | — | parser cannot extract from AT Manual |
| dat_03 | Error Code | blocked | 0 | — | parser cannot extract from AT Manual |
| dat_04 | Timing & Timeout | complete | 70 | — | - |
| dat_05 | State Machine | partial | 14 | — | below nominal threshold 20 |
| dat_06 | Init Sequence | complete | 20 | — | - |
| dat_07 | Hardware Reference | complete | 78 | — | - |
| dat_08 | Firmware Compatibility | blocked | 1 | — | Release Notes missing |
| dat_09 | SMS | complete | 14 | — | - |
| dat_10 | GPRS/Data | complete | 21 | — | - |
| dat_11 | HTTP/FTP/SSL | partial | 10 | — | HTTP/FTP/SSL manuals missing |
| dat_12 | Audio | partial | 7 | — | Audio manual missing |
| dat_13 | SIM Management | complete | 10 | — | - |
| dat_14 | Operator/APN | complete | 52 | — | - |
| dat_15 | Power Management | partial | 351 | — | pipeline over-extraction: 351 records, expected ~13-28 |
| dat_16 | Board/EVB | deferred | 1 | — | EVB schematic not available (per prompt spec) |
| dat_17 | Certificate/Key Store | blocked | 9 | — | SSL AT Command Manual missing |
| dat_18 | Certification | blocked | 1 | — | Certification documents missing |

**Totals:** complete=8, partial=4, blocked=5, deferred=1, total=18
