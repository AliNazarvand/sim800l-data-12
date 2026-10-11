#!/usr/bin/env python3
import sys, json
from pathlib import Path
from datetime import datetime, timezone
try:
    import yaml
except ImportError: sys.exit(2)
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"; REPORTS = ROOT / "reports"
def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml")); return c[0] if c else None
dat_id = sys.argv[1]
reason = sys.argv[2]
p = find(dat_id)
if not p: print(f"{dat_id} not found"); sys.exit(1)
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
for r in records:
    if not isinstance(r, dict): continue
    notes = r.get("notes") or ""
    tag = f"limit_reason: {reason}"
    if tag not in notes:
        r["notes"] = (notes + " | " + tag).strip(" |")
        r["updated_at"] = ts
with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
print(f"{dat_id}: applied limit_reason")