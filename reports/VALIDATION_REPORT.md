# Validation Report

Generated: 2026-10-13T18:07:56Z
Exit: 0

```text
{
  "datasets": [
    {
      "dataset": "dat_01",
      "file": "dat_01_at_command.yaml",
      "records": 610,
      "errors": 0,
      "schema_ok": true
    },
    {
      "dataset": "dat_02",
      "file": "dat_02_urc.yaml",
      "records": 1,
      "errors": 9,
      "schema_ok": false
    },
    {
      "dataset": "dat_03",
      "file": "dat_03_error_code.yaml",
      "records": 1,
      "errors": 9,
      "schema_ok": false
    },
    {
      "dataset": "dat_04",
      "file": "dat_04_timing_timeout.yaml",
      "records": 70,
      "errors": 0,
      "schema_ok": true
    },
    {
      "dataset": "dat_05",
      "file": "dat_05_state_machine.yaml",
      "records": 1,
      "errors": 9,
      "schema_ok": false
    },
    {
      "dataset": "dat_06",
      "file": "dat_06_init_sequence.yaml",
      "records": 1,
      "errors": 9,
      "schema_ok": false
    },
    {
      "dataset": "dat_07",
      "file": "dat_07_hardware_reference.yaml",
      "records": 78,
      "errors": 0,
      "schema_ok": true
    },
    {
      "dataset": "dat_08",
      "file": "dat_08_firmware_compatibility.yaml",
      "records": 1,
      "errors": 0,
      "schema_ok": true
    },
    {
      "dataset": "dat_09",
      "file": "dat_09_sms.yaml",
      "records": 15,
      "errors": 23,
      "schema_ok": false
    },
    {
      "dataset": "dat_10",
      "file": "dat_10_gprs_data.yaml",
      "records": 22,
      "errors": 9,
      "schema_ok": false
    },
    {
      "dataset": "dat_11",
      "file": "dat_11_http_ftp_ssl.yaml",
      "records": 11,
      "errors": 9,
      "schema_ok": false
    },
    {
      "dataset": "dat_12",
      "file": "dat_12_audio.yaml",
      "records": 8,
      "errors": 9,
      "schema_ok": false
    },
    {
      "dataset": "dat_13",
      "file": "dat_13_sim_management.yaml",
      "records": 11,
      "errors": 9,
      "schema_ok": false
    },
    {
      "dataset": "dat_14",
      "file": "dat_14_operator_apn.yaml",
      "records": 52,
      "errors": 0,
      "schema_ok": true
    },
    {
      "dataset": "dat_15",
      "file": "dat_15_power_management.yaml",
      "records": 357,
      "errors": 0,
      "schema_ok": true
    },
    {
      "dataset": "dat_16",
      "file": "dat_16_board_evb.yaml",
      "records": 1,
      "errors": 0,
      "schema_ok": true
    },
    {
      "dataset": "dat_17",
      "file": "dat_17_certificate_key_store.yaml",
      "records": 9,
      "errors": 0,
      "schema_ok": true
    },
    {
      "dataset": "dat_18",
      "file": "dat_18_certification.yaml",
      "records": 1,
      "errors": 0,
      "schema_ok": true
    }
  ],
  "errors": [
    "dat_02_urc.yaml: [0] missing: id",
    "dat_02_urc.yaml: [0] missing: category",
    "dat_02_urc.yaml: [0] missing: source",
    "dat_02_urc.yaml: [0] missing: source_type",
    "dat_02_urc.yaml: [0] missing: confidence",
    "dat_02_urc.yaml: [0] missing: status",
    "dat_02_urc.yaml: [0] missing: applicable_models",
    "dat_02_urc.yaml: [0] applicable_models missing SIM800L (R1)",
    "dat_02_urc.yaml: [0] schema: 'id' is a required property",
    "dat_03_error_code.yaml: [0] missing: id",
    "dat_03_error_code.yaml: [0] missing: category",
    "dat_03_error_code.yaml: [0] missing: source",
    "dat_03_error_code.yaml: [0] missing: source_type",
    "dat_03_error_code.yaml: [0] missing: confidence",
    "dat_03_error_code.yaml: [0] missing: status",
    "dat_03_error_code.yaml: [0] missing: applicable_models",
    "dat_03_error_code.yaml: [0] applicable_models missing SIM800L (R1)",
    "dat_03_error_code.yaml: [0] schema: 'id' is a required property",
    "dat_05_state_machine.yaml: [0] missing: id",
    "dat_05_state_machine.yaml: [0] missing: category",
    "dat_05_state_machine.yaml: [0] missing: source",
    "dat_05_state_machine.yaml: [0] missing: source_type",
    "dat_05_state_machine.yaml: [0] missing: confidence",
    "dat_05_state_machine.yaml: [0] missing: status",
    "dat_05_state_machine.yaml: [0] missing: applicable_models",
    "dat_05_state_machine.yaml: [0] applicable_models missing SIM800L (R1)",
    "dat_05_state_machine.yaml: [0] schema: 'id' is a required property",
    "dat_06_init_sequence.yaml: [0] missing: id",
    "dat_06_init_sequence.yaml: [0] missing: category",
    "dat_06_init_sequence.yaml: [0] missing: source",
    "dat_06_init_sequence.yaml: [0] missing: source_type",
    "dat_06_init_sequence.yaml: [0] missing: confidence",
    "dat_06_init_sequence.yaml: [0] missing: status",
    "dat_06_init_sequence.yaml: [0] missing: applicable_models",
    "dat_06_init_sequence.yaml: [0] applicable_models missing SIM800L (R1)",
    "dat_06_init_sequence.yaml: [0] schema: 'id' is a required property",
    "dat_09_sms.yaml: [0] missing: id",
    "dat_09_sms.yaml: [0] missing: category",
    "dat_09_sms.yaml: [0] missing: source",
    "dat_09_sms.yaml: [0] missing: source_type",
    "dat_09_sms.yaml: [0] missing: confidence",
    "dat_09_sms.yaml: [0] missing: status",
    "dat_09_sms.yaml: [0] missing: applicable_models",
    "dat_09_sms.yaml: [0] applicable_models missing SIM800L (R1)",
    "dat_09_sms.yaml: [0] schema: 'id' is a required property",
    "dat_09_sms.yaml: [1] schema: 'write' is not one of ['text', 'pdu']",
    "dat_09_sms.yaml: [2] schema: 'write' is not one of ['text', 'pdu']",
    "dat_09_sms.yaml: [3] schema: 'write' is not one of ['text', 'pdu']",
    "dat_09_sms.yaml: [4] schema: 'write' is not one of ['text', 'pdu']",
    "dat_09_sms.yaml: [5] schema: 'write' is not one of ['text', 'pdu']",
    "dat_09_sms.yaml: [6] schema: 'write' is not one of ['text', 'pdu']",
    "dat_09_sms.yaml: [7] schema: 'write' is not one of ['text', 'pdu']",
    "dat_09_sms.yaml: [8] schema: 'write' is not one of ['text', 'pdu']",
    "dat_09_sms.yaml: [9] schema: 'write' is not one of ['text', 'pdu']",
    "dat_09_sms.yaml: [10] schema: 'write' is not one of ['text', 'pdu']",
    "dat_09_sms.yaml: [11] schema: 'write' is not one of ['text', 'pdu']",
    "dat_09_sms.yaml: [12] schema: 'write' is not one of ['text', 'pdu']",
    "dat_09_sms.yaml: [13] schema: 'write' is not one of ['text', 'pdu']",
    "dat_09_sms.yaml: [14] schema: 'write' is not one of ['text', 'pdu']",
    "dat_10_gprs_data.yaml: [0] missing: id",
    "dat_10_gprs_data.yaml: [0] missing: category",
    "dat_10_gprs_data.yaml: [0] missing: source",
    "dat_10_gprs_data.yaml: [0] missing: source_type",
    "dat_10_gprs_data.yaml: [0] missing: confidence",
    "dat_10_gprs_data.yaml: [0] missing: status",
    "dat_10_gprs_data.yaml: [0] missing: applicable_models",
    "dat_10_gprs_data.yaml: [0] applicable_models missing SIM800L (R1)",
    "dat_10_gprs_data.yaml: [0] schema: 'id' is a required property",
    "dat_11_http_ftp_ssl.yaml: [0] missing: id",
    "dat_11_http_ftp_ssl.yaml: [0] missing: category",
    "dat_11_http_ftp_ssl.yaml: [0] missing: source",
    "dat_11_http_ftp_ssl.yaml: [0] missing: source_type",
    "dat_11_http_ftp_ssl.yaml: [0] missing: confidence",
    "dat_11_http_ftp_ssl.yaml: [0] missing: status",
    "dat_11_http_ftp_ssl.yaml: [0] missing: applicable_models",
    "dat_11_http_ftp_ssl.yaml: [0] applicable_models missing SIM800L (R1)",
    "dat_11_http_ftp_ssl.yaml: [0] schema: 'id' is a required property",
    "dat_12_audio.yaml: [0] missing: id",
    "dat_12_audio.yaml: [0] missing: category",
    "dat_12_audio.yaml: [0] missing: source",
    "dat_12_audio.yaml: [0] missing: source_type",
    "dat_12_audio.yaml: [0] missing: confidence",
    "dat_12_audio.yaml: [0] missing: status",
    "dat_12_audio.yaml: [0] missing: applicable_models",
    "dat_12_audio.yaml: [0] applicable_models missing SIM800L (R1)",
    "dat_12_audio.yaml: [0] schema: 'id' is a required property",
    "dat_13_sim_management.yaml: [0] missing: id",
    "dat_13_sim_management.yaml: [0] missing: category",
    "dat_13_sim_management.yaml: [0] missing: source",
    "dat_13_sim_management.yaml: [0] missing: source_type",
    "dat_13_sim_management.yaml: [0] missing: confidence",
    "dat_13_sim_management.yaml: [0] missing: status",
    "dat_13_sim_management.yaml: [0] missing: applicable_models",
    "dat_13_sim_management.yaml: [0] applicable_models missing SIM800L (R1)",
    "dat_13_sim_management.yaml: [0] schema: 'id' is a required property"
  ],
  "schema_used": {
    "dat_01_at_command.yaml": "dat_01",
    "dat_02_urc.yaml": "dat_02",
    "dat_03_error_code.yaml": "dat_03",
    "dat_04_timing_timeout.yaml": "dat_04",
    "dat_05_state_machine.yaml": "dat_05",
    "dat_06_init_sequence.yaml": "dat_06",
    "dat_07_hardware_reference.yaml": "dat_07",
    "dat_08_firmware_compatibility.yaml": "dat_08",
    "dat_09_sms.yaml": "dat_09",
    "dat_10_gprs_data.yaml": "dat_10",
    "dat_11_http_ftp_ssl.yaml": "dat_11",
    "dat_12_audio.yaml": "dat_12",
    "dat_13_sim_management.yaml": "dat_13",
    "dat_14_operator_apn.yaml": "dat_14",
    "dat_15_power_management.yaml": "dat_15",
    "dat_16_board_evb.yaml": "dat_16",
    "dat_17_certificate_key_store.yaml": "dat_17",
    "dat_18_certification.yaml": "dat_18"
  }
}
```
