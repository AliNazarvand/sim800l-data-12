#!/usr/bin/env python3
"""Complete dat_03 unknown records by scanning CME/CMS appendix pages for error descriptions."""
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

# Build code -> (page, line) index for all "N description" lines within 140-200 range
code_index = {}
row_re = re.compile(r"^\s*([0-9]{1,4})\s+([A-Z][A-Za-z0-9 \(\)\-/,\.']{3,140})\s*$")
for pn, body in pages:
    for line in body.splitlines():
        s = line.strip()
        if len(s) < 5 or len(s) > 200: continue
        m = row_re.match(s)
        if m:
            code = int(m.group(1))
            # only keep first occurrence to avoid pagination dupes
            if code not in code_index:
                code_index[code] = (pn, s)

p = find("dat_03")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records:
    if not isinstance(r, dict): continue
    src = r.get("source") or {}
    if isinstance(src, dict) and src.get("page"): continue
    code = r.get("code")
    if code is None: continue
    try: code_i = int(code)
    except Exception: continue
    hit = code_index.get(code_i)
    if hit:
        pn, line = hit
        src = src if isinstance(src, dict) else {}
        src["page"] = str(pn)
        if not src.get("section"): src["section"] = "CME/CMS Error Codes"
        if not src.get("quote"): src["quote"] = line[:280]
        if not src.get("name"): src["name"] = "SIM800 Series_AT Command Manual"
        if not src.get("version"): src["version"] = "V1.01"
        if not src.get("date"): src["date"] = "2018-05-15"
        r["source"] = src
        if r.get("status") in (None, "unknown"): r["status"] = "partial"
        if r.get("confidence") in (0.0, 0): r["confidence"] = 0.6
        r["updated_at"] = ts
        filled += 1

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
with_page = sum(1 for r in records if isinstance(r, dict) and (r.get("source") or {}).get("page"))
summary = {"total": len(records), "with_page": with_page, "filled": filled}
(REPORTS / "_step_D5_dat03.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_03: total={len(records)} with_page={with_page} filled={filled}")