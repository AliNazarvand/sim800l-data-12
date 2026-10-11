#!/usr/bin/env python3
"""Apply limit_reason to all records of a dataset. Idempotent."""
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
    return c[0] if c else None

if len(sys.argv) < 3:
    print("usage: _d13_apply_reason.py <dat_id> <reason>"); sys.exit(2)

dat_id = sys.argv[1]
reason = sys.argv[2]
p = find(dat_id)
if not p:
    print(f"{dat_id} not found"); sys.exit(1)

records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
applied = 0
skipped = 0
tag = f"limit_reason: {reason}"
for r in records:
    if not isinstance(r, dict): continue
    notes = r.get("notes") or ""
    if "limit_reason:" in notes:
        skipped += 1
        continue
    r["notes"] = (notes + " | " + tag).strip(" |")
    r["updated_at"] = ts
    applied += 1

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)

summary = {"dat_id": dat_id, "applied": applied, "skipped": skipped, "total": len(records)}
(REPORTS / f"_d13_{dat_id}_reason.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{dat_id}: applied={applied} skipped={skipped} total={len(records)}")