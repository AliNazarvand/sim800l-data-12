#!/usr/bin/env python3
"""Analyze remaining L3 errors from _validation_summary.json."""
import sys, json, re
from pathlib import Path
try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr); sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SRC_EX = ROOT / "sources" / "extracted"
REPORTS = ROOT / "reports"

summary_path = REPORTS / "_validation_summary.json"
if not summary_path.exists():
    print("No validation summary"); sys.exit(1)
summary = json.loads(summary_path.read_text(encoding="utf-8"))
l3 = [e for e in summary.get("errors", []) if e.get("level") == 3]

# Build index of AT Manual commands
def load_paged(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    pages = []
    parts = re.split(r"<<<PAGE\s+(\d+)>>>", text)
    for i in range(1, len(parts) - 1, 2):
        try: num = int(parts[i])
        except Exception: continue
        pages.append((num, parts[i + 1]))
    return pages

pages = load_paged(SRC_EX / "at_manual_v1_01_paged.txt")
HEADER_RE = re.compile(r"^\s*([0-9]+(?:\.[0-9]+){1,4})\s+(AT\+[A-Z0-9]+)\s+(.{2,120}?)\s*$")
manual_cmds = set()
for page_no, body in pages:
    for line in body.splitlines():
        s = line.strip()
        m = HEADER_RE.match(s)
        if m:
            manual_cmds.add(m.group(2).strip().upper())

def cmd_norm(c):
    s = str(c).strip().upper()
    if s.startswith("AT+"): s = s[3:]
    elif s.startswith("+"): s = s[1:]
    return s

def full_name(c):
    n = cmd_norm(c)
    return "AT+" + n

analyzed = []
in_manual = 0
not_in_manual = 0
for e in l3:
    err = e.get("error", "")
    ds = e.get("dataset", "?")
    cmd = ""
    for tok in err.split():
        if tok.startswith("+") or tok.startswith("AT+"):
            cmd = tok.strip(",:")
            break
    full = full_name(cmd) if cmd else ""
    is_in = full.upper() in manual_cmds
    if is_in: in_manual += 1
    else: not_in_manual += 1
    analyzed.append({
        "dataset": ds, "record": e.get("record"),
        "command": cmd, "full_name": full, "in_at_manual": is_in,
        "error": err[:200]
    })

report = {
    "total_l3": len(l3),
    "analyzed": len(analyzed),
    "in_at_manual": in_manual,
    "not_in_manual": not_in_manual,
    "details": analyzed[:200],
}
(REPORTS / "_step_D2_L3_analysis.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"L3 analyzed: {len(analyzed)} total; in_manual={in_manual} not_in_manual={not_in_manual}")