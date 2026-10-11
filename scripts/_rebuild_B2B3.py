#!/usr/bin/env python3
"""Rebuild dat_02 (URC) and dat_03 (Error Code):
   - Annotate existing records with source info if found in parsed JSON.
   - Add new records ONLY for entries confirmed in parsed JSON (structured sections).
   - No auto-detection outside explicit sections."""
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

def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml"))
    return c[0] if c else (DATA / (dat_id + ".yaml") if (DATA / (dat_id + ".yaml")).exists() else None)

def norm_urc(s):
    """normalize URC string like '+CMTI' -> 'CMTI'."""
    if not s: return None
    s = str(s).strip().upper()
    if s.startswith("+"):
        s = s[1:]
    if s.startswith("AT+"):
        s = s[3:]
    return s

parsed_path = REPORTS / "_step_B2B3_parsed.json"
if not parsed_path.exists():
    print("Parsed JSON missing; run _parse_B2B3.py first.", file=sys.stderr); sys.exit(2)
parsed = json.loads(parsed_path.read_text(encoding="utf-8"))
urc_entries = parsed.get("urc_entries", {})
err_entries = parsed.get("err_entries", {})

ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def next_id(prefix, existing_ids):
    i = 1
    while True:
        nid = f"{prefix}_{i:04d}"
        if nid not in existing_ids:
            return nid
        i += 1

def infer_urc_category(urc_str):
    u = urc_str.upper()
    if any(k in u for k in ["CMTI","CMT","CDS","SMS"]): return "SMS"
    if any(k in u for k in ["CREG","CGREG"]): return "Network"
    if any(k in u for k in ["CLIP","CRING","RING"]): return "Call"
    if any(k in u for k in ["CUSD"]): return "Call"
    if any(k in u for k in ["CIP","PDP","TCP","UDP"]): return "GPRS"
    if any(k in u for k in ["HTTP","FTP","SSL"]): return "Data"
    if any(k in u for k in ["POWER","SIM DETECT"]): return "System"
    return "General"

# ---- dat_02 URC ----
dat02_path = find("dat_02")
if dat02_path:
    records = yaml.safe_load(dat02_path.read_text(encoding="utf-8")) or []
    if not isinstance(records, list):
        records = [records]
    existing_ids = set(r.get("id") for r in records if isinstance(r, dict) and r.get("id"))
    existing_by_urc = {}
    for r in records:
        if not isinstance(r, dict): continue
        u = norm_urc(r.get("urc_string"))
        if u:
            existing_by_urc[u] = r
    annotated = 0
    added = 0
    for urc_key, info in urc_entries.items():
        norm = norm_urc(urc_key)
        if not norm:
            continue
        if norm in existing_by_urc:
            r = existing_by_urc[norm]
            src = r.get("source") or {}
            if not isinstance(src, dict): src = {}
            changed = False
            if not src.get("page") and info.get("page"):
                src["page"] = str(info["page"]); changed = True
            if not src.get("section"):
                src["section"] = "URC Section"; changed = True
            if not src.get("quote") and info.get("line"):
                src["quote"] = info["line"]; changed = True
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
            # add new
            new_id = next_id("dat_02", existing_ids)
            existing_ids.add(new_id)
            new_rec = {
                "id": new_id,
                "category": infer_urc_category(urc_key),
                "urc_string": urc_key,
                "trigger_event": info.get("description") or "",
                "related_command": None,
                "related_state": None,
                "format": info.get("line") or "",
                "parameters": [],
                "examples": [],
                "timing": None,
                "suppression_method": None,
                "source": {
                    "name": "SIM800 Series_AT Command Manual",
                    "version": "V1.01",
                    "date": "2018-05-15",
                    "page": str(info.get("page")) if info.get("page") else None,
                    "section": "URC Section",
                    "quote": info.get("line"),
                },
                "source_type": "primary",
                "confidence": 0.6,
                "status": "partial",
                "conflicts": [],
                "notes": "Extracted from AT Manual V1.01 URC section.",
                "applicable_models": ["SIM800L"],
                "tags": ["urc", "extracted"],
                "created_at": ts,
                "updated_at": ts,
            }
            records.append(new_rec)
            added += 1
    with dat02_path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False,
                       default_flow_style=False, width=1000)
    print(f"dat_02: total={len(records)} annotated={annotated} added={added}")
else:
    print("dat_02 file missing")

# ---- dat_03 Error Code ----
dat03_path = find("dat_03")
if dat03_path:
    records = yaml.safe_load(dat03_path.read_text(encoding="utf-8")) or []
    if not isinstance(records, list):
        records = [records]
    existing_ids = set(r.get("id") for r in records if isinstance(r, dict) and r.get("id"))
    existing_by_key = {}
    for r in records:
        if not isinstance(r, dict): continue
        t = str(r.get("error_type") or "").upper()
        c = r.get("code")
        if t and c is not None:
            existing_by_key[(t, int(c) if isinstance(c, int) or str(c).isdigit() else c)] = r
    annotated = 0
    added = 0
    for key, info in err_entries.items():
        etype = info.get("error_type", "UNKNOWN")
        code = info.get("code")
        k = (etype, code)
        if k in existing_by_key:
            r = existing_by_key[k]
            src = r.get("source") or {}
            if not isinstance(src, dict): src = {}
            changed = False
            if not src.get("page") and info.get("page"):
                src["page"] = str(info["page"]); changed = True
            if not src.get("section"):
                src["section"] = f"{etype} Error Codes"; changed = True
            if not src.get("quote") and info.get("line"):
                src["quote"] = info["line"]; changed = True
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
            new_id = next_id("dat_03", existing_ids)
            existing_ids.add(new_id)
            new_rec = {
                "id": new_id,
                "category": etype,
                "error_type": etype,
                "code": code,
                "meaning": info.get("meaning") or "",
                "description": "",
                "related_commands": [],
                "recovery_steps": [],
                "source": {
                    "name": "SIM800 Series_AT Command Manual",
                    "version": "V1.01",
                    "date": "2018-05-15",
                    "page": str(info.get("page")) if info.get("page") else None,
                    "section": f"{etype} Error Codes",
                    "quote": info.get("line"),
                },
                "source_type": "primary",
                "confidence": 0.6,
                "status": "partial",
                "conflicts": [],
                "notes": "Extracted from AT Manual V1.01 error code appendix.",
                "applicable_models": ["SIM800L"],
                "tags": ["error", etype.lower(), "extracted"],
                "created_at": ts,
                "updated_at": ts,
            }
            records.append(new_rec)
            added += 1
    with dat03_path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False,
                       default_flow_style=False, width=1000)
    print(f"dat_03: total={len(records)} annotated={annotated} added={added}")
else:
    print("dat_03 file missing")