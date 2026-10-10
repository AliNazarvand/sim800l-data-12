# Coverage Matrix — SIM800L-Data

**Last updated:** 2026-10-10
**Authoritative source:** `reports/COVERAGE_FINAL.md`
**Canonical validator:** `scripts/validate.py` (0 errors)

## Summary

| Category    | Count | Datasets                                                    |
|-------------|-------|-------------------------------------------------------------|
| Complete    | 2     | dat_04, dat_15                                              |
| Partial     | 3     | dat_05, dat_06, dat_07                                      |
| Blocked     | 11    | dat_01, 02, 03, 08, 09, 10, 11, 12, 13, 17, 18              |
| Deferred    | 2     | dat_14, dat_16                                              |
| **Total**   | **18**|                                                             |

## Per-Dataset Matrix

| Dataset | Name                     | Status    | Coverage | Source        | Reason              |
|---------|--------------------------|-----------|----------|---------------|---------------------|
| dat_01  | AT Command DB            | blocked   | -        | -             | AT Manual missing   |
| dat_02  | URC DB                   | blocked   | -        | -             | Depends on dat_01   |
| dat_03  | Error Code DB (CME/CMS)  | blocked   | -        | -             | Depends on dat_01   |
| dat_04  | Timing & Timeout         | complete  | 95%      | V1.00 + V2.02 | -                   |
| dat_05  | State Machine            | partial   | 80%      | V2.02         | Ring/CSD not modeled|
| dat_06  | Init Sequence            | partial   | 83%      | V2.02         | Autobaud step       |
| dat_07  | Hardware Reference       | partial   | 70%      | V2.02         | RF/ESD/AbsMax       |
| dat_08  | Firmware Compatibility   | blocked   | -        | -             | Release Notes       |
| dat_09  | SMS DB                   | blocked   | -        | -             | Depends on dat_01   |
| dat_10  | GPRS/Data DB             | blocked   | -        | -             | Depends on dat_01   |
| dat_11  | HTTP/FTP/SSL DB          | blocked   | -        | -             | Depends on dat_01   |
| dat_12  | Audio DB                 | blocked   | -        | -             | Depends on dat_01   |
| dat_13  | SIM Management DB        | blocked   | -        | -             | Depends on dat_01   |
| dat_14  | Operator/APN (MCC/MNC)   | deferred  | -        | -             | Optional            |
| dat_15  | Power Management         | complete  | 95%      | V1.00 + V2.02 | -                   |
| dat_16  | Board/EVB Definitions    | deferred  | -        | -             | EVB schematic       |
| dat_17  | Certificate/Key Store    | blocked   | -        | -             | Depends on dat_01   |
| dat_18  | Certification Data       | blocked   | -        | -             | Official certs      |

## Coverage Methodology

Coverage measured by **manual comparison** of data records against source
PDF tables, not by regex matching (previous regex approach failed — see
`reports/COVERAGE_REALITY.md`).

Complete requires: coverage >= 95% OR `coverage_estimate: high` (per R12).

## Blocker Summary

**Critical blocker:** SIM800 Series AT Command Manual is not available.
This blocks 9 datasets (dat_01, 02, 03, 09, 10, 11, 12, 13, 17).

**Secondary blockers:**
- Firmware Release Notes → dat_08
- CE/FCC/GCF certificates → dat_18
- EVB schematic → dat_16

See `TODO.md` for the full list.
