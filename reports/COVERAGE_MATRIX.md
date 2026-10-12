# COVERAGE_MATRIX.md

Generated: 2026-10-12T05:46:40Z

Rule (D-057): complete iff completed/total >= 0.90; blocked/deferred overrides apply.

| Dataset | Name | Cluster | Status | Total | Complete | Ratio | Source | Reason |
|---|---|---|---|---|---|---|---|---|
| dat_01 | AT Command | B | partial | 334 | 0 | 0% | SIM800 Series AT Command Manual | Ratio < 90%; see dat_XX_REPORT.md |
| dat_02 | URC | B | partial | 206 | 16 | 7/8% | SIM800 Series AT Command Manual | Ratio < 90%; see dat_XX_REPORT.md |
| dat_03 | Error Code | B | complete | 255 | 237 | 92/9% | SIM800 Series AT Command Manual | Ratio >= 90% |
| dat_04 | Timing & Timeout | A | partial | 29 | 0 | 0% | SIM800H&SIM800L Hardware Design | Ratio < 90%; see dat_XX_REPORT.md |
| dat_05 | State Machine | A | partial | 23 | 0 | 0% | SIM800 Series AT Command Manual; SIM800H&SIM800L Hardware Design | Ratio < 90%; see dat_XX_REPORT.md |
| dat_06 | Init Sequence | A | partial | 25 | 0 | 0% | SIM800 Series AT Command Manual; SIM800H&SIM800L Hardware Design | Ratio < 90%; see dat_XX_REPORT.md |
| dat_07 | Hardware Reference | A | complete | 56 | 56 | 100% | SIM800H&SIM800L Hardware Design | Ratio >= 90% |
| dat_08 | Firmware Compatibility | C | blocked | 1 | 0 | 0% | SIM800 Firmware Release Notes | Primary source missing / override (D-042, D-047) |
| dat_09 | SMS | B | complete | 14 | 13 | 92/9% | SIM800 Series AT Command Manual | Ratio >= 90% |
| dat_10 | GPRS/Data | B | partial | 24 | 21 | 87/5% | SIM800 Series AT Command Manual | Ratio < 90%; see dat_XX_REPORT.md |
| dat_11 | HTTP/FTP/SSL | B | blocked | 38 | 19 | 50% | SIM800 Series AT Command Manual | Primary source missing / override (D-042, D-047) |
| dat_12 | Audio | B | partial | 13 | 8 | 61/5% | SIM800 Series AT Command Manual | Ratio < 90%; see dat_XX_REPORT.md |
| dat_13 | SIM Management | B | complete | 10 | 10 | 100% | SIM800 Series AT Command Manual | Ratio >= 90% |
| dat_14 | Operator/APN | C | deferred | 52 | 0 | 0% | - | Owner not requested / external source (D-046, D-049) |
| dat_15 | Power Management | A | blocked | 14 | 0 | 0% | SIM800 Sleep Mode Application Note; SIM800H&SIM800L Hardware Design | Primary source missing / override (D-042, D-047) |
| dat_16 | Board/EVB | A | deferred | 1 | 0 | 0% | SIM800L EVB Schematic | Owner not requested / external source (D-046, D-049) |
| dat_17 | Certificate/Key Store | B | blocked | 9 | 0 | 0% | SIM800 Series AT Command Manual | Primary source missing / override (D-042, D-047) |
| dat_18 | Certification | C | blocked | 1 | 0 | 0% | SIM800L Certification Documents | Primary source missing / override (D-042, D-047) |
