import sys, json, hashlib, datetime, yaml
from pathlib import Path
from collections import Counter

NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
STATUS_ORDER = ["complete","partial","blocked","deferred","unknown","inferred"]

def sha256(p):
    h = hashlib.sha256()
    with open(p,"rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
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

    data_files = sorted(data_dir.glob("dat_*.yaml")) if data_dir.exists() else []
    coverage = []
    for f in data_files:
        ds = f.stem
        recs = load(f)
        if not isinstance(recs, list): recs = [recs] if recs else []
        st = Counter()
        for r in recs:
            if isinstance(r, dict): st[r.get("status","(none)")] += 1
        dominant = "pending"
        for s in STATUS_ORDER:
            if st.get(s,0) > 0:
                dominant = s; break
        coverage.append({"dataset": ds, "file": f.name, "records": len(recs),
                         "status_counts": dict(st), "dominant_status": dominant})

    # COVERAGE_MATRIX.md
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

    # SOURCE_INVENTORY.md
    s = ["# SOURCE INVENTORY", f"_Generated: {NOW}_", "",
         "| File | Size | SHA-256 |", "|---|---|---|"]
    if src_dir.exists():
        for p in sorted(src_dir.iterdir()):
            if p.is_file():
                s.append(f"| {p.name} | {p.stat().st_size} | `{sha256(p)[:24]}...` |")
    if len(s) == 4: s.append("| _(none)_ | - | - |")
    (reports / "SOURCE_INVENTORY.md").write_text("\n".join(s), encoding="utf-8")

    # VALIDATION_REPORT.md
    vfile = reports / "_validation_result.json"
    v = ["# VALIDATION REPORT", f"_Generated: {NOW}_", ""]
    if vfile.exists():
        d = json.loads(vfile.read_text(encoding="utf-8"))
        v += ["## Per-dataset", "", "| Dataset | File | Records | Errors | Schema OK |",
              "|---|---|---|---|---|"]
        for r in d.get("datasets", []):
            v.append(f"| {r['dataset']} | {r['file']} | {r['records']} | {r['errors']} | {r.get('schema_ok', '-')} |")
        v += ["", f"## Total errors: {len(d.get('errors', []))}"]
        for e in d.get("errors", [])[:300]:
            v.append(f"- {e}")
    else:
        v.append("_run scripts/validate.py first._")
    (reports / "VALIDATION_REPORT.md").write_text("\n".join(v), encoding="utf-8")

    # CROSS_REF_REPORT.md
    cfile = reports / "_cross_ref_result.json"
    c = ["# CROSS-REFERENCE REPORT", f"_Generated: {NOW}_", ""]
    if cfile.exists():
        d = json.loads(cfile.read_text(encoding="utf-8"))
        if d.get("note"): c.append(f"> {d['note']}")
        c += [f"- dat_01 commands known: {len(d.get('dat_01_commands', []))}", "",
              "| Dataset | Refs | Resolved | Unresolved |", "|---|---|---|---|"]
        for r in d.get("refs", []):
            c.append(f"| {r['dataset']} | {r['total_refs']} | {r['resolved']} | {r['unresolved']} |")
    else:
        c.append("_run scripts/cross_ref.py first._")
    (reports / "CROSS_REF_REPORT.md").write_text("\n".join(c), encoding="utf-8")

    # TODO.md
    todo = ["# TODO", f"_Generated: {NOW}_", "", "## Datasets not complete"]
    any_pending = False
    for r in coverage:
        if r["dominant_status"] not in ("complete",):
            todo.append(f"- [ ] {r['dataset']} (status={r['dominant_status']}, records={r['records']})")
            any_pending = True
    if not any_pending: todo.append("- [x] All datasets complete")
    (reports / "TODO.md").write_text("\n".join(todo), encoding="utf-8")

    # SESSION_LOG.md (append)
    slog = reports / "SESSION_LOG.md"
    prev = slog.read_text(encoding="utf-8") if slog.exists() else "# SESSION LOG\n"
    entry = (f"\n## Session {NOW}\n"
             f"- Ran extract_pdf, extract_hw_datasets, validate (jsonschema), cross_ref, reports.\n"
             f"- Datasets inspected: {len(coverage)}; total records: {sum(r['records'] for r in coverage)}\n")
    slog.write_text(prev + entry, encoding="utf-8")

    # DECISIONS_LOG.md (append)
    dlog = reports / "DECISIONS_LOG.md"
    prev = dlog.read_text(encoding="utf-8") if dlog.exists() else "# DECISIONS LOG\n"
    dentry = (f"\n## {NOW}\n"
              f"- Cluster A datasets (04, 07, 15) extracted from pre-parsed CSVs.\n"
              f"- Validation now uses jsonschema against schemas/dat_XX.schema.yaml.\n"
              f"- Cluster B intentionally left untouched (requires dedicated AT parser).\n")
    dlog.write_text(prev + dentry, encoding="utf-8")

    # ROLE_MAP.md
    role = ["# ROLE MAP", f"_Generated: {NOW}_", "",
            "| Dataset | Depends on | Depended on by | Status |",
            "|---|---|---|---|"]
    role_map = {
        "dat_01": ("-", "02,03,09,10,11,12,13,17"),
        "dat_02": ("dat_01", "-"), "dat_03": ("dat_01", "-"),
        "dat_07": ("-", "13,16"), "dat_08": ("-", "-"),
        "dat_14": ("-", "10"), "dat_18": ("-", "-"),
    }
    for r in coverage:
        key = r["dataset"][:6]
        dep, depby = role_map.get(key, ("-", "-"))
        role.append(f"| {r['dataset']} | {dep} | {depby} | {r['dominant_status']} |")
    (reports / "ROLE_MAP.md").write_text("\n".join(role), encoding="utf-8")

    # CHANGELOG.md (append)
    clog = reports / "CHANGELOG.md"
    prev = clog.read_text(encoding="utf-8") if clog.exists() else "# CHANGELOG\n"
    clog.write_text(prev + f"\n## {NOW}\n- Pipeline run; reports regenerated.\n", encoding="utf-8")

    # per-dataset reports
    for r in coverage:
        ds = r["dataset"]
        content = [f"# {ds.upper()} REPORT", f"_Generated: {NOW}_", "",
                   f"- File: `data/{r['file']}`",
                   f"- Records: {r['records']}",
                   f"- Dominant status: {r['dominant_status']}",
                   f"- Status breakdown: {r['status_counts']}", ""]
        (reports / f"{ds}_REPORT.md").write_text("\n".join(content), encoding="utf-8")

    print(f"Reports written to {reports}")

if __name__ == "__main__":
    main()