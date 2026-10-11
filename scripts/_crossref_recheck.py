#!/usr/bin/env python3
"""_crossref_recheck.py — fixed.
   load() accepts either Path or str (via Path(f)).
"""
from pathlib import Path
import yaml

ROOT    = Path(__file__).resolve().parent.parent
DATA    = ROOT / "data"
REPORTS = ROOT / "reports"

def normalize_cmd(c):
    s = str(c).strip().upper()
    if s.startswith("AT+"):
        s = s[3:]
    elif s.startswith("+"):
        s = s[1:]
    return s

def load(f):
    """Accept Path or str."""
    p = f if isinstance(f, Path) else Path(f)
    try:
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or []
        return d if isinstance(d, list) else [d]
    except Exception as e:
        print(f"  [load error] {p}: {e}")
        return []

def find(dat):
    c = sorted(DATA.glob(dat + "_*.yaml"))
    return c[0] if c else None

def collect(dat, key="command"):
    f = find(dat)
    if not f: return set()
    return {normalize_cmd(r[key]) for r in load(f)
            if isinstance(r, dict) and r.get(key)}

def main():
    d01 = collect("dat_01")
    issues = []
    for dat in ["dat_09","dat_10","dat_11","dat_12","dat_13","dat_15","dat_17"]:
        f = find(dat)
        if not f: continue
        for r in load(f):
            if isinstance(r, dict) and r.get("command"):
                if normalize_cmd(r["command"]) not in d01:
                    issues.append((r.get("id","?"), dat, r["command"]))
    f = find("dat_02")
    if f:
        for r in load(f):
            if isinstance(r, dict) and r.get("related_command"):
                if normalize_cmd(r["related_command"]) not in d01:
                    issues.append((r.get("id","?"), "dat_02",
                                   r["related_command"]))

    lines = ["# CROSSREF_RECHECK", ""]
    lines.append(f"dat_01 normalized commands: {len(d01)}")
    lines.append(f"Remaining issues after normalization: {len(issues)}")
    lines.append("")
    lines.append("## Full list of remaining issues")
    lines.append("")
    for (rid, dat, cmd) in issues:
        lines.append(f"- {rid} in {dat}: `{cmd}`")
    lines.append("")
    missing = sorted({normalize_cmd(c) for (_, _, c) in issues})
    lines.append("## Distinct missing normalized commands")
    lines.append(f"Count: {len(missing)}")
    lines.append("")
    for c in missing:
        lines.append(f"- {c}")

    (REPORTS / "CROSSREF_RECHECK.md").write_text("\n".join(lines),
                                                 encoding="utf-8")
    print(f"dat_01 commands: {len(d01)}")
    print(f"Remaining issues: {len(issues)}")
    print(f"Distinct missing commands: {len(missing)}")

if __name__ == "__main__":
    main()
