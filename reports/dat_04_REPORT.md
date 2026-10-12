# dat_04 REPORT — Timing & Timeout

- status: partial
- coverage: medium
- records_total: 29
- records_active: 6
- records_legacy: 23
- generated: 2026-10-12T03:00:00Z

## Active timing parameters

| # | id | parameter | min | typ | max | unit | page | line |
|---|---|---|---|---|---|---|---|---|
| 1 | dat_04_0014 | Power-on PWRKEY pull-down time | 1000 | - | - | ms | 22 | L662 |
| 2 | dat_04_0015 | Power-down PWRKEY pull-down time | 1000 | - | - | ms | 23 | L701 |
| 3 | dat_04_0016 | Restart wait after STATUS low | 800 | - | - | ms | 24 | L758 |
| 4 | dat_04_0017 | RESET pin low power time | - | 105 | - | ms | 26 | L782 |
| 5 | dat_04_0010 | DRX cycle in idle mode (not registered) | 64 | - | - | ms | 49 | - |
| 6 | dat_04_0012 | DRX cycle in idle mode (registered) | 64 | - | - | ms | 49 | - |

Notes:
- Records 0014..0017 are newly extracted from V2.02 body text.
- Records 0010 and 0012 are salvaged from malformed legacy records;
  their source.page was corrected to 49, parameter was renamed to
  "DRX cycle in idle mode", and min value was set to 64.

## Out of scope (belong to other datasets)

- RESET pin VIH min 2.4V, VIL max 0.6V -> dat_07 (Hardware)
- Current consumption at CFUN 0/1/4 (0.83 / 1.04 / 0.92 mA) -> dat_15 (Power)
- Under/over-voltage thresholds -> dat_15 (Power)
- Temperature thresholds -> dat_15 (Power)
- DTR pull-down wake time ~50ms -> dat_05 (State Machine)
- Sleep Mode 2 entry (no RXD data for 5s) -> dat_05 (State Machine)

## Limitations

- Figures 12, 13, 14, 16 contain precise min/typ/max timing tables,
  but the values are rasterized images and are not present in the
  extracted text.
- OCR of pages 22-27 (V2.02) is required for full extraction.
- Coverage is "medium" (not "high") because exact typ/max values are
  missing.
- Dataset remains "partial" until OCR is performed.

## History

- 2026-10-12: Previous file contained a YAML anchor (&id001) reused by
  11 records, plus records out of dat_04 scope (VBUS voltage, SIM speed,
  current consumption, bibliography). File was archived to
  reports/_archive/dat_04_legacy_<timestamp>.yaml and rewritten.
- See DECISIONS_LOG.md entry D-043 for full rationale.