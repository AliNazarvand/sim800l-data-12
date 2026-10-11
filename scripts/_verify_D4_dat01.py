#!/usr/bin/env python3
"""Verify dat_01 complete claim: sample records, count fields."""
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
    return c[0] if c else (DATA / (dat_id + ".yaml") if (DATA / (dat_id + ".yaml")).exists() else None)

p = find("dat_01")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]

with_page = 0
with_section = 0
with_quote = 0
with_command = 0
with_parameters = 0
with_response = 0
with_syntax = 0
partial = 0
blocked = 0
unknown = 0
for r in records:
    if not isinstance(r, dict): continue
    src = r.get("source") or {}
    if isinstance(src, dict):
        if src.get("page"): with_page += 1
        if src.get("section"): with_section += 1
        if src.get("quote"): with_quote += 1
    if r.get("command"): with_command += 1
    if r.get("parameters"): with_parameters += 1
    if r.get("response_success"): with_response += 1
    if r.get("syntax"): with_syntax += 1
    st = r.get("status")
    if st == "partial": partial += 1
    elif st == "blocked": blocked += 1
    elif st == "unknown": unknown += 1

# samples
samples = []
for r in records[:5]:
    if not isinstance(r, dict): continue
    samples.append({
        "id": r.get("id"),
        "command": r.get("command"),
        "syntax": r.get("syntax"),
        "status": r.get("status"),
        "page": (r.get("source") or {}).get("page"),
        "has_parameters": bool(r.get("parameters")),
        "has_response": bool(r.get("response_success")),
    })

summary = {
    "total": len(records),
    "with_page": with_page,
    "with_section": with_section,
    "with_quote": with_quote,
    "with_command": with_command,
    "with_parameters": with_parameters,
    "with_response": with_response,
    "with_syntax": with_syntax,
    "status_partial": partial,
    "status_blocked": blocked,
    "status_unknown": unknown,
    "samples": samples,
}
(REPORTS / "_step_D4_dat01_verify.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({k: v for k, v in summary.items() if k != "samples"}, ensure_ascii=False, indent=2))
print("--- samples ---")
for s in samples:
    print(f"  {s['id']} cmd={s['command']} status={s['status']} page={s['page']} params={s['has_parameters']} resp={s['has_response']}")