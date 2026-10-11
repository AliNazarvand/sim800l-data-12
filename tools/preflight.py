#!/usr/bin/env python3
"""preflight.py — quick sanity checks before CI validation."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SCHEMAS = ROOT / "schemas"

issues = []
for i in range(1, 19):
    dat_id = f"dat_{i:02d}"
    if not (SCHEMAS / f"{dat_id}.schema.yaml").exists():
        issues.append(f"missing schema: {dat_id}.schema.yaml")
    found = list(DATA.glob(f"{dat_id}_*.yaml"))
    if not found:
        issues.append(f"missing data file for {dat_id}")

if issues:
    print("Preflight issues:")
    for i in issues:
        print(" -", i)
    sys.exit(1)
print("Preflight OK")
