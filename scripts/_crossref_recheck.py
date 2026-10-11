#!/usr/bin/env python3
import sys
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

def normalize_cmd(c):
    s = str(c).strip().upper()
    if s.startswith("AT+"): s = s[3:]
    elif s.startswith("+"): s = s[1:]
    return s

def load(f):
    try:
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or []
        return d if isinstance(d, list) else [d]
    except Exception:
        return []

def find(dat):
    c = sorted(DATA.glob(dat + "_*.yaml"))
    return c[0] if c else None

def collect(dat, key="command"):
    f = find(dat)
    if not f: return set()
    return {normalize_cmd(r[key]) for r in load(f)
            if isinstance(r, dict) and r.get(key)}

d01 = collect("dat_01")
issues = []
for dat in ["dat_09","dat_10","dat_11","dat_12","dat_13","dat_15","dat_17"]:
    for r in load(find(dat).name) if find(dat) else []:
        if isinstance(r, dict) and r.get("command"):
            if normalize_cmd(r["command"]) not in d01:
                issues.append(f"{r.get('id','?')} in {dat}: '{r['command']}'")
for r in load(find("dat_02").name) if find("dat_02") else []:
    if isinstance(r, dict) and r.get("related_command"):
        if normalize_cmd(r["related_command"]) not in d01:
            issues.append(f"{r.get('id','?')} in dat_02: related '{r['related_command']}'")

lines = ["# CROSSREF_RECHECK", ""]
lines.append(f"dat_01 normalized commands: {len(d01)}")
lines.append(f"Remaining issues after normalization: {len(issues)}")
lines.append("")
lines.append("## Sample of remaining issues (first 30)")
lines.append("")
for x in issues[:30]:
    lines.append(f"- {x}")
lines.append("")
lines.append("## Distinct missing commands")
missing_cmds = sorted({x.split("'")[1] for x in issues if "'" in x})
lines.append(f"Count: {len(missing_cmds)}")
lines.append("")
for c in missing_cmds[:80]:
    lines.append(f"- {c}")

(REPORTS / "CROSSREF_RECHECK.md").write_text("\n".join(lines), encoding="utf-8")
print(f"dat_01 commands: {len(d01)}")
print(f"Remaining issues: {len(issues)}")
print(f"Distinct missing commands: {len(missing_cmds)}")
print(f"Report: {REPORTS / 'CROSSREF_RECHECK.md'}")
