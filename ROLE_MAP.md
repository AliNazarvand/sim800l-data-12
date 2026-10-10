# ROLE_MAP — نقش و وابستگی دیتاست‌ها

| دیتاست | نقش | وابسته به | وابسته‌های آن | وضعیت |
|---|---|---|---|---|
| dat_01 | مرجع commandها | - | dat_02, 03, 09, 10, 11, 12, 13, 17 | partial |
| dat_02 | مرجع URCها | dat_01 | - | partial |
| dat_03 | مرجع خطاها | dat_01 | - | partial |
| dat_04 | مرجع زمان‌بندی | - | dat_05, dat_06, dat_15 | complete |
| dat_05 | مرجع حالت‌ها | dat_04 | dat_06, dat_15 | complete |
| dat_06 | مرجع init | dat_01, dat_04, dat_05 | - | complete |
| dat_07 | مرجع سخت‌افزار | - | dat_13, dat_15, dat_16 | complete |
| dat_08 | سازگاری فرمور | - | - | blocked |
| dat_09 | مرجع SMS | dat_01 | - | partial |
| dat_10 | مرجع GPRS/Data | dat_01, dat_05 | dat_11 | partial |
| dat_11 | مرجع HTTP/FTP/SSL | dat_01, dat_10 | dat_17 | partial |
| dat_12 | مرجع Audio | dat_01 | - | partial |
| dat_13 | مرجع SIM | dat_01, dat_07 | - | partial |
| dat_14 | مرجع اپراتور/APN | - | dat_10 | external |
| dat_15 | مرجع Power | dat_04, dat_05, dat_07 | - | complete |
| dat_16 | مرجع EVB | dat_07 | - | deferred |
| dat_17 | مرجع Certificate | dat_01, dat_11 | - | blocked |
| dat_18 | مرجع Certification | - | - | blocked |