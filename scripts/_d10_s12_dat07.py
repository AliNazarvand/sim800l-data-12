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
    return c[0] if c else None
p = find("dat_07")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("function"): continue
    name = r.get("name") or ""
    cat = r.get("category") or ""
    if name:
        r["function"] = f"{cat}: {name}"
        r["updated_at"] = ts
        filled += 1
    elif cat:
        r["function"] = cat
        r["updated_at"] = ts
        filled += 1

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
wf = sum(1 for r in records if isinstance(r, dict) and r.get("function"))
(REPORTS / "_step_D10_dat07.json").write_text(json.dumps({"total":len(records),"with_function":wf,"filled":filled}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_07: total={len(records)} with_function={wf} filled={filled}")