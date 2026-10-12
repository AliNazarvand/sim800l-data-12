# Data Integrity Report -- sim800l-data

_Last updated: 2026-10-12_

> **IMPORTANT:** This report documents **known data-integrity issues**
> discovered after running `diagnose_sources.py` and `audit_data_integrity.py`.
>
> The 1128 records in `data/*.yaml` have been **counted** but **NOT**
> manually verified against the source PDFs. The issues below are
> structural / self-admitted, not exhaustive.

## Findings from diagnose_sources.py

### Finding 1: `_at_commands_index.json` is DERIVED, not a source

- Its keys are command names; values are `dat_01_NNNN` IDs.
- Total keys (335) matches total records in dat_01 (334 + 1).
- Therefore, this JSON **cannot** be used to re-extract dat_01.
- The real source is `sources/extracted/at_v1_01_full.txt`.

### Finding 2: `dat_02` contains AT commands mislabeled as URC

Example record (`dat_02_0001`):

```yaml
- id: dat_02_0001
  urc_string: +CAAS          # <-- this is an AT command, not a URC
  trigger_event: event code (indicating   # <-- truncated sentence
  notes: Suspected command syntax, not URC. Needs manual verification.
```

The record **self-admits** the problem in its `notes` field.

### Finding 3: `dat_07` has fewer pins than expected

- Extracted: 56 pins
- Expected (V2.02): ~88 pins
- Missing: ~32 pins

## Audit Output

```
=== DATA INTEGRITY AUDIT (read-only) ===
ROOT: D:\Project\Electronic Project\Control Board SMS 2\Documents\New folder (2)\New 2\Datasheet\01 - sim800l-data\021

=== dat_01 AT Command Audit ===
  Total records: 334
  Commands with 'AT+' prefix : 0
  Commands with '+' prefix   : 334
  Commands WITHOUT any prefix: 0

=== dat_02 URC Audit ===
  Total records: 206
  Self-marked as 'Suspected' : 188
  Possibly truncated triggers: 39
  Sample suspected IDs       : ['dat_02_0001', 'dat_02_0002', 'dat_02_0003', 'dat_02_0004', 'dat_02_0005']

=== dat_03 Error Code Audit ===
  Total records: 255
  Unique (error_type, code): 255
  Duplicates (>1 occurrence): 0

=== dat_07 Hardware Pin Audit ===
  Total records: 56
  Expected (approx): 88
  Coverage (approx): 63.6%
  Unique pin names: 56

=== SUMMARY ===
  dat_01: 0 of 334 (0.0%) lack '+' prefix
  dat_02: 188 records self-marked as suspected
  dat_03: 0 duplicate (error_type, code) pairs
  dat_07: 56 pins (63.6% of ~88)

  NO data files were modified.
  See reports/DATA_INTEGRITY_REPORT.md for details.
```

## Why v13 does NOT fix these issues

A PowerShell script **cannot** fix data that requires reading the PDF:

1. **dat_01 format**: To determine whether `GCAP` should be `+GCAP`,
   a human must look at the AT Command Manual PDF.
2. **dat_02 mislabel**: To separate URCs from AT commands, someone must
   read the URC section of the manual and cross-reference with dat_01.
3. **dat_07 coverage**: To add the missing ~32 pins, someone must read
   the Pin Description table on page 16 of the hardware design.
4. **dat_03 duplicates**: To remove duplicates, someone must decide
   which error code is canonical.

## Recommended Next Steps

See `MANUAL_VERIFICATION_CHECKLIST.md` for a step-by-step guide.

## Verdict

- **Infrastructure:** Complete
- **Data integrity:** NOT VERIFIED
- **Format correctness (dat_01):** TO BE DETERMINED (see audit output above)
- **Content correctness (dat_02):** KNOWN ISSUES
- **Coverage (dat_07):** PARTIAL

**Conclusion:** The project is ready for **manual verification**, not
for blind downstream use. Do NOT propagate to `sim800l-driver`
without first verifying records against the source PDFs.