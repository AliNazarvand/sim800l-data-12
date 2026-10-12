# Data Dictionary -- sim800l-data

## Common Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | yes | Unique identifier: dat_XX_NNNN |
| category | string | yes | Category within dataset |
| source | object | yes | Source document reference |
| source_type | enum | yes | primary / secondary / external |
| confidence | number | yes | 0.0 -- 1.0 |
| status | enum | yes | complete / partial / unknown / inferred / blocked / deferred |
| conflicts | array | no | List of source conflicts |
| notes | string | no | Additional notes |
| tags | array | no | Tags |
| applicable_models | array | yes | Must contain SIM800L |
| created_at | string | yes | ISO 8601 datetime |
| updated_at | string | yes | ISO 8601 datetime |

## Dataset-Specific Fields

See individual schema files in `schemas/` for dataset-specific field definitions.