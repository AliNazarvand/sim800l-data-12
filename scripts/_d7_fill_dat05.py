#!/usr/bin/env python3
"""Fill dat_05 related_commands based on state name."""
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

STATE_CMDS = {
    "OFF": ["AT+CFUN=0"],
    "POWER_ON": ["AT", "AT+CFUN=1", "AT+CPIN?"],
    "SIM_READY": ["AT+CPIN?", "AT+CIMI", "AT+CCID"],
    "NETWORK_SEARCH": ["AT+CREG?", "AT+CGREG?", "AT+COPS?"],
    "REGISTERED": ["AT+CREG?", "AT+CSQ"],
    "PDP_ACTIVE": ["AT+CGATT?", "AT+CGDCONT", "AT+CIICR"],
    "DATA_MODE": ["AT+CIPSTART", "AT+CIPSEND", "AT+CIPCLOSE"],
    "SMS_MODE": ["AT+CMGF", "AT+CMGS", "AT+CMGR"],
    "CALL_MODE": ["ATD", "ATA", "ATH"],
    "SLEEP": ["AT+CSCLK=1", "AT+CFUN=0"],
    "CHARGE": ["AT+CBC"],
    "ERROR": ["AT+CFUN=1,1"],
}

p = find("dat_05")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("related_commands"): continue
    name = (r.get("state_name") or "").upper()
    cmds = STATE_CMDS.get(name)
    if cmds:
        r["related_commands"] = cmds
        r["updated_at"] = ts
        filled += 1

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
with_cmds = sum(1 for r in records if isinstance(r, dict) and r.get("related_commands"))
summary = {"total": len(records), "with_related_commands": with_cmds, "filled": filled}
(REPORTS / "_step_D7_dat05.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_05: total={len(records)} with_related_commands={with_cmds} filled={filled}")