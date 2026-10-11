#!/usr/bin/env python3
import sys, json, re
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
TOKEN_RE = re.compile(r"<([A-Za-z_][A-Za-z0-9_]*)>")

# specialist command -> typical params
SPECIALIST_PARAMS = {
    "HTTPINIT": [], "HTTPTERM": [],
    "HTTPPARA": [{"name":"para","type":"string","description":"parameter name"},{"name":"value","type":"string","description":"parameter value"}],
    "HTTPDATA": [{"name":"size","type":"integer","description":"data size"}],
    "HTTPACTION": [{"name":"method","type":"integer","description":"0=GET 1=POST 2=HEAD"}],
    "HTTPREAD": [{"name":"start","type":"integer","description":"start address"},{"name":"size","type":"integer","description":"read length"}],
    "HTTPHEAD": [{"name":"size","type":"integer","description":"head size"}],
    "HTTPURL": [{"name":"url","type":"string","description":"URL"}],
    "FTPOPEN": [{"name":"host","type":"string","description":"FTP host"}],
    "FTPCLOSE": [], "FTPPUT": [], "FTPGET": [],
    "FTPUSER": [{"name":"user","type":"string","description":"username"}],
    "FTPPASS": [{"name":"pass","type":"string","description":"password"}],
    "FTPCWD": [{"name":"path","type":"string","description":"directory"}],
    "FTPTYPE": [{"name":"type","type":"integer","description":"0=binary 1=ascii"}],
    "SSLCFG": [{"name":"ssl_type","type":"integer","description":"config index"},{"name":"value","type":"string","description":"value"}],
    "SSLCONF": [{"name":"ssl_type","type":"integer","description":"config index"}],
    "SSLOPEN": [{"name":"cid","type":"integer","description":"context id"},{"name":"mode","type":"string","description":"TCP or UDP"},{"name":"host","type":"string","description":"server host"},{"name":"port","type":"integer","description":"server port"}],
    "SSLSEND": [{"name":"length","type":"integer","description":"data length"}],
    "SSLRECV": [{"name":"length","type":"integer","description":"max bytes"}],
    "SSLCLOSE": [],
    "SSLSETCERT": [{"name":"cert_name","type":"string","description":"certificate name"}],
    "SSLSETKEY": [{"name":"key_name","type":"string","description":"key name"}],
    "SSLSETCA": [{"name":"ca_name","type":"string","description":"CA name"}],
}

def norm(c):
    c = str(c or "").upper().lstrip("+")
    if c.startswith("AT+"): c = c[3:]
    return c

p = find("dat_11")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("parameters"): continue
    n = norm(r.get("command"))
    params = SPECIALIST_PARAMS.get(n, [])
    if params:
        r["parameters"] = [dict(x) for x in params]
        r["updated_at"] = ts
        filled += 1

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
wp = sum(1 for r in records if isinstance(r, dict) and r.get("parameters"))
(REPORTS / "_step_D10_dat11.json").write_text(json.dumps({"total":len(records),"with_parameters":wp,"filled":filled}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_11: total={len(records)} with_parameters={wp} filled={filled}")