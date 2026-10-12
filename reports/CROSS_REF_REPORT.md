# Cross-Reference Report -- sim800l-data

_Last updated: 2026-10-12_

## Summary

- **Cross-reference issues:** 0
- **Severity:** warning (does not fail schema validation)
- **Normalization:** AT+X / +X / X / ATX=... treated as the same command.

## cross_ref.py output

```
Loaded 18 dataset file(s).
  Commands indexed (normalized) : 334
  States indexed                : 19
  Pins indexed                  : 56

Cross-reference check complete. Issues: 0
```

## Dataset dependency snapshot

| Dataset | Depends On | Status |
|---------|------------|--------|
| dat_01 | - | partial |
| dat_02 | dat_01 | partial |
| dat_03 | dat_01 | partial |
| dat_04 | V1.00 + V2.02 | partial |
| dat_05 | dat_04 | partial |
| dat_06 | dat_04 + dat_05 | partial |
| dat_07 | V1.00 + V2.02 | partial |
| dat_08 | Release Notes (missing) | blocked |
| dat_09 | dat_01 | partial |
| dat_10 | dat_01 | partial |
| dat_11 | dat_01 | partial |
| dat_12 | dat_01 | partial |
| dat_13 | dat_01 | partial |
| dat_14 | mcc-mnc.com (external) | partial |
| dat_15 | V1.00 + V2.02 | partial |
| dat_16 | EVB schematic (missing) | deferred |
| dat_17 | dat_01 + dat_11 | partial |
| dat_18 | Cert docs (missing) | blocked |