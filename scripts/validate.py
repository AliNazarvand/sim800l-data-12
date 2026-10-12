#!/usr/bin/env python3
"""Validate YAML datasets (4-level) for the sim800l-data project.

Level 1: schema validation
Level 2: business logic (id uniqueness, source presence, applicable_models)
Level 3: cross-reference (URC/error/command links)
Level 4: consistency (timestamps, no example-only in data/)
"""
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
    import jsonschema
except ImportError as exc:
    print(f"[FATAL] Missing dependency: {exc}", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = ROOT / "schemas"
DATA_DIR = ROOT / "data"

ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z?)?$")
ID_RE = re.compile(r"^dat_\d{2}_\d{4}$")


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def as_list(x):
    if x is None:
        return []
    if isinstance(x, list):
        return x
    return [x]


def level1(data, schema, name):
    errors = []
    for idx, record in enumerate(as_list(data)):
        try:
            jsonschema.validate(instance=record, schema=schema)
        except jsonschema.ValidationError as exc:
            errors.append(f"L1 {name}[{idx}]: {exc.message}")
    return errors


def level2(data, name):
    errors = []
    seen = set()
    for idx, record in enumerate(as_list(data)):
        if not isinstance(record, dict):
            continue
        rid = record.get("id")
        if not rid:
            errors.append(f"L2 {name}[{idx}]: missing id")
            continue
        if not ID_RE.match(str(rid)):
            errors.append(f"L2 {name}[{idx}]: invalid id format: {rid}")
        if rid in seen:
            errors.append(f"L2 {name}[{idx}]: duplicate id: {rid}")
        seen.add(rid)
        if not record.get("source"):
            errors.append(f"L2 {name}[{idx}]: missing source")
        if "SIM800L" not in (record.get("applicable_models") or []):
            errors.append(f"L2 {name}[{idx}]: applicable_models missing SIM800L")
    return errors


def level3(all_data):
    """Cross-ref: commands referenced in dependent datasets must exist in dat_01."""
    errors = []
    dat01 = all_data.get("dat_01_at_command") or all_data.get("dat_01") or []
    cmd_set = set()
    for r in as_list(dat01):
        if isinstance(r, dict) and r.get("command"):
            cmd_set.add(r["command"])
            cmd_set.add(r["command"].lstrip("+"))
    if not cmd_set:
        return errors  # dat_01 empty: L3 informational only
    for name, data in all_data.items():
        if name == "dat_01_at_command" or name == "dat_01":
            continue
        for idx, record in enumerate(as_list(data)):
            if not isinstance(record, dict):
                continue
            candidates = []
            if record.get("command"):
                candidates.append(record["command"])
            for c in as_list(record.get("related_commands")):
                candidates.append(c)
            for c in candidates:
                if c and c.startswith("+") and c not in cmd_set and c.lstrip("+") not in cmd_set:
                    errors.append(f"L3 {name}[{idx}]: command {c} not in dat_01")
    return errors


def level4(data, name):
    errors = []
    for idx, record in enumerate(as_list(data)):
        if not isinstance(record, dict):
            continue
        if record.get("status") == "example-only":
            errors.append(f"L4 {name}[{idx}]: example-only in data/ (R21 violation)")
        if record.get("status") == "synthetic":
            errors.append(f"L4 {name}[{idx}]: synthetic forbidden (R6 violation)")
        for f in ("created_at", "updated_at"):
            v = record.get(f)
            if v and not ISO_RE.match(str(v)):
                errors.append(f"L4 {name}[{idx}]: {f} not ISO 8601: {v}")
    return errors


def main():
    total = 0
    all_data = {}
    for schema_path in sorted(SCHEMAS_DIR.glob("dat_*.schema.yaml")):
        stem = schema_path.stem.replace(".schema", "")
        data_path = DATA_DIR / f"{stem}.yaml"
        try:
            schema = load_yaml(schema_path)
        except Exception as exc:
            print(f"[ERROR] L1 {stem}: schema parse failed: {exc}", file=sys.stderr)
            total += 1
            continue
        if not data_path.exists():
            continue
        try:
            data = load_yaml(data_path)
        except Exception as exc:
            print(f"[ERROR] L1 {stem}: data parse failed: {exc}", file=sys.stderr)
            total += 1
            continue
        all_data[stem] = data
        errs = []
        errs += level1(data, schema, stem)
        errs += level2(data, stem)
        errs += level4(data, stem)
        for e in errs:
            print(f"[ERROR] {e}", file=sys.stderr)
        total += len(errs)

    l3_errs = level3(all_data)
    for e in l3_errs:
        print(f"[ERROR] {e}", file=sys.stderr)
    total += len(l3_errs)

    if total:
        print(f"\nValidation FAILED: {total} error(s).", file=sys.stderr)
        return 1
    print("Validation PASSED: all datasets are schema-valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())