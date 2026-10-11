#!/usr/bin/env python3
"""Diagnose dat_15: count, status distribution, sample."""
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

path = find("dat_15")
if path is None:
    print("dat_15 file not found"); sys.exit(1)
records = yaml.safe_load(path.read_text(encoding="utf-8")) or []
if not isinstance(records, list):
    records = [records]
from collections import Counter
status_counts = Counter(r.get("status") for r in records if isinstance(r, dict))
cat_counts = Counter(r.get("category") for r in records if isinstance(r, dict))
sample = records[0] if records else None
report = {
    "file": path.name,
    "total": len(records),
    "status_counts": dict(status_counts),
    "category_counts": dict(cat_counts),
    "sample_record": sample
}
out = REPORTS / "_step_A2_dat15_diagnosis.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
print(json.dumps({
    "total": len(records),
    "status_counts": dict(status_counts),
    "category_counts": dict(cat_counts)
}, ensure_ascii=False, indent=2))