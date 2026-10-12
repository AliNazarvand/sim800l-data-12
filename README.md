# sim800l-data

Structured, traceable, schema-valid datasets for the **SIM800L** module.

_Last updated: 2026-10-12_

## Datasets (current status)

| ID | Name | Status | Real | Documented |
|----|------|--------|------|------------|
| dat_01 | AT Command | partial | 334 | 0 |
| dat_02 | URC | partial | 206 | 0 |
| dat_03 | Error Code | partial | 255 | 0 |
| dat_04 | Timing & Timeout | partial | 40 | 0 |
| dat_05 | State Machine | partial | 31 | 0 |
| dat_06 | Init Sequence | partial | 32 | 0 |
| dat_07 | Hardware Reference | partial | 56 | 0 |
| dat_08 | Firmware Compatibility | blocked | 0 | 1 |
| dat_09 | SMS | partial | 14 | 0 |
| dat_10 | GPRS/Data | partial | 24 | 0 |
| dat_11 | HTTP/FTP/SSL | partial | 38 | 0 |
| dat_12 | Audio | partial | 13 | 0 |
| dat_13 | SIM Management | partial | 10 | 0 |
| dat_14 | Operator/APN | partial | 52 | 0 |
| dat_15 | Power Management | partial | 14 | 0 |
| dat_16 | Board/EVB | deferred | 0 | 1 |
| dat_17 | Certificate/Key Store | partial | 9 | 0 |
| dat_18 | Certification | blocked | 0 | 1 |

## Cross-Reference Status

- Strict issues: **0**
- Soft issues: **0**

## Validation

```bash
pip install pyyaml jsonschema
python scripts/validate.py          # schema validation (4-level)
python scripts/cross_ref.py         # cross-reference checks
python scripts/diagnose_sources.py  # inspect source formats
```

## License

MIT