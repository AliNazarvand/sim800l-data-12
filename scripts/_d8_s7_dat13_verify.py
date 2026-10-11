#!/usr/bin/env python3
import sys, json
from pathlib import Path
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

p = find("dat_13")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
wp = sum(1 for r in records if isinstance(r, dict) and r.get("parameters"))
summary = {"total": len(records), "with_parameters": wp}
(REPORTS / "_step_D8_dat13_verify.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_13: total={len(records)} with_parameters={wp}")