#!/usr/bin/env python3
"""Resolve remaining unknown records in dat_01: fuzzy search for +CMD in AT Manual.
   If found -> partial with page/quote; else -> blocked."""
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

def norm_cmd(c):
    if not c: return None
    s = str(c).strip().upper()
    if s.startswith("AT+"): s = s[3:]
    elif s.startswith("+"): s = s[1:]
    return s

def fuzzy_find(cmd):
    """Look for '+CMD' or 'AT+CMD' anywhere in a line."""
    norm = norm_cmd(cmd)
    if not norm or len(norm) < 2: return None
    pat_plus = re.compile(r"\+\s*" + re.escape(norm) + r"\b", re.IGNORECASE)
    pat_atplus = re.compile(r"AT\+\s*" + re.escape(norm) + r"\b", re.IGNORECASE)
    for page_no, body in pages:
        for line in body.splitlines():
            s = line.strip()
            if len(s) < 4 or len(s) > 260: continue
            if pat_atplus.search(s) or pat_plus.search(s):
                return (page_no, s)
    return None

p = find("dat_01")
if not p:
    print("dat_01 not found"); sys.exit(1)
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

unknown_total = 0
resolved = 0
blocked = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("status") != "unknown": continue
    unknown_total += 1
    cmd = r.get("command")
    hit = fuzzy_find(cmd) if cmd else None
    if hit:
        page_no, line = hit
        src = r.get("source") or {}
        if not isinstance(src, dict): src = {}
        src["page"] = str(page_no)
        if not src.get("section"): src["section"] = "AT Manual V1.01"
        src["quote"] = line[:260]
        if not src.get("name"): src["name"] = "SIM800 Series_AT Command Manual"
        if not src.get("version"): src["version"] = "V1.01"
        if not src.get("date"): src["date"] = "2018-05-15"
        r["source"] = src
        r["status"] = "partial"
        r["confidence"] = 0.5
        r["updated_at"] = ts
        resolved += 1
    else:
        r["status"] = "blocked"
        r["confidence"] = 0.0
        notes = r.get("notes") or ""
        marker = "Not found in AT Manual V1.01"
        if marker not in notes:
            r["notes"] = (notes + " | " + marker + "; original extraction likely spurious.").strip(" |")
        r["updated_at"] = ts
        blocked += 1

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)

summary = {"unknown_total": unknown_total, "resolved": resolved, "blocked": blocked, "total": len(records)}
(REPORTS / "_step_D3_dat01_resolve.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_01: unknown_total={unknown_total} resolved={resolved} blocked={blocked} total={len(records)}")