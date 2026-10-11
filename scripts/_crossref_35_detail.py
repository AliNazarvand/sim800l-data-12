#!/usr/bin/env python3
"""Detail analysis of remaining cross-ref issues.
   For each issue: raw command, normalized, and whether a raw form of
   the same command exists anywhere in dat_01.
"""
from pathlib import Path
from collections import defaultdict
import yaml

ROOT    = Path(__file__).resolve().parent.parent
DATA    = ROOT / "data"
REPORTS = ROOT / "reports"

def normalize_cmd(c):
    s = str(c).strip().upper()
    if s.startswith("AT+"): s = s[3:]
    elif s.startswith("+"): s = s[1:]
    return s

def load(f):
    p = f if isinstance(f, Path) else Path(f)
    try:
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or []
        return d if isinstance(d, list) else [d]
    except Exception:
        return []

def find(dat):
    c = sorted(DATA.glob(dat + "_*.yaml"))
    return c[0] if c else None

def collect_raw(dat, key="command"):
    f = find(dat)
    if not f: return []
    return [r[key] for r in load(f)
            if isinstance(r, dict) and r.get(key)]

def main():
    # all raw commands in dat_01 (and their normalized forms)
    d01_raw = collect_raw("dat_01")
    d01_norm_set = {normalize_cmd(c) for c in d01_raw}
    # map: normalized -> list of raw forms in dat_01
    d01_norm_to_raw = defaultdict(set)
    for c in d01_raw:
        d01_norm_to_raw[normalize_cmd(c)].add(c)

    # gather all issues from B/C datasets
    targets = ["dat_09","dat_10","dat_11","dat_12","dat_13","dat_15","dat_17"]
    issues = []
    for dat in targets:
        f = find(dat)
        if not f: continue
        for r in load(f):
            if not isinstance(r, dict): continue
            c = r.get("command")
            if not c: continue
            n = normalize_cmd(c)
            if n not in d01_norm_set:
                issues.append({
                    "id": r.get("id","?"),
                    "dataset": dat,
                    "raw": c,
                    "norm": n,
                })
    # dat_02 related_command
    f = find("dat_02")
    if f:
        for r in load(f):
            if not isinstance(r, dict): continue
            c = r.get("related_command")
            if not c: continue
            n = normalize_cmd(c)
            if n not in d01_norm_set:
                issues.append({
                    "id": r.get("id","?"),
                    "dataset": "dat_02",
                    "raw": c,
                    "norm": n,
                })

    # group by dataset
    by_dataset = defaultdict(list)
    for it in issues:
        by_dataset[it["dataset"]].append(it)

    # distinct normalized missing
    distinct_norm = sorted({it["norm"] for it in issues})

    # write report
    L = []
    L.append("# CROSSREF_35_REAL")
    L.append("")
    L.append(f"dat_01 normalized commands: {len(d01_norm_set)}")
    L.append(f"Total remaining issues: {len(issues)}")
    L.append(f"Distinct missing normalized commands: {len(distinct_norm)}")
    L.append("")
    L.append("## Issues grouped by dataset")
    L.append("")
    for dat in sorted(by_dataset.keys()):
        items = by_dataset[dat]
        L.append(f"### {dat} ({len(items)} issues)")
        L.append("")
        for it in items:
            L.append(f"- `{it['id']}` : raw=`{it['raw']}`  norm=`{it['norm']}`")
        L.append("")
    L.append("## Distinct missing commands (normalized)")
    L.append("")
    L.append("| # | Normalized | Count | In dat_01 with other raw? |")
    L.append("|---|-----------|-------|---------------------------|")
    norm_count = defaultdict(int)
    for it in issues:
        norm_count[it["norm"]] += 1
    for i, n in enumerate(distinct_norm, 1):
        raw_in_d01 = ", ".join(sorted(d01_norm_to_raw.get(n, []))) or "—"
        L.append(f"| {i} | {n} | {norm_count[n]} | {raw_in_d01} |")
    L.append("")
    L.append("## Interpretation")
    L.append("")
    L.append("- 'In dat_01 with other raw?' = whether dat_01 stores the same")
    L.append("  command under a different raw form (e.g. '+X' vs 'AT+X').")
    L.append("  If this column is '—', the command is truly absent from dat_01.")
    L.append("  If it is non-'—', the command exists but the comparison form differs.")
    L.append("- After normalization, all issues above are truly missing from dat_01,")
    L.append("  by definition. This column only shows if a *raw* match exists.")

    out = REPORTS / "CROSSREF_35_REAL.md"
    out.write_text("\n".join(L), encoding="utf-8")

    print(f"Issues: {len(issues)}")
    print(f"Distinct missing: {len(distinct_norm)}")
    print(f"Report: {out}")

if __name__ == "__main__":
    main()
