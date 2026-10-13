# VALIDATION REPORT
_Generated: 2026-10-13T13:20:29Z_

| Dataset | File | Records | Errors | Schema OK |
|---|---|---|---|---|
| dat_01 | dat_01_at_command.yaml | 335 | 0 | True |
| dat_02 | dat_02_urc.yaml | 18 | 0 | True |
| dat_03 | dat_03_error_code.yaml | 255 | 0 | True |
| dat_04 | dat_04_timing_timeout.yaml | 0 | 0 | True |
| dat_05 | dat_05_state_machine.yaml | 31 | 0 | True |
| dat_06 | dat_06_init_sequence.yaml | 35 | 0 | True |
| dat_07 | dat_07_hardware_reference.yaml | 0 | 0 | True |
| dat_08 | dat_08_firmware_compatibility.yaml | 1 | 0 | True |
| dat_09 | dat_09_sms.yaml | 14 | 0 | True |
| dat_10 | dat_10_gprs_data.yaml | 24 | 0 | True |
| dat_11 | dat_11_http_ftp_ssl.yaml | 38 | 0 | True |
| dat_12 | dat_12_audio.yaml | 13 | 0 | True |
| dat_13 | dat_13_sim_management.yaml | 10 | 0 | True |
| dat_14 | dat_14_operator_apn.yaml | 52 | 0 | True |
| dat_15 | dat_15_power_management.yaml | 6 | 36 | False |
| dat_16 | dat_16_board_evb.yaml | 1 | 0 | True |
| dat_17 | dat_17_certificate_key_store.yaml | 9 | 0 | True |
| dat_18 | dat_18_certification.yaml | 1 | 0 | True |

## Total errors: 36
- dat_15_power_management.yaml: [0] missing: source_type
- dat_15_power_management.yaml: [0] missing: confidence
- dat_15_power_management.yaml: [0] missing: status
- dat_15_power_management.yaml: [0] missing: applicable_models
- dat_15_power_management.yaml: [0] applicable_models missing SIM800L (R1)
- dat_15_power_management.yaml: [1] missing: source_type
- dat_15_power_management.yaml: [1] missing: confidence
- dat_15_power_management.yaml: [1] missing: status
- dat_15_power_management.yaml: [1] missing: applicable_models
- dat_15_power_management.yaml: [1] applicable_models missing SIM800L (R1)
- dat_15_power_management.yaml: [2] missing: source_type
- dat_15_power_management.yaml: [2] missing: confidence
- dat_15_power_management.yaml: [2] missing: status
- dat_15_power_management.yaml: [2] missing: applicable_models
- dat_15_power_management.yaml: [2] applicable_models missing SIM800L (R1)
- dat_15_power_management.yaml: [3] missing: source_type
- dat_15_power_management.yaml: [3] missing: confidence
- dat_15_power_management.yaml: [3] missing: status
- dat_15_power_management.yaml: [3] missing: applicable_models
- dat_15_power_management.yaml: [3] applicable_models missing SIM800L (R1)
- dat_15_power_management.yaml: [4] missing: source_type
- dat_15_power_management.yaml: [4] missing: confidence
- dat_15_power_management.yaml: [4] missing: status
- dat_15_power_management.yaml: [4] missing: applicable_models
- dat_15_power_management.yaml: [4] applicable_models missing SIM800L (R1)
- dat_15_power_management.yaml: [5] missing: source_type
- dat_15_power_management.yaml: [5] missing: confidence
- dat_15_power_management.yaml: [5] missing: status
- dat_15_power_management.yaml: [5] missing: applicable_models
- dat_15_power_management.yaml: [5] applicable_models missing SIM800L (R1)
- dat_15_power_management.yaml: [0] schema: 'source_type' is a required property
- dat_15_power_management.yaml: [1] schema: 'source_type' is a required property
- dat_15_power_management.yaml: [2] schema: 'source_type' is a required property
- dat_15_power_management.yaml: [3] schema: 'source_type' is a required property
- dat_15_power_management.yaml: [4] schema: 'source_type' is a required property
- dat_15_power_management.yaml: [5] schema: 'source_type' is a required property