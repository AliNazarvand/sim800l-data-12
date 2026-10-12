# Prompt Compliance Checklist -- sim800l-data

_Last updated: 2026-10-12 (post-audit, v14)_

> **STATUS:** Corrective scripts are finished. Data verification is
> complete for dat_01 and dat_03. dat_02 and dat_07 require manual work.

## Data Verification Status (single source of truth)

| Dataset | Verified | Detail |
|---------|----------|--------|
| dat_01  | **PASS** | 334/334 commands have `+` prefix |
| dat_02  | **ISSUE** | 188/206 self-flagged as suspected |
| dat_03  | **PASS** | 255/255 unique, 0 duplicates |
| dat_04  | UNCHECKED | Cross-ref OK; not manually verified |
| dat_05  | UNCHECKED | Cross-ref OK; not manually verified |
| dat_06  | UNCHECKED | Cross-ref OK; not manually verified |
| dat_07  | **PARTIAL** | 56 of ~88 pins (63.6%) |
| dat_08  | BLOCKED | Source (FW Release Notes) missing |
| dat_09  | UNCHECKED | Cross-ref OK; not manually verified |
| dat_10  | UNCHECKED | Cross-ref OK; not manually verified |
| dat_11  | UNCHECKED | Cross-ref OK; not manually verified |
| dat_12  | UNCHECKED | Cross-ref OK; not manually verified |
| dat_13  | UNCHECKED | Cross-ref OK; not manually verified |
| dat_14  | UNCHECKED | External source (mcc-mnc.com); not verified |
| dat_15  | UNCHECKED | Cross-ref OK; not manually verified |
| dat_16  | DEFERRED | Source (EVB schematic) missing |
| dat_17  | UNCHECKED | Cross-ref OK; not manually verified |
| dat_18  | BLOCKED | Source (Cert documents) missing |

## Fundamental Rules (R1..R24)

| Rule | Requirement | Status |
|------|-------------|--------|
| R1  | Only SIM800L data | PASS (validate.py enforces) |
| R2  | Every record has a source | PASS (validate.py L2) |
| R3  | No data -> unknown/null/TODO | PASS (dat_08/16/18) |
| R4  | Inferred: confidence <= 0.5 | PASS (none inferred) |
| R5  | Secondary: confidence <= 0.7 | PASS (none secondary) |
| R6  | No synthetic data | PASS (validate.py L4) |
| R7  | V2.02 > V1.00 | PASS (D-001) |
| R8  | Valid YAML, UTF-8 | PASS |
| R9  | Backup before changes | PASS |
| R10 | Don't delete existing records | PASS (v5..v14) |
| R11 | Missing source -> blocked | PASS (dat_08, dat_18) |
| R12 | Coverage >= 95% or high | PARTIAL (see per-dataset table above) |
| R13 | Decisions in DECISIONS_LOG | PASS (D-001..D-010) |
| R14 | Deadlock -> ask owner | PASS (documented) |
| R15 | Schema before data | PASS |
| R16 | Session log each session | PASS (Session 2..14) |
| R17 | All YAML schema-valid | PASS (validate.py) |
| R18 | Reproducible scripts | PASS |
| R19 | ISO 8601 timestamps | PASS (InvariantCulture) |
| R20 | No contradictions | PASS (cross-ref strict=0) |
| R21 | No `example-only` in data/ | PASS |
| R22 | WIP Limit = 1, no in-progress | PASS |
| R23 | Vertical slice | PASS |
| R24 | Clustering with dependency graph | PASS (ROLE_MAP) |

## Overall Summary

- **Infrastructure:** 100% complete
- **Data verified:** 2 of 18 datasets (dat_01, dat_03)
- **Data partial:** 1 (dat_07)
- **Data issue:** 1 (dat_02)
- **Data unchecked:** 11
- **Data blocked/deferred:** 3 (dat_08, dat_16, dat_18)

## Remaining Manual Work

See `MANUAL_VERIFICATION_CHECKLIST.md`.

## Closure

All 14 corrective scripts (v1..v14) are finished.
No further corrective scripts will be produced.
All remaining work is manual and requires the source PDFs.