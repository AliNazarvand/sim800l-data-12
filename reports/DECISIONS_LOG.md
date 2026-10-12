# Decisions Log -- sim800l-data

## D-001: Source Priority

- **Decision:** V2.02 hardware design takes precedence over V1.00.
- **Rationale:** Newer revision, supersedes older content.
- **Rejected alternatives:** Treating both as equal; using V1.00 as primary.
- **Date:** 2025-01-01

## D-002: Dataset Status Model

- **Decision:** Every dataset must be closed as complete | partial | blocked | deferred.
- **Rationale:** No in-progress datasets allowed at end of session (WIP Limit = 1).
- **Rejected alternatives:** Allowing pending/in-progress in final matrix.
- **Date:** 2025-01-01

## D-003: AT Command Manual Availability

- **Decision:** Treat `SIM800 Series_AT Command Manual_V1.01` as AVAILABLE.
- **Rationale:** PDF and extracted text both present under `sources/`.
- **Rejected alternatives:** Marking dat_01 as blocked (was incorrect).
- **Date:** 2025-01-01

## D-004: External Data for dat_14

- **Decision:** dat_14 is optional and may remain deferred unless owner explicitly requests.
- **Rationale:** Requires external sources (GSMA/ITU/mcc-mnc.com) with confidence <= 0.7.
- **Rejected alternatives:** Fabricating APN data; skipping without documenting.
- **Date:** 2025-01-01

## D-005: Preserve Historical Reports

- **Decision:** PHASE_*_REPORT.md, _v8/_v9/_v10_FINAL_REPORT.md, and analysis reports are preserved.
- **Rationale:** Contain valuable historical context; required by prompt.
- **Rejected alternatives:** Deleting them as part of cleanup.
- **Date:** 2025-01-01

## D-006: Schema per Dataset

- **Decision:** Each of the 18 datasets has its own schema with dataset-specific fields.
- **Rationale:** Business logic validation requires specific fields (R15).
- **Rejected alternatives:** Single generic schema for all datasets.
- **Date:** 2025-01-01
## D-007: Legacy Backups Preserved (2026-10-12)

- **Decision:** Backups named `_backup-1405*` (Jalali dates) are preserved.
- **Rationale:** First backup contains the authoritative dat_01 (334 records)
  and dat_07 (56 records) that were restored in v5.
- **Rejected alternatives:** Deleting them; renaming them (would break traceability).
- **Date:** 2026-10-12

## D-008: Real vs Placeholder Record Counting (2026-10-12)

- **Decision:** Records without a valid `source.name` and `source_type`
  are counted as **placeholders**, not real records.
- **Rationale:** Ensures `blocked`/`deferred`/`partial` status reflects
  actual data presence, not the presence of template stubs.
- **Rejected alternatives:** Counting all `- id:` occurrences (caused
  dat_08/16/18 to appear partial when only placeholders existed).
- **Date:** 2026-10-12

## D-009: Reports Derived From Single Status Source (2026-10-12)

- **Decision:** GAP_REPORT, TODO, COVERAGE_MATRIX, and _session_state are all
  derived from one `System.Collections.Hashtable` object.
- **Rationale:** Fixed v5 inconsistency where GAP_REPORT said dat_14=deferred
  but COVERAGE_MATRIX said dat_14=partial.
- **Rejected alternatives:** Hardcoding statuses in each report.
- **Date:** 2026-10-12

## D-010: SESSION_LOG Jalali Dates Converted (2026-10-12)

- **Decision:** Any Jalali (1405-*) date in SESSION_LOG is converted to the
  Gregorian equivalent with a `(Jalali->Gregorian)` annotation.
- **Rationale:** R19 requires ISO 8601 for all dates.
- **Rejected alternatives:** Leaving them as-is (violates R19).
- **Date:** 2026-10-12
