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
EXT = {
    200:["Check MS not support this command"], 201:["Check memory full"],
    202:["Check memory allocation failure"], 203:["Check modem not ready"],
    204:["Check unsupported operation"], 205:["Check invalid parameter"],
    206:["Check required SIM not present"], 207:["Check PIN required"],
    208:["Check PUK required"], 209:["Check SIM failure"],
    210:["Check SIM busy"], 211:["Check SIM wrong"], 212:["Check no network"],
    213:["Check network not registered"], 214:["Check no GPRS"],
    215:["Check no service"], 216:["Check call failure"],
    217:["Check SMS failure"], 218:["Check data failure"],
    219:["Check audio failure"], 220:["Check generic error"],
    300:["Check command parameters"], 301:["Check command syntax"],
    302:["Check modem state"], 303:["Check network state"],
    400:["Check UART flow control"], 401:["Check UART framing"],
    402:["Check baud rate"], 500:["Check module firmware"],
    501:["Check module hardware"], 502:["Check power supply"],
    600:["Check SIM card slot"], 601:["Check antenna connection"],
    700:["Check module reset"], 800:["Contact technical support"],
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
    steps = EXT.get(ci)
    if steps:
        r["recovery_steps"] = steps; r["updated_at"] = ts; filled += 1
with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
wr = sum(1 for r in records if isinstance(r, dict) and r.get("recovery_steps"))
(REPORTS / "_step_D11_dat03.json").write_text(json.dumps({"total":len(records),"with_recovery":wr,"filled":filled}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_03: total={len(records)} with_recovery={wr} filled={filled}")