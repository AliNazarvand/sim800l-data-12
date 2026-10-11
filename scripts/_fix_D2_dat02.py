#!/usr/bin/env python3
"""Attempt to recover suspicious dat_02 URC records by finding real URC format in AT Manual."""
import sys, json, re
from pathlib import Path
from datetime import datetime, timezone
try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr); sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SRC_EX = ROOT / "sources" / "extracted"
REPORTS = ROOT / "reports"

def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml"))
    return c[0] if c else (DATA / (dat_id + ".yaml") if (DATA / (dat_id + ".yaml")).exists() else None)

def load_paged(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    pages = []
    parts = re.split(r"<<<PAGE\s+(\d+)>>>", text)
    for i in range(1, len(parts) - 1, 2):
        try: num = int(parts[i])
        except Exception: continue
        pages.append((num, parts[i + 1]))
    return pages

pages = load_paged(SRC_EX / "at_manual_v1_01_paged.txt")

def norm_urc(s):
    if not s: return None
    s = str(s).strip().upper()
    if s.startswith("AT+"): s = s[3:]
    elif s.startswith("+"): s = s[1:]
    return s

def find_urc_in_manual(urc_name):
    """URC in manual usually looks like '+CMTI: <mem>,<index>'"""
    norm = norm_urc(urc_name)
    if not norm: return None
    # Try patterns: "+NORM:" or "+NORM " (with params)
    pats = [
        re.compile(r"^\s*\+" + re.escape(norm) + r"\s*[:<>]", re.IGNORECASE),
        re.compile(r"^\s*\+" + re.escape(norm) + r"\b", re.IGNORECASE),
    ]
    for page_no, body in pages:
        for line in body.splitlines():
            s = line.strip()
            if len(s) < 4 or len(s) > 260: continue
            if re.match(r"^[+]?[A-Z0-9]+\s*\.{3,}", s): continue
            for p in pats:
                if p.match(s):
                    # باید حداقل یک نشانه URC داشته باشد
                    if any(m in s for m in [":", "<", ">"]):
                        return (page_no, s)
    return None

p = find("dat_02")
if not p:
    print("dat_02 not found"); sys.exit(1)
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
recovered = 0; still_suspicious = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("status") != "unknown": continue
    urc = r.get("urc_string")
    if not urc: continue
    hit = find_urc_in_manual(urc)
    if hit:
        page_no, line = hit
        src = r.get("source") or {}
        if not isinstance(src, dict): src = {}
        src["page"] = str(page_no)
        if not src.get("section"): src["section"] = "URC Section"
        src["quote"] = line[:260]
        if not src.get("name"): src["name"] = "SIM800 Series_AT Command Manual"
        if not src.get("version"): src["version"] = "V1.01"
        if not src.get("date"): src["date"] = "2018-05-15"
        r["source"] = src
        r["status"] = "partial"
        r["confidence"] = 0.6
        r["updated_at"] = ts
        recovered += 1
    else:
        still_suspicious += 1

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
summary = {"recovered": recovered, "still_suspicious": still_suspicious, "total": len(records)}
(REPORTS / "_step_D2_dat02_fix.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_02: recovered={recovered} still_suspicious={still_suspicious} total={len(records)}")