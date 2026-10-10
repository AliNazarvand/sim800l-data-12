# sim800l-data

A data-only, machine-readable, schema-validated reference repository for the
**SIM800L** (and, where explicitly required, **SIM800H**) cellular module.

This repository contains **data only** — no drivers, no libraries, no
compilable code. The only Python files live under `tools/` and exist solely
for schema validation, JSON generation, and PDF preflight checks.

## Current Status — Awaiting Primary Source PDFs

**Phase 1 has not produced any dataset yet.** The two primary Hardware Design
PDFs were not accessible when this repository was last touched. Per the
project's explicit rule ("Before any other action, the two source PDFs must
be obtained; if they are not accessible, stop work and report"), no data has
been extracted and no dataset has been fabricated.

See `PHASE_1_REPORT.md` for the stop report and next steps.

### To proceed

1. Place the two PDFs in one of these locations (any of them is fine):
   - `./` (repository root)
   - `./sources/`
   - `./pdfs/`
   - the parent folder of this repository
   with exactly these file names:
   - `SIM800L_Hardware_Design_V1.00.pdf`
   - `SIM800H&SIM800L_Hardware_Design_V2.02.PDF`
2. Re-run the project pipeline. `tools/preflight.py` will confirm the PDFs
   are reachable before any further work begins.

## Primary Sources

- `SIM800L_Hardware_Design_V1.00` — v1.00, 2013-08-20
- `SIM800H&SIM800L_Hardware_Design_V2.02` — v2.02, 2015-07-27

**Conflict rule:** In any conflict between V1.00 and V2.02, **V2.02 wins**.

## Repository Layout

```
sim800l-data/
├── README.md
├── LICENSE
├── NOTICE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── PHASE_1_REPORT.md
├── requirements.txt
├── schemas/            JSON-Schema per dataset (added when data exists)
├── data/               YAML datasets (source of truth)
├── raw/                Raw extraction notes and diagram descriptions
├── sources/            Place the two primary PDFs here
├── tools/
│   ├── preflight.py    Verifies the two source PDFs are present
│   ├── validate.py     Validates YAML against schemas
│   └── generate_json.py  Produces valid JSON from YAML
├── docs/
│   ├── data_dictionary.md
│   ├── source_mapping.md
│   ├── conflict_log.md
│   ├── diagram_mapping.md
│   └── validation_guide.md
└── .github/workflows/  CI: validate.yml
```

## Tools

```bash
pip install -r requirements.txt
python tools/preflight.py           # verify PDFs are reachable
python tools/validate.py            # validate data/**/*.yaml
python tools/generate_json.py       # write JSON next to each YAML
python tools/generate_json.py --check   # CI mode
```

See `docs/validation_guide.md`.

## Legal Notice

Data extracted from SIMCom documents may be subject to redistribution
restrictions. See `NOTICE` and `LICENSE`. The `_meta.license_note` field of
every record points to `NOTICE`.

---

## توضیحات فارسی

این مخزن یک مرجع **داده‌محور** برای ماژول SIM800L (و در موارد مشخص SIM800H)
است و هیچ کد اجرایی، درایور یا کتابخانه‌ای در آن عرضه نمی‌شود.

**وضعیت فعلی:** هنوز هیچ دیتاستی تولید نشده است، چون دو فایل PDF مرجع در
زمان اجرا در دسترس نبودند. طبق قاعده صریح پروژه («اگر دسترسی به PDF
امکان‌پذیر نیست، کار متوقف و گزارش شود»)، هیچ داده‌ای استخراج یا بازسازی
نشده است. برای ادامه، دو PDF را در یکی از مسیرهای `./`، `./sources/`،
`./pdfs/` یا پوشه والد این ریپازیتوری با همان نام‌های دقیق قرار دهید و سپس
`tools/preflight.py` را اجرا کنید.

برای جزئیات، فایل `PHASE_1_REPORT.md` را ببینید.