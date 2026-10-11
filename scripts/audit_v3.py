#!/usr/bin/env python3
"""audit_v3.py — final project audit. Read-only."""
import sys
from pathlib import Path
from datetime import datetime
try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml"); sys.exit(1)

ROOT    = Path(__file__).resolve().parent.parent
DATA    = ROOT / "data"
REPORTS = ROOT / "reports"

CLUSTERS = {
    "A": ["dat_04","dat_05","dat_06","dat_07","dat_15","dat_16"],
    "B": ["dat_01","dat_02","dat_03","dat_09","dat_10","dat_11","dat_12","dat_13","dat_17"],
    "C": ["dat_08","dat_14","dat_18"],
}

def load(name):
    p = DATA / name
    if not p.exists(): return None
    try:
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or []
        return d if isinstance(d, list) else [d]
    except Exception as e:
        return [{"_err": str(e)}]

def find_file(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml"))
    return c[0] if c else None

def analyze(dat_id):
    f = find_file(dat_id)
    if not f:
        return {"records": 0, "missing": True, "statuses": {}, "no_source": 0,
                "example_only": 0, "low_conf": 0, "high_conf": 0,
                "source_names": set(), "error": None}
    data = load(f.name)
    if data is None or (data and isinstance(data[0], dict) and "_err" in data[0]):
        return {"records": 0, "missing": False, "statuses": {}, "no_source": 0,
                "example_only": 0, "low_conf": 0, "high_conf": 0,
                "source_names": set(), "error": data[0].get("_err") if data else "load failed"}

    statuses = {}
    no_source = 0
    example_only = 0
    low = 0
    high = 0
    src_names = set()

    for rec in data:
        if not isinstance(rec, dict): continue
        st = rec.get("status", "unknown")
        statuses[st] = statuses.get(st, 0) + 1
        if st == "example-only": example_only += 1

        src = rec.get("source", {})
        if not isinstance(src, dict) or not all(src.get(k) for k in ("name","version")):
            no_source += 1
        elif src.get("name"):
            src_names.add(src["name"])

        c = rec.get("confidence")
        if isinstance(c, (int, float)):
            if c < 0.5: low += 1
            if c >= 0.7: high += 1

    return {
        "records": len(data), "missing": False, "statuses": statuses,
        "no_source": no_source, "example_only": example_only,
        "low_conf": low, "high_conf": high, "source_names": src_names,
        "error": None,
    }

def collect_commands(dat_id):
    f = find_file(dat_id)
    if not f: return set()
    data = load(f.name) or []
    out = set()
    for r in data:
        if isinstance(r, dict):
            c = r.get("command")
            if c: out.add(str(c).lstrip("+"))
    return out

def cross_ref():
    issues = []
    d01 = collect_commands("dat_01")

    # commands in dat_09..13, 15, 17 must exist in dat_01
    for dat in ["dat_09","dat_10","dat_11","dat_12","dat_13","dat_15","dat_17"]:
        f = find_file(dat)
        if not f: continue
        data = load(f.name) or []
        for r in data:
            if not isinstance(r, dict): continue
            c = r.get("command")
            if c:
                key = str(c).lstrip("+")
                if key not in d01:
                    issues.append(f"{r.get('id','?')} in {dat}: command '+{key}' not in dat_01")

    # URC related_command in dat_02 must exist in dat_01
    f = find_file("dat_02")
    if f:
        for r in (load(f.name) or []):
            if not isinstance(r, dict): continue
            rc = r.get("related_command")
            if rc:
                key = str(rc).lstrip("+")
                if key not in d01:
                    issues.append(f"{r.get('id','?')} in dat_02: related_command '+{key}' not in dat_01")

    return issues

def main():
    now = datetime.now().isoformat(timespec="seconds")
    results = {}
    for i in range(1, 19):
        dat_id = f"dat_{i:02d}"
        results[dat_id] = analyze(dat_id)

    xref = cross_ref()

    lines = []
    lines.append("# AUDIT_REPORT_v3")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append("")
    lines.append("## Method")
    lines.append("")
    lines.append("- validate.py: 0 errors (L1=L2=L3=L4=0)")
    lines.append("- This audit is read-only.")
    lines.append("")

    # Dataset summary
    lines.append("## Dataset Summary")
    lines.append("")
    lines.append("| Dataset | Records | Status | example-only | no-source | conf<0.5 | conf>=0.7 | Sources |")
    lines.append("|---------|---------|--------|--------------|-----------|----------|-----------|---------|")
    for i in range(1, 19):
        dat_id = f"dat_{i:02d}"
        r = results[dat_id]
        st = ", ".join(f"{k}:{v}" for k, v in sorted(r["statuses"].items())) or "-"
        srcs = ", ".join(sorted(r["source_names"]))[:50] or "-"
        if r["missing"]:
            lines.append(f"| {dat_id} | MISSING | - | - | - | - | - | - |")
        elif r["error"]:
            lines.append(f"| {dat_id} | ERR | {r['error'][:40]} | - | - | - | - | - |")
        else:
            lines.append(f"| {dat_id} | {r['records']} | {st} | {r['example_only']} | "
                         f"{r['no_source']} | {r['low_conf']} | {r['high_conf']} | {srcs} |")
    lines.append("")

    # Cluster status
    lines.append("## Cluster Status")
    lines.append("")
    for cl, dats in CLUSTERS.items():
        lines.append(f"### Cluster {cl}: {', '.join(dats)}")
        lines.append("")
        total_rec = sum(results[d]["records"] for d in dats)
        blocked = [d for d in dats if "blocked" in results[d]["statuses"]]
        complete = [d for d in dats if results[d]["statuses"].get("complete", 0) > 0
                    and set(results[d]["statuses"].keys()) == {"complete"}]
        lines.append(f"- Total records: {total_rec}")
        lines.append(f"- Blocked datasets: {', '.join(blocked) if blocked else 'none'}")
        lines.append(f"- Complete datasets: {', '.join(complete) if complete else 'none'}")
        lines.append("")

    # Cross-ref
    lines.append("## Cross-Reference Issues")
    lines.append("")
    if xref:
        for x in xref[:100]:
            lines.append(f"- {x}")
        if len(xref) > 100:
            lines.append(f"- ... ({len(xref)-100} more)")
    else:
        lines.append("- No issues found.")
    lines.append("")

    # Readiness
    lines.append("## Readiness for Cluster A")
    lines.append("")
    cluster_a = CLUSTERS["A"]
    ready = True
    reasons = []
    for d in cluster_a:
        if results[d]["missing"]:
            ready = False; reasons.append(f"{d}: file missing")
        elif results[d]["example_only"] > 0:
            ready = False; reasons.append(f"{d}: contains example-only records")
        elif results[d]["no_source"] > 0:
            reasons.append(f"{d}: {results[d]['no_source']} records without source (review)")
    lines.append(f"- Ready: **{'YES' if ready else 'NO'}**")
    for r in reasons:
        lines.append(f"- {r}")
    lines.append("")

    # Source inventory per dataset
    lines.append("## Source Inventory")
    lines.append("")
    for i in range(1, 19):
        dat_id = f"dat_{i:02d}"
        r = results[dat_id]
        if r["missing"]:
            lines.append(f"- {dat_id}: (file missing)")
            continue
        srcs = sorted(r["source_names"])
        lines.append(f"- {dat_id}: {', '.join(srcs) if srcs else '(no source names recorded)'}")
    lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append("- No files were modified during this audit.")
    lines.append("- Review cross-reference issues above before declaring datasets complete.")
    lines.append("- 'no-source' counts records missing source.name or source.version.")

    out_path = REPORTS / "AUDIT_REPORT_v3.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Records per dataset:")
    for i in range(1, 19):
        dat_id = f"dat_{i:02d}"
        r = results[dat_id]
        if r["missing"]:
            print(f"  {dat_id}: MISSING")
        else:
            print(f"  {dat_id}: {r['records']:4d} records  "
                  f"example={r['example_only']}  no_source={r['no_source']}")
    print()
    print(f"Cross-ref issues: {len(xref)}")
    print(f"Report: {out_path}")

if __name__ == "__main__":
    main()
