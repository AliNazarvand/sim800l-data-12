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