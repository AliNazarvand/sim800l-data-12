# sim800l-data — SIM800L structured dataset

Module-specific, source-documented, schema-validated dataset for the SIM800L module.

Generated: 2026-10-13T18:13:14Z

## Status Summary

| Dataset | Name | Status | Real Records | Reason |
|---------|------|--------|--------------|--------|
| dat_01 | AT Command | complete | 335 | coverage=100% |
| dat_02 | URC | blocked | 0 | parser cannot extract from AT Manual |
| dat_03 | Error Code | blocked | 0 | parser cannot extract from AT Manual |
| dat_04 | Timing & Timeout | complete | 70 | - |
| dat_05 | State Machine | partial | 14 | below nominal threshold 20 |
| dat_06 | Init Sequence | complete | 20 | - |
| dat_07 | Hardware Reference | complete | 78 | - |
| dat_08 | Firmware Compatibility | blocked | 1 | Release Notes missing |
| dat_09 | SMS | complete | 14 | - |
| dat_10 | GPRS/Data | complete | 21 | - |
| dat_11 | HTTP/FTP/SSL | partial | 10 | HTTP/FTP/SSL manuals missing |
| dat_12 | Audio | partial | 7 | Audio manual missing |
| dat_13 | SIM Management | complete | 10 | - |
| dat_14 | Operator/APN | complete | 52 | - |
| dat_15 | Power Management | partial | 351 | pipeline over-extraction: 351 records, expected ~13-28 |
| dat_16 | Board/EVB | deferred | 1 | EVB schematic not available (per prompt spec) |
| dat_17 | Certificate/Key Store | blocked | 9 | SSL AT Command Manual missing |
| dat_18 | Certification | blocked | 1 | Certification documents missing |

**Totals:** complete=8, partial=4, blocked=5, deferred=1 (of 18 datasets).

## Sources Present

- sources/originals/SIM800 Series_AT Command Manual_V1.01.pdf
- sources/originals/SIM800H&SIM800L_Hardware_Design_V2.02.PDF
- sources/originals/SIM800L_Hardware_Design_V1.00.pdf

## Known Limitations

- **dat_02, dat_03 (blocked):** parser (_parse_B2B3.py) cannot extract URC/CME-CMS entries.
- **dat_11, dat_12 (partial):** specialist manuals (HTTP/FTP/SSL, Audio) are missing.
- **dat_15 (partial):** _rebuild_dat15.py over-extracts (351 records, expected ~13-28).
- **dat_08, dat_17, dat_18 (blocked):** external sources missing (Release Notes, SSL manual, certification docs).
- **dat_16 (deferred):** EVB schematic missing per prompt spec.

## Validation

All YAML files pass schema validation. Cross-reference checks pass.
