#!/usr/bin/env python3
"""Step 1 final: clear source.date on records where it is empty/auto/None,
   mark them as unknown/0.0. Applies to ALL datasets. Idempotent."""
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

INVALID_DATE = {None, "", "auto"}

def find_data_file(dat_id):
    candidates = sorted(DATA.glob(f"{dat_id}_*.yaml"))
    if candidates:
        return candidates[0]
    exact = DATA / f"{dat_id}.yaml"
    if exact.exists():
        return exact
    return None

def process(dat_id):
    path = find_data_file(dat_id)
    if path is None:
        return {"dat_id": dat_id, "file": None, "count": 0, "ids": [], "note": "file missing"}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"dat_id": dat_id, "file": path.name, "count": 0, "ids": [],
                "note": f"parse error: {e}"}
    if data is None:
        return {"dat_id": dat_id, "file": path.name, "count": 0, "ids": [], "note": "empty"}
    records = data if isinstance(data, list) else [data]
    affected = []
    for rec in records:
        if not isinstance(rec, dict):
            continue
        src = rec.get("source") or {}
        d = src.get("date")
        if d in INVALID_DATE:
            if "date" in src:
                del src["date"]
            rec["status"] = "unknown"
            rec["confidence"] = 0.0
            affected.append(rec.get("id", "?"))
            rec["source"] = src
    if affected:
        with path.open("w", encoding="utf-8", newline="\n") as f:
            yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False,
                           default_flow_style=False, width=1000)
    return {"dat_id": dat_id, "file": path.name,
            "count": len(affected), "ids": affected, "note": "ok"}

results = []
for i in range(1, 19):
    results.append(process(f"dat_{i:02d}"))

out = REPORTS / "_step1_dates_fix_report.json"
out.write_text(json.dumps({"results": results}, ensure_ascii=False, indent=2), encoding="utf-8")

grand_total = 0
for r in results:
    if r["count"] > 0:
        print(f"{r['dat_id']} ({r['file']}): {r['count']} records")
    grand_total += r["count"]
print(f"TOTAL affected: {grand_total}")
print(f"Report: {out}")