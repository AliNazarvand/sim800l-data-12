#!/usr/bin/env python3
"""
fix_related_fields.py — افزودن فیلدهای related_* به دو schema.

فقط این سه فیلد اضافه می‌شوند:
  - dat_07.schema.yaml: related_commands, related_states
  - dat_13.schema.yaml: related_commands

هیچ چیز دیگری تغییر نمی‌کند.
"""
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"

FIXES = {
    "dat_07.schema.yaml": {
        "related_commands": {"type": "array", "items": {"type": "string"}},
        "related_states":   {"type": "array", "items": {"type": "string"}},
    },
    "dat_13.schema.yaml": {
        "related_commands": {"type": "array", "items": {"type": "string"}},
    },
}

total = 0
for fname, new_fields in FIXES.items():
    p = SCHEMAS / fname
    if not p.exists():
        print(f"[SKIP] {fname} not found")
        continue
    schema = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(schema, dict):
        print(f"[SKIP] {fname}: not a dict")
        continue
    props = schema.setdefault("properties", {})
    added = []
    for k, v in new_fields.items():
        if k not in props:
            props[k] = v
            added.append(k)
    if added:
        p.write_text(
            yaml.safe_dump(schema, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        total += len(added)
        print(f"[OK]   {fname}: added {', '.join(added)}")
    else:
        print(f"[SKIP] {fname}: all fields already present")

print(f"[OK]   fix_related_fields.py done ({total} fields added)")