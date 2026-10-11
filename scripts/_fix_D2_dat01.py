#!/usr/bin/env python3
"""Complete dat_01 unknown records by finding command headers in AT Manual."""
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
HEADER_RE = re.compile(r"^\s*([0-9]+(?:\.[0-9]+){1,4})\s+(AT\+[A-Z0-9]+)\s+(.{2,120}?)\s*$")

cmd_index = {}
for page_no, body in pages:
    for line in body.splitlines():
        s = line.strip()
        if len(s) < 6 or len(s) > 200: continue
        if re.match(r"^AT\+[A-Z0-9]+\s*\.{3,}", s): continue
        m = HEADER_RE.match(s)
        if m:
            c = m.group(2).strip().upper()
            if c not in cmd_index:
                cmd_index[c] = {"page": page_no, "section_number": m.group(1).strip(),
                                "section_title": m.group(3).strip()[:120], "line": s[:280]}

p = find("dat_01")
if not p:
    print("dat_01 not found"); sys.exit(1)
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
recovered = 0; blocked = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("status") != "unknown": continue
    cmd = r.get("command")
    if not cmd: continue
    norm = str(cmd).strip().upper()
    if norm.startswith("AT+"): norm2 = norm
    elif norm.startswith("+"): norm2 = "AT" + norm
    else: norm2 = "AT+" + norm.lstrip("AT").lstrip("+")
    info = cmd_index.get(norm2) or cmd_index.get(norm)
    if info:
        src = r.get("source") or {}
        if not isinstance(src, dict): src = {}
        src["page"] = str(info["page"])
        if not src.get("section"):
            src["section"] = f"{info['section_number']} {info['section_title']}".strip()[:160]
        if not src.get("quote"): src["quote"] = info["line"]
        if not src.get("name"): src["name"] = "SIM800 Series_AT Command Manual"
        if not src.get("version"): src["version"] = "V1.01"
        if not src.get("date"): src["date"] = "2018-05-15"
        r["source"] = src
        r["status"] = "partial"
        r["confidence"] = 0.6
        r["updated_at"] = ts
        recovered += 1
    else:
        blocked += 1

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
summary = {"recovered": recovered, "still_unknown": blocked, "total": len(records)}
(REPORTS / "_step_D2_dat01_fix.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_01: recovered={recovered} still_unknown={blocked} total={len(records)}")