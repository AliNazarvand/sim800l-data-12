#!/usr/bin/env python3
"""Extract rows with at least 2 numeric values + unit (ms/us/mA/V) from V2.02 tables.
   Adds new records or annotates existing ones for dat_04 and dat_06."""
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

pages = load_paged(SRC_EX / "v2_02_paged.txt")

NUM_RE = re.compile(r"\b\d+(?:\.\d+)?\b")
UNIT_RE = re.compile(r"\b(ms|us|µs|mA|uA|µA|V|mV|kbps|MHz|Hz)\b", re.IGNORECASE)

def table_rows(pages, ctx_keywords):
    """Return list of (page, line) with >=2 numbers and a unit."""
    rows = []
    seen = set()
    for page_no, body in pages:
        for line in body.splitlines():
            s = line.strip()
            if len(s) < 8 or len(s) > 200: continue
            if s in seen: continue
            nums = NUM_RE.findall(s)
            if len(nums) < 2: continue
            if not UNIT_RE.search(s): continue
            low = s.lower()
            if not any(k in low for k in ctx_keywords): continue
            seen.add(s)
            rows.append((page_no, s))
    return rows

def add_extend(dat_id, ctx_keywords, category, tags):
    p = find(dat_id)
    if not p: return {"total": 0, "added": 0, "found_rows": 0}
    records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    if not isinstance(records, list): records = [records]
    existing_ids = set(r.get("id") for r in records if isinstance(r, dict) and r.get("id"))
    existing_quotes = set()
    for r in records:
        if not isinstance(r, dict): continue
        src = r.get("source") or {}
        q = src.get("quote") if isinstance(src, dict) else None
        if q: existing_quotes.add(q.strip())
    rows = table_rows(pages, ctx_keywords)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    added = 0
    counter = 9000
    for page_no, line in rows:
        if line in existing_quotes: continue
        counter += 1
        nid = f"{dat_id}_{counter:04d}"
        while nid in existing_ids:
            counter += 1
            nid = f"{dat_id}_{counter:04d}"
        existing_ids.add(nid)
        records.append({
            "id": nid,
            "category": category,
            "parameter": line[:120],
            "value_min": None, "value_typ": None, "value_max": None,
            "unit": None, "condition": None,
            "wake_source": None,
            "related_commands": [], "related_states": [],
            "source": {
                "name": "SIM800H&SIM800L_Hardware_Design",
                "version": "V2.02", "date": "2015-07-27",
                "page": str(page_no), "section": "Table (V2.02)",
                "quote": line[:280],
            },
            "source_type": "primary", "confidence": 0.4,
            "status": "partial", "conflicts": [],
            "notes": "Extracted from V2.02 table row (2+ numeric + unit). Values need manual verification.",
            "applicable_models": ["SIM800L"],
            "tags": tags,
            "created_at": ts, "updated_at": ts,
        })
        added += 1
    with p.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
    return {"total": len(records), "added": added, "found_rows": len(rows)}

ctx04 = ["timing","reset","power","sequence","ms","us","delay","current"]
ctx06 = ["initial","startup","boot","power-on","sequence","step"]
r04 = add_extend("dat_04", ctx04, "Timing", ["timing","extracted-table"])
r06 = add_extend("dat_06", ctx06, "Init Sequence", ["init","extracted-table"])
print(f"dat_04: total={r04['total']} added={r04['added']} found_rows={r04['found_rows']}")
print(f"dat_06: total={r06['total']} added={r06['added']} found_rows={r06['found_rows']}")

summary = {"dat_04": r04, "dat_06": r06}
(REPORTS / "_step_D3_dat04_06_extend.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")