# Data Integrity Report -- sim800l-data

_Last updated: 2026-10-12 (aligned with v13 audit)_

> This report reflects the READ-ONLY audit output from
> `scripts/audit_data_integrity.py`. It supersedes the earlier
> pessimistic version which incorrectly flagged dat_01 and dat_03.

## Verified Clean (no action needed)

### dat_01 -- AT Command: **PASS**

| Metric | Value |
|--------|-------|
| Total records | 334 |
| Commands with `AT+` prefix | 0 |
| Commands with `+` prefix | **334** |
| Commands without prefix | **0** |

**Conclusion:** Command format is correct. No fix needed.

### dat_03 -- Error Code: **PASS**

| Metric | Value |
|--------|-------|
| Total records | 255 |
| Unique `(error_type, code)` pairs | **255** |
| Duplicates (>1 occurrence) | **0** |

**Conclusion:** No deduplication needed.

## Known Issues (require manual work)

### dat_02 -- URC: **188 of 206 self-flagged**

The audit found 188 records whose `notes` field contains
`Suspected command syntax, not URC` (or similar). Example:

```yaml
- id: dat_02_0001
  urc_string: +CAAS                             # <-- this is an AT command
  trigger_event: event code (indicating        # <-- truncated sentence
  notes: Suspected command syntax, not URC. Needs manual verification.
```

Also, **39 records** have possibly-truncated `trigger_event` fields.

**Action required:** Each of the 188 records must be checked against
the AT Command Manual. Real URCs live in a specific section (typically
`+CMTI`, `+CMT`, `RING`, `NO CARRIER`, `+CUSD`, `+CREG`,
`+CPIN`, `+PDP DEACT`, etc.). If a record is actually an AT command,
it belongs in `dat_01_at_command.yaml`, not here.

### dat_07 -- Hardware: **56 of ~88 pins (63.6%)**

| Metric | Value |
|--------|-------|
| Extracted | 56 pins |
| Expected (V2.02) | ~88 pins |
| Missing | ~32 pins |
| Coverage | 63.6% |

**Action required:** Open `SIM800H&SIM800L_Hardware_Design_V2.02.PDF`
page 16 (Pin Description table) and add missing pin records.

## Verified Status Summary

| Dataset | Status | Coverage | Action |
|---------|--------|----------|--------|
| dat_01 | **PASS** | 334/334 | None (verified clean) |
| dat_02 | ISSUE | 18/206 clean | Review 188 flagged records |
| dat_03 | **PASS** | 255/255 | None (no duplicates) |
| dat_07 | PARTIAL | 56/88 | Add ~32 missing pins |

## Work Estimates

- **dat_02 cleanup:** 2-3 hours (read AT manual URC section, reclassify)
- **dat_07 expansion:** 1-2 hours (read pin table on page 16)
- **Total remaining work:** ~4 hours of focused manual effort

## Verdict

- **Infrastructure:** 100% complete
- **Data (dat_01, dat_03):** VERIFIED CLEAN
- **Data (dat_02, dat_07):** require MANUAL work
- **Ready for downstream (sim800l-driver):** NOT YET

See `MANUAL_VERIFICATION_CHECKLIST.md` for the practical plan.