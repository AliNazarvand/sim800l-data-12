# ROLE_MAP

| dataset | role | depends_on | used_by | status |
|---|---|---|---|---|
| dat_01 | AT command reference | - | dat_02, 03, 04, 06, 09, 10, 11, 12, 13, 15, 17 | complete |
| dat_02 | URC reference | dat_01 | dat_05 | complete |
| dat_03 | Error code reference | dat_01 | - | complete |
| dat_04 | Timing reference | V2.02, V1.00 | dat_05, dat_06, dat_15 | partial |
| dat_05 | State machine | dat_01, dat_04 | dat_02, dat_06, dat_15 | complete |
| dat_06 | Init sequence | dat_01, dat_04, dat_05 | - | partial |
| dat_07 | Hardware reference | V2.02, V1.00 | dat_13, dat_16 | complete |
| dat_08 | Firmware compatibility | external | - | blocked |
| dat_09 | SMS reference | dat_01 | - | complete |
| dat_10 | GPRS/Data reference | dat_01 | dat_14 | complete |
| dat_11 | HTTP/FTP/SSL reference | dat_01 | dat_17 | blocked |
| dat_12 | Audio reference | dat_01 | - | complete |
| dat_13 | SIM management reference | dat_01, dat_07 | - | complete |
| dat_14 | Operator/APN reference | external | dat_10 | deferred |
| dat_15 | Power reference | V2.02, V1.00 | dat_01, dat_05 | blocked |
| dat_16 | Board/EVB reference | external | - | deferred |
| dat_17 | Certificate reference | dat_01, dat_11 | - | blocked |
| dat_18 | Certification reference | external | - | blocked |