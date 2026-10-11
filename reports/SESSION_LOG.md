# SESSION_LOG

## بسته بزرگ B2+B3 clean + B4+B5 + A3-ext

- تاریخ: 1405-07-19T17:17:15Z
- برنچ: feature/complete-datasets
- موفق: 2 از 5

### جدول زیرگام‌ها

| زیرگام | نام | وضعیت | گیت | جزئیات |
|---|---|---|---|---|
| 1 | Audit B2B3 | OK | True | dat_02=188/206 susp; dat_03=7/255 susp |
| 2 | Cleanup B2B3 | OK | True | partial: dat_02 3->2, dat_03 11->11 |
| 3 | dat_09 SMS | ROLLED_BACK | False | partial=1 (<10) |
| 4 | dat_13 SIM | ROLLED_BACK | False | partial=0 (<5) |
| 5 | Annotate 04/05/06 | ROLLED_BACK | False | page%: 04=15.4 05=100 06=10 (need >=50 each) |

### وضعیت نهایی validate.py
- L1: 0
- L2: 0
- L3: 35
- L4: 0

### کار گام بعد
- ادامه خوشه B (B6, B7, B8, B9) در صورت تأمین منابع تخصصی.
- کار دستی برای dat_02/dat_03 در صورت باقی‌ماندن مشکوک‌ها.