# sim800l-data

Structured, traceable, schema-valid datasets for the **SIM800L** module.

## Scope

- **Only** SIM800L. No SIM800H, SIM900, SIM7000, or other module data unless the source explicitly states it applies to SIM800L.
- Every record must include `applicable_models` containing `SIM800L`.
- No synthetic, guessed, or unsourced data.

## Structure

```
data/       -- YAML datasets (dat_01 .. dat_18)
schemas/    -- JSON Schema for each dataset (dataset-specific)
sources/    -- Original PDFs and extracted text
reports/    -- Coverage, gaps, decisions, session logs
scripts/    -- validate.py, extract_pdf.py, cross_ref.py, ocr_pdf.py
docs/       -- Data dictionary
tools/      -- Preflight checks
```

## Datasets

| ID | Name | Status |
|----|------|--------|
| dat_01 | AT Command | partial |
| dat_02 | URC | partial |
| dat_03 | Error Code | partial |
| dat_04 | Timing & Timeout | partial |
| dat_05 | State Machine | partial |
| dat_06 | Init Sequence | partial |
| dat_07 | Hardware Reference | partial |
| dat_08 | Firmware Compatibility | blocked |
| dat_09 | SMS | partial |
| dat_10 | GPRS/Data | partial |
| dat_11 | HTTP/FTP/SSL | partial |
| dat_12 | Audio | partial |
| dat_13 | SIM Management | partial |
| dat_14 | Operator/APN | deferred |
| dat_15 | Power Management | partial |
| dat_16 | Board/EVB | deferred |
| dat_17 | Certificate/Key Store | partial |
| dat_18 | Certification | blocked |

## Available Sources

- `SIM800L_Hardware_Design_V1.00.pdf` (2013-08-20)
- `SIM800H&SIM800L_Hardware_Design_V2.02.PDF` (2015-07-27) -- priority
- `SIM800 Series_AT Command Manual_V1.01.pdf`

## Validation

```bash
pip install pyyaml jsonschema
python scripts/validate.py     # 4-level validation
python scripts/cross_ref.py    # cross-reference checks
python tools/preflight.py      # artifact presence
```

## License

MIT