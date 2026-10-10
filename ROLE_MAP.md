# ROLE MAP

| دیتاست | نقش | وابسته به | وابسته‌های آن | وضعیت |
|---|---|---|---|---|
| dat_01 | مرجع commandها | - | dat_02, 03, 09, 10, 11, 12, 13, 17 | blocked |
| dat_02 | مرجع URCها | dat_01 | - | pending_blocked |
| dat_03 | مرجع خطاها | dat_01 | - | pending_blocked |
| dat_04 | مرجع زمان‌بندی | - | dat_05, dat_06 | complete |
| dat_05 | ماشین حالت | - | dat_04, dat_15 | complete |
| dat_06 | توالی init | - | dat_04 | complete |
| dat_07 | مرجع سخت‌افزار | - | dat_13, dat_16 | complete |
| dat_08 | سازگاری فریمور | Release Notes | - | blocked |
| dat_09 | SMS | dat_01 | - | pending_blocked |
| dat_10 | GPRS/Data | dat_01 | - | pending_blocked |
| dat_11 | HTTP/FTP/SSL | dat_01 | dat_17 | pending_blocked |
| dat_12 | Audio | dat_01 | - | pending_blocked |
| dat_13 | SIM | dat_01, dat_07 | - | pending_blocked |
| dat_14 | MCC/MNC/APN | GSMA/ITU | dat_10 | deferred |
| dat_15 | Power | - | dat_05 | complete |
| dat_16 | Board/EVB | EVB Doc | dat_07 | deferred |
| dat_17 | Certificate | dat_11 | - | pending_blocked |
| dat_18 | Certification | CE/FCC | - | blocked |

> **pending_blocked** = دیتاست به دیتاست منبع (dat_01) وابسته است که خودش blocked است.