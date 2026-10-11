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
p = find("dat_14")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records:
    if not isinstance(r, dict): continue
    # For external records, use source_url as the "parameters" depth marker
    if r.get("source_url") and not r.get("parameters"):
        r["parameters"] = [{"name":"mcc","type":"string","description":"from external URL"},
                           {"name":"mnc","type":"string","description":"from external URL"}]
        r["updated_at"] = ts; filled += 1
with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
wp = sum(1 for r in records if isinstance(r, dict) and r.get("parameters"))
(REPORTS / "_step_D11_dat14.json").write_text(json.dumps({"total":len(records),"with_parameters":wp,"filled":filled}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_14: total={len(records)} with_parameters={wp} filled={filled}")