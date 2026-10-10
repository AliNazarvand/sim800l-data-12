# Coverage Final — Single Source of Truth

**Generated:** 2026-10-10
**Authoritative on:** dataset status, coverage estimate, blocker reason
**Validator:** `scripts/validate.py` (canonical, 0 errors)
**Rule applied:** R12 (complete requires coverage >= 95% or coverage_estimate=high)

## Summary

| Category    | Count | Datasets                                                    |
|-------------|-------|-------------------------------------------------------------|
| Complete    | 3     | dat_04, dat_06, dat_15                                      |
| Partial     | 2     | dat_05, dat_07                                              |
| Blocked     | 11    | dat_01, 02, 03, 08, 09, 10, 11, 12, 13, 17, 18              |
| Deferred    | 2     | dat_14, dat_16                                              |
| **Total**   | **18**|                                                             |

## Per-Dataset Detail

| ID     | Name                     | Status    | Coverage | Source        | Reason if blocked/deferred       |
|--------|--------------------------|-----------|----------|---------------|----------------------------------|
| dat_01 | AT Command DB            | blocked   | -        | -             | AT Command Manual missing        |
| dat_02 | URC DB                   | blocked   | -        | -             | Depends on dat_01                |
| dat_03 | Error Code DB (CME/CMS)  | blocked   | -        | -             | Depends on dat_01                |
| dat_04 | Timing & Timeout         | complete  | 95%      | V1.00 + V2.02 | -                                |
| dat_05 | State Machine            | partial   | 80%      | V2.02         | Ring/CSD FAX states missing      |
| dat_06 | Init Sequence            | complete  | 100%     | V2.02         | -                                |
| dat_07 | Hardware Reference       | partial   | 70%      | V2.02         | Moisture sensitivity missing     |
| dat_08 | Firmware Compatibility   | blocked   | -        | -             | Release Notes missing            |
| dat_09 | SMS DB                   | blocked   | -        | -             | Depends on dat_01                |
| dat_10 | GPRS/Data DB             | blocked   | -        | -             | Depends on dat_01                |
| dat_11 | HTTP/FTP/SSL DB          | blocked   | -        | -             | Depends on dat_01                |
| dat_12 | Audio DB                 | blocked   | -        | -             | Depends on dat_01                |
| dat_13 | SIM Management DB        | blocked   | -        | -             | Depends on dat_01                |
| dat_14 | Operator/APN (MCC/MNC)   | deferred  | -        | -             | Optional; external source needed |
| dat_15 | Power Management         | complete  | 95%      | V1.00 + V2.02 | -                                |
| dat_16 | Board/EVB Definitions    | deferred  | -        | -             | EVB schematic missing            |
| dat_17 | Certificate/Key Store    | blocked   | -        | -             | Depends on dat_01                |
| dat_18 | Certification Data       | blocked   | -        | -             | Official certificates missing    |

## Source Files Used

- `SIM800L_Hardware_Design_V1.00.pdf` (2013-08-20)
- `SIM800H&SIM800L_Hardware_Design_V2.02.PDF` (2015-07-27)

## References

- `DECISIONS_LOG.md` — authoritative decision history
- `reports/COVERAGE_REALITY.md` — detailed per-dataset analysis
- `reports/VALIDATION_CANONICAL.md` — validator policy
- `TODO.md` — blockers and next steps

## History

- **Session 12** — dat_04 complete (95%), dat_06 complete (autobaud added)
- **Session 11** — dat_15 complete (95%)
- **Session 15 (C2)** — Alignment pass (status sync)
- **Session 16 (C3)** — dat_06 restored to `complete`; coverage_pct synced
