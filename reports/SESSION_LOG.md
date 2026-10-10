# SESSION_LOG

## نشست ۲ — اعمال پاک‌سازی ریز dat_01
- گام ۴.۱: ۱ رکورد `confirmed_noise` حذف شد.
- گام ۴.۲: ۱۸ رکورد `weak_at_signal` با `status: partial` و `notes` علامت‌گذاری شدند (بدون حذف).
- `scripts/apply_refine_dat_01.py` و `scripts/diagnose_refine_dat_01.py` اضافه شدند.
- `validate.py` و `cross_ref.py` مجدداً اجرا شدند.
- گزارش‌های `COVERAGE_MATRIX`، `TODO`، `CHANGELOG`، `DECISIONS_LOG` به‌روز شدند.

## کار بعدی (نشست ۳)
- شروع خوشه A، عضو A1: `dat_07` Hardware Reference از V2.02 و V1.00.