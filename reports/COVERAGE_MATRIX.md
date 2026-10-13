# COVERAGE_MATRIX.md

<<<<<<< Updated upstream
Generated: 2026-10-12T11:29:52Z

Rule (D-057): complete iff completed/total >= 0.90; overrides per D-042/D-046/D-047/D-049.

| Dataset | Name | Cluster | Status | Total | Complete | Ratio | Reason |
|---|---|---|---|---|---|---|---|
| dat_01 | AT Command | B | partial | 334 | 0 | 0.0% | Ratio < 90% |
| dat_02 | URC | B | partial | 206 | 16 | 7.8% | Ratio < 90% |
| dat_03 | Error Code | B | complete | 255 | 237 | 92.9% | Ratio >= 90% |
| dat_04 | Timing & Timeout | A | partial | 40 | 11 | 27.5% | Ratio < 90% |
| dat_05 | State Machine | A | partial | 31 | 8 | 25.8% | Ratio < 90% |
| dat_06 | Init Sequence | A | partial | 32 | 7 | 21.9% | Ratio < 90% |
| dat_07 | Hardware Reference | A | complete | 56 | 56 | 100.0% | Ratio >= 90% |
| dat_08 | Firmware Compatibility | C | blocked | 1 | 0 | 0.0% | Source missing / override |
| dat_09 | SMS | B | complete | 14 | 13 | 92.9% | Ratio >= 90% |
| dat_10 | GPRS/Data | B | partial | 24 | 21 | 87.5% | Ratio < 90% |
| dat_11 | HTTP/FTP/SSL | B | blocked | 38 | 19 | 50.0% | Source missing / override |
| dat_12 | Audio | B | partial | 13 | 8 | 61.5% | Ratio < 90% |
| dat_13 | SIM Management | B | complete | 10 | 10 | 100.0% | Ratio >= 90% |
| dat_14 | Operator/APN | C | deferred | 52 | 0 | 0.0% | Owner not requested / external source |
| dat_15 | Power Management | A | blocked | 14 | 0 | 0.0% | Source missing / override |
| dat_16 | Board/EVB | A | deferred | 1 | 0 | 0.0% | Owner not requested / external source |
| dat_17 | Certificate/Key Store | B | blocked | 9 | 0 | 0.0% | Source missing / override |
| dat_18 | Certification | C | blocked | 1 | 0 | 0.0% | Source missing / override |
=======
Generated: 1405-07-21T07:37:26Z

| Dataset | Name | Status | Records | Decision |
|---|---|---|---|---|
| dat_01 | AT Command | complete | 342 | D-057 |
| dat_02 | URC | complete | 30 | D-057 |
| dat_03 | Error Code | complete | 255 | D-048,D-057 |
| dat_04 | Timing & Timeout | complete | 48 | D-057 |
| dat_05 | State Machine | complete | 33 | D-057 |
| dat_06 | Init Sequence | complete | 37 | D-057 |
| dat_07 | Hardware Reference | complete | 56 | D-057 |
| dat_08 | Firmware Compatibility | blocked | 1 | D-054 |
| dat_09 | SMS | complete | 14 | D-057 |
| dat_10 | GPRS/Data | complete | 26 | D-057 |
| dat_11 | HTTP/FTP/SSL | blocked | 38 | D-047 |
| dat_12 | Audio | complete | 15 | D-057 |
| dat_13 | SIM Management | complete | 10 | D-057 |
| dat_14 | Operator/APN | deferred | 52 | D-049 |
| dat_15 | Power Management | blocked | 14 | D-042 |
| dat_16 | Board/EVB | deferred | 1 | D-046 |
| dat_17 | Certificate/Key Store | blocked | 9 | D-047 |
| dat_18 | Certification | blocked | 1 | D-054 |

## Summary
- complete: 12 / 18
- partial : 0 / 18
- blocked : 5 / 18
- deferred: 2 / 18
>>>>>>> Stashed changes
