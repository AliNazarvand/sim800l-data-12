# Data Dictionary

Field meanings shared across all datasets. Dataset-specific fields are
listed per dataset below.

## Common `_meta` block (required on every record)

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable identifier: `<dataset>_<subcategory>_<NNN>`. |
| `source` | string | One of the two primary source IDs (see below). |
| `source_version` | string | `"V1.00"` or `"V2.02"`. |
| `source_page` | int or null | Page number in the source PDF. |
| `source_section` | string or null | Section heading in the source PDF. |
| `source_figure_number` | string or null | Figure/table number if the value came from a figure. |
| `extracted_at` | string (ISO date) | Date of extraction (`datetime.date.today()`). |
| `pending_fields` | array of strings | Fields whose values are deferred or unknown. |
| `compatible_models` | array | `["SIM800L"]`, `["SIM800H"]`, or both. |
| `missing_reason` | string or null | One of the allowed values below. |
| `completion_source` | string or null | Secondary source used in Phase 2a/2b. |
| `license_note` | string | Constant: `See NOTICE file for licensing and copyright information.` |

### Allowed `missing_reason` values (record level)

- `NOT_FOUND_IN_SOURCES`
- `DEFERRED_TO_PHASE_2A`
- `DEFERRED_TO_PHASE_2B`
- `CONFLICTING_SOURCES`
- `MIXED`

`INSUFFICIENT_RECORDS` is only allowed in `_dataset_meta.yaml` (`reason:`).

## dat_04 — Timing & Timeout DB

`parameter_id`, `parameter_name`, `description_fa`, `min_value`,
`typical_value`, `max_value`, `unit`, `condition`, `related_pin`, `notes_fa`.

## dat_05 — State Machine DB

States: `state_id`, `state_name`, `description_fa`, `entry_conditions`,
`exit_conditions`, `related_pins`.
Transitions: `transition_id`, `from_state`, `to_state`, `trigger`,
`hardware_condition`.

## dat_06 — Init Sequence DB

`step_number`, `action`, `hardware_operation`, `expected_result`,
`timeout_ms`, `retry_count`, `critical`, `notes_fa`.

## dat_07 — Hardware Reference DB

- `pinout.yaml`: `pin_number`, `pin_name`, `type`, `description_fa`,
  `voltage_level`, `max_rating`, `notes_fa`.
- `electrical.yaml`: `parameter`, `symbol`, `min_value`, `typical_value`,
  `max_value`, `unit`, `condition`, `notes_fa`.
- `power_consumption.yaml`: `mode`, `current_typical`, `current_max`,
  `unit`, `condition`.
- `interfaces.yaml`: `interface_name`, `type`, `supported_baud_rates`,
  `pin_mapping`, `notes_fa`.
- `physical.yaml`: `dimensions_mm`, `weight_g`, `flash_memory_mbit`,
  `ram_mbit`, `operating_temperature`, `storage_temperature`.

## dat_15 — Power Management DB

`mode_id`, `mode_name`, `description_fa`, `current_consumption_typical`,
`current_consumption_max`, `unit`, `entry_condition`, `exit_condition`,
`related_pins`.

## dat_16 — Board/EVB Definitions

`board_id`, `board_name`, `board_type`, `input_voltage`,
`regulator_onboard`, `level_shifter_onboard`, `interfaces_exposed`,
`pin_mapping`, `notes_fa`.
## Phase 2 datasets

### dat_01 — AT Command DB (deferred)
Status: `deferred` — requires `SIM800 Series_AT Command Manual.pdf`.
No records produced.

### dat_02 — URC DB (partial: HW only)
HW URC records: `urc_code`, `urc_name`, `description_fa`, `trigger`,
`related_pins`.
AT URC records (pending): populated when the AT Command Manual is available.

### dat_03 — Error Code DB (CME/CMS) (deferred)
Status: `deferred` — requires AT Command Manual.

### dat_08 — Firmware Compatibility Matrix (deferred)
Status: `deferred` — requires AT Command Manual + secondary firmware matrices.

### dat_09 — SMS DB (deferred)
Status: `deferred` — requires AT Command Manual.

### dat_10 — GPRS/Data DB (deferred)
Status: `deferred` — requires AT Command Manual.

### dat_11 — HTTP/FTP/SSL DB (deferred)
Status: `deferred` — requires AT Command Manual.

### dat_12 — Audio DB (partial: HW only)
HW audio records:
- `category` — one of `pin`, `characteristic`, `design_guide`.
- For `pin`: `pin_name`, `pin_number` (array), `direction`, `function_fa`.
- For `characteristic`: `parameter` + characteristic-specific numeric/string fields.
- For `design_guide`: `parameter`, `notes_fa`, and design values.

AT audio records (pending): `audio_at.yaml`, empty until Manual arrives.

### dat_13 — SIM Management DB (partial: HW only)
HW SIM records: same shape as dat_12 HW records.
AT SIM records (pending): `sim_management_at.yaml`, empty until Manual arrives.

### dat_14 — Operator/APN DB (MCC/MNC) (deferred)
Status: `deferred` — requires external MCC/MNC and APN databases.

### dat_17 — Certificate/Key Store (deferred)
Status: `deferred` — requires external certificate/key store sources.

### dat_18 — Certification Data (deferred)
Status: `deferred` — requires external certification body sources.

## Phase 2c updates

### dat_01 — AT Command DB (partial: 18 records)
Records now include: `command`, `syntax` (best-effort), `parameters` (empty
until Manual), `responses` (default OK/ERROR), `purpose_en`, `purpose_fa`,
`category`. Full grammar and parameter lists remain pending from the AT
Command Manual.

### dat_02 — URC DB (partial: 12 records)
Added `+CFUN: 1` and `+CPIN: READY` to `urc_at.yaml` (both mentioned in
Section 4.5.1). Remaining AT-related URCs (e.g. +CMTI, RING, +CIPRXGET)
require the AT Command Manual.

### dat_09 — SMS DB (partial: 3 capability records)
Records: `capability`, `description_en`, `description_fa`.
AT-command records (AT+CMGS, AT+CMGR, etc.) remain pending.

### dat_10 — GPRS/Data DB (partial: 7 capability records)
Records: `capability`, `description_en`, `description_fa`.
AT-command records (AT+CGATT, AT+CSTT, etc.) remain pending.
