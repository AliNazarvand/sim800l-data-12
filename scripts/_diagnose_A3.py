#!/usr/bin/env python3
"""Diagnose dat_04, dat_05, dat_06: count, status distribution, whether values are filled."""
import json, sys
from pathlib import Path
try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr); sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml"))
    return c[0] if c else (DATA / (dat_id + ".yaml") if (DATA / (dat_id + ".yaml")).exists() else None)

from collections import Counter

report = {}
for ds in ["dat_04", "dat_05", "dat_06"]:
    p = find(ds)
    if p is None:
        report[ds] = {"file": None, "total": 0, "note": "missing"}
        continue
    records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    if not isinstance(records, list):
        records = [records]
    status_counts = Counter(r.get("status") for r in records if isinstance(r, dict))
    # آیا مقادیر عددی پر شده‌اند؟
    filled_values = 0
    empty_values = 0
    for r in records:
        if not isinstance(r, dict):
            continue
        # برای dat_04: value_min/typ/max یا min/typ/max
        # برای dat_05: state_name + description
        # برای dat_06: step_order + command
        has_data = False
        for k in ("value_min","value_typ","value_max","min","typ","max","state_name","step_order","command"):
            v = r.get(k)
            if v is not None and v != "" and v != [] and v != {}:
                has_data = True
                break
        if has_data:
            filled_values += 1
        else:
            empty_values += 1
    # نمونه
    sample = records[0] if records else None
    report[ds] = {
        "file": p.name,
        "total": len(records),
        "status_counts": dict(status_counts),
        "filled_values": filled_values,
        "empty_values": empty_values,
        "sample_record": sample,
    }

out = REPORTS / "_step_A3_diagnosis.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

for ds in ["dat_04", "dat_05", "dat_06"]:
    r = report[ds]
    print(f"{ds}: file={r.get('file')} total={r.get('total')} status={r.get('status_counts')} "
          f"filled={r.get('filled_values')} empty={r.get('empty_values')}")