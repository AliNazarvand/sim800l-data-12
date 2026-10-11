#!/usr/bin/env python3
"""Diagnose: for each of dat_09/10/12/13, check syntax/quote content."""
import sys, json
from pathlib import Path
try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr); sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml"))
    return c[0] if c else None

diagnostics = {}
for dat_id in ("dat_09","dat_10","dat_12","dat_13"):
    p = find(dat_id)
    if not p:
        diagnostics[dat_id] = {"error": "file missing"}
        continue
    records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    if not isinstance(records, list): records = [records]
    total = len(records)
    with_syntax = sum(1 for r in records if isinstance(r, dict) and r.get("syntax"))
    with_angle = 0
    with_eq_angle = 0
    samples = []
    for r in records:
        if not isinstance(r, dict): continue
        syn = str(r.get("syntax") or "")
        src = r.get("source") or {}
        quote = str(src.get("quote") or "") if isinstance(src, dict) else ""
        text = syn + " " + quote
        if "<" in text and ">" in text:
            with_angle += 1
            if "=<" in text or "= <" in text:
                with_eq_angle += 1
        if len(samples) < 3:
            samples.append({
                "id": r.get("id"), "command": r.get("command"),
                "syntax": syn[:80], "quote": quote[:80],
            })
    diagnostics[dat_id] = {
        "total": total,
        "with_syntax": with_syntax,
        "with_angle": with_angle,
        "with_eq_angle": with_eq_angle,
        "samples": samples,
    }

(REPORTS / "_step_D9_diagnosis.json").write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2), encoding="utf-8")
for k, v in diagnostics.items():
    print(f"{k}: total={v.get('total')} with_syntax={v.get('with_syntax')} with_angle={v.get('with_angle')} with_eq_angle={v.get('with_eq_angle')}")