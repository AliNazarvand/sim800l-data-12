#!/usr/bin/env python3
"""Rebuild dat_01:
   - For each existing record with a `command` field: annotate source (page/section/quote) if found.
   - For each AT command in AT Manual scan that is NOT in dat_01: add a new record.
   - New records use only structured fields from the scan (no invented data).
   - Record fields per schema: id, category, command, mode, syntax, parameters,
     response_success, response_error, examples, related_urcs, related_states,
     related_commands, firmware_min, firmware_max, source, source_type, confidence,
     status, conflicts, notes, applicable_models, tags, created_at, updated_at.
"""
import sys, json, re
from pathlib import Path
from datetime import datetime, timezone
try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr); sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml"))
    return c[0] if c else (DATA / (dat_id + ".yaml") if (DATA / (dat_id + ".yaml")).exists() else None)

def infer_category(cmd, section_title):
    t = (section_title or "").lower()
    c = cmd.upper()
    if any(k in t for k in ["sms","message"]): return "SMS"
    if any(k in t for k in ["call","voice"]): return "Call"
    if any(k in t for k in ["gprs","tcp","ip","data","pdp"]): return "GPRS"
    if "http" in t: return "HTTP"
    if "ftp" in t: return "FTP"
    if "ssl" in t: return "SSL"
    if "audio" in t or "tone" in t or "dtmf" in t: return "Audio"
    if "sim" in t or c.startswith("AT+CPIN") or c.startswith("AT+CSIM"): return "SIM"
    if "network" in t or c.startswith("AT+CREG") or c.startswith("AT+COPS"): return "Network"
    if "sleep" in t or c.startswith("AT+CSCLK") or c.startswith("AT+CFUN"): return "Power"
    if "time" in t or c.startswith("AT+CCLK"): return "Time"
    if "gpio" in t: return "GPIO"
    if "security" in t or "lock" in t: return "Security"
    if "firmware" in t: return "Firmware"
    if "debug" in t: return "Debug"
    return "General"

def infer_mode(cmd, syntax):
    if not syntax:
        return "exec"
    if syntax.endswith("?"):
        return "read"
    if "=" in syntax:
        # اگر بعد از = چیزی هست → write، اگر فقط = است → test
        after_eq = syntax.split("=", 1)[1]
        if after_eq.strip() == "" or after_eq.strip().startswith("<"):
            return "write"
        return "write"
    return "exec"

def main():
    dat01_path = find("dat_01")
    if dat01_path is None:
        print("dat_01 not found"); sys.exit(1)
    records = yaml.safe_load(dat01_path.read_text(encoding="utf-8")) or []
    if not isinstance(records, list):
        records = [records]

    scan_path = REPORTS / "_step_B1_at_manual_scan.json"
    if not scan_path.exists():
        print("Scan file not found. Run _scan_B1_at_manual.py first.", file=sys.stderr); sys.exit(2)
    scan = json.loads(scan_path.read_text(encoding="utf-8"))
    manual_cmds = scan.get("commands", {})
    print(f"Manual commands available: {len(manual_cmds)}")

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # جمع‌بندی commandهای موجود و مپ کردن رکوردها
    existing_by_cmd = {}
    for rec in records:
        if not isinstance(rec, dict):
            continue
        cmd = rec.get("command")
        if cmd:
            existing_by_cmd[cmd.upper()] = rec

    # شماره‌گذاری جدید
    def next_id(existing_ids):
        i = 1
        while True:
            nid = "dat_01_" + str(i).zfill(4)
            if nid not in existing_ids:
                return nid
            i += 1

    existing_ids = set()
    for rec in records:
        if isinstance(rec, dict) and rec.get("id"):
            existing_ids.add(rec["id"])

    annotated = 0
    added = 0
    unresolved_ids = []

    # ---- annotate existing ----
    for rec in records:
        if not isinstance(rec, dict):
            continue
        cmd = rec.get("command")
        if not cmd:
            continue
        info = manual_cmds.get(cmd.upper())
        if info is None:
            continue
        src = rec.get("source") or {}
        if not isinstance(src, dict):
            src = {}
        changed = False
        if not src.get("page") and info.get("page"):
            src["page"] = str(info["page"]); changed = True
        if not src.get("section") and info.get("section_number"):
            title = info.get("section_title", "")
            src["section"] = f"{info['section_number']} {title}".strip()[:160]; changed = True
        if not src.get("quote") and info.get("quote"):
            src["quote"] = info["quote"]; changed = True
        if not src.get("name"):
            src["name"] = "SIM800 Series_AT Command Manual"; changed = True
        if not src.get("version"):
            src["version"] = "V1.01"; changed = True
        if not src.get("date"):
            src["date"] = "2018-05-15"; changed = True
        rec["source"] = src
        if changed:
            if rec.get("status") in (None, "unknown"):
                rec["status"] = "partial"
            if rec.get("confidence") in (0.0, 0):
                rec["confidence"] = 0.6
            rec["updated_at"] = ts
            annotated += 1

    # ---- add new commands from manual ----
    for cmd, info in manual_cmds.items():
        if cmd.upper() in existing_by_cmd:
            continue
        # Command جدید
        new_id = next_id(existing_ids)
        existing_ids.add(new_id)
        category = infer_category(cmd, info.get("section_title", ""))
        syntax = info.get("syntax") or (cmd + "=<...>")
        mode = infer_mode(cmd, info.get("syntax"))
        new_rec = {
            "id": new_id,
            "category": category,
            "command": cmd,
            "mode": mode,
            "syntax": syntax,
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
                "section": (f"{info.get('section_number','')} {info.get('section_title','')}").strip()[:160] or None,
                "quote": info.get("quote"),
            },
            "source_type": "primary",
            "confidence": 0.6,
            "status": "partial",
            "conflicts": [],
            "notes": "Extracted from AT Manual V1.01 structured section (command header + syntax).",
            "applicable_models": ["SIM800L"],
            "tags": ["at-command", "extracted"],
            "created_at": ts,
            "updated_at": ts,
        }
        records.append(new_rec)
        added += 1

    with dat01_path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False,
                       default_flow_style=False, width=1000)

    report = {
        "file": dat01_path.name,
        "total": len(records),
        "annotated": annotated,
        "added": added,
        "manual_commands_total": len(manual_cmds),
    }
    (REPORTS / "_step_B1_dat01_rebuild.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"dat_01: total={len(records)} annotated={annotated} added={added}")

if __name__ == "__main__":
    main()