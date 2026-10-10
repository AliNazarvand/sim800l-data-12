# Validation Guide

## اجرا

```bash
python scripts/validate.py
python scripts/cross_ref.py
python tools/preflight.py
```

## سطوح اعتبارسنجی

1. **Schema**: شکل داده (اجباری بودن، نوع، enum).
2. **Business logic**: confidence، source_type، status.
3. **Cross-ref**: ارجاعات بین دیتاست‌ها.
4. **Consistency**: سازگاری بین دیتاست‌های مرتبط.

## قواعد قطعی

- status ممنوعه در data/: `example-only`, `synthetic`.
- `applicable_models` باید شامل `SIM800L` باشد.
- `source_type` ∈ {primary, secondary, external}.
- `confidence` ∈ [0.0, 1.0].

## خروجی‌ها

- `reports/VALIDATION_REPORT.md`
- `reports/CROSS_REF_REPORT.md`
