#!/usr/bin/env python3
"""Rebuild dat_09 (SMS) from AT Manual V1.01 structured sections."""
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

SMS_COMMANDS = ["AT+CMGF","AT+CSMS","AT+CPMS","AT+CMGS","AT+CMGR","AT+CMGL","AT+CMGD",
                "AT+CMGW","AT+CSCA","AT+CSCS","AT+CSMP","AT+CNMI","AT+CSDH","AT+CMEE"]

def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml"))
    return c[0] if c else (DATA / (dat_id + ".yaml") if (DATA / (dat_id + ".yaml")).exists() else None)

def load_paged(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    pages = []
    parts = re.split(r"<<<PAGE\s+(\d+)>>>", text)
    for i in range(1, len(parts) - 1, 2):
        try:
            num = int(parts[i])
        except Exception:
            continue
        pages.append((num, parts[i + 1]))
    return pages

pages = load_paged(SRC_EX / "at_manual_v1_01_paged.txt")

# Header pattern: "N.N.N AT+XXX Title"
HEADER_RE = re.compile(r"^\s*([0-9]+(?:\.[0-9]+){1,4})\s+(AT\+[A-Z0-9]+)\s+(.{2,120}?)\s*$")

found = {}
for page_no, body in pages:
    for line in body.splitlines():
        s = line.strip()
        if len(s) < 6 or len(s) > 200:
            continue
        if re.match(r"^AT\+[A-Z0-9]+\s*\.{3,}", s):
            continue
        m = HEADER_RE.match(s)
        if m:
            cmd = m.group(2).strip()
            if cmd in SMS_COMMANDS and cmd not in found:
                found[cmd] = {
                    "command": cmd,
                    "section_number": m.group(1).strip(),
                    "section_title": m.group(3).strip()[:120],
                    "page": page_no,
                    "quote": s[:280],
                }

ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
dat09 = find("dat_09")
if not dat09:
    print("dat_09 not found"); sys.exit(1)
records = yaml.safe_load(dat09.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
existing_ids = set(r.get("id") for r in records if isinstance(r, dict) and r.get("id"))
existing_by_cmd = {}
for r in records:
    if not isinstance(r, dict): continue
    cmd = r.get("command")
    if cmd:
        existing_by_cmd[str(cmd).upper()] = r

added = 0
annotated = 0

def next_id():
    i = 1
    while True:
        nid = f"dat_09_{i:04d}"
        if nid not in existing_ids:
            return nid
        i += 1

for cmd, info in found.items():
    cmd_u = cmd.upper()
    if cmd_u in existing_by_cmd:
        r = existing_by_cmd[cmd_u]
        src = r.get("source") or {}
        if not isinstance(src, dict): src = {}
        changed = False
        if not src.get("page") and info.get("page"):
            src["page"] = str(info["page"]); changed = True
        if not src.get("section"):
            src["section"] = f"{info['section_number']} {info['section_title']}".strip()[:160]; changed = True
        if not src.get("quote") and info.get("quote"):
            src["quote"] = info["quote"]; changed = True
        if not src.get("name"):
            src["name"] = "SIM800 Series_AT Command Manual"; changed = True
        if not src.get("version"):
            src["version"] = "V1.01"; changed = True
        if not src.get("date"):
            src["date"] = "2018-05-15"; changed = True
        r["source"] = src
        if changed:
            if r.get("status") in (None, "unknown"):
                r["status"] = "partial"
            if r.get("confidence") in (0.0, 0):
                r["confidence"] = 0.6
            r["updated_at"] = ts
            annotated += 1
    else:
        nid = next_id()
        existing_ids.add(nid)
        records.append({
            "id": nid,
            "category": "SMS",
            "mode": "write",
            "command": cmd,
            "syntax": info.get("quote") or (cmd + "=<...>"),
            "parameters": [],
            "response_success": None,
            "response_error": None,
            "examples": [],
            "related_urcs": [],
            "related_states": [],
            "related_commands": [],
            "firmware_min": None,
            "firmware_max": None,
            "source": {
                "name": "SIM800 Series_AT Command Manual",
                "version": "V1.01",
                "date": "2018-05-15",
                "page": str(info.get("page")) if info.get("page") else None,
                "section": f"{info.get('section_number','')} {info.get('section_title','')}".strip()[:160] or None,
                "quote": info.get("quote"),
            },
            "source_type": "primary",
            "confidence": 0.6,
            "status": "partial",
            "conflicts": [],
            "notes": "Extracted from AT Manual V1.01 SMS section.",
            "applicable_models": ["SIM800L"],
            "tags": ["sms", "extracted"],
            "created_at": ts,
            "updated_at": ts,
        })
        added += 1

with dat09.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False,
                   default_flow_style=False, width=1000)

partial_count = sum(1 for r in records if isinstance(r, dict) and r.get("status") == "partial")
report = {
    "file": dat09.name,
    "total": len(records),
    "added": added,
    "annotated": annotated,
    "partial": partial_count,
    "commands_found": len(found),
    "commands": list(found.keys()),
}
(REPORTS / "_step_B4_dat09.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_09: total={len(records)} added={added} annotated={annotated} partial={partial_count} found={len(found)}")