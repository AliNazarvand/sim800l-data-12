# ROLE MAP

| Dataset | Role | Depends on | Status |
|---|---|---|---|
| dat_01 | command reference | - | see coverage |
| dat_02 | URC reference | dat_01 | see coverage |
| dat_03 | error codes | dat_01 | see coverage |
| dat_04 | timing | dat_05, dat_06 | see coverage |
| dat_05 | state machine | dat_04 | see coverage |
| dat_06 | init sequences | dat_01, dat_05 | see coverage |
| dat_07 | hardware pins | dat_16 | dat_13 |
| dat_08 | firmware matrix | - | see coverage |
| dat_09 | SMS | dat_01 | see coverage |
| dat_10 | GPRS | dat_01, dat_14 | see coverage |
| dat_11 | HTTP/FTP/SSL | dat_01, dat_17 | see coverage |
| dat_12 | Audio | dat_01 | see coverage |
| dat_13 | SIM mgmt | dat_01, dat_07 | see coverage |
| dat_14 | MCC/MNC | external | dat_10 |
| dat_15 | power mgmt | dat_05 | see coverage |
| dat_16 | board/EVB | - | dat_07 |
| dat_17 | cert/key store | dat_01 | dat_11 |
| dat_18 | certification | - | see coverage |
