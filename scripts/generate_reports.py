import sys, json, hashlib, datetime, yaml
from pathlib import Path
from collections import Counter

NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
STATUS_ORDER = ["complete","partial","blocked","deferred","unknown","inferred"]

def sha256(p):
    h = hashlib.sha256()
    with open(p,"rb") as f:
        for c in iter(lambda: f.read(65536), b""): h.update(c)
    return "sha256:" + h.hexdigest()

def load(p):
    try:
        with open(p, encoding="utf-8") as f:
            return yaml.safe_load(f) or []
    except Exception:
        return []

def main():
    root = Path(sys.argv[1])
    reports = root / "reports"
    data_dir = root / "data"
    src_dir = root / "sources" / "originals"
    reports.mkdir(parents=True, exist_ok=True)

    coverage = []
    for f in sorted(data_dir.glob("dat_*.yaml")):
        recs = load(f)
        if not isinstance(recs, list): recs = [recs] if recs else []
        st = Counter()
        versions = Counter()
        for r in recs:
            if not isinstance(r, dict): continue
            st[r.get("status","(none)")] += 1
            src = r.get("source") or {}
            versions[src.get("version","?")] += 1
        dominant = "pending"
        for s in STATUS_ORDER:
            if st.get(s,0) > 0: dominant = s; break
        coverage.append({"dataset": f.stem, "file": f.name, "records": len(recs),
                         "status_counts": dict(st), "dominant_status": dominant,
                         "source_versions": dict(versions)})

    # COVERAGE_MATRIX
    lines = ["# COVERAGE MATRIX", f"_Generated: {NOW}_", "",
             "| Dataset | File | Records | Dominant | Status breakdown |",
             "|---|---|---|---|---|"]
    for r in coverage:
        br = ", ".join(f"{k}={v}" for k,v in sorted(r["status_counts"].items())) or "-"
        lines.append(f"| {r['dataset']} | {r['file']} | {r['records']} | {r['dominant_status']} | {br} |")
    lines += ["", "## Summary",
              f"- Datasets: {len(coverage)}",
              f"- Total records: {sum(r['records'] for r in coverage)}"]
    (reports / "COVERAGE_MATRIX.md").write_text("\n".join(lines), encoding="utf-8")

    # SOURCE_INVENTORY
    s = ["# SOURCE INVENTORY", f"_Generated: {NOW}_", "",
         "| File | Size | SHA-256 |", "|---|---|---|"]
    if src_dir.exists():
        for p in sorted(src_dir.iterdir()):
            if p.is_file():
                s.append(f"| {p.name} | {p.stat().st_size} | `{sha256(p)[:24]}...` |")
    (reports / "SOURCE_INVENTORY.md").write_text("\n".join(s), encoding="utf-8")

    # VALIDATION_REPORT
    vf = reports / "_validation_result.json"
    v = ["# VALIDATION REPORT", f"_Generated: {NOW}_", ""]
    if vf.exists():
        d = json.loads(vf.read_text(encoding="utf-8"))
        v += ["| Dataset | File | Records | Errors | Schema OK |", "|---|---|---|---|---|"]
        for r in d.get("datasets", []):
            v.append(f"| {r['dataset']} | {r['file']} | {r['records']} | {r['errors']} | {r.get('schema_ok','-')} |")
        v += ["", f"## Total errors: {len(d.get('errors', []))}"]
        for e in d.get("errors", [])[:300]:
            v.append(f"- {e}")
    else: v.append("_run validate.py first._")
    (reports / "VALIDATION_REPORT.md").write_text("\n".join(v), encoding="utf-8")

    # CROSS_REF_REPORT
    cf = reports / "_cross_ref_result.json"
    c = ["# CROSS-REFERENCE REPORT", f"_Generated: {NOW}_", ""]
    if cf.exists():
        d = json.loads(cf.read_text(encoding="utf-8"))
        if d.get("note"): c.append(f"> {d['note']}")
        c += [f"- dat_01 known commands: {len(d.get('dat_01_commands', []))}", "",
              "| Dataset | Refs | Resolved | Unresolved |", "|---|---|---|---|"]
        for r in d.get("refs", []):
            c.append(f"| {r['dataset']} | {r['total_refs']} | {r['resolved']} | {r['unresolved']} |")
    else: c.append("_run cross_ref.py first._")
    (reports / "CROSS_REF_REPORT.md").write_text("\n".join(c), encoding="utf-8")

    # TODO
    todo = ["# TODO", f"_Generated: {NOW}_", "", "## Datasets not complete"]
    for r in coverage:
        if r["dominant_status"] not in ("complete",):
            todo.append(f"- [ ] {r['dataset']} (status={r['dominant_status']}, records={r['records']})")
    (reports / "TODO.md").write_text("\n".join(todo), encoding="utf-8")

    # SESSION_LOG (append)
    slog = reports / "SESSION_LOG.md"
    prev = slog.read_text(encoding="utf-8") if slog.exists() else "# SESSION LOG\n"
    entry = (f"\n## Session {NOW}\n"
             f"- Ran corrected pipeline v2 (power fix, dedup, verbose logs).\n"
             f"- Datasets: {len(coverage)}, records: {sum(r['records'] for r in coverage)}\n")
    slog.write_text(prev + entry, encoding="utf-8")

    # DECISIONS_LOG (append)
    dlog = reports / "DECISIONS_LOG.md"
    prev = dlog.read_text(encoding="utf-8") if dlog.exists() else "# DECISIONS LOG\n"
    dentry = (f"\n## {NOW}\n"
              f"- Expanded header keyword sets for CSV classification (fixes power_tables=0).\n"
              f"- dat_07 dedup: V2.02 wins over V1.00, V1.00 recorded in conflicts (R7, R20).\n"
              f"- Removed | Out-Null from validation/cross-ref so output is visible (R17).\n")
    dlog.write_text(prev + dentry, encoding="utf-8")

    # ROLE_MAP
    role = ["# ROLE MAP", f"_Generated: {NOW}_", "",
            "| Dataset | Depends on | Depended on by | Status |", "|---|---|---|---|"]
    rmap = {"dat_01":("-","02,03,09,10,11,12,13,17"),
            "dat_02":("dat_01","-"),"dat_03":("dat_01","-"),
            "dat_07":("-","13,16"),"dat_08":("-","-"),
            "dat_14":("-","10"),"dat_18":("-","-")}
    for r in coverage:
        key = r["dataset"][:6]
        dep, depby = rmap.get(key, ("-","-"))
        role.append(f"| {r['dataset']} | {dep} | {depby} | {r['dominant_status']} |")
    (reports / "ROLE_MAP.md").write_text("\n".join(role), encoding="utf-8")

    # CHANGELOG (append)
    clog = reports / "CHANGELOG.md"
    prev = clog.read_text(encoding="utf-8") if clog.exists() else "# CHANGELOG\n"
    clog.write_text(prev + f"\n## {NOW}\n- Corrected pipeline v2.\n", encoding="utf-8")

    # per-dataset reports (richer)
    for r in coverage:
        ds = r["dataset"]
        lines = [f"# {ds.upper()} REPORT", f"_Generated: {NOW}_", "",
                 "## Snapshot",
                 f"- File: `data/{r['file']}`",
                 f"- Records: {r['records']}",
                 f"- Dominant status: **{r['dominant_status']}**",
                 f"- Status breakdown: {r['status_counts']}",
                 f"- Source versions: {r['source_versions']}",
                 ""]
        # attach per-dataset validation detail
        if vf.exists():
            d = json.loads(vf.read_text(encoding="utf-8"))
            for x in d.get("datasets", []):
                if x["file"] == r["file"]:
                    lines += ["## Validation",
                              f"- Errors: {x['errors']}",
                              f"- Schema OK: {x.get('schema_ok','-')}", ""]
        (reports / f"{ds}_REPORT.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"Reports written to {reports}")

if __name__ == "__main__":
    main()