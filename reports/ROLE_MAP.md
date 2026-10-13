# ROLE MAP -- sim800l-data

Generated: 2026-10-13T17:47:17Z

| Dataset | Role | Depends on | Status |
|---------|------|------------|--------|
| dat_01 | AT command reference | - | complete |
| dat_02 | URC reference | dat_01 | complete |
| dat_03 | Error code reference | dat_01 | partial |
| dat_04 | Timing reference | - | complete |
| dat_05 | State machine | dat_04 | partial |
| dat_06 | Init sequence | dat_05 | complete |
| dat_07 | Hardware reference | - | complete |
| dat_08 | Firmware compatibility | - | blocked |
| dat_09 | SMS reference | dat_01 | complete |
| dat_10 | GPRS/Data reference | dat_01 | complete |
| dat_11 | HTTP/FTP/SSL reference | dat_01 | partial |
| dat_12 | Audio reference | dat_01 | partial |
| dat_13 | SIM management | dat_01, dat_07 | complete |
| dat_14 | Operator/APN | - | complete |
| dat_15 | Power management | dat_07 | complete |
| dat_16 | Board/EVB | dat_07 | blocked |
| dat_17 | Cert/Key store | dat_01, dat_11 | complete |
| dat_18 | Certification | - | blocked |
