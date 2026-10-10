# CROSS REFERENCE REPORT

این گزارش به‌صورت خودکار توسط `scripts/cross_ref.py` تولید/به‌روزرسانی می‌شود.
تا زمان اجرای آن، وضعیت اولیه به این شکل است:

| از | به | نوع ارجاع | وضعیت |
|---|---|---|---|
| dat_02 | dat_01 | URC → command | pending_blocked |
| dat_03 | dat_01 | error → command | pending_blocked |
| dat_09 | dat_01 | SMS command → AT | pending_blocked |
| dat_10 | dat_01 | GPRS command → AT | pending_blocked |
| dat_11 | dat_01 | HTTP/FTP/SSL → AT | pending_blocked |
| dat_12 | dat_01 | Audio → AT | pending_blocked |
| dat_13 | dat_01 | SIM → AT | pending_blocked |
| dat_17 | dat_11 | cert → SSL | pending_blocked |
| dat_04 | dat_05, dat_06 | timing → state/init | pending |
| dat_07 | dat_16 | pin → board | pending |
| dat_15 | dat_05 | power state → state machine | pending |

پس از اجرای `python scripts/cross_ref.py` این فایل با ارجاعات واقعی بازنویسی می‌شود.