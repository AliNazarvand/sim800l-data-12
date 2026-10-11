#!/usr/bin/env python3
import json
from pathlib import Path
try:
    import yaml
except ImportError: raise
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"; REPORTS = ROOT / "reports"
def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml")); return c[0] if c else None
targets = ['dat_03','dat_04','dat_10','dat_11','dat_12','dat_14','dat_15']
out = {}
all_ok = True
for ds in targets:
    p = find(ds)
    if not p:
        out[ds] = {"error": "file missing"}; all_ok = False; continue
    recs = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    if not isinstance(recs, list): recs = [recs]
    cnt = 0
    for r in recs:
        if isinstance(r, dict) and "limit_reason:" in str(r.get("notes") or ""):
            cnt += 1
    out[ds] = {"total": len(recs), "with_limit_reason": cnt, "ok": cnt == len(recs)}
    if cnt != len(recs): all_ok = False
(REPORTS / "_d13_verify_reasons.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"all_ok={all_ok}")
for ds, v in out.items():
    print(f"  {ds}: {v}")