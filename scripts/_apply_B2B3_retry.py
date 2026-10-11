#!/usr/bin/env python3
"""Apply parsed retry results to dat_02 (URC) and dat_03 (Error Code)."""
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
    if not s: return None
    s = str(s).strip().upper()
    if s.startswith("AT+"):
        s = s[3:]
    elif s.startswith("+"):
        s = s[1:]
    return s

ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
parsed = json.loads((REPORTS / "_step_B2B3_parsed_retry.json").read_text(encoding="utf-8"))
urc_entries = parsed.get("urc_entries", {})
err_entries = parsed.get("err_entries", {})

# ---------- dat_02 ----------
dat02 = find("dat_02")
if dat02:
    records = yaml.safe_load(dat02.read_text(encoding="utf-8")) or []
    if not isinstance(records, list):
        records = [records]
    existing_ids = set(r.get("id") for r in records if isinstance(r, dict) and r.get("id"))
    existing_by_urc = {}
    for r in records:
        if not isinstance(r, dict): continue
        u = norm_urc(r.get("urc_string"))
        if u:
            existing_by_urc[u] = r
    added = 0
    annotated = 0
    def next_id():
        i = 1
        while True:
            nid = f"dat_02_{i:04d}"
            if nid not in existing_ids:
                return nid
            i += 1
    for u, info in urc_entries.items():
        n = norm_urc(u)
        if not n: continue
        if n in existing_by_urc:
            r = existing_by_urc[n]
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
            nid = next_id()
            existing_ids.add(nid)
            records.append({
                "id": nid,
                "category": "URC",
                "urc_string": u,
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
                "notes": "Extracted from AT Manual V1.01 (broad retry).",
                "applicable_models": ["SIM800L"],
                "tags": ["urc", "extracted"],
                "created_at": ts,
                "updated_at": ts,
            })
            added += 1
    with dat02.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False,
                       default_flow_style=False, width=1000)
    print(f"dat_02: total={len(records)} annotated={annotated} added={added}")

# ---------- dat_03 ----------
dat03 = find("dat_03")
if dat03:
    records = yaml.safe_load(dat03.read_text(encoding="utf-8")) or []
    if not isinstance(records, list):
        records = [records]
    existing_ids = set(r.get("id") for r in records if isinstance(r, dict) and r.get("id"))
    existing_by_key = {}
    for r in records:
        if not isinstance(r, dict): continue
        t = str(r.get("error_type") or "").upper()
        c = r.get("code")
        if t and c is not None:
            existing_by_key[(t, int(c) if str(c).isdigit() else c)] = r
    added = 0
    annotated = 0
    def next_id3():
        i = 1
        while True:
            nid = f"dat_03_{i:04d}"
            if nid not in existing_ids:
                return nid
            i += 1
    for key, info in err_entries.items():
        et = info.get("error_type", "UNKNOWN")
        code = info.get("code")
        k = (et, code)
        if k in existing_by_key:
            r = existing_by_key[k]
            src = r.get("source") or {}
            if not isinstance(src, dict): src = {}
            changed = False
            if not src.get("page") and info.get("page"):
                src["page"] = str(info["page"]); changed = True
            if not src.get("section"):
                src["section"] = f"{et} Error Codes"; changed = True
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
            nid = next_id3()
            existing_ids.add(nid)
            records.append({
                "id": nid,
                "category": et,
                "error_type": et,
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
                    "section": f"{et} Error Codes",
                    "quote": info.get("line"),
                },
                "source_type": "primary",
                "confidence": 0.6,
                "status": "partial",
                "conflicts": [],
                "notes": "Extracted from AT Manual V1.01 (broad retry).",
                "applicable_models": ["SIM800L"],
                "tags": ["error", et.lower(), "extracted"],
                "created_at": ts,
                "updated_at": ts,
            })
            added += 1
    with dat03.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False,
                       default_flow_style=False, width=1000)
    print(f"dat_03: total={len(records)} annotated={annotated} added={added}")