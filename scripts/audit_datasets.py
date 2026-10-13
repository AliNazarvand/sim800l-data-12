"""
Read-only audit of data/ to detect data-quality problems:
  - duplicate ids
  - duplicate (pin_number, name) in dat_07
  - records without source.page
  - records with status=complete but confidence<0.8
  - status distribution per dataset
Writes reports/DATA_HEALTH_REPORT.md and prints JSON summary.
"""
import sys, json, yaml, re
from pathlib import Path
from collections import Counter, defaultdict

def load(p):
    try:
        with open(p, encoding="utf-8") as f:
            return yaml.safe_load(f) or []
    except Exception:
        return []

def norm(s):
    return re.sub(r"\s+", " ", str(s or "").strip().lower())

def main():
    root = Path(sys.argv[1])
    data_dir = root / "data"
    reports = root / "reports"
    reports.mkdir(parents=True, exist_ok=True)

    findings = {"datasets": [], "global": {"duplicate_ids": [],
                "dat07_duplicate_pins": [], "missing_source_page": 0,
                "complete_low_conf": 0}}

    for f in sorted(data_dir.glob("dat_*.yaml")):
        recs = load(f)
        if not isinstance(recs, list): recs = [recs] if recs else []
        ds = f.stem
        ids = Counter()
        missing_page = 0
        low_conf = 0
        for r in recs:
            if not isinstance(r, dict): continue
            ids[r.get("id","?")] += 1
            src = r.get("source") or {}
            if not src.get("page"):
                missing_page += 1
            if r.get("status") == "complete":
                try:
                    if float(r.get("confidence", 0)) < 0.8:
                        low_conf += 1
                except (TypeError, ValueError):
                    pass
        dups = [k for k, v in ids.items() if v > 1]
        findings["datasets"].append({
            "dataset": ds, "records": len(recs),
            "duplicate_ids": len(dups),
            "missing_source_page": missing_page,
            "complete_low_conf": low_conf,
        })
        findings["global"]["missing_source_page"] += missing_page
        findings["global"]["complete_low_conf"] += low_conf
        for d in dups:
            findings["global"]["duplicate_ids"].append({"dataset": ds, "id": d})

    # dat_07 pin dedup check
    p07 = data_dir / "dat_07_hardware_reference.yaml"
    if p07.exists():
        recs = load(p07)
        if isinstance(recs, list):
            keys = Counter()
            for r in recs:
                if not isinstance(r, dict): continue
                k = (norm(r.get("pin_number")), norm(r.get("name")))
                if k != ("",""): keys[k] += 1
            for k, v in keys.items():
                if v > 1:
                    findings["global"]["dat07_duplicate_pins"].append({
                        "pin_number": k[0], "name": k[1], "count": v})

    (reports / "_data_health.json").write_text(
        json.dumps(findings, indent=2), encoding="utf-8")

    # markdown report
    lines = ["# DATA HEALTH REPORT", "",
             "## Per-dataset",
             "| Dataset | Records | Dup IDs | Missing source.page | complete + conf<0.8 |",
             "|---|---|---|---|---|"]
    for d in findings["datasets"]:
        lines.append(f"| {d['dataset']} | {d['records']} | {d['duplicate_ids']} | {d['missing_source_page']} | {d['complete_low_conf']} |")
    lines += ["", "## Global findings",
              f"- Total missing source.page: {findings['global']['missing_source_page']}",
              f"- Total complete with conf<0.8: {findings['global']['complete_low_conf']}",
              f"- dat_07 duplicate pins: {len(findings['global']['dat07_duplicate_pins'])}",
              f"- Duplicate ids: {len(findings['global']['duplicate_ids'])}"]
    if findings["global"]["dat07_duplicate_pins"]:
        lines += ["", "### dat_07 duplicate pins"]
        for x in findings["global"]["dat07_duplicate_pins"][:50]:
            lines.append(f"- pin={x['pin_number']} name={x['name']} count={x['count']}")
    (reports / "DATA_HEALTH_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(findings, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()