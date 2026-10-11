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
p05 = find("dat_05"); p04 = find("dat_04")
if not p05: sys.exit(1)
records05 = yaml.safe_load(p05.read_text(encoding="utf-8")) or []
if not isinstance(records05, list): records05 = [records05]
dat04 = yaml.safe_load(p04.read_text(encoding="utf-8")) or [] if p04 else []
if not isinstance(dat04, list): dat04 = [dat04]
timing_by_state = {}
for r in dat04:
    if not isinstance(r, dict): continue
    state = r.get("related_state")
    if state:
        timing_by_state.setdefault(str(state).upper(), []).append(r.get("id"))
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records05:
    if not isinstance(r, dict): continue
    if r.get("related_timings"): continue
    st = (r.get("state_name") or "").upper()
    timings = timing_by_state.get(st, [])
    if timings:
        r["related_timings"] = timings[:5]; r["updated_at"] = ts; filled += 1
with p05.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records05, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
wt = sum(1 for r in records05 if isinstance(r, dict) and r.get("related_timings"))
(REPORTS / "_step_D11_dat05_timings.json").write_text(json.dumps({"total":len(records05),"with_timings":wt,"filled":filled}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_05: total={len(records05)} with_timings={wt} filled={filled}")