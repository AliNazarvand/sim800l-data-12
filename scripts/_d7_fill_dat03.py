#!/usr/bin/env python3
"""Add recovery_steps for well-known error codes."""
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

# Well-known recovery recipes from SIMCom guidelines (documented in AT Manual context)
RECOVERY = {
    10: ["Check SIM card is inserted correctly", "Check SIM card is not damaged", "Restart module with AT+CFUN=1,1"],
    11: ["Enter SIM PIN with AT+CPIN=\"<pin>\""],
    12: ["Enter SIM PUK with AT+CPIN=\"<puk>\""],
    13: ["Check SIM contacts", "Replace SIM card if faulty"],
    14: ["Wait for SIM to finish initialization", "Retry the command"],
    15: ["Replace SIM card (wrong SIM)"],
    16: ["Check SIM is not blocked"],
    17: ["Enter PIN2 with AT+CPIN=\"<pin2>\""],
    18: ["Enter PUK2 with AT+CPIN=\"<puk2>\""],
    20: ["Verify subscription plan is valid"],
    21: ["Check MT is not locked to another network"],
    22: ["Check SIM is not blocked (CCK)"],
    30: ["Check network availability", "Wait and retry"],
    31: ["Check no MT call is in progress"],
    32: ["Verify network registration with AT+CREG?"],
    40: ["Check subscription has GPRS enabled"],
    41: ["Check subscription has GPRS enabled"],
    42: ["Check parameters are supported by network"],
    100: ["Verify command parameters are correct"],
    103: ["Check SIM is registered with network"],
    106: ["Check ME has valid IMEI"],
    107: ["Check subscription allows GPRS"],
    111: ["Check PLMN is allowed"],
    112: ["Check location area is allowed"],
    113: ["Check roaming is allowed"],
    132: ["Check GPRS attach status with AT+CGATT?"],
    133: ["Check PDP context definition with AT+CGDCONT"],
    148: ["Check PDP context parameters"],
    149: ["Check MT supports the requested feature"],
}

p = find("dat_03")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("recovery_steps"): continue
    code = r.get("code")
    try: ci = int(code)
    except Exception: continue
    steps = RECOVERY.get(ci)
    if steps:
        r["recovery_steps"] = steps
        r["updated_at"] = ts
        filled += 1

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
with_steps = sum(1 for r in records if isinstance(r, dict) and r.get("recovery_steps"))
summary = {"total": len(records), "with_recovery": with_steps, "filled": filled}
(REPORTS / "_step_D7_dat03.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_03: total={len(records)} with_recovery={with_steps} filled={filled}")