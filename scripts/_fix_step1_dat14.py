#!/usr/bin/env python3
"""Fix dat_14: ensure source_type=external, confidence<=0.7, applicable_models contains SIM800L.
   Idempotent. Does not touch other datasets."""
import sys
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

def find_data_file(dat_id):
    candidates = sorted(DATA.glob(f"{dat_id}_*.yaml"))
    if candidates:
        return candidates[0]
    exact = DATA / f"{dat_id}.yaml"
    if exact.exists():
        return exact
    return None

def process():
    path = find_data_file("dat_14")
    if path is None:
        return {"file": None, "count": 0, "note": "file missing"}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"file": path.name, "count": 0, "note": f"parse error: {e}"}
    if data is None:
        return {"file": path.name, "count": 0, "note": "empty"}
    records = data if isinstance(data, list) else [data]
    modified = 0
    for rec in records:
        if not isinstance(rec, dict):
            continue
        changed = False
        # R1: applicable_models must include SIM800L
        models = rec.get("applicable_models") or []
        if "SIM800L" not in models:
            models = list(models) + ["SIM800L"]
            rec["applicable_models"] = models
            changed = True
        # R6: source_type=external
        if rec.get("source_type") != "external":
            rec["source_type"] = "external"
            changed = True
        # R6: confidence <= 0.7
        conf = rec.get("confidence")
        if not isinstance(conf, (int, float)) or conf > 0.7:
            rec["confidence"] = 0.7 if (isinstance(conf, (int, float)) and conf > 0.7) else 0.5
            changed = True
        if changed:
            modified += 1
    if modified:
        with path.open("w", encoding="utf-8", newline="\n") as f:
            yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False,
                           default_flow_style=False, width=1000)
    return {"file": path.name, "count": modified,
            "total_records": len(records), "note": "ok"}

r = process()
out = REPORTS / "_step1_dat14_report.json"
out.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_14 ({r.get('file')}): {r.get('count')} modified of {r.get('total_records', 0)} total ({r.get('note')})")