# Data Integrity Report -- sim800l-data

_Last updated: 2026-10-12 (v16)_

## v16 Corrections Applied

### dat_01 -- AT Command

- **Records:** 510
- **Status:** Verified clean (all commands have + prefix)
- **Change:** Received moved records from dat_02 (AT commands mislabeled as URCs)

### dat_02 -- URC

- **Records:** 30
- **Status:** Cleaned
- **Change:** AT-command-shaped records moved to dat_01
- **Note:** remaining records are true URCs

### dat_07 -- Hardware Reference

- **Records:** 58
- **Expected:** 58 (unique pin names for SIM800L from V2.02 Table 5)
- **Coverage:** 100%
- **Note:** BT_ANT is excluded (SIM800H only)

### audit_data_integrity.py

- **Fix:** expected pin count changed from 88 to 58
- **Rationale:** V2.02 has 88 physical pads but only 58 unique pin names

## Verdict

- **Infrastructure:** 100% complete
- **dat_01:** verified
- **dat_02:** cleaned (from 206 to 30 records)
- **dat_03:** verified (255 unique pairs, 0 duplicates)
- **dat_07:** complete (58 / 58)