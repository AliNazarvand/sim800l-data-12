# ROLE_MAP

| دیتاست | نقش | وابسته به | وابسته‌های آن | وضعیت |
|---|---|---|---|---|
| dat_01 | مرجع commandها | - | dat_02, 03, 09, 10, 11, 12, 13, 17 | partial |
| dat_02 | مرجع URCها | dat_01 | - | pending |
| dat_03 | مرجع Error Code | dat_01 | - | pending |
| dat_04 | مرجع Timing | - | - | pending |
| dat_05 | مرجع State | - | - | pending |
| dat_06 | مرجع Init | - | - | pending |
| dat_07 | مرجع Hardware | - | dat_13, dat_16 | pending |
| dat_08 | مرجع Firmware | - | - | blocked |
| dat_09 | مرجع SMS | dat_01 | - | pending |
| dat_10 | مرجع GPRS | dat_01 | - | blocked |
| dat_11 | مرجع HTTP/FTP/SSL | dat_01 | dat_17 | blocked |
| dat_12 | مرجع Audio | dat_01 | - | blocked |
| dat_13 | مرجع SIM | dat_01, dat_07 | - | pending |
| dat_14 | مرجع APN | - | - | deferred |
| dat_15 | مرجع Power | - | - | pending |
| dat_16 | مرجع Board | dat_07 | - | deferred |
| dat_17 | مرجع Cert | dat_01, dat_11 | - | blocked |
| dat_18 | مرجع Certification | - | - | blocked |