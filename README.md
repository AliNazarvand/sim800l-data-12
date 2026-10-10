# sim800l-data

A data-only, machine-readable, schema-validated reference repository for the
**SIM800L** (and, where explicitly required, **SIM800H**) cellular module.

This repository contains **data only** — no drivers, no libraries, no
compilable code. The only Python files live under `tools/` and exist solely
for schema validation, JSON generation, and PDF preflight checks.

## Phase 1 Status

Phase 1 delivers six hardware-focused datasets extracted only from the two
primary hardware design PDFs.

| ID     | Dataset                       | Records | Status   |
|--------|-------------------------------|---------|----------|
| dat_07 | Hardware Reference DB         | 80      | partial  |
| dat_04 | Timing & Timeout DB           | 11      | complete |
| dat_15 | Power Management DB           | 4       | partial  |
| dat_05 | State Machine DB              | 19      | complete |
| dat_06 | Init Sequence DB              | 5       | complete |
| dat_16 | Board/EVB Definitions         | 0       | deferred |

See `PHASE_1_REPORT.md` for the complete status, gaps, and deferrals.

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
├── schemas/            JSON-Schema per dataset
├── data/               YAML datasets (source of truth)
├── raw/                Raw extraction notes and diagram descriptions
├── sources/            Place the two primary PDFs here
├── tools/
│   ├── preflight.py
│   ├── validate.py
│   └── generate_json.py
├── docs/
│   ├── data_dictionary.md
│   ├── source_mapping.md
│   ├── conflict_log.md
│   ├── diagram_mapping.md
│   └── validation_guide.md
└── .github/workflows/  CI: validate.yml
```

## How to Use

1. Read the relevant YAML under `data/<dataset>/`.
2. JSON equivalents are auto-generated next to each YAML by
   `tools/generate_json.py`. Never edit JSON by hand.
3. Consult `docs/source_mapping.md` for the source page/section of each field.
4. Consult `docs/conflict_log.md` for V1.00 vs V2.02 resolutions.

## Running Validation and JSON Generation

```bash
pip install -r requirements.txt
python tools/validate.py
python tools/generate_json.py
python tools/generate_json.py --check   # CI mode
```

See `docs/validation_guide.md`.

## Legal Notice

Data extracted from SIMCom documents may be subject to redistribution
restrictions. See `NOTICE` and `LICENSE`. The `_meta.license_note` field of
every record points to `NOTICE`.

## Phase 2 Roadmap

- **Phase 2a** — Completion of Phase 1 datasets with secondary sources
  (AT Command Manual).
- **Phase 2b** — Datasets that require secondary sources.

Phase 2a will not start until `PHASE_1_REPORT.md` is explicitly approved.

---

## توضیحات فارسی

این مخزن یک مرجع **داده‌محور** برای ماژول SIM800L (و در موارد مشخص SIM800H)
است. هیچ کد اجرایی، درایور یا کتابخانه‌ای در آن عرضه نمی‌شود؛ تنها داده
(YAML به‌عنوان منبع اصلی)، Schemaهای اعتبارسنجی، مستندات Markdown و دو ابزار
سبک داخلی در `tools/` وجود دارد.

**قاعده طلایی:** هیچ داده‌ای از دانش پیشین مدل تولید نمی‌شود. هر فیلدی که
در منابع موجود نباشد با `null` و `_meta.missing_reason` علامت‌گذاری می‌شود.

برای جزئیات شکاف‌ها و وضعیت هر دیتاست، فایل `PHASE_1_REPORT.md` را ببینید.