#!/usr/bin/env python3
import sys, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
s = json.loads((REPORTS / "_validation_summary.json").read_text(encoding="utf-8"))
l3 = [e for e in s.get("errors", []) if e.get("level") == 3]
cmds = set()
for e in l3:
    err = e.get("error","")
    for tok in err.split():
        if tok.startswith("+") or tok.startswith("AT+"):
            c = tok.strip(",:")
            c = c.upper().lstrip("+")
            if c.startswith("AT"): c = c[2:]
            cmds.add(c); break
out = {"total": len(l3), "commands": sorted(cmds)}
(REPORTS / "_step_D11_L3_analysis.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"L3 total={len(l3)} unique_cmds={len(cmds)}")
for c in sorted(cmds): print(f"  {c}")