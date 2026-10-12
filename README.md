# sim800l-data

Structured, traceable, schema-valid datasets for the **SIM800L** module.

_Last updated: 2026-10-12_

## Scope

- **Only** SIM800L. No SIM800H, SIM900, SIM7000, or other module data unless the source explicitly states it applies to SIM800L.
- Every record includes `applicable_models` containing `SIM800L`.
- No synthetic, guessed, or unsourced data.

## Structure

```
data/       -- YAML datasets (dat_01 .. dat_18)
schemas/    -- JSON Schema per dataset
sources/    -- Original PDFs and extracted text
reports/    -- Coverage, gaps, decisions, session logs
scripts/    -- validate.py, extract_pdf.py, cross_ref.py, ocr_pdf.py, diagnose_sources.py
tools/      -- Preflight checks
```

## Datasets (current status)

| ID | Name | Status | Real records |
|----|------|--------|--------------|
| dat_01 | AT Command | partial | 275 |
| dat_02 | URC | partial | 206 |
| dat_03 | Error Code | partial | 255 |
| dat_04 | Timing & Timeout | partial | 40 |
| dat_05 | State Machine | partial | 31 |
| dat_06 | Init Sequence | partial | 32 |
| dat_07 | Hardware Reference | partial | 56 |
| dat_08 | Firmware Compatibility | blocked | 0 |
| dat_09 | SMS | partial | 14 |
| dat_10 | GPRS/Data | partial | 24 |
| dat_11 | HTTP/FTP/SSL | partial | 38 |
| dat_12 | Audio | partial | 13 |
| dat_13 | SIM Management | partial | 10 |
| dat_14 | Operator/APN | partial | 52 |
| dat_15 | Power Management | partial | 13 |
| dat_16 | Board/EVB | deferred | 0 |
| dat_17 | Certificate/Key Store | partial | 9 |
| dat_18 | Certification | blocked | 0 |

## Available Sources

- `SIM800L_Hardware_Design_V1.00.pdf` (2013-08-20)
- `SIM800H&SIM800L_Hardware_Design_V2.02.PDF` (2015-07-27) -- priority
- `SIM800 Series_AT Command Manual_V1.01.pdf`

## Validation

```bash
pip install pyyaml jsonschema
python scripts/validate.py          # 4-level validation
python scripts/cross_ref.py         # cross-reference checks
python scripts/diagnose_sources.py  # inspect source formats
```

## License

MIT