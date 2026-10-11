#!/usr/bin/env python3
"""Re-annotate a dataset from V2.02 with broader keywords.
   CLI: <dat_id> <search_keys_csv> <ctx_keywords_csv> <out_json>"""
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

def find_term(term, pages, ctx_keywords):
    if not term: return None
    pat = re.compile(r"\b" + re.escape(str(term).strip()) + r"\b", re.IGNORECASE)
    for page_no, body in pages:
        for line in body.splitlines():
            s = line.strip()
            if len(s) < 4 or len(s) > 260: continue
            if pat.search(s):
                if any(k in s.lower() for k in ctx_keywords):
                    return (page_no, s)
    return None

def main():
    dat_id = sys.argv[1]
    search_keys = sys.argv[2].split(",")
    ctx_keywords = [k.strip().lower() for k in sys.argv[3].split(",")]
    out_json = sys.argv[4]

    pages = load_paged(SRC_EX / "v2_02_paged.txt")
    p = find(dat_id)
    if not p:
        print(f"{dat_id} not found"); sys.exit(1)
    records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    if not isinstance(records, list): records = [records]
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with_page = 0; updated = 0
    for r in records:
        if not isinstance(r, dict): continue
        src = r.get("source") or {}
        if not isinstance(src, dict): src = {}
        if src.get("page"):
            with_page += 1
            continue
        for k in search_keys:
            v = r.get(k)
            if v:
                hit = find_term(v, pages, ctx_keywords)
                if hit:
                    page_no, line = hit
                    src["page"] = str(page_no)
                    if not src.get("section"): src["section"] = "SIM800H&SIM800L_Hardware_Design V2.02"
                    if not src.get("quote"): src["quote"] = line[:260]
                    if not src.get("name"): src["name"] = "SIM800H&SIM800L_Hardware_Design"
                    if not src.get("version"): src["version"] = "V2.02"
                    if not src.get("date"): src["date"] = "2015-07-27"
                    r["source"] = src
                    if r.get("status") == "unknown": r["status"] = "partial"
                    if r.get("confidence") in (0.0, 0): r["confidence"] = 0.5
                    r["updated_at"] = ts
                    updated += 1; with_page += 1
                    break
    with p.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
    pct = (with_page / len(records) * 100) if records else 0
    summary = {"total": len(records), "with_page": with_page, "updated": updated, "page_pct": round(pct, 1)}
    (REPORTS / out_json).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{dat_id}: total={len(records)} with_page={with_page} updated={updated} page_pct={pct:.1f}%")

if __name__ == "__main__":
    main()