# VALIDATION_10_ERRORS

Generated: 1405-07-20 00:49:44

## Summary

Remaining L1 errors after nullable fix: 28

## Classification

| Category | Count |
|----------|-------|
| type mismatch | 9 |
| other | 19 |

## All error rows

```
| dat_01 | dat_01_at_command.yaml |
| dat_02 | dat_02_urc.yaml |
| dat_03 | dat_03_error_code.yaml |
| dat_04 | dat_04_timing_timeout.yaml |
| dat_05 | dat_05_state_machine.yaml |
| dat_06 | dat_06_init_sequence.yaml |
| dat_07 | dat_07_hardware_reference.yaml |
| dat_08 | dat_08_firmware_compatibility.yaml |
| dat_09 | dat_09_sms.yaml |
| dat_10 | dat_10_gprs_data.yaml |
| dat_11 | dat_11_http_ftp_ssl.yaml |
| dat_12 | dat_12_audio.yaml |
| dat_13 | dat_13_sim_management.yaml |
| dat_14 | dat_14_operator_apn.yaml |
| dat_15 | dat_15_power_management.yaml |
| dat_16 | dat_16_board_evb.yaml |
| dat_17 | dat_17_certificate_key_store.yaml |
| dat_18 | dat_18_certification.yaml |
| dat_06 | 1 | dat_06_0002:dependency_step | 'dat_06_0001' is not of type 'integer', 'null' |  |
| dat_06 | 1 | dat_06_0003:dependency_step | 'dat_06_0002' is not of type 'integer', 'null' |  |
| dat_06 | 1 | dat_06_0004:dependency_step | 'dat_06_0003' is not of type 'integer', 'null' |  |
| dat_06 | 1 | dat_06_0005:dependency_step | 'dat_06_0004' is not of type 'integer', 'null' |  |
| dat_06 | 1 | dat_06_0006:dependency_step | 'dat_06_0005' is not of type 'integer', 'null' |  |
| dat_06 | 1 | dat_06_0007:dependency_step | 'dat_06_0006' is not of type 'integer', 'null' |  |
| dat_06 | 1 | dat_06_0008:dependency_step | 'dat_06_0007' is not of type 'integer', 'null' |  |
| dat_06 | 1 | dat_06_0009:dependency_step | 'dat_06_0008' is not of type 'integer', 'null' |  |
| dat_06 | 1 | dat_06_0010:dependency_step | 'dat_06_0009' is not of type 'integer', 'null' |  |
| dat_09 | 1 | dat_09_0014:mode | 'write' is not one of ['text', 'pdu'] |  |
```

## Recommendation

- If most errors are format: date on null values:
    - Either remove format: date from nullable date fields,
    - Or split into anyOf: [{type: string, format: date}, {type: null}].
- If most errors are enum violation: add null to the enum list.
- If errors are actual data problems: fix the specific records.
