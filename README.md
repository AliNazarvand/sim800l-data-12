# sim800l-data

SIM800L structured dataset — module-specific, source-documented, schema-validated.

## Status Summary

| Dataset | Name | Status | Records |
|---|---|---|---|
| dat_01 | AT Command | partial | 335 |
| dat_02 | URC | partial | 18 |
| dat_03 | Error Code | complete | 255 |
| dat_04 | Timing & Timeout | complete | 70 |
| dat_05 | State Machine | complete | 31 |
| dat_06 | Init Sequence | complete | 35 |
| dat_07 | Hardware Reference | complete | 83 |
| dat_08 | Firmware Compatibility | blocked | 1 |
| dat_09 | SMS | complete | 14 |
| dat_10 | GPRS/Data | complete | 24 |
| dat_11 | HTTP/FTP/SSL | complete | 38 |
| dat_12 | Audio | complete | 13 |
| dat_13 | SIM Management | complete | 10 |
| dat_14 | Operator/APN | complete | 52 |
| dat_15 | Power Management | complete | 28 |
| dat_16 | Board/EVB | blocked | 1 |
| dat_17 | Certificate/Key Store | blocked | 9 |
| dat_18 | Certification | blocked | 1 |

## Known Limits

- **dat_01 (partial)**: 278 of 335 records lack per-parameter detail because the AT Command Manual V1.01 has ToC-level entries only for many commands.
- **dat_02 (partial)**: 18 URC records; the manual does not provide full examples for all URCs.
- **dat_08, dat_16, dat_18 (blocked)**: firmware release notes, EVB schematic, and CE/FCC certificates are not in the project.
- **dat_17 (blocked)**: SSL certificate commands require the SIM800 SSL AT Command Manual, which is not present.

## Missing Source Documents

- SIM800 Series SSL AT Command Manual
- SIM800 Series HTTP AT Command Manual
- SIM800 Series FTP AT Command Manual
- SIM800 Series Audio AT Command Manual
- SIM800 Series Firmware Release Notes
- SIM800L EVB Schematic
- CE / FCC / RoHS / GCF / PTCRB certificates

## Sources Present

- \sources/originals/SIM800 Series_AT Command Manual_V1.01.pdf\
- \sources/originals/SIM800H&SIM800L_Hardware_Design_V2.02.PDF\
- \sources/originals/SIM800L_Hardware_Design_V1.00.pdf\

## Validation

- \scripts/validate.py\ (jsonschema, business rules)
- \scripts/cross_ref.py\ (source-aware unresolved classification)
- \scripts/audit_datasets.py\ (data health)

All YAML files validate with 0 schema errors.