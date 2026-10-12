# sim800l-data

Structured data for the SIMCom SIM800L module — schemas, YAML datasets,
and reproducible validation tooling.

## Status

Phase 2 complete.

| status   | count | datasets |
|----------|-------|----------|
| complete | 4 | dat_03, dat_07, dat_09, dat_13 |
| partial  | 7 | dat_01, dat_02, dat_04, dat_05, dat_06, dat_10, dat_12 |
| blocked  | 5 | dat_08, dat_11, dat_15, dat_17, dat_18 |
| deferred | 2 | dat_14, dat_16 |

See `reports/COVERAGE_MATRIX.md` for the authoritative table.

## Layout

- `data/` — 18 YAML datasets (`dat_01_*.yaml` .. `dat_18_*.yaml`)
- `schemas/` — 18 JSON-Schema (Draft-07) files
- `sources/originals/` — source PDFs
- `sources/extracted/` — extracted text and tables
- `reports/` — coverage, decisions, session logs
- `scripts/` — validation, cross-reference, PDF extraction, OCR

## Scripts

```
python scripts/validate.py --root .
python scripts/cross_ref.py --root .
python scripts/extract_pdf.py --input sources/originals/file.pdf
python scripts/ocr_pdf.py --input sources/originals/scanned.pdf
```

## Rules

The project follows rules R1..R24 (see `PHASE_2_REPORT.md` for the
consolidated rule reference). Every record must:

- be attributable to a primary or secondary source with page/quote
- be schema-valid
- carry `applicable_models: [SIM800L]`
- never be `synthetic` or `example-only` inside `data/`

## License

TBD.