# Validation Guide

## Prerequisites

- Python 3.11 or newer
- `pip`

## Install

```bash
pip install -r requirements.txt
```

## Preflight

```bash
python tools/preflight.py
```

Searches the repository root, `./sources/`, `./pdfs/`, and the parent folder
for the two primary source PDFs. Exit code 0 = both found; 1 = at least one
missing.

## Validate YAML against schemas

```bash
python tools/validate.py
```

- Validates every `data/**/*.yaml` against `schemas/<dataset>.schema.json`
  (when that schema file exists).
- Validates every `_dataset_meta.yaml` for required keys, status values,
  `record_count` consistency, and ISO 8601 dates.
- Enforces constant `_meta.license_note`, allowed `missing_reason` values,
  id pattern, and id uniqueness per dataset.

Exit code 0 = success. Exit code 1 = at least one error, printed to stderr.

## Generate JSON

```bash
python tools/generate_json.py
```

Writes a `.json` file next to every `data/**/*.yaml`, including
`_dataset_meta.yaml`.

### About the "AUTO-GENERATED — DO NOT EDIT" marker

The project brief asks for generated JSON files to carry the header string
`AUTO-GENERATED — DO NOT EDIT`. Standard JSON has **no comment syntax**, so a
literal `# ...` header would make the file unparseable and violate the
"machine-readable" requirement.

Instead, the marker is embedded as a reserved top-level key in every
generated file:

```json
{
  "_auto_generated": {
    "marker": "AUTO-GENERATED — DO NOT EDIT",
    "generator": "tools/generate_json.py"
  },
  ...payload...
}
```

Every consumer that reads a generated JSON can check
`obj["_auto_generated"]["marker"]` to detect an auto-generated file. The file
parses with any standard JSON library (`json.loads`, `jq`, etc.) without
special handling.

## Check mode (CI)

```bash
python tools/generate_json.py --check
```

Writes nothing. Exits non-zero if any JSON is missing or out of sync.

## Common errors

| Message | Cause | Fix |
|---|---|---|
| `missing dependency` | `pyyaml`/`jsonschema` not installed | `pip install -r requirements.txt` |
| `YAML parse error` | malformed YAML | fix YAML syntax |
| `record_count=... does not match actual ...` | stale `_dataset_meta.yaml` | update the meta |
| `status=deferred requires reason` | deferred without reason | add `reason:` |
| `_meta.license_note: must equal ...` | wrong constant | set the exact string |
| `DRIFT: ...` | generated JSON out of sync | re-run `tools/generate_json.py` |
## Phase 2 additions

`DATASET_MAP` in `tools/validate.py` now recognises all 18 datasets
(dat_01 .. dat_18). Datasets with `status: deferred` and `record_count: 0`
have their YAML files validated as empty `records: []` lists; the
`_dataset_meta.yaml` is still validated for required keys, status,
reason, and ISO date.

Deferred datasets require the following sources not currently present in
the repository:

- AT Command Manual: dat_01, dat_03, dat_08, dat_09, dat_10, dat_11,
  AT-part of dat_02, AT-part of dat_12, AT-part of dat_13.
- Secondary sources: dat_14, dat_17, dat_18 (Phase 2b).

Partial datasets (dat_02, dat_12, dat_13) list their pending AT fields
in `_dataset_meta.yaml.pending_fields`.
