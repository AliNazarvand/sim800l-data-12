# SIM800L Knowledge Base

پایگاه دانش ساختاریافته برای ماژول **SIM800L** (فقط).

## وضعیت نهایی

- ۱۸ دیتاست در فرمت YAML کانونیک
- ۱۳ دیتاست complete
- ۱ دیتاست external (dat_14)
- ۴ دیتاست inferred (dat_08, 16, 17, 18) - پذیرش مستند
- ۰ دیتاست blocked
- ۰ فایل JSON legacy
- ۰ پوشه tools/ یا raw/

## ساختار

```
sim800l-data/
├── data/            # دیتاست‌های YAML کانونیک
├── schemas/         # 18 schema (JSON Schema draft-07 در قالب YAML)
├── sources/
│   ├── originals/   # PDFهای رسمی
│   └── extracted/   # متن استخراج‌شده (*.txt + manifest.json)
├── reports/         # گزارش‌های مدیریتی و dat_XX_REPORT
├── scripts/         # validate.py, cross_ref.py, extract_*.py
└── docs/            # مستندات
```

## اجرا

```bash
pip install pyyaml jsonschema pymupdf pdfplumber
python scripts/validate.py       # اعتبارسنجی ۴ سطحی با jsonschema
python scripts/cross_ref.py      # ۷ قاعده cross-ref واقعی
python scripts/extract_pdf.py    # استخراج متن PDF
python scripts/extract_figures.py# استخراج شکل‌های معنادار (فیلتر شده)
python scripts/extract_tables.py # استخراج جدول‌های معنادار (فیلتر شده)
python scripts/preflight.py      # بررسی منابع
```

## قواعد

- R1: فقط SIM800L
- R2: هیچ رکورد بدون source
- R4: inferred با confidence ≤ 0.5
- R6: هیچ synthetic
- R7: V2.02 > V1.00
- R21: هیچ example-only در data/

## فرمت داده

- فقط **YAML** (JSON legacy حذف شده)
- Schemaها در قالب **JSON Schema draft-07** با فرمت YAML
- اعتبارسنجی با کتابخانه `jsonschema`
