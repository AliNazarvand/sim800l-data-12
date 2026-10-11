#!/usr/bin/env python3
"""Safe cleanup of dat_01 and dat_07: parse YAML, clear invalid source fields,
   set status=unknown, confidence=0.0, track ids for TODO."""
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

def clean_source(src):
    """Return (changed, src) after clearing invalid page/section/quote."""
    changed = False
    if not isinstance(src, dict):
        return False, src
    page = src.get("page")
    if page in INVALID_PAGE:
        if "page" in src:
            del src["page"]
            changed = True
    section = src.get("section")
    if section in INVALID_SECTION:
        if "section" in src:
            del src["section"]
            changed = True
    # Normalize quote: if it looks like garbage (no real text), clear it
    quote = src.get("quote")
    if quote is None:
        src["quote"] = ""
    return changed, src

def process(dat_id):
    path = DATA / f"{dat_id}.yaml"
    if not path.exists():
        return {"dat_id": dat_id, "modified_ids": [], "count": 0, "note": "file missing"}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"dat_id": dat_id, "modified_ids": [], "count": 0, "note": f"parse error: {e}"}
    if data is None:
        return {"dat_id": dat_id, "modified_ids": [], "count": 0, "note": "empty"}
    records = data if isinstance(data, list) else [data]
    modified_ids = []
    for rec in records:
        if not isinstance(rec, dict):
            continue
        src = rec.get("source") or {}
        changed, src = clean_source(src)
        rec["source"] = src
        # If any invalid source data was found, mark record as unknown
        if changed:
            rec["status"] = "unknown"
            rec["confidence"] = 0.0
            rid = rec.get("id", "?")
            modified_ids.append(rid)
    # Write back preserving list shape
    with path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False,
                       default_flow_style=False, width=1000)
    return {"dat_id": dat_id, "modified_ids": modified_ids,
            "count": len(modified_ids), "note": "ok"}

results = [process("dat_01"), process("dat_07")]

out = REPORTS / "_step1_fix_report.json"
out.write_text(json.dumps({"results": results}, ensure_ascii=False, indent=2), encoding="utf-8")

for r in results:
    print(f"{r['dat_id']}: modified {r['count']} records ({r['note']})")
print(f"Report written to: {out}")