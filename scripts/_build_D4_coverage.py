#!/usr/bin/env python3
"""Build COVERAGE_MATRIX using with_page-based rule (reflects reality)."""
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

# overrides
FORCED = {
    "dat_08": ("blocked", "external source (Release Notes) not available"),
    "dat_16": ("deferred", "EVB document not available"),
    "dat_18": ("blocked", "certification documents not available"),
    "dat_17": ("blocked", "SSL Manual not available"),
    "dat_14": ("partial", "52 external records; needs GSMA/ITU to complete"),
}

rows = []
for i in range(1, 19):
    dat_id = f"dat_{i:02d}"
    p = find(dat_id)
    if not p:
        rows.append({"dat_id": dat_id, "name": NAMES[dat_id], "count": 0,
                     "with_page": 0, "status": "blocked", "reason": "file missing"})
        continue
    records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    if not isinstance(records, list): records = [records]
    cnt = len(records)
    with_page = sum(1 for r in records if isinstance(r, dict)
                    and isinstance(r.get("source"), dict)
                    and r["source"].get("page"))
    # apply forced overrides first
    if dat_id in FORCED:
        st, reason = FORCED[dat_id]
    else:
        if cnt == 0:
            st, reason = "blocked", "no records"
        elif with_page == cnt and cnt > 0:
            st, reason = "complete", f"all {cnt} records sourced"
        elif with_page > 0:
            st, reason = "partial", f"{with_page}/{cnt} records sourced"
        else:
            st, reason = "blocked", "no records sourced"
    rows.append({"dat_id": dat_id, "name": NAMES[dat_id], "count": cnt,
                 "with_page": with_page, "status": st, "reason": reason})

lines = ["# COVERAGE_MATRIX", "",
         "| دیتاست | نام | status | count | with_page | دلیل |",
         "|---|---|---|---|---|---|"]
for r in rows:
    lines.append(f"| {r['dat_id']} | {r['name']} | {r['status']} | {r['count']} | {r['with_page']} | {r['reason']} |")
lines.append("")
lines.append("## قواعد")
lines.append("- status: complete (all sourced) | partial (some sourced) | blocked (none sourced) | deferred")
lines.append("- with_page = تعداد رکوردهایی که source.page معتبر دارند")

(REPORTS / "COVERAGE_MATRIX.md").write_text("\n".join(lines), encoding="utf-8")
(REPORTS / "_step_D4_coverage.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"COVERAGE rebuilt for {len(rows)} datasets")
counts = {"complete": 0, "partial": 0, "blocked": 0, "deferred": 0}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
    print(f"  {r['dat_id']}: {r['status']:9s} count={r['count']:4d} with_page={r['with_page']}")
print(f"Summary: complete={counts['complete']} partial={counts['partial']} blocked={counts['blocked']} deferred={counts['deferred']}")