# sim800l-data

Structured, traceable, schema-valid datasets for the **SIM800L** module.

_Last updated: 2026-10-12_

## Datasets (current status)

| ID | Name | Status | Real | Documented |
|----|------|--------|------|------------|
| dat_01 | AT Command | partial | 334 | 0 |
| dat_02 | URC | partial | 205 | 1 |
| dat_03 | Error Code | partial | 249 | 6 |
| dat_04 | Timing & Timeout | partial | 17 | 23 |
| dat_05 | State Machine | partial | 20 | 11 |
| dat_06 | Init Sequence | partial | 22 | 10 |
| dat_07 | Hardware Reference | partial | 56 | 0 |
| dat_08 | Firmware Compatibility | blocked | 0 | 1 |
| dat_09 | SMS | partial | 14 | 0 |
| dat_10 | GPRS/Data | partial | 21 | 3 |
| dat_11 | HTTP/FTP/SSL | partial | 19 | 19 |
| dat_12 | Audio | partial | 9 | 4 |
| dat_13 | SIM Management | partial | 10 | 0 |
| dat_14 | Operator/APN | partial | 0 | 52 |
| dat_15 | Power Management | partial | 13 | 1 |
| dat_16 | Board/EVB | deferred | 0 | 1 |
| dat_17 | Certificate/Key Store | partial | 0 | 9 |
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