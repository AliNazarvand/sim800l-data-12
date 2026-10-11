#!/usr/bin/env python3
"""COVERAGE with strict params criterion: complete = with_page==count AND params_pct>=50%."""
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
FORCED = {
    "dat_08": ("blocked", "external source (Release Notes) not available"),
    "dat_16": ("deferred", "EVB document not available"),
    "dat_18": ("blocked", "certification documents not available"),
    "dat_17": ("blocked", "SSL Manual not available"),
    "dat_14": ("partial", "external records only"),
}
# primary depth field per dataset
PARAM_FIELD = {
    "dat_01": "parameters", "dat_02": "parameters", "dat_03": "recovery_steps",
    "dat_04": "value_typ", "dat_05": "related_commands", "dat_06": "expected_response",
    "dat_07": "function", "dat_09": "parameters", "dat_10": "parameters",
    "dat_11": "parameters", "dat_12": "parameters", "dat_13": "parameters",
    "dat_15": "value_typ",
}
def has_param(r, field):
    v = r.get(field)
    return v not in (None, "", [], {})

rows = []
for i in range(1, 19):
    dat_id = f"dat_{i:02d}"
    p = find(dat_id)
    if not p:
        rows.append({"dat_id": dat_id, "name": NAMES[dat_id], "count": 0, "with_page": 0,
                     "with_params": 0, "params_pct": 0, "status": "blocked", "reason": "missing"})
        continue
    records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    if not isinstance(records, list): records = [records]
    cnt = len(records); wp = 0; wpar = 0
    field = PARAM_FIELD.get(dat_id, "")
    for r in records:
        if not isinstance(r, dict): continue
        src = r.get("source") or {}
        if isinstance(src, dict) and src.get("page"): wp += 1
        elif r.get("source_type") == "external" and r.get("source_url"): wp += 1
        if field and has_param(r, field): wpar += 1
    params_pct = (wpar/cnt*100) if cnt>0 else 0
    if dat_id in FORCED:
        st, reason = FORCED[dat_id]
    else:
        if cnt == 0:
            st, reason = "blocked", "no records"
        elif wp == cnt and params_pct >= 50:
            st, reason = "complete", f"all sourced; params_pct={params_pct:.0f}%"
        elif wp == cnt:
            st, reason = "partial", f"all sourced; params_pct={params_pct:.0f}%"
        elif wp > 0:
            st, reason = "partial", f"{wp}/{cnt} sourced; params_pct={params_pct:.0f}%"
        else:
            st, reason = "blocked", "no records sourced"
    rows.append({"dat_id": dat_id, "name": NAMES[dat_id], "count": cnt, "with_page": wp,
                 "with_params": wpar, "params_pct": round(params_pct,1), "status": st, "reason": reason})

lines = ["# COVERAGE_MATRIX","",
         "| دیتاست | نام | status | count | with_page | with_params | params_pct |",
         "|---|---|---|---|---|---|---|"]
for r in rows:
    lines.append(f"| {r['dat_id']} | {r['name']} | {r['status']} | {r['count']} | {r['with_page']} | {r['with_params']} | {r['params_pct']}% |")
lines.append("")
lines.append("## قواعد")
lines.append("- complete: with_page==count AND params_pct >= 50%")
lines.append("- partial: with_page==count but params_pct < 50%")
lines.append("- blocked/deferred: no source")

(REPORTS / "COVERAGE_MATRIX.md").write_text("\n".join(lines), encoding="utf-8")
(REPORTS / "_step_D10_coverage.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
counts = {"complete":0,"partial":0,"blocked":0,"deferred":0}
for r in rows:
    counts[r["status"]] = counts.get(r["status"],0)+1
print(f"COVERAGE c={counts['complete']} p={counts['partial']} b={counts['blocked']} d={counts['deferred']}")
for r in rows:
    print(f"  {r['dat_id']}: {r['status']:9s} cnt={r['count']:4d} wp={r['with_page']:4d} wpar={r['with_params']:4d} ({r['params_pct']}%)")