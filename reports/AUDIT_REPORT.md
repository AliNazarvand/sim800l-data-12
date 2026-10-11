# AUDIT_REPORT

Generated: 1405-07-19 23:24:18
Method: Git-first selective restore + backup fallback

## Recovery Summary

| Metric | Count |
|--------|-------|
| Restored | 1370 |
| Kept     | 18 |
| Skipped  | 0 |
| Failed   | 0 |
| Deleted  | 0 (policy) |

## Data Files

| File | Records | Size (B) | SHA256 (first 12) |
|------|---------|----------|-------------------|
| dat_01_at_command.yaml | 334 | 383429 | B7A4F891E2EC |
| dat_02_urc.yaml | 206 | 209246 | 8875CDC789D3 |
| dat_03_error_code.yaml | 255 | 174646 | 7E7A76C03A17 |
| dat_04_timing_timeout.yaml | 25 | 19980 | 965F8152A704 |
| dat_05_state_machine.yaml | 11 | 9515 | D31F11C3B146 |
| dat_06_init_sequence.yaml | 10 | 8033 | B53903D1F348 |
| dat_07_hardware_reference.yaml | 78 | 69982 | CFD93961673F |
| dat_08_firmware_compatibility.yaml | 1 | 410 | 56F39960538E |
| dat_09_sms.yaml | 14 | 19583 | DC0AD68725E2 |
| dat_10_gprs_data.yaml | 24 | 22182 | 07D696FBA766 |
| dat_11_http_ftp_ssl.yaml | 38 | 29512 | 7607F4D43A2A |
| dat_12_audio.yaml | 13 | 11649 | BD9D1EDB0D1A |
| dat_13_sim_management.yaml | 10 | 9517 | 05A853C60F65 |
| dat_14_operator_apn.yaml | 52 | 45610 | 6BF1CDCC6B73 |
| dat_15_power_management.yaml | 14 | 11204 | B5BC781A173B |
| dat_16_board_evb.yaml | 1 | 388 | DA1CA8833E10 |
| dat_17_certificate_key_store.yaml | 9 | 4578 | 64448B696B6D |
| dat_18_certification.yaml | 1 | 408 | 9ED77A777383 |

## Schemas

- dat_01.schema.yaml (877 B)
- dat_02.schema.yaml (877 B)
- dat_03.schema.yaml (877 B)
- dat_04.schema.yaml (877 B)
- dat_05.schema.yaml (877 B)
- dat_06.schema.yaml (877 B)
- dat_07.schema.yaml (877 B)
- dat_08.schema.yaml (877 B)
- dat_09.schema.yaml (877 B)
- dat_10.schema.yaml (877 B)
- dat_11.schema.yaml (877 B)
- dat_12.schema.yaml (877 B)
- dat_13.schema.yaml (877 B)
- dat_14.schema.yaml (877 B)
- dat_15.schema.yaml (877 B)
- dat_16.schema.yaml (877 B)
- dat_17.schema.yaml (877 B)
- dat_18.schema.yaml (877 B)

## Scripts

- _analyze_D2_L3.py (2594 B)
- _annotate_B4_040506.py (4783 B)
- _annotate_B6_0406.py (3869 B)
- _apply_B2B3_retry.py (8259 B)
- _audit_B2B3.py (2955 B)
- _build_cross_ref_report.py (2740 B)
- _build_D3_coverage.py (4136 B)
- _build_D4_coverage.py (3783 B)
- _build_D6_coverage.py (3754 B)
- _check_B2B3_dat01.py (1506 B)
- _check_B6_clusterC.py (1518 B)
- _check_D6_dat14.py (1116 B)
- _clean_D5_04_15.py (1856 B)
- _cleanup_B2B3.py (2605 B)
- _d10_build_sections.py (1576 B)
- _d10_s1_dat09.py (2376 B)
- _d10_s11_dat06.py (1882 B)
- _d10_s12_dat07.py (1467 B)
- _d10_s13_coverage.py (4576 B)
- _d10_s2_dat10.py (2301 B)
- _d10_s3_dat12.py (2279 B)
- _d10_s4_dat13.py (2269 B)
- _d10_s5_dat11.py (3647 B)
- _d10_s6_dat02.py (809 B)
- _d10_s7_dat05.py (1829 B)
- _d10_s8_dat03.py (4983 B)
- _d10_s9_dat04.py (3366 B)
- _d11_s1_dat15.py (3056 B)
- _d11_s10_dat02_urcs.py (2368 B)
- _d11_s11_dat05_tim.py (1759 B)
- _d11_s12_dat07_alt.py (1703 B)
- _d11_s13_dat09_ex.py (1399 B)
- _d11_s14_l3_analysis.py (845 B)
- _d11_s2_dat04.py (3245 B)
- _d11_s23_table.py (2905 B)
- _d11_s3_dat10.py (2182 B)
- _d11_s4_dat12.py (2170 B)
- _d11_s5_dat03.py (2508 B)
- _d11_s6_dat11.py (3352 B)
- _d11_s7_dat14.py (1479 B)
- _d11_s8_dat01_err.py (1344 B)
- _d11_s9_dat01_fw.py (1226 B)
- _d12_a3_confirm.py (513 B)
- _d12_b_apply_reason.py (1100 B)
- _d12_e26_table.py (3187 B)
- _d13_apply_reason.py (1665 B)
- _d13_verify_reasons.py (1102 B)
- _d6_generic_filler.py (4151 B)
- _d7_build_coverage.py (4627 B)
- _d7_fill_dat01_params.py (3446 B)
- _d7_fill_dat02.py (2326 B)
- _d7_fill_dat03.py (3243 B)
- _d7_fill_dat05.py (2169 B)
- _d7_finalize_blocked.py (2254 B)
- _d7_phase1_table.py (3244 B)
- _d8_s1_dat01_params.py (2311 B)
- _d8_s10_dat15_values.py (2283 B)
- _d8_s12_coverage.py (4166 B)
- _d8_s15_table.py (2829 B)
- _d8_s2_dat04_values.py (3676 B)
- _d8_s3_dat09.py (2147 B)
- _d8_s4_dat10.py (2084 B)
- _d8_s5_dat11.py (1602 B)
- _d8_s6_dat12.py (2079 B)
- _d8_s7_dat13_verify.py (825 B)
- _d8_s8_dat02_related.py (2915 B)
- _d8_s9_dat06.py (3520 B)
- _d9_s1_diagnose.py (2052 B)
- _d9_s2_parse_fix.py (2419 B)
- _d9_s3_dat01_params.py (3604 B)
- _d9_s4_coverage.py (4595 B)
- _dedup_B1_dat01.py (6044 B)
- _diagnose_A3.py (2445 B)
- _diagnose_B1.py (1855 B)
- _diagnose_dat14.py (1937 B)
- _diagnose_dat15.py (1496 B)
- _extend_D3_dat04_06.py (4737 B)
- _extend_D3_dat15.py (3914 B)
- _extract_at_manual.py (1595 B)
- _fill_D5_dat01_params.py (2299 B)
- _fill_D6_dat01_params.py (2190 B)
- _fix_D2_dat01.py (3484 B)
- _fix_D2_dat02.py (3697 B)
- _fix_D3_dat01.py (3806 B)
- _fix_D3_L3.py (2918 B)
- _fix_D5_dat03.py (3307 B)
- _fix_D5_dat07.py (3903 B)
- _fix_D5_dat11.py (1713 B)
- _fix_D5_dat12.py (1717 B)
- _fix_step1_dat14.py (2637 B)
- _fix_step1_data.py (2808 B)
- _fix_step1_dates.py (2556 B)
- _inspect_B2B3.py (2818 B)
- _parse_B2B3_retry.py (4196 B)
- _parse_B2B3.py (4867 B)
- _phase1_summary.py (2148 B)
- _reannotate_v202.py (3810 B)
- _rebuild_B1_dat01.py (7947 B)
- _rebuild_B2B3.py (9371 B)
- _rebuild_B4_dat09.py (6042 B)
- _rebuild_B4_dat13.py (5790 B)
- _rebuild_B6_dat10.py (6141 B)
- _rebuild_B6_dat11.py (5183 B)
- _rebuild_B6_dat12.py (4847 B)
- _rebuild_dat07.py (6307 B)
- _rebuild_dat15.py (8949 B)
- _scan_A3_structures.py (5486 B)
- _scan_B1_at_manual.py (5596 B)
- _scan_B2B3_sections.py (2021 B)
- _scan_B6_dat17.py (1906 B)
- _status_all.py (849 B)
- _verify_D4_dat01.py (2655 B)
- cross_ref.py (2321 B)
- extract_at_commands.py (6111 B)
- extract_dat_07.py (10572 B)
- extract_pdf.py (2653 B)
- ocr_pdf.py (952 B)
- validate.py (12435 B)

## Reports

- CHANGELOG.md
- CLEANUP_V6_REPORT.md
- CLEANUP_V7_REPORT.md
- COVERAGE_MATRIX.md
- CROSS_REF_REPORT.md
- dat_01_REPORT.md
- dat_02_REPORT.md
- dat_03_REPORT.md
- dat_04_REPORT.md
- dat_05_REPORT.md
- dat_06_REPORT.md
- dat_07_REPORT.md
- dat_08_REPORT.md
- dat_09_REPORT.md
- dat_10_REPORT.md
- dat_11_REPORT.md
- dat_12_REPORT.md
- dat_13_REPORT.md
- dat_14_REPORT.md
- dat_15_REPORT.md
- dat_16_REPORT.md
- dat_17_REPORT.md
- dat_18_REPORT.md
- DECISIONS_LOG.md
- GAP_REPORT.md
- PHASE_1_FINAL_TABLE.md
- PHASE_1_REPORT.md
- ROLE_MAP.md
- SESSION_LOG.md
- SOURCE_INVENTORY.md
- TODO.md
- VALIDATION_REPORT.md

## Sources (originals)

- .gitkeep (0 B, sha=E3B0C44298FC)
- SIM800 Series_AT Command Manual_V1.01.pdf (7280172 B, sha=F84E3716BA38)
- SIM800H&SIM800L_Hardware_Design_V2.02.PDF (2766992 B, sha=55A9A3F07C9A)
- SIM800L_Hardware_Design_V1.00.pdf (2830869 B, sha=7FE4BF41FFB8)

## Git Status After Recovery

```
?? CHANGELOG.md
?? reports/recovery-14050719-232020.log
?? reports/recovery-14050719-232150.log
?? tools/
```

### Recent commits
```
c28f928 D13: apply limit_reason to 7 partial datasets, close Phase 1 (L3=0, v1.0.0-phase1)
1f371ae D11 partial: 16/25 OK ΓÇö see SESSION_LOG
b09efcd D10: 20 substeps (15/18 OK), production criteria
c7439a8 D9: fix else bug, redefine complete (with_page AND strict_depth>=50%), diagnose params
625cfa9 Batch D8 partial: 10/10 OK ΓÇö see SESSION_LOG
```

## Notes

- No files were deleted in this run.
- No Git push was performed.
- No PDF extraction or dataset population was performed.
- Tracked files were restored from Git HEAD (c28f928 / v1.0.0-phase1).
- Untracked temporary files were restored from backup folder.
- Data files with existing records were kept untouched.
