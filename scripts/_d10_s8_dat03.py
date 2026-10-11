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

RECOVERY_EXT = {
    1:["Check phone is not busy"], 2:["Check operator definition"],
    3:["Check operator is allowed"], 4:["Check operation is supported"],
    5:["Check PH-SIM PIN is entered correctly"], 6:["Enter PH-FSIM PIN"],
    7:["Enter PH-FSIM PUK"], 8:["Check wait timer"], 9:["Check SIM state"],
    10:["Insert SIM"], 11:["Enter SIM PIN"], 12:["Enter SIM PUK"],
    13:["Check SIM contacts"], 14:["Wait for SIM init"], 15:["Replace SIM"],
    16:["Check SIM is not blocked"], 17:["Enter PIN2"], 18:["Enter PUK2"],
    19:["PH-FSIM PIN required"], 20:["Check subscription"],
    21:["Check MT is locked"], 22:["Check SIM is not blocked (CCK)"],
    23:["Check parameters are within range"], 24:["Check command syntax"],
    25:["Check SIM index"], 26:["Check SIM dial string"],
    27:["Check PUK2 attempts"], 28:["Check PIN2 attempts"],
    30:["Check network availability"], 31:["Check no MT call in progress"],
    32:["Check network registration"], 33:["Check call ID is valid"],
    40:["Check GPRS subscription"], 41:["Check GPRS subscription"],
    42:["Check parameters are supported"], 43:["Check parameter range"],
    44:["Check parameter value"], 45:["Check parameter format"],
    46:["Check command parameter"], 47:["Check SIM"],
    100:["Verify command parameters"], 101:["Check PDP context is not active"],
    102:["Check ME is not busy"], 103:["Check SIM is registered"],
    106:["Check ME IMEI"], 107:["Check GPRS allowed by subscription"],
    108:["Check GPRS not barred"], 109:["Check GPRS is active"],
    110:["Check PDP address"], 111:["Check PLMN is allowed"],
    112:["Check location area allowed"], 113:["Check roaming allowed"],
    114:["Check operator is allowed"], 115:["Check no network is available"],
    116:["Check PDP already active"], 117:["Check network registration"],
    118:["Check GPRS is not attached"], 119:["Check GPRS is attached"],
    120:["Check command is not supported"], 121:["Check congestion"],
    122:["Check response format"], 123:["Check CLI is available"],
    124:["Check service is not subscribed"], 125:["Check resource is unavailable"],
    126:["Check resource is restricted"], 127:["Check service is disabled"],
    128:["Check service is enabled"], 129:["Check operation is not allowed"],
    132:["Check GPRS attach status"], 133:["Check PDP context"],
    134:["Check service is not subscribed"], 135:["Check SIM is not inserted"],
    136:["Check bearer service"], 137:["Check MS class"],
    138:["Check network failure"], 139:["Check operation temporary failure"],
    140:["Check operator is not defined"], 141:["Check SAPI is invalid"],
    142:["Check LLC or SNDCP failure"], 143:["Check insufficient resources"],
    144:["Check missing or unknown APN"], 145:["Check unknown PDP address"],
    146:["Check operator determined barring"], 147:["Check regular deactivation"],
    148:["Check activation rejected"], 149:["Check MT does not support"],
    150:["Check service option is not supported"], 151:["Check service option is not subscribed"],
    152:["Check service option temporary out of order"], 153:["Check NSAPI already used"],
    154:["Check reactivation required"], 155:["Check feature not supported"],
    156:["Check semantic error in TFT"], 157:["Check syntactical error in TFT"],
    158:["Check bearer service not implemented"], 159:["Check multi-PDP not supported"],
    160:["Check multicast not supported"], 161:["Check error message"],
    162:["Check recovery on network failure"],
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
    steps = RECOVERY_EXT.get(ci)
    if steps:
        r["recovery_steps"] = steps
        r["updated_at"] = ts
        filled += 1

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
wr = sum(1 for r in records if isinstance(r, dict) and r.get("recovery_steps"))
(REPORTS / "_step_D10_dat03.json").write_text(json.dumps({"total":len(records),"with_recovery":wr,"filled":filled}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_03: total={len(records)} with_recovery={wr} filled={filled}")