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
    return c[0] if c else (DATA / (dat_id + ".yaml") if (DATA / (dat_id + ".yaml")).exists() else None)

p = find("dat_14")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
with_url = 0
with_type_ext = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("source_url"): with_url += 1
    if r.get("source_type") == "external": with_type_ext += 1

summary = {"total": len(records), "with_source_url": with_url, "with_source_type_external": with_type_ext}
(REPORTS / "_step_D6_dat14.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_14: total={len(records)} with_source_url={with_url} with_source_type_external={with_type_ext}")