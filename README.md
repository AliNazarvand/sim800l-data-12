# SIM800L-Data

A structured, source-verified knowledge base for the SIMCom **SIM800L** module.

## Current Status (2026-10-10)

| Category    | Count | Datasets                                          |
|-------------|-------|---------------------------------------------------|
| Complete    | 3     | dat_04 (Timing), dat_06 (Init), dat_15 (Power)    |
| Partial     | 2     | dat_05 (State Machine), dat_07 (Hardware)         |
| Blocked     | 11    | dat_01, 02, 03, 08, 09, 10, 11, 12, 13, 17, 18   |
| Deferred    | 2     | dat_14 (MCC/MNC), dat_16 (EVB)                    |

**Validation:** 0 errors (`scripts/validate.py`)
**Authoritative coverage:** `reports/COVERAGE_FINAL.md`
**Project summary:** `PROJECT_STATUS.md`

## Sources

- `SIM800L_Hardware_Design_V1.00.pdf` (2013-08-20)
- `SIM800H&SIM800L_Hardware_Design_V2.02.PDF` (2015-07-27)

Extracted text: `sources/extracted/v1.00.txt`, `sources/extracted/v2.02.txt`.

## Structure

```
sim800l-data/
  data/         — 18 dataset folders (YAML records + _dataset_meta)
  schemas/      — 18 JSON schemas (canonical + YAML)
  sources/      — Original PDFs + extracted text
  reports/      — Per-dataset reports + coverage/validation reports
  scripts/      — Extraction, validation, cross-ref tools
  docs/         — Data dictionary, validation guide, source mapping
```

## Key Reports

| File                              | Purpose                              |
|-----------------------------------|--------------------------------------|
| `PROJECT_STATUS.md`               | Top-level status summary             |
| `reports/COVERAGE_FINAL.md`       | **Single source of truth** for status|
| `reports/COVERAGE_REALITY.md`     | Detailed per-dataset coverage        |
| `reports/VALIDATION_CANONICAL.md` | Validator policy                     |
| `DECISIONS_LOG.md`                | All technical decisions with reasons |
| `TODO.md`                         | Missing sources and blockers         |

## Validation

```bash
python scripts/validate.py
```

Expected output: `total errors: 0`.

## Blockers

**Critical:** SIM800 Series AT Command Manual is not available. This blocks
9 AT-command-based datasets. See `TODO.md` for the full list.

Without these sources, **100% coverage is impossible** without fabricating
data — which is prohibited by rules R2, R3, and R6 of the project spec.

## Applicable Models

**SIM800L only.** All records carry `applicable_models: [SIM800L]`.

## License

See `NOTICE` and `LICENSE`.
