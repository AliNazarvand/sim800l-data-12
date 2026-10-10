import pathlib, yaml
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

DS = [
    ("dat_01","AT Command DB","AT Manual","primary",60),
    ("dat_02","URC DB","AT Manual","primary",20),
    ("dat_03","Error Code DB (CME/CMS)","AT Manual","primary",100),
    ("dat_04","Timing & Timeout","V1.00/V2.02","primary",15),
    ("dat_05","State Machine","V1.00/V2.02","primary",10),
    ("dat_06","Init Sequence","V1.00/V2.02","primary",15),
    ("dat_07","Hardware Reference","V1.00/V2.02","primary",40),
    ("dat_08","Firmware Compat","Release Notes","missing",0),
    ("dat_09","SMS DB","AT Manual","primary",10),
    ("dat_10","GPRS/Data DB","AT Manual","primary",30),
    ("dat_11","HTTP/FTP/SSL","AT Manual","primary",30),
    ("dat_12","Audio DB","AT Manual","primary",10),
    ("dat_13","SIM Management","AT Manual","primary",10),
    ("dat_14","Operator/APN","external","external",0),
    ("dat_15","Power Management","V1.00/V2.02","primary",20),
    ("dat_16","Board/EVB","EVB Schematic","missing",0),
    ("dat_17","Certificate/Key","SSL Manual","missing",0),
    ("dat_18","Certification","CE/FCC","missing",0),
]

def count(pfx):
    fs = sorted(DATA.glob(f"{pfx}_*.yaml")) or sorted(DATA.glob(f"{pfx}.yaml"))
    if not fs: return 0, ""
    try: d = yaml.safe_load(fs[0].read_text(encoding="utf-8")) or {}
    except Exception: return 0, fs[0].name
    recs = d.get("records") if isinstance(d, dict) else d
    return (len(recs) if isinstance(recs, list) else 0), fs[0].name

rows = []
c = p = b = d_ = 0
tot = 0
for pfx, name, src, kind, th in DS:
    n, fn = count(pfx)
    tot += n
    if kind == "missing" and n == 0: st = "blocked"; b += 1
    elif kind == "external" and n == 0: st = "deferred"; d_ += 1
    elif n >= th: st = "complete"; c += 1
    elif n >= 1: st = "partial"; p += 1
    else: st = "blocked"; b += 1
    rows.append((pfx, name, st, n, src, fn, th))

cm = ["# COVERAGE MATRIX","",f"Generated {NOW}.",f"**Total: {tot}**","",
      "| Dataset | Title | Status | Records | Threshold | File | Source |",
      "|---|---|---|---|---|---|---|"]
for r in rows: cm.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[6]} | {r[5]} | {r[4]} |")
(ROOT/"COVERAGE_MATRIX.md").write_text("\n".join(cm), encoding="utf-8")

gap = ["# GAP REPORT","",f"Generated {NOW}.","",
       f"- complete: {c}",f"- partial : {p}",f"- blocked : {b}",f"- deferred: {d_}",
       f"- total   : {tot}","",
       "| Dataset | Status | Records |", "|---|---|---|"]
for r in rows: gap.append(f"| {r[0]} {r[1]} | {r[2]} | {r[3]} |")
(ROOT/"GAP_REPORT.md").write_text("\n".join(gap), encoding="utf-8")

todo = ["# TODO","",f"Generated {NOW}.","","## Blocked"]
for r in rows:
    if r[2]=="blocked": todo.append(f"- [ ] {r[0]} {r[1]} — {r[4]}")
todo += ["","## Deferred"]
for r in rows:
    if r[2]=="deferred": todo.append(f"- [ ] {r[0]} {r[1]} — {r[4]}")
(ROOT/"TODO.md").write_text("\n".join(todo), encoding="utf-8")

rm = ["# ROLE MAP","",f"Generated {NOW}.","",
      "| Dataset | Title | Status | Records | Source |","|---|---|---|---|---|"]
for r in rows: rm.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |")
(ROOT/"ROLE_MAP.md").write_text("\n".join(rm), encoding="utf-8")

print(f"reports: total={tot} complete={c} partial={p} blocked={b} deferred={d_}")