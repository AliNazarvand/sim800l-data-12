"""
Conservative status hygiene:
  - For any record with status='complete' AND missing source.page:
      -> status = 'partial', add note 'missing source.page (R2)'
  - For any record with status='complete' AND confidence < 0.8:
      -> status = 'partial', add note 'confidence<0.8 (R2)'
  - Never deletes records; only downgrades status and appends notes.
"""
import sys, yaml
from pathlib import Path

def load(p):
    try:
        with open(p, encoding="utf-8") as f:
            return yaml.safe_load(f) or []
    except Exception:
        return None

def main():
    root = Path(sys.argv[1])
    data_dir = root / "data"
    changed_total = 0
    per_ds = []
    for f in sorted(data_dir.glob("dat_*.yaml")):
        recs = load(f)
        if not isinstance(recs, list): continue
        changed = 0
        for r in recs:
            if not isinstance(r, dict): continue
            if r.get("status") != "complete": continue
            src = r.get("source") or {}
            reason = None
            if not src.get("page"):
                reason = "missing source.page (R2)"
            else:
                try:
                    if float(r.get("confidence", 1.0)) < 0.8:
                        reason = "confidence<0.8 (R2)"
                except (TypeError, ValueError):
                    reason = "non-numeric confidence (R2)"
            if reason:
                r["status"] = "partial"
                notes = (r.get("notes") or "")
                if reason not in notes:
                    r["notes"] = (notes + "; " if notes else "") + reason
                changed += 1
        if changed:
            with open(f, "w", encoding="utf-8") as fh:
                yaml.safe_dump(recs, fh, allow_unicode=True, sort_keys=False)
            changed_total += changed
            per_ds.append({"dataset": f.stem, "downgraded": changed})
    print(f"Total records downgraded: {changed_total}")
    for d in per_ds:
        print(f"  {d['dataset']}: {d['downgraded']}")

if __name__ == "__main__":
    main()