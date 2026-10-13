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
        for r in recs:
            if isinstance(r, dict): st[r.get("status","(none)")] += 1
        dominant = "pending"
        for s in STATUS_ORDER:
            if st.get(s,0) > 0: dominant = s; break
        coverage.append({
            "dataset": f.stem, "file": f.name, "records": len(recs),
            "status_counts": dict(st), "dominant_status": dominant,
        })

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

    # CROSS_REF_REPORT (with blocked-source section)
    cf = reports / "_cross_ref_result.json"
    c = ["# CROSS-REFERENCE REPORT", f"_Generated: {NOW}_", ""]
    if cf.exists():
        d = json.loads(cf.read_text(encoding="utf-8"))
        if d.get("note"): c.append(f"> {d['note']}")
        c += [f"- dat_01 known commands: {len(d.get('dat_01_commands', []))}", "",
              "| Dataset | Refs | Resolved | Unresolved |",
              "|---|---|---|---|"]
        for r in d.get("refs", []):
            c.append(f"| {r['dataset']} | {r['total_refs']} | {r['resolved']} | {r['unresolved']} |")
        bs = d.get("blocked_source", {})
        if bs:
            c += ["", "## Unresolved refs classified by required manual",
                  "These are NOT errors — they require manuals not present in the project.", ""]
            for manual, items in sorted(bs.items()):
                c.append(f"### {manual} ({len(items)} refs)")
                for it in items:
                    c.append(f"- {it}")
                c.append("")
    else: c.append("_run cross_ref.py first._")
    (reports / "CROSS_REF_REPORT.md").write_text("\n".join(c), encoding="utf-8")

    # TODO.md (honest, complete)
    todo = ["# TODO", f"_Generated: {NOW}_", "",
            "## Blocked datasets (source missing)"]
    blocked_list = []
    for r in coverage:
        if r["dominant_status"] == "blocked":
            blocked_list.append(r["dataset"])
    if blocked_list:
        for b in blocked_list:
            todo.append(f"- [ ] {b}")
    else:
        todo.append("- (none)")

    todo += ["", "## Missing source documents"]
    missing_docs = []
    if cf.exists():
        d = json.loads(cf.read_text(encoding="utf-8"))
        for manual in d.get("blocked_source", {}).keys():
            missing_docs.append(manual)
    if missing_docs:
        for m in missing_docs:
            todo.append(f"- [ ] {m}")
    else:
        todo.append("- (none)")

    todo += ["", "## Partial datasets (source available, coverage limited)"]
    partial_list = []
    for r in coverage:
        if r["dominant_status"] == "partial":
            partial_list.append(f"{r['dataset']} (records={r['records']})")
    if partial_list:
        for p in partial_list:
            todo.append(f"- [ ] {p}")
    else:
        todo.append("- (none)")

    (reports / "TODO.md").write_text("\n".join(todo), encoding="utf-8")

    # SESSION_LOG (append)
    slog = reports / "SESSION_LOG.md"
    prev = slog.read_text(encoding="utf-8") if slog.exists() else "# SESSION LOG\n"
    entry = (f"\n## Session {NOW}\n"
             f"- v6: status hygiene (dat_14, dat_11, dat_17), cross-ref classified.\n"
             f"- Datasets: {len(coverage)}, records: {sum(r['records'] for r in coverage)}\n")
    slog.write_text(prev + entry, encoding="utf-8")

    # ROLE_MAP
    role = ["# ROLE MAP", f"_Generated: {NOW}_", "",
            "| Dataset | Depends on | Depended on by | Status |",
            "|---|---|---|---|"]
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
    clog.write_text(prev + f"\n## {NOW}\n- v6 pipeline: status hygiene + source-aware cross-ref.\n", encoding="utf-8")

    # per-dataset reports
    for r in coverage:
        ds = r["dataset"]
        lines = [f"# {ds.upper()} REPORT", f"_Generated: {NOW}_", "",
                 "## Snapshot",
                 f"- File: `data/{r['file']}`",
                 f"- Records: {r['records']}",
                 f"- Dominant status: **{r['dominant_status']}**",
                 f"- Status breakdown: {r['status_counts']}",
                 ""]
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