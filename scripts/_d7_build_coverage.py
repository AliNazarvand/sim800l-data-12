#!/usr/bin/env python3
"""Rebuild COVERAGE_MATRIX with 'depth' (share of records with meaningful fields)."""
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

NAMES = {
    "dat_01":"AT Command","dat_02":"URC","dat_03":"Error Code",
    "dat_04":"Timing & Timeout","dat_05":"State Machine","dat_06":"Init Sequence",
    "dat_07":"Hardware Reference","dat_08":"Firmware Compatibility",
    "dat_09":"SMS","dat_10":"GPRS/Data","dat_11":"HTTP/FTP/SSL",
    "dat_12":"Audio","dat_13":"SIM Management","dat_14":"Operator/APN",
    "dat_15":"Power Management","dat_16":"Board/EVB",
    "dat_17":"Certificate/Key Store","dat_18":"Certification",
}

FORCED = {
    "dat_08": ("blocked", "external source (Release Notes) not available"),
    "dat_16": ("deferred", "EVB document not available"),
    "dat_18": ("blocked", "certification documents not available"),
    "dat_17": ("blocked", "SSL Manual not available"),
}

DEPTH_FIELDS = {
    "dat_01": ["parameters","response_success","examples"],
    "dat_02": ["parameters","examples","related_command"],
    "dat_03": ["recovery_steps","meaning"],
    "dat_04": ["value_min","value_typ","value_max","unit"],
    "dat_05": ["related_commands","related_urcs"],
    "dat_06": ["command","expected_response","related_state"],
    "dat_07": ["function","voltage_min","voltage_max"],
    "dat_09": ["parameters","examples","encoding"],
    "dat_10": ["parameters","response_success","examples"],
    "dat_11": ["parameters","examples"],
    "dat_12": ["parameters","examples"],
    "dat_13": ["parameters","response"],
    "dat_15": ["value_min","value_typ","unit"],
}

def has_depth(r, fields):
    for f in fields:
        v = r.get(f)
        if v not in (None, "", [], {}):
            return True
    return False

rows = []
for i in range(1, 19):
    dat_id = f"dat_{i:02d}"
    p = find(dat_id)
    if not p:
        rows.append({"dat_id": dat_id, "name": NAMES[dat_id], "count": 0,
                     "with_page": 0, "with_depth": 0, "status": "blocked", "reason": "file missing"})
        continue
    records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    if not isinstance(records, list): records = [records]
    cnt = len(records)
    wp = 0; wd = 0
    fields = DEPTH_FIELDS.get(dat_id, [])
    for r in records:
        if not isinstance(r, dict): continue
        src = r.get("source") or {}
        if isinstance(src, dict) and src.get("page"):
            wp += 1
        elif r.get("source_type") == "external" and r.get("source_url"):
            wp += 1
        if fields and has_depth(r, fields):
            wd += 1
    if dat_id in FORCED:
        st, reason = FORCED[dat_id]
    else:
        if cnt == 0:
            st, reason = "blocked", "no records"
        elif wp == cnt and cnt > 0:
            st, reason = "complete", f"all {cnt} records sourced"
        elif wp > 0:
            st, reason = "partial", f"{wp}/{cnt} sourced"
        else:
            st, reason = "blocked", "no records sourced"
    depth_pct = (wd / cnt * 100) if cnt > 0 else 0
    rows.append({"dat_id": dat_id, "name": NAMES[dat_id], "count": cnt,
                 "with_page": wp, "with_depth": wd, "depth_pct": round(depth_pct,1),
                 "status": st, "reason": reason})

lines = ["# COVERAGE_MATRIX", "",
         "| دیتاست | نام | status | count | with_page | with_depth | depth% |",
         "|---|---|---|---|---|---|---|"]
for r in rows:
    lines.append(f"| {r['dat_id']} | {r['name']} | {r['status']} | {r['count']} | {r['with_page']} | {r['with_depth']} | {r['depth_pct']}% |")

(REPORTS / "COVERAGE_MATRIX.md").write_text("\n".join(lines), encoding="utf-8")
(REPORTS / "_step_D7_coverage.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

counts = {"complete":0,"partial":0,"blocked":0,"deferred":0}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
print(f"COVERAGE rebuilt: c={counts['complete']} p={counts['partial']} b={counts['blocked']} d={counts['deferred']}")
for r in rows:
    print(f"  {r['dat_id']}: {r['status']:9s} cnt={r['count']:4d} wp={r['with_page']:4d} wd={r['with_depth']:4d} ({r['depth_pct']}%)")