# Role Map

| دیتاست | نقش | وابسته به | وابسته‌های آن | وضعیت |
|--------|------|-----------|----------------|-------|
| dat_01 | مرجع commandها | - | dat_02, 03, 09, 10, 11, 12, 13, 17 | complete |
| dat_02 | مرجع URCها | dat_01 | - | complete |
| dat_03 | مرجع خطاها | dat_01 | - | complete |
| dat_04 | تایمینگ | - | dat_05, 06 | complete |
| dat_05 | State Machine | dat_04 | dat_06 | complete |
| dat_06 | Init Sequence | dat_04, 05 | - | complete |
| dat_07 | Hardware | - | dat_13, 15, 16 | complete |
| dat_08 | Firmware | - | - | inferred |
| dat_09 | SMS | dat_01 | - | complete |
| dat_10 | GPRS | dat_01 | dat_14 | complete |
| dat_11 | HTTP/FTP/SSL | dat_01 | dat_17 | complete |
| dat_12 | Audio | dat_01 | - | complete |
| dat_13 | SIM Management | dat_01, 07 | - | complete |
| dat_14 | Operator/APN | - | dat_10 | external |
| dat_15 | Power | dat_04, 05, 07 | - | complete |
| dat_16 | Board/EVB | dat_07 | - | inferred |
| dat_17 | Cert/Key | dat_01 | dat_11 | inferred |
| dat_18 | Certification | - | - | inferred |
