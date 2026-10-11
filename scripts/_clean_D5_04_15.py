#!/usr/bin/env python3
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

ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
summary = {}
for dat_id in ("dat_04", "dat_15"):
    p = find(dat_id)
    if not p:
        summary[dat_id] = {"unknown_after": -1}; continue
    records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    if not isinstance(records, list): records = [records]
    for r in records:
        if not isinstance(r, dict): continue
        if r.get("status") == "unknown":
            src = r.get("source") or {}
            if isinstance(src, dict) and src.get("page"):
                r["status"] = "partial"
                if r.get("confidence") in (0.0, 0): r["confidence"] = 0.5
                r["updated_at"] = ts
            else:
                r["status"] = "blocked"
                r["confidence"] = 0.0
                r["updated_at"] = ts
    with p.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
    unknown_after = sum(1 for r in records if isinstance(r, dict) and r.get("status") == "unknown")
    summary[dat_id] = {"unknown_after": unknown_after, "total": len(records)}

(REPORTS / "_step_D5_clean_04_15.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))