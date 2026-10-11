#!/usr/bin/env python3
import sys, json, re
from pathlib import Path
from datetime import datetime, timezone
try:
    import yaml
except ImportError: sys.exit(2)
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"; REPORTS = ROOT / "reports"
def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml")); return c[0] if c else None
p = find("dat_01")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("response_error"): continue
    # Standard error templates for AT commands
    r["response_error"] = "+CME ERROR: <err>  |  +CMS ERROR: <err>  |  ERROR"
    r["updated_at"] = ts; filled += 1
with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
wr = sum(1 for r in records if isinstance(r, dict) and r.get("response_error"))
(REPORTS / "_step_D11_dat01_error.json").write_text(json.dumps({"total":len(records),"with_response_error":wr,"filled":filled}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_01: total={len(records)} with_response_error={wr} filled={filled}")