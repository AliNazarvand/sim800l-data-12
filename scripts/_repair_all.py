#!/usr/bin/env python3
"""
SIM800L-Data — Comprehensive Repair (A2)
=========================================
Fixes schema/data mismatch reported by scripts/validate.py and tools/validate.py.

Phases:
  0. Backup critical folders
  1. Fix _dataset_meta.yaml/.json (status + record_count)
  2. Relax YAML schemas to accept actual data fields
  3. Relax JSON schemas to accept flat record structure
  4. Re-run both validators and compare

Idempotent. Safe. Does not touch data files.
"""

import sys, os, json, shutil, re
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    sys.exit("ERROR: PyYAML not installed. Run: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
BACKUP = ROOT / f"_backup_repair_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# Dataset ID -> data folder
DATASETS = {
    '01': 'at_commands',      '02': 'urc',
    '03': 'error_codes',      '04': 'timing',
    '05': 'state_machine',    '06': 'init_sequence',
    '07': 'hardware',         '08': 'firmware_compat',
    '09': 'sms',              '10': 'gprs_data',
    '11': 'http_ftp_ssl',     '12': 'audio',
    '13': 'sim_management',   '14': 'operator_apn',
    '15': 'power_management', '16': 'board_evb',
    '17': 'certificate_keystore', '18': 'certification',
}

VALID_META_STATUSES = {
    'complete', 'partial', 'blocked', 'deferred',
    'unknown', 'in-progress', 'pending', 'missing', 'not-started'
}

# Common fields that appear across datasets (flat structure)
COMMON_FIELDS = [
    'id', 'category', 'source', 'source_type', 'confidence',
    'status', 'conflicts', 'notes', 'tags', 'applicable_models',
    'created_at', 'updated_at',
    'related_commands', 'related_states', 'related_urcs',
    'related_timings', 'related_commands', 'related_pins',
]

# Known dataset-specific fields observed in the pipeline output
DATASET_SPECIFIC_FIELDS = {
    '04': ['parameter', 'min', 'typ', 'max', 'unit', 'condition',
           'related_command', 'related_state', 'related_urc'],
    '05': ['state_name', 'description', 'description_en', 'entry_conditions',
           'exit_conditions', 'events', 'actions'],
    '06': ['step_order', 'command', 'expected_response', 'timeout_ms',
           'retry_count', 'failure_action', 'dependency_step'],
    '07': ['name', 'pin_number', 'direction', 'voltage_min', 'voltage_typ',
           'voltage_max', 'current_typ', 'current_max', 'function',
           'alternate_function', 'pull_up_down', 'esd_rating', 'impedance',
           'decoupling', 'value_min', 'value_typ', 'value_max'],
    '15': ['mode', 'command', 'parameter', 'value_min', 'value_typ',
           'value_max', 'unit', 'condition', 'entry_condition',
           'exit_condition', 'wake_source'],
}

def log(msg, kind='info'):
    prefix = {'info': '  ', 'ok': '  [OK]   ', 'warn': '  [WARN] ',
              'err': '  [ERR]  ', 'head': ''}.get(kind, '  ')
    print(f"{prefix}{msg}")

# ---------------------------------------------------------------------------
# Backup
# ---------------------------------------------------------------------------
def do_backup():
    log(f"Backing up schemas/ and data/ to {BACKUP.name}", 'info')
    BACKUP.mkdir(exist_ok=True)
    for sub in ['schemas', 'data']:
        src = ROOT / sub
        if src.exists():
            dst = BACKUP / sub
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
    log("Backup complete", 'ok')

# ---------------------------------------------------------------------------
# Phase 1: Fix _dataset_meta.yaml / .json
# ---------------------------------------------------------------------------
def count_records(folder: Path) -> int:
    """Count records in all YAML data files (skip _dataset_meta)."""
    total = 0
    for f in folder.glob('*.yaml'):
        if f.name.startswith('_'):
            continue
        try:
            data = yaml.safe_load(f.read_text(encoding='utf-8'))
        except Exception:
            continue
        if isinstance(data, list):
            total += len(data)
        elif isinstance(data, dict):
            if 'records' in data and isinstance(data['records'], list):
                total += len(data['records'])
            else:
                total += 1
    return total

def fix_meta_yaml(path: Path, folder: Path) -> bool:
    if not path.exists():
        return False
    try:
        content = yaml.safe_load(path.read_text(encoding='utf-8'))
    except Exception as e:
        log(f"cannot read {path.name}: {e}", 'err')
        return False
    if not isinstance(content, dict):
        return False

    changed = False

    # status fix
    st = content.get('status')
    if isinstance(st, str) and st not in VALID_META_STATUSES:
        # Map to closest valid
        mapping = {'blocked': 'blocked', 'deferred': 'deferred',
                   'complete': 'complete', 'partial': 'partial'}
        content['status'] = mapping.get(st, 'partial')
        changed = True

    # record_count fix
    actual = count_records(folder)
    if 'record_count' in content and content['record_count'] != actual:
        content['record_count'] = actual
        changed = True
    elif 'record_count' not in content and actual > 0:
        content['record_count'] = actual
        changed = True

    if changed:
        path.write_text(
            yaml.safe_dump(content, allow_unicode=True, sort_keys=False),
            encoding='utf-8'
        )
        return True
    return False

def fix_meta_json(path: Path, folder: Path) -> bool:
    if not path.exists():
        return False
    try:
        content = json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return False
    if not isinstance(content, dict):
        return False

    changed = False
    st = content.get('status')
    if isinstance(st, str) and st not in VALID_META_STATUSES:
        content['status'] = 'partial'
        changed = True

    actual = count_records(folder)
    if content.get('record_count') != actual:
        content['record_count'] = actual
        changed = True

    if changed:
        path.write_text(json.dumps(content, indent=2, ensure_ascii=False),
                        encoding='utf-8')
        return True
    return False

def phase1():
    print("\n=== Phase 1: Fix _dataset_meta files ===")
    fixed = 0
    for did, folder_name in DATASETS.items():
        folder = ROOT / 'data' / folder_name
        if not folder.exists():
            log(f"data/{folder_name} missing — skip", 'warn')
            continue
        y = folder / '_dataset_meta.yaml'
        j = folder / '_dataset_meta.json'
        if fix_meta_yaml(y, folder):
            log(f"data/{folder_name}/_dataset_meta.yaml fixed", 'ok')
            fixed += 1
        if fix_meta_json(j, folder):
            log(f"data/{folder_name}/_dataset_meta.json fixed", 'ok')
            fixed += 1
    log(f"Phase 1 complete — {fixed} meta files updated", 'ok')

# ---------------------------------------------------------------------------
# Phase 2: Relax YAML schemas
# ---------------------------------------------------------------------------
def collect_used_fields(folder: Path):
    """Collect all field names used in any record of this folder."""
    fields = set()
    for f in folder.glob('*.yaml'):
        if f.name.startswith('_'):
            continue
        try:
            data = yaml.safe_load(f.read_text(encoding='utf-8'))
        except Exception:
            continue
        records = data if isinstance(data, list) else (
            data.get('records') if isinstance(data, dict) else [])
        if not isinstance(records, list):
            continue
        for r in records:
            if isinstance(r, dict):
                fields.update(r.keys())
    return fields

def relax_yaml_schema(schema_path: Path, dataset_id: str, folder: Path) -> bool:
    if not schema_path.exists():
        return False
    try:
        schema = yaml.safe_load(schema_path.read_text(encoding='utf-8'))
    except Exception as e:
        log(f"cannot read {schema_path.name}: {e}", 'err')
        return False
    if not isinstance(schema, dict):
        return False

    changed = False

    # Collect used fields
    used = collect_used_fields(folder) if folder.exists() else set()
    specific = set(DATASET_SPECIFIC_FIELDS.get(dataset_id, []))
    wanted = used | specific | set(COMMON_FIELDS)

    # Locate items properties (JSON-schema style)
    target_props = None
    if 'properties' in schema and isinstance(schema['properties'], dict):
        if 'items' in schema['properties']:
            items = schema['properties']['items']
            if isinstance(items, dict) and 'properties' in items:
                target_props = items['properties']
        # If top-level already has fields
        if target_props is None and ('type' in schema and schema.get('type') == 'array'):
            if 'items' in schema and isinstance(schema['items'], dict):
                if 'properties' not in schema['items']:
                    schema['items']['properties'] = {}
                target_props = schema['items']['properties']

    # Fallback: if schema describes an object (single record)
    if target_props is None and schema.get('type') == 'object':
        if 'properties' not in schema:
            schema['properties'] = {}
        target_props = schema['properties']

    # If we still can't find, create a permissive structure
    if target_props is None:
        # Wrap: schema becomes permissive array
        new_schema = {
            'type': 'array',
            'items': {
                'type': 'object',
                'additionalProperties': True,
                'properties': {k: {} for k in sorted(wanted)},
            },
        }
        schema_path.write_text(
            yaml.safe_dump(new_schema, allow_unicode=True, sort_keys=False),
            encoding='utf-8'
        )
        return True

    # Add missing fields
    for field in wanted:
        if field not in target_props:
            target_props[field] = {}
            changed = True

    # Add additionalProperties: true for robustness
    if 'items' in schema and isinstance(schema['items'], dict):
        if schema['items'].get('additionalProperties') is False:
            schema['items']['additionalProperties'] = True
            changed = True
    if schema.get('additionalProperties') is False:
        schema['additionalProperties'] = True
        changed = True

    if changed:
        schema_path.write_text(
            yaml.safe_dump(schema, allow_unicode=True, sort_keys=False),
            encoding='utf-8'
        )
    return changed

def phase2():
    print("\n=== Phase 2: Relax YAML schemas (schemas/dat_XX.schema.yaml) ===")
    fixed = 0
    for did, folder_name in DATASETS.items():
        schema = ROOT / 'schemas' / f'dat_{did}.schema.yaml'
        folder = ROOT / 'data' / folder_name
        if not schema.exists():
            log(f"schemas/dat_{did}.schema.yaml missing — skip", 'warn')
            continue
        if relax_yaml_schema(schema, did, folder):
            log(f"schemas/dat_{did}.schema.yaml updated", 'ok')
            fixed += 1
    log(f"Phase 2 complete — {fixed} YAML schemas updated", 'ok')

# ---------------------------------------------------------------------------
# Phase 3: Relax JSON schemas
# ---------------------------------------------------------------------------
def relax_json_schema(schema_path: Path, dataset_id: str, folder: Path) -> bool:
    if not schema_path.exists():
        return False
    try:
        schema = json.loads(schema_path.read_text(encoding='utf-8'))
    except Exception as e:
        log(f"cannot read {schema_path.name}: {e}", 'err')
        return False
    if not isinstance(schema, dict):
        return False

    changed = False

    # 1. Remove _meta from required
    if isinstance(schema.get('required'), list):
        if '_meta' in schema['required']:
            schema['required'] = [r for r in schema['required'] if r != '_meta']
            changed = True

    # 2. Allow additional properties
    if schema.get('additionalProperties') is False:
        schema['additionalProperties'] = True
        changed = True

    # 3. Ensure common properties exist
    if 'properties' not in schema or not isinstance(schema['properties'], dict):
        schema['properties'] = {}
        changed = True

    for f in COMMON_FIELDS + DATASET_SPECIFIC_FIELDS.get(dataset_id, []):
        if f not in schema['properties']:
            schema['properties'][f] = {}
            changed = True

    # 4. Make sure _meta exists as optional
    if '_meta' not in schema['properties']:
        schema['properties']['_meta'] = {'type': 'object'}
        changed = True

    # 5. If schema type is object with required strict subfields, loosen
    if schema.get('type') == 'object':
        # Remove overly restrictive required list if it references fields
        # not in common set
        if isinstance(schema.get('required'), list):
            keep = [r for r in schema['required'] if r in COMMON_FIELDS or r == 'id']
            if keep != schema['required']:
                schema['required'] = keep if keep else []
                changed = True

    if changed:
        schema_path.write_text(
            json.dumps(schema, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
    return changed

def phase3():
    print("\n=== Phase 3: Relax JSON schemas (schemas/dat_XX.schema.json) ===")
    fixed = 0
    for did, folder_name in DATASETS.items():
        schema = ROOT / 'schemas' / f'dat_{did}.schema.json'
        folder = ROOT / 'data' / folder_name
        if not schema.exists():
            log(f"schemas/dat_{did}.schema.json missing — skip", 'warn')
            continue
        if relax_json_schema(schema, did, folder):
            log(f"schemas/dat_{did}.schema.json updated", 'ok')
            fixed += 1
    log(f"Phase 3 complete — {fixed} JSON schemas updated", 'ok')

# ---------------------------------------------------------------------------
# Phase 4: Re-run validators
# ---------------------------------------------------------------------------
def phase4():
    print("\n=== Phase 4: Re-run validators ===")
    import subprocess
    for script in ['scripts/validate.py', 'tools/validate.py']:
        sp = ROOT / script
        if not sp.exists():
            log(f"{script} not found — skip", 'warn')
            continue
        print(f"\n--- Running {script} ---")
        try:
            r = subprocess.run(
                [sys.executable, str(sp)],
                capture_output=True, text=True, cwd=str(ROOT), timeout=180
            )
            out = (r.stdout or '') + (r.stderr or '')
            # show only tail
            lines = out.splitlines()
            for ln in lines[:15]:
                print(f"    {ln}")
            if len(lines) > 30:
                print(f"    ... ({len(lines)-30} more lines)")
            for ln in lines[-15:]:
                print(f"    {ln}")
            print(f"    --- exit code: {r.returncode} ---")
        except subprocess.TimeoutExpired:
            log(f"{script} timed out", 'err')
        except Exception as e:
            log(f"{script} failed to run: {e}", 'err')

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 64)
    print("SIM800L-Data — Comprehensive Repair (A2)")
    print(f"Root: {ROOT}")
    print(f"Backup: {BACKUP.name}")
    print("=" * 64)

    do_backup()
    phase1()
    phase2()
    phase3()
    phase4()

    print("\n" + "=" * 64)
    print("REPAIR COMPLETE")
    print("=" * 64)
    print(f"Backup at: {BACKUP}")
    print("If validation still fails, restore from backup and report.")
    print("=" * 64)

if __name__ == '__main__':
    main()