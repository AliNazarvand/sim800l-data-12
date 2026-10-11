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
ALL_PARAMS = {
    "HTTPINIT": [], "HTTPTERM": [],
    "HTTPPARA": [{"name":"para","type":"string","description":"parameter"},{"name":"value","type":"string","description":"value"}],
    "HTTPDATA": [{"name":"size","type":"integer","description":"data size"}],
    "HTTPACTION": [{"name":"method","type":"integer","description":"0=GET 1=POST 2=HEAD"}],
    "HTTPREAD": [{"name":"start","type":"integer"},{"name":"size","type":"integer"}],
    "HTTPHEAD": [{"name":"size","type":"integer"}],
    "HTTPSTATUS": [{"name":"method","type":"integer"}],
    "HTTPURL": [{"name":"url","type":"string"}],
    "HTTPSSSL": [{"name":"ssl","type":"integer"}],
    "FTPOPEN": [{"name":"host","type":"string"}],
    "FTPCLOSE": [], "FTPPUT": [], "FTPGET": [], "FTPDELE": [], "FTPMKD": [], "FTPRMD": [],
    "FTPLIST": [], "FTPFLST": [],
    "FTPUSER": [{"name":"user","type":"string"}],
    "FTPPASS": [{"name":"pass","type":"string"}],
    "FTPCWD": [{"name":"path","type":"string"}],
    "FTPPWD": [],
    "FTPTYPE": [{"name":"type","type":"integer"}],
    "FTPMODE": [{"name":"mode","type":"integer"}],
    "FTPPUTOPT": [{"name":"value","type":"string"}],
    "FTPGETPATH": [{"name":"path","type":"string"}],
    "FTPPUTPATH": [{"name":"path","type":"string"}],
    "FTPPORT": [{"name":"port","type":"integer"}],
    "SSLCFG": [{"name":"ssl_type","type":"integer"},{"name":"value","type":"string"}],
    "SSLCONF": [{"name":"ssl_type","type":"integer"}],
    "SSLOPEN": [{"name":"cid","type":"integer"},{"name":"mode","type":"string"},{"name":"host","type":"string"},{"name":"port","type":"integer"}],
    "SSLSEND": [{"name":"length","type":"integer"}],
    "SSLRECV": [{"name":"length","type":"integer"}],
    "SSLCLOSE": [],
    "SSLSETCERT": [{"name":"cert_name","type":"string"}],
    "SSLSETKEY": [{"name":"key_name","type":"string"}],
    "SSLSETCA": [{"name":"ca_name","type":"string"}],
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
    params = ALL_PARAMS.get(n, [])
    if params:
        r["parameters"] = [dict(x) for x in params]; r["updated_at"] = ts; filled += 1
with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
wp = sum(1 for r in records if isinstance(r, dict) and r.get("parameters"))
(REPORTS / "_step_D11_dat11.json").write_text(json.dumps({"total":len(records),"with_parameters":wp,"filled":filled}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_11: total={len(records)} with_parameters={wp} filled={filled}")