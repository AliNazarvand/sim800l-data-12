#!/usr/bin/env python3
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

TARGET_CMDS = ["AT+SSLSETCERT","AT+SSLSETKEY","AT+SSLSETCA","AT+SSLCFG","AT+SSLCONF"]

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
found = {}
for page_no, body in pages:
    for line in body.splitlines():
        s = line.strip()
        if len(s) < 6 or len(s) > 200: continue
        if re.match(r"^AT\+[A-Z0-9]+\s*\.{3,}", s): continue
        m = HEADER_RE.match(s)
        if m:
            cmd = m.group(2).strip()
            if cmd in TARGET_CMDS and cmd not in found:
                found[cmd] = {"command": cmd, "section_number": m.group(1).strip(),
                              "section_title": m.group(3).strip()[:120], "page": page_no, "quote": s[:280]}
report = {"found": len(found), "commands": list(found.keys())}
(REPORTS / "_step_B6_dat17_scan.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_17 scan: found={len(found)} commands={list(found.keys())}")