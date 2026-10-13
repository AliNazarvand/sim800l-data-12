# TODO.md

Generated: 2026-10-12T11:29:52Z

## Missing sources

- [ ] SIM800 Series TCP/IP AT Command Manual  (needed by: dat_10)
- [ ] SIM800 Series HTTP AT Command Manual  (needed by: dat_11)
- [ ] SIM800 Series FTP AT Command Manual  (needed by: dat_11)
- [ ] SIM800 Series SSL AT Command Manual  (needed by: dat_11, dat_17)
- [ ] SIM800 Series Audio AT Command Manual  (needed by: dat_12)
- [ ] SIM800 Series SIM AT Command Manual  (needed by: dat_13)
- [ ] SIM800L Datasheet  (needed by: dat_07)
- [ ] SIM800 Series Sleep Mode Application Note  (needed by: dat_15)
- [ ] SIM800 Series URC Application Note  (needed by: dat_02)
- [ ] SIM800 Series Firmware Release Notes  (needed by: dat_08)
- [ ] SIM800 Series Certification Documents  (needed by: dat_18)
- [ ] GSMA / ITU / mcc-mnc.com  (needed by: dat_14)

## Blocked / deferred datasets
- [ ] dat_08 - blocked
- [x] dat_11 - complete (per COVERAGE_MATRIX; corrected in v14)
- [ ] dat_14 - deferred
- [ ] dat_15 - blocked
- [ ] dat_16 - blocked (per COVERAGE_MATRIX; corrected in v14)
- [ ] dat_17 - blocked
- [ ] dat_18 - blocked

## Follow-ups
- [ ] Fix scripts/extract_pdf.py --input argument (D-067)
- [ ] Translate D-001..D-041 in DECISIONS_LOG.md to English
- [ ] Manually review parser output if dat_01 still partial


---
<!-- v12-blocked-datasets -->

## v12 Blocked Datasets -- Required Resources (2026-10-13T04:44:33Z)

| Dataset | Missing source | Suggested official source |
|---|---|---|
| dat_08 | Firmware Release Notes | https://www.simcom.com/ (Products) |
| dat_15 | Sleep Mode Application Note | https://www.simcom.com/ (App Notes) |
| dat_16 | EVB Schematic / BOM | https://www.simcom.com/ (EVB Docs) |
| dat_17 | SSL AT Command Manual | https://www.simcom.com/ (AT Manuals) |
| dat_18 | Certification (CE, FCC, GCF, PTCRB, RoHS, IC, TA, RCM) | CE: https://ec.europa.eu/ ; FCC: https://fcc.gov/oet/ea/fccid ; GCF: https://www.gcfcertification.org/ ; PTCRB: https://www.ptcrb.com/ |

Per R11: these remain blocked until the official source is on disk.
Per R14: no synthetic data is permitted as a substitute.