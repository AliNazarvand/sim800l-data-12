#!/usr/bin/env python3
"""Finalize dataset: mark records without source as blocked (no data loss)."""
import sys, json
from pathlib import Path
from datetime import datetime, timezone
try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr); sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml"))
    return c[0] if c else (DATA / (dat_id + ".yaml") if (DATA / (dat_id + ".yaml")).exists() else None)

dat_id = sys.argv[1]
out_json = sys.argv[2]
reason = sys.argv[3] if len(sys.argv) > 3 else "No source found in available documents"

p = find(dat_id)
if not p:
    print(f"{dat_id} not found"); sys.exit(1)
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
converted = 0
for r in records:
    if not isinstance(r, dict): continue
    src = r.get("source") or {}
    has_page = isinstance(src, dict) and src.get("page")
    if has_page: continue
    if r.get("status") in (None, "unknown", "partial"):
        r["status"] = "blocked"
        r["confidence"] = 0.0
        notes = r.get("notes") or ""
        if reason not in notes:
            r["notes"] = (notes + " | " + reason + ".").strip(" |")
        r["updated_at"] = ts
        converted += 1

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)

unknown = sum(1 for r in records if isinstance(r, dict) and r.get("status") == "unknown")
blocked_c = sum(1 for r in records if isinstance(r, dict) and r.get("status") == "blocked")
partial = sum(1 for r in records if isinstance(r, dict) and r.get("status") == "partial")
summary = {"total": len(records), "converted": converted, "unknown": unknown, "blocked": blocked_c, "partial": partial}
(REPORTS / out_json).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{dat_id}: total={len(records)} converted={converted} unknown={unknown} blocked={blocked_c} partial={partial}")