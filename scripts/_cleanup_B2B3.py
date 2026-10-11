#!/usr/bin/env python3
"""Mark suspicious records as unknown/0.0 based on audit output."""
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
    return c[0] if c else (DATA / (dat_id + ".yaml") if (DATA / (dat_id + ".yaml")).exists() else None)

audit = json.loads((REPORTS / "_step_B4_audit_B2B3.json").read_text(encoding="utf-8"))
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def clean(dat_id, suspicious_ids):
    p = find(dat_id)
    if not p:
        return 0, 0
    records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    if not isinstance(records, list): records = [records]
    before_partial = sum(1 for r in records if isinstance(r, dict) and r.get("status") == "partial")
    changed = 0
    for r in records:
        if not isinstance(r, dict): continue
        rid = r.get("id")
        if rid in suspicious_ids:
            r["status"] = "unknown"
            r["confidence"] = 0.0
            notes = r.get("notes") or ""
            if "Suspected command syntax, not URC" not in notes and dat_id == "dat_02":
                r["notes"] = (notes + " | Suspected command syntax, not URC. Needs manual verification.").strip(" |")
            if "Suspected non-error-code entry" not in notes and dat_id == "dat_03":
                r["notes"] = (notes + " | Suspected non-error-code entry. Needs manual verification.").strip(" |")
            r["updated_at"] = ts
            changed += 1
    after_partial = sum(1 for r in records if isinstance(r, dict) and r.get("status") == "partial")
    with p.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False,
                       default_flow_style=False, width=1000)
    return before_partial, after_partial

b2, a2 = clean("dat_02", audit.get("dat_02", {}).get("suspicious", []))
b3, a3 = clean("dat_03", audit.get("dat_03", {}).get("suspicious", []))
print(f"dat_02 partial: {b2} -> {a2}")
print(f"dat_03 partial: {b3} -> {a3}")

# ذخیره نتیجه برای گیت
(REPORTS / "_step_B4_cleanup.json").write_text(json.dumps({
    "dat_02": {"before_partial": b2, "after_partial": a2},
    "dat_03": {"before_partial": b3, "after_partial": a3},
}, ensure_ascii=False, indent=2), encoding="utf-8")