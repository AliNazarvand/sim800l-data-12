#!/usr/bin/env python3
"""Generic filler: search for missing-page records using AT Manual text."""
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

def fuzzy(term):
    if not term: return None
    pat = re.compile(re.escape(str(term).strip()), re.IGNORECASE)
    for pn, body in pages:
        for line in body.splitlines():
            s = line.strip()
            if len(s) < 4 or len(s) > 240: continue
            if pat.search(s):
                return (pn, s)
    return None

def process(dat_id):
    p = find(dat_id)
    if not p:
        return {"total": 0, "with_page": 0, "filled": 0, "blocked": 0, "note": "file missing"}
    records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    if not isinstance(records, list): records = [records]
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    filled = 0; blocked = 0
    for r in records:
        if not isinstance(r, dict): continue
        src = r.get("source") or {}
        if isinstance(src, dict) and src.get("page"): continue
        # Try terms: meaning, description, code
        hit = None
        for key in ("meaning", "description", "command", "category", "parameter", "state_name"):
            v = r.get(key)
            if v:
                hit = fuzzy(str(v)[:40])
                if hit: break
        code = r.get("code")
        if not hit and code is not None:
            hit = fuzzy(str(code))
        if hit:
            pn, line = hit
            src = src if isinstance(src, dict) else {}
            src["page"] = str(pn)
            if not src.get("section"): src["section"] = "AT Manual V1.01"
            if not src.get("quote"): src["quote"] = line[:260]
            if not src.get("name"): src["name"] = "SIM800 Series_AT Command Manual"
            if not src.get("version"): src["version"] = "V1.01"
            if not src.get("date"): src["date"] = "2018-05-15"
            r["source"] = src
            if r.get("status") in (None, "unknown"): r["status"] = "partial"
            if r.get("confidence") in (0.0, 0): r["confidence"] = 0.5
            r["updated_at"] = ts
            filled += 1
        else:
            r["status"] = "blocked"
            r["confidence"] = 0.0
            notes = r.get("notes") or ""
            marker = "Not found in AT Manual V1.01"
            if marker not in notes:
                r["notes"] = (notes + " | " + marker + ".").strip(" |")
            r["updated_at"] = ts
            blocked += 1
    with p.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
    with_page = sum(1 for r in records if isinstance(r, dict) and (r.get("source") or {}).get("page"))
    blocked_c = sum(1 for r in records if isinstance(r, dict) and r.get("status") == "blocked")
    return {"total": len(records), "with_page": with_page, "filled": filled, "blocked": blocked_c}

dat_id = sys.argv[1]
out_json = sys.argv[2]
summary = process(dat_id)
(REPORTS / out_json).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{dat_id}: total={summary['total']} with_page={summary['with_page']} filled={summary['filled']} blocked={summary['blocked']}")