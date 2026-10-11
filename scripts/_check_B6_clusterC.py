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

summary = {}
# dat_08, dat_18 → blocked (no source)
summary["dat_08"] = {"status": "blocked", "reason": "Release Notes not available"}
summary["dat_18"] = {"status": "blocked", "reason": "Certification documents not available"}

# dat_14 → check external records
p = find("dat_14")
if p:
    records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    if not isinstance(records, list): records = [records]
    total = len(records)
    ext_ok = 0; conf_ok = 0
    for r in records:
        if not isinstance(r, dict): continue
        if r.get("source_type") == "external": ext_ok += 1
        c = r.get("confidence")
        if isinstance(c, (int, float)) and c <= 0.7: conf_ok += 1
    summary["dat_14"] = {"status": "partial", "total": total, "external": ext_ok, "conf_le_07": conf_ok}
else:
    summary["dat_14"] = {"status": "blocked", "reason": "file missing"}

(REPORTS / "_step_B6_clusterC.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))