# TODO -- sim800l-data

_Last updated: 2026-10-12_

## Immediate
- [ ] Run `python scripts/diagnose_sources.py` to inspect source file formats
      (_at_commands_index.json, hw_v2_02_full.txt).
- [ ] Inspect existing extraction scripts and reuse if compatible:
      - scripts/_rebuild_B1_dat01.py
      - scripts/_rebuild_dat07.py
      - scripts/extract_at_commands.py
      - scripts/extract_dat_07.py
- [ ] dat_01 currently has 334 records (target: full AT command set).
- [ ] dat_07 currently has 56 records (target: all hardware pins).

## Blocked (source missing)
- [ ] dat_08 -- needs SIM800 Series Firmware Release Notes
- [ ] dat_18 -- needs SIM800 Series Certification Documents

## Deferred (optional / external)
- [ ] dat_14 -- needs GSMA / ITU / mcc-mnc.com (optional)
- [ ] dat_16 -- needs SIM800L EVB schematic

## Verification
- [ ] Run `python scripts/validate.py`.
- [ ] Run `python scripts/cross_ref.py`.
- [ ] Spot-check records against source PDFs.