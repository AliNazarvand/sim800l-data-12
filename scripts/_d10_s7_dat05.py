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
STATE_URCS = {
    "OFF": [],
    "POWER_ON": ["RDY"],
    "SIM_READY": ["+CPIN"],
    "NETWORK_SEARCH": ["+CREG","+CGREG"],
    "REGISTERED": ["+CREG","+CGREG"],
    "PDP_ACTIVE": ["+PDP: DEACT"],
    "DATA_MODE": ["+CIPRXGET","+CIPCLOSE","+CIPSTATUS"],
    "SMS_MODE": ["+CMTI","+CMT","+CDS"],
    "CALL_MODE": ["RING","NO CARRIER","+CLIP"],
    "SLEEP": [],
    "CHARGE": [],
    "ERROR": ["+POWER DOWN"],
}
p = find("dat_05")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("related_urcs"): continue
    name = (r.get("state_name") or "").upper()
    urcs = STATE_URCS.get(name, [])
    if urcs:
        r["related_urcs"] = list(urcs)
        r["updated_at"] = ts
        filled += 1

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
wu = sum(1 for r in records if isinstance(r, dict) and r.get("related_urcs"))
(REPORTS / "_step_D10_dat05.json").write_text(json.dumps({"total":len(records),"with_related_urcs":wu,"filled":filled}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_05: total={len(records)} with_related_urcs={wu} filled={filled}")