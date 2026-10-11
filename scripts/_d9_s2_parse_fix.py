#!/usr/bin/env python3
"""Re-parse params for dat_09/10/12/13 only when source.quote/syntax has <...>."""
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

def infer_type(name):
    n = name.lower()
    if n in ("index","mode","level","channel","port","cid","bearer","n","i","p","stat"):
        return "integer"
    return "string"

ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
summary = {}
for dat_id in ("dat_09","dat_10","dat_12","dat_13"):
    p = find(dat_id)
    if not p:
        summary[dat_id] = {"error": "file missing"}
        continue
    records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    if not isinstance(records, list): records = [records]
    filled = 0
    for r in records:
        if not isinstance(r, dict): continue
        if r.get("parameters"): continue
        parts = []
        if r.get("syntax"): parts.append(str(r["syntax"]))
        src = r.get("source") or {}
        if isinstance(src, dict) and src.get("quote"): parts.append(str(src["quote"]))
        text = " ".join(parts)
        names = TOKEN_RE.findall(text)
        if not names:
            continue
        seen = set(); params = []
        for n in names:
            if n in seen: continue
            seen.add(n)
            params.append({"name": n, "type": infer_type(n), "description": ""})
        if params:
            r["parameters"] = params
            r["updated_at"] = ts
            filled += 1
    with p.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
    wp = sum(1 for r in records if isinstance(r, dict) and r.get("parameters"))
    summary[dat_id] = {"total": len(records), "with_parameters": wp, "filled": filled}
    print(f"{dat_id}: total={len(records)} with_parameters={wp} filled={filled}")

(REPORTS / "_step_D9_parse_fix.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")