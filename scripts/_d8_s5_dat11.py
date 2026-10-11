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
    return c[0] if c else (DATA / (dat_id + ".yaml") if (DATA / (dat_id + ".yaml")).exists() else None)

p = find("dat_11")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("examples"): continue
    src = r.get("source") or {}
    quote = src.get("quote") if isinstance(src, dict) else None
    cmd = r.get("command")
    ex = None
    if quote: ex = str(quote)[:200]
    elif cmd: ex = str(cmd)
    if ex:
        r["examples"] = [ex]
        r["updated_at"] = ts
        filled += 1

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)

we = sum(1 for r in records if isinstance(r, dict) and r.get("examples"))
summary = {"total": len(records), "with_examples": we, "filled": filled}
(REPORTS / "_step_D8_dat11.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_11: total={len(records)} with_examples={we} filled={filled}")