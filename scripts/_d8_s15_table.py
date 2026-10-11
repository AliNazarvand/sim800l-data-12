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

NAMES = {
    "dat_01":"AT Command","dat_02":"URC","dat_03":"Error Code",
    "dat_04":"Timing & Timeout","dat_05":"State Machine","dat_06":"Init Sequence",
    "dat_07":"Hardware Reference","dat_08":"Firmware Compatibility",
    "dat_09":"SMS","dat_10":"GPRS/Data","dat_11":"HTTP/FTP/SSL",
    "dat_12":"Audio","dat_13":"SIM Management","dat_14":"Operator/APN",
    "dat_15":"Power Management","dat_16":"Board/EVB",
    "dat_17":"Certificate/Key Store","dat_18":"Certification",
}

STRICT_FIELDS = {
    "dat_01": ["parameters"], "dat_02": ["parameters","examples"], "dat_03": ["recovery_steps"],
    "dat_04": ["value_typ"], "dat_05": ["related_commands"], "dat_06": ["expected_response"],
    "dat_07": ["function"], "dat_09": ["parameters","examples"], "dat_10": ["parameters"],
    "dat_11": ["examples"], "dat_12": ["parameters"], "dat_13": ["parameters"], "dat_15": ["value_typ"],
}

def has_strict(r, fields):
    for f in fields:
        v = r.get(f)
        if v not in (None, "", [], {}):
            return True
    return False

lines = ["# PHASE 1 — Final Summary v3","",
         "| dat_id | name | status | count | with_page | strict_depth | strict_pct | completion% |",
         "|---|---|---|---|---|---|---|---|"]
for i in range(1, 19):
    dat_id = f"dat_{i:02d}"
    p = find(dat_id)
    if not p:
        lines.append(f"| {dat_id} | {NAMES[dat_id]} | blocked | 0 | 0 | 0 | 0% | 0% |")
        continue
    records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    if not isinstance(records, list): records = [records]
    cnt = len(records); wp = 0; wd = 0
    fields = STRICT_FIELDS.get(dat_id, [])
    for r in records:
        if not isinstance(r, dict): continue
        src = r.get("source") or {}
        if isinstance(src, dict) and src.get("page"): wp += 1
        elif r.get("source_type") == "external" and r.get("source_url"): wp += 1
        if fields and has_strict(r, fields): wd += 1
    cnt_pct = (wp/cnt*100) if cnt>0 else 0
    strict_pct = (wd/cnt*100) if cnt>0 else 0
    if cnt == 0: st = "blocked"
    elif wp == cnt and cnt > 0: st = "complete"
    elif wp > 0: st = "partial"
    else: st = "blocked"
    lines.append(f"| {dat_id} | {NAMES[dat_id]} | {st} | {cnt} | {wp} | {wd} | {strict_pct:.1f}% | {cnt_pct:.1f}% |")

(REPORTS / "PHASE_1_FINAL_TABLE.md").write_text("\n".join(lines), encoding="utf-8")
print("PHASE_1_FINAL_TABLE.md written (v3)")