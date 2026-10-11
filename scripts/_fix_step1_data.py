#!/usr/bin/env python3
"""Safe cleanup of dat_01 and dat_07 with glob-aware file lookup."""
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

INVALID_PAGE = {"auto", "unknown", "", None}
INVALID_SECTION = {"auto-extracted", "unknown", "", None}

def find_data_file(dat_id):
    candidates = sorted(DATA.glob(f"{dat_id}_*.yaml"))
    if candidates:
        return candidates[0]
    exact = DATA / f"{dat_id}.yaml"
    if exact.exists():
        return exact
    return None

def clean_source(src):
    changed = False
    if not isinstance(src, dict):
        return False, src
    if src.get("page") in INVALID_PAGE and "page" in src:
        del src["page"]
        changed = True
    if src.get("section") in INVALID_SECTION and "section" in src:
        del src["section"]
        changed = True
    if src.get("quote") is None:
        src["quote"] = ""
    return changed, src

def process(dat_id):
    path = find_data_file(dat_id)
    if path is None:
        return {"dat_id": dat_id, "file": None, "modified_ids": [], "count": 0, "note": "file missing"}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"dat_id": dat_id, "file": path.name, "modified_ids": [], "count": 0,
                "note": f"parse error: {e}"}
    if data is None:
        return {"dat_id": dat_id, "file": path.name, "modified_ids": [], "count": 0, "note": "empty"}
    records = data if isinstance(data, list) else [data]
    modified_ids = []
    for rec in records:
        if not isinstance(rec, dict):
            continue
        src = rec.get("source") or {}
        changed, src = clean_source(src)
        rec["source"] = src
        if changed:
            rec["status"] = "unknown"
            rec["confidence"] = 0.0
            modified_ids.append(rec.get("id", "?"))
    with path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False,
                       default_flow_style=False, width=1000)
    return {"dat_id": dat_id, "file": path.name, "modified_ids": modified_ids,
            "count": len(modified_ids), "note": "ok"}

results = [process("dat_01"), process("dat_07")]

out = REPORTS / "_step1_fix_report.json"
out.write_text(json.dumps({"results": results}, ensure_ascii=False, indent=2), encoding="utf-8")

for r in results:
    print(f"{r['dat_id']} ({r['file']}): modified {r['count']} records ({r['note']})")
print(f"Report written to: {out}")