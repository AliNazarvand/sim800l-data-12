#!/usr/bin/env python3
"""Fix L3 errors: for each cross-ref error, decide on the source record.
   If source has valid page/quote -> keep; else -> mark record blocked."""
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

summary_path = REPORTS / "_validation_summary.json"
if not summary_path.exists():
    print("No validation summary"); sys.exit(1)
s = json.loads(summary_path.read_text(encoding="utf-8"))
l3 = [e for e in s.get("errors", []) if e.get("level") == 3]
print(f"L3 errors to process: {len(l3)}")

ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
decisions = []
# group by dataset
by_ds = {}
for e in l3:
    ds = e.get("dataset", "?")
    by_ds.setdefault(ds, []).append(e)

for ds, errs in by_ds.items():
    p = find(ds)
    if not p:
        for e in errs:
            decisions.append({"dataset": ds, "record": e.get("record"), "decision": "skipped-no-file"})
        continue
    records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    if not isinstance(records, list): records = [records]
    by_id = {r.get("id"): r for r in records if isinstance(r, dict) and r.get("id")}
    for e in errs:
        rec_id = e.get("record")
        r = by_id.get(rec_id)
        if not r:
            decisions.append({"dataset": ds, "record": rec_id, "decision": "record-not-found"})
            continue
        src = r.get("source") or {}
        has_valid_source = isinstance(src, dict) and src.get("page") and src.get("quote")
        if has_valid_source:
            decisions.append({"dataset": ds, "record": rec_id, "decision": "kept-partial"})
        else:
            r["status"] = "blocked"
            r["confidence"] = 0.0
            notes = r.get("notes") or ""
            marker = "Command missing from AT Manual V1.01 cross-ref"
            if marker not in notes:
                r["notes"] = (notes + " | " + marker + ".").strip(" |")
            r["updated_at"] = ts
            decisions.append({"dataset": ds, "record": rec_id, "decision": "marked-blocked"})
    with p.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)

out = {
    "total_l3": len(l3),
    "decided": len(decisions),
    "decisions": decisions,
}
(REPORTS / "_step_D3_L3_decisions.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"L3 decisions: {len(decisions)} / {len(l3)}")