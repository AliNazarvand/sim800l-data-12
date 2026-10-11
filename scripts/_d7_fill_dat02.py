#!/usr/bin/env python3
"""Fill dat_02 URC parameters/examples by parsing format field."""
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

PARAM_RE = re.compile(r"<([A-Za-z_][A-Za-z0-9_]*)>")

def infer_type(name):
    n = name.lower()
    if n in ("index","mem","n","cid"): return "integer"
    return "string"

p = find("dat_02")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records:
    if not isinstance(r, dict): continue
    fmt = r.get("format") or ""
    quote = ""
    if isinstance(r.get("source"), dict):
        quote = r["source"].get("quote") or ""
    text = " ".join([fmt, quote])
    names = PARAM_RE.findall(text)
    if names and not r.get("parameters"):
        seen = set(); params = []
        for n in names:
            if n in seen: continue
            seen.add(n)
            params.append({"name": n, "type": infer_type(n), "description": ""})
        r["parameters"] = params
        r["updated_at"] = ts
        filled += 1
    if fmt and not r.get("examples"):
        r["examples"] = [fmt]
        r["updated_at"] = ts

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)

with_params = sum(1 for r in records if isinstance(r, dict) and r.get("parameters"))
with_examples = sum(1 for r in records if isinstance(r, dict) and r.get("examples"))
summary = {"total": len(records), "with_parameters": with_params, "with_examples": with_examples, "filled": filled}
(REPORTS / "_step_D7_dat02.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_02: total={len(records)} with_parameters={with_params} with_examples={with_examples}")