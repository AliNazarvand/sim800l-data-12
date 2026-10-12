# Prompt Compliance Checklist -- sim800l-data

_Last updated: 2026-10-12_

This document maps the project state to prompt requirements (R1..R24).

## Fundamental Rules

| Rule | Requirement | Status |
|------|-------------|--------|
| R1  | Only SIM800L data | PASS (validate.py enforces applicable_models contains SIM800L) |
| R2  | Every record has a source | PASS (validate.py L2 checks source presence) |
| R3  | No data -> status unknown, null, recorded in TODO | PASS (see reports/TODO.md) |
| R4  | Inferred data: confidence <= 0.5 | PASS (none currently inferred) |
| R5  | Secondary source: confidence <= 0.7 | PASS (none currently secondary) |
| R6  | No synthetic data (except dat_14 external) | PASS (validate.py L4 blocks synthetic) |
| R7  | V2.02 > V1.00 precedence | PASS (documented in DECISIONS_LOG D-001) |
| R8  | Valid YAML, UTF-8, no tabs | PASS (validate.py runs cleanly) |
| R9  | Backup + feature branch before changes | PASS (backups in sim800l-data-backups/) |
| R10 | Merge rules: don't delete existing records | PASS (v5..v11 preserve data) |
| R11 | Missing source -> dataset blocked, not partial | PASS (dat_08=blocked, dat_18=blocked) |
| R12 | Coverage >= 95% or coverage_estimate: high | PARTIAL (records present; formal coverage % not computed) |
| R13 | Every technical decision in DECISIONS_LOG | PASS (D-001..D-010 documented) |
| R14 | Deadlock criteria -> stop, ask owner | PASS (documented for dat_08/16/18) |
| R15 | Schema before data | PASS (all 18 schemas exist) |
| R16 | Session log summary each session | PASS (Session 2..10 logged; 7 as gap-note) |
| R17 | All YAML schema-valid | PASS (validate.py PASSED) |
| R18 | Reproducible scripts | PASS (extract_pdf, validate, cross_ref, ocr_pdf, diagnose_sources) |
| R19 | ISO 8601 timestamps | PASS (InvariantCulture everywhere) |
| R20 | No contradictory data across datasets | PASS (cross-ref strict=0) |
| R21 | example-only records forbidden in data/ | PASS (validate.py L4 blocks them) |
| R22 | WIP Limit = 1; no in-progress in matrix | PASS (no in-progress in COVERAGE_MATRIX) |
| R23 | Vertical slice: schema->data->report->validation->cross-ref->commit | PASS |
| R24 | Clustering with dependency graph | PASS (ROLE_MAP.md documents all dependencies) |

## Dataset Status Summary

- **Partial:** 15 (data present, verification pending)
- **Blocked:** 2 (source document missing: dat_08, dat_18)
- **Deferred:** 1 (optional/external: dat_16)
- **Complete:** 0 (none reached 95% coverage)

## Real vs Documented Records

- **Real records:** 1128
- **Documented placeholders:** 3 (dat_08, dat_16, dat_18)

## Cross-Reference

- **Strict issues:** 0
- **Soft issues:** 0

## Schema Validation

- **validate.py:** PASSED

## Required Files

All 81 required files present.

## Remaining Work (Manual, not script)

- [ ] Run `python scripts/diagnose_sources.py` to inspect source formats.
- [ ] Manually verify records in dat_01/02/03/07 against source PDFs.
- [ ] Decide about documented placeholders in dat_08/16/18.
- [ ] Expand dat_07 (currently 56 pins; target ~88).
- [ ] Check dat_02 (206 URC) and dat_03 (255 errors) for duplicates.