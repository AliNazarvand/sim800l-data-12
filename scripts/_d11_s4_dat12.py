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
sections = json.loads((REPORTS / "_section_index.json").read_text(encoding="utf-8"))
TOKEN_RE = re.compile(r"<([A-Za-z_][A-Za-z0-9_]*)>")
def cmd_full(c):
    c = str(c or "").upper()
    if c.startswith("AT+"): return c
    if c.startswith("+"): return "AT" + c
    return "AT+" + c
def infer(n):
    n = n.lower(); return "integer" if n in ("level","mode","channel") else "string"
p = find("dat_12")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("parameters"): continue
    cmd = cmd_full(r.get("command")); info = sections.get(cmd)
    parts = []
    if r.get("syntax"): parts.append(str(r["syntax"]))
    src = r.get("source") or {}
    if isinstance(src, dict) and src.get("quote"): parts.append(str(src["quote"]))
    if info: parts.append(info.get("body",""))
    names = TOKEN_RE.findall(" ".join(parts))
    if not names: continue
    seen=set(); params=[]
    for n in names:
        if n in seen: continue
        seen.add(n); params.append({"name":n,"type":infer(n),"description":""})
    if params:
        r["parameters"] = params; r["updated_at"] = ts; filled += 1
with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
wp = sum(1 for r in records if isinstance(r, dict) and r.get("parameters"))
(REPORTS / "_step_D11_dat12.json").write_text(json.dumps({"total":len(records),"with_parameters":wp,"filled":filled}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_12: total={len(records)} with_parameters={wp} filled={filled}")