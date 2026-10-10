# CLEANUP_V7_REPORT

تاریخ: 14050719-000048
برنچ: chore/cleanup-v7

## ۱) Refine the 59
- خروجی: `reports/dat_01_REFINE.md` و `reports/dat_01_REFINE.json`
- هیچ داده‌ای از `data/` حذف نشد.

## ۲) Cleanup دور دوم

### ۲.۱ — فایل‌های JSON/LOG/TMP در ریشه scripts/ (4)
- _step_b_result.json
- _v4_report_state.json
- _v4_state.json
- _v5_summary.json

### ۲.۲ — گزارش‌های CLEANUP کهنه به reports/archive/ (2)
- CLEANUP_V4_REPORT.md
- CLEANUP_V5_REPORT.md

### ۲.۳ — CSVهای ریز جداول به _raw/

| پوشه | تعداد CSV منتقل‌شده |
|---|---|
| at_v1_01 | 727 |
| hw_v1_00 | 94 |
| hw_v2_02 | 98 |

## یادداشت
- هیچ فایلی در `data/` یا `schemas/` لمس نشد.
- فایل‌های منتقل‌شده قابل بازگردانی هستند (از `scripts/archive/legacy/` یا `reports/archive/` یا `_raw/`).
- گام بعدی: خوشه A (dat_07) با یک اسکریپت کوچک مجزا.