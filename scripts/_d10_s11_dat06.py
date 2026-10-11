#!/usr/bin/env python3
import sys, json
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
    return c[0] if c else None
p = find("dat_06")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
converted = 0
for r in records:
    if not isinstance(r, dict): continue
    src = r.get("source") or {}
    has_page = isinstance(src, dict) and src.get("page")
    if has_page: continue
    if r.get("status") in (None, "unknown", "partial"):
        r["status"] = "blocked"
        r["confidence"] = 0.0
        notes = r.get("notes") or ""
        marker = "No additional init source in V2.02"
        if marker not in notes:
            r["notes"] = (notes + " | " + marker + ".").strip(" |")
        r["updated_at"] = ts
        converted += 1

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
u = sum(1 for r in records if isinstance(r, dict) and r.get("status") == "unknown")
b = sum(1 for r in records if isinstance(r, dict) and r.get("status") == "blocked")
pp = sum(1 for r in records if isinstance(r, dict) and r.get("status") == "partial")
(REPORTS / "_step_D10_dat06.json").write_text(json.dumps({"total":len(records),"unknown":u,"blocked":b,"partial":pp,"converted":converted}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_06: total={len(records)} unknown={u} blocked={b} partial={pp} converted={converted}")