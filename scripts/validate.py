#!/usr/bin/env python3
"""Validate YAML datasets (4-level) for the sim800l-data project.

Level 1: schema validation (jsonschema)
Level 2: business logic (id uniqueness, source presence, applicable_models)
Level 3: cross-reference (URCs -> commands, errors -> commands, etc.)
Level 4: consistency (timestamps, no `example-only` in data/, no synthetic)
"""
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
    import jsonschema
except ImportError as exc:
    print(f"[FATAL] Missing dependency: {exc}", file=sys.stderr)
    print("Install with: pip install pyyaml jsonschema", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = ROOT / "schemas"
DATA_DIR = ROOT / "data"

ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z?)?$")
ID_RE = re.compile(r"^dat_\d{2}_\d{4}$")


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def level1_schema(data: Any, schema: Any, name: str) -> list:
    errors = []
    if data is None:
        return errors
    if not isinstance(data, list):
        data = [data]
    for idx, record in enumerate(data):
        try:
            jsonschema.validate(instance=record, schema=schema)
        except jsonschema.ValidationError as exc:
            errors.append(f"L1 {name}[{idx}]: {exc.message}")
    return errors


def level2_business(data: Any, name: str) -> list:
    errors = []
    if not isinstance(data, list):
        return errors
    seen_ids = set()
    for idx, record in enumerate(data):
        if not isinstance(record, dict):
            continue
        rid = record.get("id")
        if not rid:
            errors.append(f"L2 {name}[{idx}]: missing id")
            continue
        if not ID_RE.match(str(rid)):
            errors.append(f"L2 {name}[{idx}]: invalid id format: {rid}")
        if rid in seen_ids:
            errors.append(f"L2 {name}[{idx}]: duplicate id: {rid}")
        seen_ids.add(rid)
        if not record.get("source"):
            errors.append(f"L2 {name}[{idx}]: missing source")
        models = record.get("applicable_models", [])
        if "SIM800L" not in models:
            errors.append(f"L2 {name}[{idx}]: applicable_models does not contain SIM800L")
    return errors


def level4_consistency(data: Any, name: str) -> list:
    errors = []
    if not isinstance(data, list):
        return errors
    for idx, record in enumerate(data):
        if not isinstance(record, dict):
            continue
        if record.get("status") == "example-only":
            errors.append(f"L4 {name}[{idx}]: example-only record found in data/ (R21 violation)")
        if record.get("status") == "synthetic":
            errors.append(f"L4 {name}[{idx}]: synthetic record forbidden (R6 violation)")
        for field in ("created_at", "updated_at"):
            v = record.get(field)
            if v and not ISO_RE.match(str(v)):
                errors.append(f"L4 {name}[{idx}]: {field} not ISO 8601: {v}")
    return errors


def main() -> int:
    total = 0
    all_data = {}
    for schema_path in sorted(SCHEMAS_DIR.glob("dat_*.schema.yaml")):
        stem = schema_path.stem.replace(".schema", "")
        data_path = DATA_DIR / f"{stem}.yaml"
        if not schema_path.exists():
            continue
        schema = load_yaml(schema_path)
        if not data_path.exists():
            print(f"[INFO] No data file for {stem}", file=sys.stderr)
            continue
        data = load_yaml(data_path)
        all_data[stem] = data
        errs = []
        errs += level1_schema(data, schema, stem)
        errs += level2_business(data, stem)
        errs += level4_consistency(data, stem)
        for e in errs:
            print(f"[ERROR] {e}", file=sys.stderr)
        total += len(errs)

    # Level 3: cross-ref
    # Build command index from dat_01
    dat01 = all_data.get("dat_01_at_command") or all_data.get("dat_01") or []
    if isinstance(dat01, list):
        cmd_index = {r.get("command") for r in dat01 if isinstance(r, dict) and r.get("command")}
    else:
        cmd_index = set()

    if cmd_index:
        for name, data in all_data.items():
            if not isinstance(data, list):
                continue
            for idx, record in enumerate(data):
                if not isinstance(record, dict):
                    continue
                cmds = []
                if record.get("command"):
                    cmds.append(record["command"])
                for c in record.get("related_commands", []) or []:
                    cmds.append(c)
                for c in cmds:
                    if c and c not in cmd_index and c.startswith("+"):
                        # Only warn, not error, since dat_01 may be incomplete
                        print(f"[WARN] L3 {name}[{idx}]: command {c} not in dat_01", file=sys.stderr)

    if total:
        print(f"\nValidation FAILED: {total} error(s).", file=sys.stderr)
        return 1
    print("Validation PASSED: all datasets are schema-valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())