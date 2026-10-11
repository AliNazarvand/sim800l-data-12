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
    return c[0] if c else (DATA / (dat_id + ".yaml") if (DATA / (dat_id + ".yaml")).exists() else None)

TOKEN_RE = re.compile(r"<([A-Za-z_][A-Za-z0-9_]*)>")
def infer_type(name):
    return "integer" if name.lower() in ("index","cid","bearer","port") else "string"

p = find("dat_10")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records:
    if not isinstance(r, dict): continue
    text = " ".join([str(r.get("syntax") or ""), str(r.get("command") or "")])
    src = r.get("source") or {}
    if isinstance(src, dict): text += " " + str(src.get("quote") or "")
    names = TOKEN_RE.findall(text)
    if names and not r.get("parameters"):
        seen=set(); params=[]
        for n in names:
            if n in seen: continue
            seen.add(n)
            params.append({"name": n, "type": infer_type(n), "description": ""})
        r["parameters"] = params
        filled += 1
    if r.get("command") and not r.get("examples"):
        r["examples"] = [str(r["command"])]
    r["updated_at"] = ts

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)

wp = sum(1 for r in records if isinstance(r, dict) and r.get("parameters"))
summary = {"total": len(records), "with_parameters": wp, "filled": filled}
(REPORTS / "_step_D8_dat10.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_10: total={len(records)} with_parameters={wp} filled={filled}")