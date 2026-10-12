# Role Map -- sim800l-data

_Last updated: 2026-10-12_

| Dataset | Role | Depends On | Dependents | Status |
|---------|------|------------|------------|--------|
| dat_01 | AT Command reference | - | dat_02,03,09,10,11,12,13,17 | partial |
| dat_02 | URC reference | dat_01 | - | partial |
| dat_03 | Error Code reference | dat_01 | - | partial |
| dat_04 | Timing reference | V1.00, V2.02 | dat_05, dat_06 | partial |
| dat_05 | State Machine reference | dat_04 | dat_06 | partial |
| dat_06 | Init Sequence reference | dat_04, dat_05 | - | partial |
| dat_07 | Hardware reference | V2.02, V1.00 | dat_16 | partial |
| dat_08 | Firmware compatibility | Release Notes | - | blocked |
| dat_09 | SMS reference | dat_01 | - | partial |
| dat_10 | GPRS/Data reference | dat_01 | - | partial |
| dat_11 | HTTP/FTP/SSL reference | dat_01 | dat_17 | partial |
| dat_12 | Audio reference | dat_01 | - | partial |
| dat_13 | SIM Management reference | dat_01, dat_07 | - | partial |
| dat_14 | Operator/APN reference | external | dat_10 | partial |
| dat_15 | Power Management reference | V2.02, V1.00 | dat_05 | partial |
| dat_16 | Board/EVB reference | dat_07 | - | deferred |
| dat_17 | Certificate/Key Store reference | dat_01, dat_11 | - | partial |
| dat_18 | Certification reference | Official docs | - | blocked |