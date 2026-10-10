# sim800l-data

داده‌محور، ماشین‌خوان و منبع‌دار برای ماژول **SIM800L**.

## وضعیت پروژه (FINAL)

| دسته | تعداد | وضعیت |
|---|---|---|
| A (سخت‌افزاری — از دو PDF رسمی) | 5 | ✅ complete |
| A (Board/EVB) | 1 | deferred (سند رسمی گم) |
| B (AT-based) | 9 | blocked (نیازمند AT Command Manual) |
| C (خارجی/رسمی) | 3 | blocked/deferred |

### دیتاست‌های کامل (5)

- **dat_04** — Timing & Timeout (20 رکورد)
- **dat_05** — State Machine (23 رکورد)
- **dat_06** — Init Sequence (6 رکورد)
- **dat_07** — Hardware Reference (~100 رکورد)
- **dat_15** — Power Management (26 رکورد)

## منابع

- `sources/originals/SIM800L_Hardware_Design_V1.00.pdf`
- `sources/originals/SIM800H&SIM800L_Hardware_Design_V2.02.PDF`

## ساختار

- `data/` — رکوردها به تفکیک دیتاست
- `schemas/` — 18 schema YAML
- `scripts/` — validate, cross_ref, extract_pdf, ocr_pdf
- `reports/` — 18 گزارش دیتاست + گزارش‌های مدیریتی
- `COVERAGE_MATRIX.md` — ماتریس وضعیت نهایی
- `DECISIONS_LOG.md` — تصمیمات فنی
- `SESSION_LOG.md` — 13 نشست

## اعتبارسنجی

```bash
python scripts/validate.py
python scripts/cross_ref.py
```

## Rules (R1..R21)

- R1: فقط SIM800L — `applicable_models` شامل `SIM800L`.
- R2: هر رکورد `source` دارد.
- R12: `complete` تنها با `coverage_estimate: high`.
- R20: داده‌ی متناقض بین دیتاست‌ها ممنوع.
- R21: هیچ رکورد `example-only` در `data/`.