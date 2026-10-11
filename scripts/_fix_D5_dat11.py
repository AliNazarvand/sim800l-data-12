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

p = find("dat_11")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
converted = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("status") == "unknown":
        r["status"] = "blocked"
        r["confidence"] = 0.0
        notes = r.get("notes") or ""
        marker = "Specialist source required (HTTP/FTP/SSL Manual)"
        if marker not in notes:
            r["notes"] = (notes + " | " + marker + ". Not in AT Manual V1.01.").strip(" |")
        r["updated_at"] = ts
        converted += 1

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)

remaining_unknown = sum(1 for r in records if isinstance(r, dict) and r.get("status") == "unknown")
summary = {"total": len(records), "converted": converted, "remaining_unknown": remaining_unknown}
(REPORTS / "_step_D5_dat11.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_11: converted={converted} remaining_unknown={remaining_unknown}")