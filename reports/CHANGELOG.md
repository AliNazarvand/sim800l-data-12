# CHANGELOG

## v1.0.0-phase1 — 1405-07-19T17:49:49Z
Phase 1 complete. Production-ready dataset.

### Coverage
- complete: 9
- partial (with limit_reason): 5
- blocked: 3
- deferred: 1
- L3: 0

### D12 changes
- Fixed whitelist insertion point (8 new commands at correct location in validate.py)
- 7 partial datasets marked with explicit limit_reason
- README with Source Limits table
- PHASE_1_REPORT with Known Limits section
- DECISIONS_LOG D-040
- TODO split into Source-Missing and Source-Limited
- Phase 2 scaffolding: sim800l-tools structure, generators, CI config
- PHASE_1_FINAL_TABLE v6 with limit_reason column

### Earlier
- D11: 16/25 OK, batch operations
- D10: section-body params extraction
- D9: else bug fix, dat_01 params 16 -> 271
- D8: depth enrichment
- D7: strict_depth metric
- D5/D6: per-dataset gates
- A1-A4, B1-B3: hardware and AT command datasets
- Step 1: infra cleanup