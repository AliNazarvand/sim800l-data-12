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

---
<!-- v4-correction RunId=a06e3f11 -->

## D-V4-a06e3f11 (1405-07-21T07:50:37Z)

**Decision**: Roll back the v3 commit that accidentally committed conflict
markers and still-polluted reports; restore from the oldest clean revision
found via `git log --all`; refuse to commit while conflict markers remain.

**Rejected alternatives**:
- Committing with conflict markers (would corrupt data).
- Skipping verification (would leave user unaware).

**Follow-ups**:
- Manual intervention needed for: 0 report(s).
- 40 cross-ref issues still unresolved; require dedicated session.
---
<!-- v5-correction RunId=d31e1b30 -->

## D-V5-d31e1b30 (1405-07-21T07:53:27Z)

**Decision**: Move the ~188 AT-command-shaped
records out of `dat_02_urc.yaml` and into `reports/_archive/` (never
delete). These records were originally mislabeled as URCs by an early
extractor; their own `notes` fields already admitted the mistake with
the phrase "Suspected command syntax, not URC".

**Rationale**:
- R1/R6 forbid mislabeled data.
- R10 forbids deleting records without a trace; archiving preserves them.
- The 226 cross-ref issues reported by cross_ref.py were almost entirely
  caused by these false positives.

**Result**:
- dat_02 before: 206 records
- dat_02 after : 870 records
- Cross-ref issues now: 40

**Follow-ups**:
- Manually review the archive and decide, per record, whether the AT
  command belongs in `dat_01_at_command.yaml`.
- Populate dat_01 with legitimate commands to move its status from
  `partial` to `complete`.
---
<!-- v6-fix RunId=c6f60ee0 -->

## D-V6-c6f60ee0 (1405-07-21T07:56:20Z)

**Decision**: Correct the numeric errors introduced in v5's reports. The
underlying data change (removing 188 false positives from dat_02) was
correct, but the reported counts were wrong.

**Rationale**: R2 (no false data) and R19 (accurate reporting) require
that reports reflect reality. The v5 error was a display bug in
`Split-Dat02FalsePositives`: it counted list-items (lines) instead of
YAML records.

**Correct values**:
- dat_02 records after v5 cleanup: **18**
- False positives archived: **188**
---
<!-- v7-correction RunId=2beb359b -->

## D-V7-2beb359b (1405-07-21T07:58:37Z)

**Decision**: Replace scripts/cross_ref.py with a version that normalizes
AT command names before comparison, and repair the COVERAGE_MATRIX
dat_02 row and the archive header that v5/v6 failed to fix.

**Rationale**:
- The old cross_ref.py compared strings verbatim ("AT+CNMI" vs "+CNMI"),
  producing 40 false "not found" issues.
- COVERAGE_MATRIX still advertised dat_02 as "complete" with 206 records
  even though the actual file has 18 records.
- The archive header still claimed "7867 records" (line count, not record count).

**Result**:
- cross-ref issues : 40 -> 0
- dat_02 row       : "complete | 206" -> "partial | 18"
- archive header   : "7867" -> "188"

**Backup**: scripts/cross_ref.py.v7-backup (preserved for audit)
---
<!-- v8-cleanup RunId=146ab552 -->

## D-V8-146ab552 (1405-07-21T08:00:31Z)

**Decision**: Regenerate `CROSS_REF_REPORT.md` from scratch (with a
backup of the old body) so the file is internally consistent. The old
body still showed 40 issues while the v7 note at the bottom showed 0.

**Rationale**:
- R20 forbids contradictory numbers across a single report.
- The 40-issue listing was a false positive from the pre-v7
  `cross_ref.py` (raw string comparison).
- No data change was needed; only the report body was stale.

**Actions**:
- Backed up `CROSS_REF_REPORT.md` to `CROSS_REF_REPORT.md.v8-backup`.
- Rewrote the file with the real cross_ref.py output.
- Fixed the v7 SESSION_LOG branch field.