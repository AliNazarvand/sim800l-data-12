#!/usr/bin/env python3
"""Diagnose dat_14: status distribution, source_type, confidence, sample."""
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
    c = sorted(DATA.glob(f"{dat_id}_*.yaml"))
    return c[0] if c else (DATA / f"{dat_id}.yaml" if (DATA / f"{dat_id}.yaml").exists() else None)

path = find("dat_14")
if path is None:
    print("dat_14 file not found"); sys.exit(1)
records = yaml.safe_load(path.read_text(encoding="utf-8")) or []
if not isinstance(records, list):
    records = [records]

from collections import Counter
status_counts = Counter(r.get("status") for r in records if isinstance(r, dict))
st_counts = Counter(r.get("source_type") for r in records if isinstance(r, dict))
conf_counts = Counter(r.get("confidence") for r in records if isinstance(r, dict))
models_ok = sum(1 for r in records if isinstance(r, dict) and "SIM800L" in (r.get("applicable_models") or []))

sample = records[0] if records else None

report = {
    "file": path.name,
    "total": len(records),
    "status_counts": dict(status_counts),
    "source_type_counts": dict(st_counts),
    "confidence_counts": {str(k): v for k, v in conf_counts.items()},
    "applicable_models_with_SIM800L": models_ok,
    "sample_record": sample
}
out = REPORTS / "_step2_dat14_diagnosis.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
print(json.dumps({
    "total": len(records),
    "status_counts": dict(status_counts),
    "source_type_counts": dict(st_counts),
    "confidence_counts": {str(k): v for k, v in conf_counts.items()},
    "models_ok": models_ok
}, ensure_ascii=False, indent=2))