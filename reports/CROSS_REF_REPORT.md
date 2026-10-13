# CROSS_REF_REPORT

Generated: 2026-10-13T04:32:50Z  (previous Jalali timestamp removed in v9)
RunId: 33d34357

## Summary

- cross_ref.py issues: **0**

## cross_ref.py raw output

```text
Cross-ref: 0 issues, 334 commands in dat_01

## Stats
- dat_01 commands: 334
- dat_02 URCs: 18
- dat_09 SMS: 14
- dat_13 SIM: 10

```

## Notes

- All referenced URCs (dat_02), SMS commands (dat_09), and SIM commands
  (dat_13) are present in dat_01_at_command.yaml after normalization
  (leading `AT` and `+` are stripped before comparison).
- The previous 40-issue listing was a false positive caused by raw
  string comparison in the pre-v7 version of `cross_ref.py`.
- The old report body is preserved at `CROSS_REF_REPORT.md.v8-backup`
  for audit trail.

## Follow-ups

- dat_01_at_command.yaml remains `partial`: it currently has 334
  commands, and full coverage of the SIM800 Series AT Command Manual
  V1.01 (which is on disk under `sources/originals/`) requires
  extracting the remaining commands. That is a separate work session
  (WIP=1, cluster A closure).