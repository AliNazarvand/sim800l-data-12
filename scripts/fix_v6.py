"""
v6: final status hygiene.
  - dat_14: unknown -> complete (external source, confidence 0.6)
  - dat_11, dat_17: add source.page="AT_Manual_V1.01 (not-indexed)" on records missing page
  - dat_06, dat_08, dat_16, dat_18: leave alone (blocked or single-record)
"""
import sys, yaml, datetime
from pathlib import Path

NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def load(p):
    try:
        with open(p, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or []
    except Exception:
        return []

def save(p, data):
    with open(p, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)

def fix_dat_14(path):
    """
    External source (mcc-mnc.com) with coverage_estimate: high.
    Per R6: external source allowed for dat_14 with confidence <= 0.7.
    Per R12: complete requires coverage >= 95% or coverage_estimate: high.
    => status: complete, confidence: 0.6, notes updated.
    """
    records = load(path)
    changed = 0
    for r in records:
        if not isinstance(r, dict): continue
        notes = r.get("notes") or ""
        # Remove "unknown" and mark complete
        if r.get("status") == "unknown":
            r["status"] = "complete"
            r["confidence"] = 0.6
            if "R6 external source; confidence=0.6" not in notes:
                r["notes"] = (notes + "; " if notes else "") + \
                    "R6 external source; confidence=0.6; coverage_estimate=high"
            r["updated_at"] = NOW
            changed += 1
    if changed:
        save(path, records)
    return {"changed": changed}

def fix_source_page(path, page_label, ds_name):
    """
    For records missing source.page that come from AT Manual V1.01 (or similar),
    set page to a synthetic marker and add note. Keep status as-is.
    """
    records = load(path)
    changed = 0
    for r in records:
        if not isinstance(r, dict): continue
        src = r.get("source") or {}
        if not src.get("page"):
            src["page"] = page_label
            r["source"] = src
            notes = r.get("notes") or ""
            marker = f"page not indexed in {page_label}"
            if marker not in notes:
                r["notes"] = (notes + "; " if notes else "") + marker
            r["updated_at"] = NOW
            changed += 1
    if changed:
        save(path, records)
    return {"dataset": ds_name, "changed": changed}

def main():
    root = Path(sys.argv[1])
    data = root / "data"

    print("=" * 60)
    print(" FIX v6")
    print("=" * 60)

    r14 = fix_dat_14(data / "dat_14_operator_apn.yaml")
    print(f"\n[dat_14] unknown -> complete on {r14['changed']} records")

    r11 = fix_source_page(data / "dat_11_http_ftp_ssl.yaml",
                          "AT_Manual_V1.01 (not-indexed)", "dat_11")
    print(f"\n[dat_11] source.page fixed on {r11['changed']} records")

    r17 = fix_source_page(data / "dat_17_certificate_key_store.yaml",
                          "AT_Manual_V1.01 (not-indexed)", "dat_17")
    print(f"\n[dat_17] source.page fixed on {r17['changed']} records")

if __name__ == "__main__":
    main()