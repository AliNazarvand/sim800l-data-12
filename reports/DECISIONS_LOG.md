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