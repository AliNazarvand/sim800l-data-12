#!/usr/bin/env python3
"""Generate all final umbrella reports from actual data on disk."""
import pathlib, yaml
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

DS = [
    ("dat_01", "AT Command DB",         "AT Manual",       "primary",  100),
    ("dat_02", "URC DB",                "AT Manual",       "primary",   30),
    ("dat_03", "Error Code DB",         "AT Manual",       "primary",  200),
    ("dat_04", "Timing & Timeout",      "V1.00/V2.02",     "primary",   15),
    ("dat_05", "State Machine",         "V1.00/V2.02",     "primary",   10),
    ("dat_06", "Init Sequence",         "V1.00/V2.02",     "primary",   15),
    ("dat_07", "Hardware Reference",    "V1.00/V2.02",     "primary",   60),
    ("dat_08", "Firmware Compatibility","Release Notes",   "missing",    0),
    ("dat_09", "SMS DB",                "AT Manual",       "primary",   10),
    ("dat_10", "GPRS/Data DB",          "AT Manual",       "primary",   30),
    ("dat_11", "HTTP/FTP/SSL DB",       "AT Manual",       "primary",   30),
    ("dat_12", "Audio DB",              "AT Manual",       "primary",   10),
    ("dat_13", "SIM Management",        "AT Manual",       "primary",    8),
    ("dat_14", "Operator/APN",          "external",        "external",   0),
    ("dat_15", "Power Management",      "V1.00/V2.02",     "primary",   20),
    ("dat_16", "Board/EVB",             "EVB Schematic",   "missing",    0),
    ("dat_17", "Certificate/Key Store", "SSL Manual",      "missing",    0),
    ("dat_18", "Certification",         "CE/FCC",          "missing",    0),
]

REASONS = {
    "dat_08": "SIM800 Series Firmware Release Notes not present in sources/originals.",
    "dat_14": "Optional. Requires external GSMA/ITU MCC-MNC source.",
    "dat_16": "Official SIM800L EVB schematic not present in sources/originals.",
    "dat_17": "SIM800 Series SSL AT Command Manual not present in sources/originals.",
    "dat_18": "Official CE/FCC/GCF/PTCRB certificates not present in sources/originals.",
}

def count(pfx):
    fs = sorted(DATA.glob(f"{pfx}_*.yaml")) or sorted(DATA.glob(f"{pfx}.yaml"))
    if not fs: return 0, ""
    try:
        d = yaml.safe_load(fs[0].read_text(encoding="utf-8")) or {}
    except Exception:
        return 0, fs[0].name
    recs = d.get("records") if isinstance(d, dict) else d
    return (len(recs) if isinstance(recs, list) else 0), fs[0].name

rows = []
c = p = b = df = 0
tot = 0
for pfx, name, src, kind, th in DS:
    n, fn = count(pfx)
    tot += n
    if kind == "missing" and n == 0:
        st = "blocked"; b += 1
    elif kind == "external" and n == 0:
        st = "deferred"; df += 1
    elif n >= th:
        st = "complete"; c += 1
    elif n >= 1:
        st = "partial"; p += 1
    else:
        st = "blocked"; b += 1
    reason = REASONS.get(pfx, "-")
    rows.append({"id": pfx, "name": name, "status": st, "n": n,
                 "threshold": th, "file": fn, "source": src, "reason": reason})

# ---- COVERAGE_MATRIX.md
cm = ["# COVERAGE MATRIX", "", f"Generated: {NOW}",
      f"**Total records: {tot}**",
      f"**Summary: complete={c}, partial={p}, blocked={b}, deferred={df}**", "",
      "| Dataset | Title | Status | Records | Threshold | File | Source |",
      "|---|---|---|---|---|---|---|"]
for r in rows:
    cm.append(f"| {r['id']} | {r['name']} | {r['status']} | {r['n']} | {r['threshold']} | {r['file']} | {r['source']} |")
(ROOT / "COVERAGE_MATRIX.md").write_text("\n".join(cm), encoding="utf-8")

# ---- GAP_REPORT.md
gap = ["# GAP REPORT", "", f"Generated: {NOW}", "",
       "## Summary",
       f"- complete: {c}",
       f"- partial : {p}",
       f"- blocked : {b}",
       f"- deferred: {df}",
       f"- total records: {tot}", ""]
for label, key in [("Complete","complete"),("Partial","partial"),("Blocked","blocked"),("Deferred","deferred")]:
    gap.append(f"## {label}")
    for r in rows:
        if r["status"] == key:
            extra = f" — {r['reason']}" if r["reason"] != "-" else ""
            gap.append(f"- {r['id']} {r['name']}: {r['n']} records{extra}")
    gap.append("")
(ROOT / "GAP_REPORT.md").write_text("\n".join(gap), encoding="utf-8")

# ---- TODO.md
todo = ["# TODO", "", f"Generated: {NOW}", "",
        "## Missing sources (blocking)", ""]
for r in rows:
    if r["status"] == "blocked":
        todo.append(f"- [ ] **{r['id']} {r['name']}** — {r['reason']}")
todo += ["", "## Deferred", ""]
for r in rows:
    if r["status"] == "deferred":
        todo.append(f"- [ ] **{r['id']} {r['name']}** — {r['reason']}")
todo += ["", "## How to unblock",
         "",
         "Place the required file in `sources/originals/`, then re-run the extraction scripts:",
         "",
         "| Missing source | Unblocks |",
         "|---|---|",
         "| SIM800 Series AT Command Manual (V1.09+) | dat_01, 02, 03, 08, 09, 10, 11, 12, 13 |",
         "| SIM800 Series SSL AT Command Manual | dat_17 |",
         "| SIM800 Series Firmware Release Notes | dat_08 |",
         "| SIM800L EVB Schematic | dat_16 |",
         "| SIM800L CE/FCC/GCF certificates | dat_18 |",
         "| GSMA/ITU MCC-MNC data (optional) | dat_14 |",
         "",
         "After adding sources, run:",
         "```",
         "python scripts/extract_all.py",
         "python scripts/populate_crossrefs.py", 
         "python scripts/reports.py",
         "```"]
(ROOT / "TODO.md").write_text("\n".join(todo), encoding="utf-8")

# ---- ROLE_MAP.md
rm = ["# ROLE MAP", "", f"Generated: {NOW}", "",
      "| Dataset | Title | Status | Records | Source |",
      "|---|---|---|---|---|"]
for r in rows:
    rm.append(f"| {r['id']} | {r['name']} | {r['status']} | {r['n']} | {r['source']} |")
(ROOT / "ROLE_MAP.md").write_text("\n".join(rm), encoding="utf-8")

print(f"reports: total={tot} complete={c} partial={p} blocked={b} deferred={df}")