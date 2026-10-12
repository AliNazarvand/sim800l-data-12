# ROLE MAP

Generated: 2026-10-12T14:39:53Z

| Dataset | Role | Depends On | Depended By | Status |
|---|---|---|---|---|
| dat_01 | AT Command reference | - | dat_02,dat_03,dat_09,dat_10,dat_12,dat_13 | partial |
| dat_02 | URC reference | dat_01 | - | partial |
| dat_03 | Error code reference | dat_01 | - | complete |
| dat_04 | Timing reference | - | dat_05,dat_06 | partial |
| dat_05 | State machine | dat_04 | dat_06 | partial |
| dat_06 | Init sequence | dat_04,dat_05 | - | partial |
| dat_07 | Hardware reference | - | dat_13 | complete |
| dat_08 | Firmware compat | dat_01 | - | blocked |
| dat_09 | SMS | dat_01 | - | complete |
| dat_10 | GPRS/Data | dat_01 | dat_14 | partial |
| dat_11 | HTTP/FTP/SSL | dat_01,dat_17 | - | blocked |
| dat_12 | Audio | dat_01 | - | partial |
| dat_13 | SIM management | dat_01,dat_07 | - | complete |
| dat_14 | Operator/APN | - | dat_10 | deferred |
| dat_15 | Power management | - | - | blocked |
| dat_16 | Board/EVB | dat_07 | - | deferred |
| dat_17 | Certificate/Key Store | dat_01,dat_11 | - | blocked |
| dat_18 | Certification | - | - | blocked |
