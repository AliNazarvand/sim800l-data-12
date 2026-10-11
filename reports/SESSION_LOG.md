# SESSION_LOG

## Batch B6+B7+B8+B9 + cluster C — گیت per-dataset

- تاریخ: 1405-07-19T17:19:43Z
- موفق: 4 / 6

| زیرگام | نام | نتیجه | وضعیت |
|---|---|---|---|
| 1_dat10 | dat_10 GPRS/Data | sum=21 | OK |
| 2_dat11 | dat_11 HTTP/FTP/SSL | sum=10 found=10 | OK |
| 3_dat12 | dat_12 Audio | sum=7 found=7 | OK |
| 4_dat17 | dat_17 Cert/Key | found=0 | BLOCKED |
| 5_0406 | annotate dat_04/dat_06 | d04=15.4% d06=10% | ROLLED_BACK |
| 6_clusterC | cluster C status | see report | OK |

### وضعیت validate.py
- L1: 0
- L2: 0
- L3: 35
- L4: 0

### تغییرات کلیدی این نشست
- گیت‌ها per-dataset طراحی شدند (نه group).
- معیار موفقیت = annotated_or_added یا page_pct (نه partial count).
- هر دیتاست fail مستقل rollback شد.
- منابع تخصصی (HTTP/FTP/SSL/Audio/Cert) طبق D-019 فقط با ساختار header-محور بررسی شدند.

### کار گام بعد
- کار دستی برای dat_11, dat_12, dat_17 در صورت نیاز.
- یا ادامه خوشه C.