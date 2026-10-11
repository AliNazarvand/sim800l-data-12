#!/usr/bin/env python3
import sys, json
from pathlib import Path
try:
    import yaml
except ImportError: sys.exit(2)
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"; REPORTS = ROOT / "reports"
def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml")); return c[0] if c else None
NAMES = {"dat_01":"AT Command","dat_02":"URC","dat_03":"Error Code","dat_04":"Timing & Timeout",
         "dat_05":"State Machine","dat_06":"Init Sequence","dat_07":"Hardware Reference",
         "dat_08":"Firmware Compatibility","dat_09":"SMS","dat_10":"GPRS/Data","dat_11":"HTTP/FTP/SSL",
         "dat_12":"Audio","dat_13":"SIM Management","dat_14":"Operator/APN","dat_15":"Power Management",
         "dat_16":"Board/EVB","dat_17":"Certificate/Key Store","dat_18":"Certification"}
FORCED = {"dat_08":("blocked","external source"),"dat_16":("deferred","EVB"),
          "dat_18":("blocked","cert"),"dat_17":("blocked","SSL"),"dat_14":("partial","external")}
PARAM_FIELD = {"dat_01":"parameters","dat_02":"parameters","dat_03":"recovery_steps",
               "dat_04":"value_typ","dat_05":"related_commands","dat_06":"expected_response",
               "dat_07":"function","dat_09":"parameters","dat_10":"parameters","dat_11":"parameters",
               "dat_12":"parameters","dat_13":"parameters","dat_15":"value_typ"}
def hp(r,f):
    v = r.get(f); return v not in (None,"",[],{})
rows = []
for i in range(1,19):
    dat_id = f"dat_{i:02d}"; p = find(dat_id)
    if not p:
        rows.append({"dat_id":dat_id,"name":NAMES[dat_id],"status":"blocked","cnt":0,"wp":0,"wpar":0,"pct":0}); continue
    recs = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    if not isinstance(recs, list): recs = [recs]
    cnt = len(recs); wp = 0; wpar = 0; field = PARAM_FIELD.get(dat_id,"")
    for r in recs:
        if not isinstance(r, dict): continue
        src = r.get("source") or {}
        if isinstance(src, dict) and src.get("page"): wp += 1
        elif r.get("source_type") == "external" and r.get("source_url"): wp += 1
        if field and hp(r, field): wpar += 1
    pct = (wpar/cnt*100) if cnt else 0
    if dat_id in FORCED: st = FORCED[dat_id][0]
    elif cnt == 0: st = "blocked"
    elif wp == cnt and pct >= 50: st = "complete"
    elif wp > 0: st = "partial"
    else: st = "blocked"
    rows.append({"dat_id":dat_id,"name":NAMES[dat_id],"status":st,"cnt":cnt,"wp":wp,"wpar":wpar,"pct":round(pct,1)})
lines = ["# PHASE 1 FINAL TABLE v5","",
         "| dat_id | name | status | count | with_page | with_params | params_pct |",
         "|---|---|---|---|---|---|---|"]
for r in rows:
    lines.append(f"| {r['dat_id']} | {r['name']} | {r['status']} | {r['cnt']} | {r['wp']} | {r['wpar']} | {r['pct']}% |")
(REPORTS / "PHASE_1_FINAL_TABLE.md").write_text("\n".join(lines), encoding="utf-8")
print("PHASE_1_FINAL_TABLE.md v5 written")