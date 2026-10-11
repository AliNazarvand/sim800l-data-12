# COVERAGE_MATRIX

| دیتاست | نام | status | count | partial | unknown | blocked | with_page | دلیل |
|---|---|---|---|---|---|---|---|---|
| dat_01 | AT Command | complete | 334 | 334 | 0 | 0 | 334 | all records annotated |
| dat_02 | URC | partial | 206 | 189 | 1 | 0 | 206 | 189/206 partial |
| dat_03 | Error Code | partial | 255 | 11 | 7 | 0 | 186 | 11/255 partial |
| dat_04 | Timing & Timeout | blocked | 13 | 0 | 0 | 0 | 13 | no partial records |
| dat_05 | State Machine | blocked | 11 | 0 | 0 | 0 | 0 | no partial records |
| dat_06 | Init Sequence | blocked | 10 | 0 | 0 | 0 | 5 | no partial records |
| dat_07 | Hardware Reference | partial | 78 | 75 | 3 | 0 | 75 | 75/78 partial |
| dat_08 | Firmware Compatibility | blocked | 1 | 0 | 0 | 1 | 0 | external source not available |
| dat_09 | SMS | partial | 14 | 1 | 0 | 0 | 14 | 1/14 partial |
| dat_10 | GPRS/Data | blocked | 24 | 0 | 0 | 3 | 21 | no partial records |
| dat_11 | HTTP/FTP/SSL | blocked | 38 | 0 | 0 | 19 | 10 | no partial records |
| dat_12 | Audio | partial | 13 | 1 | 0 | 4 | 7 | 1/13 partial |
| dat_13 | SIM Management | blocked | 10 | 0 | 0 | 0 | 10 | no partial records |
| dat_14 | Operator/APN | partial | 52 | 0 | 52 | 0 | 0 | 52 external records |
| dat_15 | Power Management | blocked | 1 | 0 | 0 | 1 | 0 | structured power parameters not extractable |
| dat_16 | Board/EVB | deferred | 1 | 0 | 0 | 1 | 0 | EVB document not available |
| dat_17 | Certificate/Key Store | blocked | 9 | 0 | 0 | 9 | 0 | no partial records |
| dat_18 | Certification | blocked | 1 | 0 | 0 | 1 | 0 | external source not available |

## قواعد
- status دیتاست: complete | partial | blocked | deferred
- unknown فقط برای رکورد مجاز است.
- blocked با رکورد متناقض نیست (D-022).