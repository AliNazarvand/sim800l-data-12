# sim800l-data

Structured, sourced, reproducible dataset for SIM800L.

## Validation
- L1 (Schema): 0
- L2 (Business): 0
- L3 (Cross-ref): 8
- L4 (Consistency): 0

## Coverage Summary (production criteria)
- complete: 9
- partial: 5
- blocked: 3
- deferred: 1

## Definitions
- complete: all records sourced AND params_pct >= 50%.
- params_pct: share of records with primary depth field (parameters/recovery_steps/value_typ/related_commands/function).
- partial: sourced but params_pct < 50%.

## Reports
- reports/COVERAGE_MATRIX.md
- reports/DECISIONS_LOG.md
- reports/SESSION_LOG.md
- reports/PHASE_1_REPORT.md