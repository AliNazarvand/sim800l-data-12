# Source Mapping

Every data field must be traceable to a page/section in a primary source.

The complete per-record source metadata is stored inside each record under
`_meta` (fields `source`, `source_version`, `source_page`, `source_section`,
`source_figure_number`). The table below lists representative mappings for
each dataset; the definitive reference for any specific record is always its
own `_meta` block.

| dataset | record_id | field | source_document | source_version | source_page | source_section | source_figure |
|---------|-----------|-------|-----------------|----------------|-------------|----------------|---------------|
| dat_07 | dat_07_pinout_001 | pin_number | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 16 | 3.2 | Table 5 |
| dat_07 | dat_07_pinout_016 | description_fa | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 16 | 3.2 | Table 5 |
| dat_07 | dat_07_pinout_044 | pin_name | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 17 | 3.2 | Table 5 |
| dat_07 | dat_07_electrical_001 | min_value | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 58 | 6.2 | Table 43 |
| dat_07 | dat_07_electrical_004 | min_value | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 58 | 6.3 | Table 44 |
| dat_07 | dat_07_electrical_008 | typical_value | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 59 | 6.6 | Table 47 |
| dat_07 | dat_07_power_consumption_002 | current_typical | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 60 | 6.8 | Table 49 |
| dat_07 | dat_07_interfaces_001 | supported_baud_rates | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 29 | 4.5.1 | null |
| dat_07 | dat_07_physical_001 | dimensions_mm | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 11 | 2.2 | Table 2 |
| dat_04 | dat_04_timing_001 | min_value | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 22 | 4.2.1 | null |
| dat_04 | dat_04_timing_002 | min_value | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 23 | 4.2.2.1 | Figure 13 |
| dat_04 | dat_04_timing_003 | min_value | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 26 | 4.2.3 | Figure 16 |
| dat_04 | dat_04_timing_005 | min_value | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 21 | 4.1 | Figure 8 |
| dat_04 | dat_04_timing_007 | min_value | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 51 | 4.18 | Figure 48 |
| dat_15 | dat_15_mode_002 | current_consumption_typical | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 60 | 6.8 | Table 49 |
| dat_15 | dat_15_mode_003 | current_consumption_typical | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 60 | 6.8 | Table 49 |
| dat_15 | dat_15_mode_004 | current_consumption_typical | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 26 | 4.3.1 | null |
| dat_05 | dat_05_state_002 | entry_conditions | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 23 | 4.2.1 | Figure 12 |
| dat_05 | dat_05_state_005 | entry_conditions | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 25 | 4.2.3 | Figure 16 |
| dat_05 | dat_05_transition_003 | trigger | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 23 | 4.2.2.1 | Figure 13 |
| dat_06 | dat_06_step_001 | hardware_operation | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 20 | 4.1 | Figure 5 |
| dat_06 | dat_06_step_002 | hardware_operation | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 22 | 4.2.1 | Figure 10 |
| dat_06 | dat_06_step_004 | hardware_operation | SIM800H&SIM800L_Hardware_Design_V2.02 | V2.02 | 23 | 4.2.1 | Figure 12 |

Notes
-----
- `source_document` must be exactly one of:
  - `SIM800L_Hardware_Design_V1.00`
  - `SIM800H&SIM800L_Hardware_Design_V2.02`
- `source_figure` is populated only when the value came from a figure/diagram.
  Otherwise `null`.