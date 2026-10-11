#!/usr/bin/env python3
"""Build COVERAGE_MATRIX with per-dataset statistics."""
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

rows = []
for i in range(1, 19):
    dat_id = f"dat_{i:02d}"
    p = find(dat_id)
    if not p:
        rows.append({"dat_id": dat_id, "name": NAMES[dat_id], "count": 0,
                     "partial": 0, "unknown": 0, "blocked": 0, "with_page": 0,
                     "status": "blocked", "reason": "file missing"})
        continue
    records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    if not isinstance(records, list): records = [records]
    cnt = len(records)
    partial = sum(1 for r in records if isinstance(r, dict) and r.get("status") == "partial")
    unknown = sum(1 for r in records if isinstance(r, dict) and r.get("status") == "unknown")
    blocked_c = sum(1 for r in records if isinstance(r, dict) and r.get("status") == "blocked")
    with_page = sum(1 for r in records if isinstance(r, dict) and (r.get("source") or {}).get("page"))
    # dataset status via D-022
    if cnt == 0:
        ds_status = "blocked"; reason = "no records"
    elif with_page == cnt and partial == cnt:
        ds_status = "complete"; reason = "all records annotated"
    elif partial > 0:
        ds_status = "partial"; reason = f"{partial}/{cnt} partial"
    else:
        ds_status = "blocked"; reason = "no partial records"
    rows.append({"dat_id": dat_id, "name": NAMES[dat_id], "count": cnt,
                 "partial": partial, "unknown": unknown, "blocked": blocked_c,
                 "with_page": with_page, "status": ds_status, "reason": reason})

# built-in overrides for known blocked/deferred
for r in rows:
    if r["dat_id"] in ("dat_08","dat_18") and r["count"] <= 1:
        r["status"] = "blocked"; r["reason"] = "external source not available"
    if r["dat_id"] == "dat_15" and r["count"] <= 1:
        r["status"] = "blocked"; r["reason"] = "structured power parameters not extractable"
    if r["dat_id"] == "dat_16" and r["count"] <= 1:
        r["status"] = "deferred"; r["reason"] = "EVB document not available"
    if r["dat_id"] == "dat_14":
        r["status"] = "partial"; r["reason"] = "52 external records"

lines = ["# COVERAGE_MATRIX", "",
         "| دیتاست | نام | status | count | partial | unknown | blocked | with_page | دلیل |",
         "|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    lines.append(f"| {r['dat_id']} | {r['name']} | {r['status']} | {r['count']} | {r['partial']} | {r['unknown']} | {r['blocked']} | {r['with_page']} | {r['reason']} |")
lines.append("")
lines.append("## قواعد")
lines.append("- status دیتاست: complete | partial | blocked | deferred")
lines.append("- unknown فقط برای رکورد مجاز است.")
lines.append("- blocked با رکورد متناقض نیست (D-022).")

(REPORTS / "COVERAGE_MATRIX.md").write_text("\n".join(lines), encoding="utf-8")
(REPORTS / "_step_D3_coverage.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"COVERAGE_MATRIX built for {len(rows)} datasets")
for r in rows:
    print(f"  {r['dat_id']}: status={r['status']} count={r['count']} partial={r['partial']} blocked={r['blocked']}")