#!/usr/bin/env python3
"""Schema and rule validator for sim800l-data.

Checks performed:
- YAML files parse
- Required common fields present
- id uniqueness within each dataset
- applicable_models contains SIM800L
- No records with status == 'synthetic'
- No records with status == 'example-only' inside data/
"""
import sys
import os
import glob
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")

REQUIRED = ["id", "category", "source", "source_type", "confidence",
            "status", "applicable_models"]

def fail(msg):
    print("ERROR:", msg)

def check_file(path):
    errors = []
    with open(path, "r", encoding="utf-8") as f:
        try:
            doc = yaml.safe_load(f) or {}
        except Exception as e:
            errors.append(f"{path}: YAML parse error: {e}")
            return errors
    records = doc.get("records", []) if isinstance(doc, dict) else doc
    if not isinstance(records, list):
        return errors
    seen_ids = set()
    for i, rec in enumerate(records):
        if not isinstance(rec, dict):
            errors.append(f"{path}: record {i} is not a mapping")
            continue
        for key in REQUIRED:
            if key not in rec:
                errors.append(f"{path}: record {i} missing field {key}")
        rid = rec.get("id")
        if rid:
            if rid in seen_ids:
                errors.append(f"{path}: duplicate id {rid}")
            seen_ids.add(rid)
        models = rec.get("applicable_models") or []
        if "SIM800L" not in models:
            errors.append(f"{path}: record {rid} does not list SIM800L")
        st = rec.get("status")
        if st == "synthetic":
            errors.append(f"{path}: record {rid} has forbidden status synthetic")
        if st == "example-only":
            errors.append(f"{path}: record {rid} has forbidden status example-only inside data/")
    return errors

def main():
    all_errors = []
    for path in glob.glob(os.path.join(DATA_DIR, "*.yaml")):
        all_errors.extend(check_file(path))
    if all_errors:
        for e in all_errors:
            fail(e)
        sys.exit(1)
    print("Validation OK")

if __name__ == "__main__":
    main()