#!/usr/bin/env python3
"""Fill dat_01 parameters by scanning syntax, source.quote and the AT Manual
for <param> placeholders and =<param>,<param> patterns."""
import sys, json, re
from pathlib import Path
from datetime import datetime, timezone
try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr); sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SRC_EX = ROOT / "sources" / "extracted"
REPORTS = ROOT / "reports"

def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml"))
    return c[0] if c else (DATA / (dat_id + ".yaml") if (DATA / (dat_id + ".yaml")).exists() else None)

def load_paged(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    pages = []
    parts = re.split(r"<<<PAGE\s+(\d+)>>>", text)
    for i in range(1, len(parts) - 1, 2):
        try: num = int(parts[i])
        except Exception: continue
        pages.append((num, parts[i + 1]))
    return pages

# index heading lines by command
pages = load_paged(SRC_EX / "at_manual_v1_01_paged.txt")
HEADER_RE = re.compile(r"^\s*([0-9]+(?:\.[0-9]+){1,4})\s+(AT\+[A-Z0-9]+)\s+(.{2,120}?)\s*$")
cmd_heading = {}
for pn, body in pages:
    for line in body.splitlines():
        s = line.strip()
        m = HEADER_RE.match(s)
        if m:
            c = m.group(2).strip().upper()
            if c not in cmd_heading:
                cmd_heading[c] = (pn, s)

PARAM_RE = re.compile(r"<([A-Za-z_][A-Za-z0-9_]*)>")

def infer_type(name):
    n = name.lower()
    if n in ("index","mode","level","channel","port","cid","bearer","n","i","p"):
        return "integer"
    return "string"

p = find("dat_01")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("parameters"): continue
    # gather text: syntax + quote + heading line
    syntax = r.get("syntax") or ""
    quote = ""
    if isinstance(r.get("source"), dict):
        quote = r["source"].get("quote") or ""
    cmd = r.get("command") or ""
    cmd_full = cmd.upper()
    if not cmd_full.startswith("AT+"):
        if cmd_full.startswith("+"):
            cmd_full = "AT" + cmd_full
        else:
            cmd_full = "AT+" + cmd_full
    heading = cmd_heading.get(cmd_full)
    heading_line = heading[1] if heading else ""

    text = " ".join([syntax, quote, heading_line])
    names = PARAM_RE.findall(text)
    seen = set(); params = []
    for n in names:
        if n in seen: continue
        seen.add(n)
        params.append({"name": n, "type": infer_type(n), "description": ""})
    if params:
        r["parameters"] = params
        r["updated_at"] = ts
        filled += 1

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)

with_params = sum(1 for r in records if isinstance(r, dict) and r.get("parameters"))
summary = {"total": len(records), "with_parameters": with_params, "filled": filled}
(REPORTS / "_step_D7_dat01_params.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_01: total={len(records)} with_parameters={with_params} filled={filled}")