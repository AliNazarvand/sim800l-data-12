# META CONSISTENCY REPORT

| دیتاست | COVERAGE_MATRIX | _dataset_meta | وضعیت |
|---|---|---|---|

تعداد ناسازگاری: 0
تعداد دیتاست بدون status در _dataset_meta: 0

## محتوای خام همه _dataset_meta.yaml

### dat_01 — data\at_commands\_dataset_meta.yaml
```yaml
dataset_id: "dat_01"
dataset_name: "AT Command DB"
phase_completed: 2
record_count: 18
min_records_required: 15
status: "blocked"
reason: null
pending_fields:
  - "syntax details (full AT+XXX=<params> grammar from AT Command Manual)"
  - "parameters (type, range, defaults)"
  - "responses (full list of response codes)"
completion_source: null
last_updated: "2026-10-10"
retry_count: 0
```

### dat_02 — data\urc\_dataset_meta.yaml
```yaml
dataset_id: "dat_02"
dataset_name: "URC DB"
phase_completed: 2
record_count: 12
min_records_required: 8
status: "blocked"
reason: null
pending_fields:
  - "urc_at_* additional URCs from AT Command Manual (+CMTI, +CMT, +CLIP, +CRING, RING, +CIPRXGET, +CIPCLOSE, +PDP: DEACT, ...)"
completion_source: null
last_updated: "2026-10-10"
retry_count: 0
```

### dat_03 — data\error_codes\_dataset_meta.yaml
```yaml
dataset_id: "dat_03"
dataset_name: "Error Code DB (CME/CMS)"
phase_completed: 2
record_count: 0
min_records_required: 50
status: "blocked"
reason: "INSUFFICIENT_RECORDS"
pending_fields: []
completion_source: null
last_updated: "2026-10-10"
retry_count: 0
```

### dat_04 — data\timing\_dataset_meta.yaml
```yaml
dataset_id: "dat_04"
dataset_name: "Timing & Timeout DB"
phase_completed: 1
record_count: 11
min_records_required: 5
status: "complete"
reason: null
pending_fields: []
completion_source: null
last_updated: "2026-10-10"
retry_count: 0
coverage_estimate: "high"
coverage_pct: "100%"
coverage_note: "Under-voltage power-down اضافه شد (ص 24)."
```

### dat_05 — data\state_machine\_dataset_meta.yaml
```yaml
dataset_id: "dat_05"
dataset_name: "State Machine DB"
phase_completed: 1
record_count: 19
min_records_required: "5_states_6_transitions"
status: "complete"
reason: null
pending_fields: []
completion_source: null
last_updated: "2026-10-10"
retry_count: 0
coverage_estimate: "high"
coverage_pct: "95%"
coverage_note: "4 حالت عملیاتی (IDLE/TALK/GPRS_STANDBY/GPRS_DATA) از Table 4 اضافه شد."
```

### dat_06 — data\init_sequence\_dataset_meta.yaml
```yaml
dataset_id: "dat_06"
dataset_name: "Init Sequence DB"
phase_completed: 1
record_count: 5
min_records_required: 5
status: "complete"
reason: null
pending_fields: []
completion_source: null
last_updated: "2026-10-10"
retry_count: 0
coverage_estimate: "high"
coverage_pct: "100%"
coverage_note: "Autobauding sync اضافه شد (ص ۳۰)."
```

### dat_07 — data\hardware\_dataset_meta.yaml
```yaml
dataset_id: "dat_07"
dataset_name: "Hardware Reference DB"
phase_completed: 1
record_count: 80
min_records_required: "all_pins_in_pdf + 10_electrical_parameters"
status: "complete"
reason: null
pending_fields:
  - "pin_records_for_remaining_GND_grouped_pins_if_required_individually"
completion_source: null
last_updated: "2026-10-10"
retry_count: 0
coverage_estimate: "high"
coverage_pct: "95%"
coverage_note: "~20 رکورد RF/ESD/Absolute Max/Frequencies از جداول 42-56 اضافه شد."
```

### dat_08 — data\firmware_compat\_dataset_meta.yaml
```yaml
dataset_id: "dat_08"
dataset_name: "Firmware Compatibility Matrix"
phase_completed: 2
record_count: 0
min_records_required: 5
status: "blocked"
reason: "INSUFFICIENT_RECORDS"
pending_fields: []
completion_source: null
last_updated: "2026-10-10"
retry_count: 0
```

### dat_09 — data\sms\_dataset_meta.yaml
```yaml
dataset_id: "dat_09"
dataset_name: "SMS DB"
phase_completed: 2
record_count: 3
min_records_required: 3
status: "blocked"
reason: null
pending_fields:
  - "AT+CMGS, AT+CMGR, AT+CMGD, AT+CMGW, AT+CMGF, AT+CSCA, AT+CPMS, AT+CNMI (from AT Command Manual)"
completion_source: null
last_updated: "2026-10-10"
retry_count: 0
```

### dat_10 — data\gprs_data\_dataset_meta.yaml
```yaml
dataset_id: "dat_10"
dataset_name: "GPRS/Data DB"
phase_completed: 2
record_count: 7
min_records_required: 7
status: "blocked"
reason: null
pending_fields:
  - "AT+CGATT, AT+CGDCONT, AT+CSTT, AT+CIICR, AT+CIFSR, AT+CIPSTART, AT+CIPSEND, AT+CIPCLOSE, AT+CIPSTATUS (from AT Command Manual)"
completion_source: null
last_updated: "2026-10-10"
retry_count: 0
```

### dat_11 — data\http_ftp_ssl\_dataset_meta.yaml
```yaml
dataset_id: "dat_11"
dataset_name: "HTTP/FTP/SSL DB"
phase_completed: 2
record_count: 0
min_records_required: 10
status: "blocked"
reason: "INSUFFICIENT_RECORDS"
pending_fields: []
completion_source: null
last_updated: "2026-10-10"
retry_count: 0
```

### dat_12 — data\audio\_dataset_meta.yaml
```yaml
dataset_id: "dat_12"
dataset_name: "Audio DB"
phase_completed: 1
record_count: 8
min_records_required: 5
status: "blocked"
reason: null
pending_fields:
  - "audio_at_* (AT-command-related audio records deferred; AT Command Manual not available)"
completion_source: null
last_updated: "2026-10-10"
retry_count: 0
```

### dat_13 — data\sim_management\_dataset_meta.yaml
```yaml
dataset_id: "dat_13"
dataset_name: "SIM Management DB"
phase_completed: 1
record_count: 8
min_records_required: 5
status: "blocked"
reason: null
pending_fields:
  - "sim_management_at_* (AT-command-related SIM records deferred; AT Command Manual not available)"
completion_source: null
last_updated: "2026-10-10"
retry_count: 0
```

### dat_14 — data\operator_apn\_dataset_meta.yaml
```yaml
dataset_id: "dat_14"
dataset_name: "Operator/APN DB (MCC/MNC)"
phase_completed: 2
record_count: 0
min_records_required: 20
status: "deferred"
reason: "INSUFFICIENT_RECORDS"
pending_fields: []
completion_source: null
last_updated: "2026-10-10"
retry_count: 0
```

### dat_15 — data\power_management\_dataset_meta.yaml
```yaml
dataset_id: "dat_15"
dataset_name: "Power Management DB"
phase_completed: 1
record_count: 4
min_records_required: 3
status: "complete"
reason: null
pending_fields:
  - "MINIMUM_FUNCTIONALITY.current_consumption_typical"
  - "MINIMUM_FUNCTIONALITY.current_consumption_max"
completion_source: null
last_updated: "2026-10-10"
retry_count: 0
coverage_estimate: "high"
coverage_pct: "95%"
coverage_note: "تمام مقادیر جریان Table 49 (p60) و Table 8 (p26) اضافه شد — 22 رکورد جدید"
```

### dat_16 — data\board_evb\_dataset_meta.yaml
```yaml
dataset_id: "dat_16"
dataset_name: "Board/EVB Definitions"
phase_completed: 1
record_count: 0
min_records_required: "1_board_with_5_fields"
status: "deferred"
reason: "INSUFFICIENT_RECORDS"
pending_fields: []
completion_source: null
last_updated: "2026-10-10"
retry_count: 3
```

### dat_17 — data\certificate_keystore\_dataset_meta.yaml
```yaml
dataset_id: "dat_17"
dataset_name: "Certificate/Key Store"
phase_completed: 2
record_count: 0
min_records_required: 5
status: "blocked"
reason: "INSUFFICIENT_RECORDS"
pending_fields: []
completion_source: null
last_updated: "2026-10-10"
retry_count: 0
```

### dat_18 — data\certification\_dataset_meta.yaml
```yaml
dataset_id: "dat_18"
dataset_name: "Certification Data"
phase_completed: 2
record_count: 0
min_records_required: 5
status: "blocked"
reason: "INSUFFICIENT_RECORDS"
pending_fields: []
completion_source: null
last_updated: "2026-10-10"
retry_count: 0
```

