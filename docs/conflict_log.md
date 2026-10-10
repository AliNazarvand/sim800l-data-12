# Conflict Log (V1.00 vs V2.02)

Resolution rule: **V2.02 is authoritative**. V1.00-only data is retained
only when of historical/technical value; such records carry
`deprecated_in: "V2.02"` and `source_version: "V1.00"`.

| dataset | record_id | field | v1_value | v2_value | resolution | decided_by | date | notes |
|---------|-----------|-------|----------|----------|------------|-----------|------|-------|
| dat_04 | dat_04_timing_002 | min_value | 1.5 s | 1.0 s | V2.02_wins | auto_rule | 2026-10-10 | V1.00 (sec 4.2.2.1) states "at least 1.5 second"; V2.02 (sec 4.2.2.1) states "at least 1 second". V2.02 is authoritative. |
| dat_15 | dat_15_mode_003 | current_consumption_typical | 50 uA | 150 uA | V2.02_wins | auto_rule | 2026-10-10 | Power-down current typical: V1.00 Table 48 = 50 uA; V2.02 Table 49 = 150 uA. |
| dat_15 | dat_15_mode_003 | current_consumption_max | 60 uA | 200 uA | V2.02_wins | auto_rule | 2026-10-10 | Power-down current max: V1.00 Table 48 = 60 uA; V2.02 Table 49 = 200 uA. |

Allowed `resolution` values: `V2.02_wins`, `V1.00_wins`, `both_kept`,
`manual_review`.