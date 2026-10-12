# COVERAGE_MATRIX

| دیتاست | نام | status | count | with_page | with_params | params_pct |
|---|---|---|---|---|---|---|
| dat_01 | AT Command | complete | 334 | 334 | 334 | 100% |
| dat_02 | URC | complete | 206 | 206 | 205 | 99.5% |
| dat_03 | Error Code | complete | 255 | 255 | 249 | 97.6% |
| dat_04 | Timing & Timeout | partial | 29 | 29 | 6 | 20.7% |
| dat_05 | State Machine | complete | 23 | 23 | 12 | 52.2% |
| dat_06 | Init Sequence | partial | 25 | 24 | 15 | 60% |
| dat_07 | Hardware Reference | complete | 56 | 56 | 56 | 100% |
| dat_08 | Firmware Compatibility | blocked | - | - | - | - |
| dat_09 | SMS | complete | 14 | 14 | 14 | 100% |
| dat_10 | GPRS/Data | complete | 24 | 24 | 21 | 87.5% |
| dat_11 | HTTP/FTP/SSL | blocked | - | - | - | - |
| dat_12 | Audio | complete | 13 | 13 | 9 | 69.2% |
| dat_13 | SIM Management | complete | 10 | 10 | 10 | 100% |
| dat_14 | Operator/APN | deferred | 52 | - | - | - |
| dat_15 | Power Management | blocked | - | - | - | - |
| dat_16 | Board/EVB | deferred | - | - | - | - |
| dat_17 | Certificate/Key Store | blocked | - | - | - | - |
| dat_18 | Certification | blocked | - | - | - | - |

## قواعد
- complete: with_page==count AND params_pct >= 50%
- partial: with_page==count but params_pct < 50%
- blocked/deferred: no source