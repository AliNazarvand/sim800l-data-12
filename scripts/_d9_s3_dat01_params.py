#!/usr/bin/env python3
"""Fill dat_01 params by scanning AT Manual section body for <...> placeholders."""
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
    return c[0] if c else None

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
TOKEN_RE = re.compile(r"<([A-Za-z_][A-Za-z0-9_]*)>")

# Build section body index: command -> concatenated body until next header
sections = {}
current_cmd = None
current_body = []
for pn, body in pages:
    for line in body.splitlines():
        s = line.strip()
        m = HEADER_RE.match(s)
        if m:
            if current_cmd:
                sections[current_cmd] = " ".join(current_body)
            current_cmd = m.group(2).strip().upper()
            current_body = []
        elif current_cmd and len(s) < 200:
            current_body.append(s)
if current_cmd:
    sections[current_cmd] = " ".join(current_body)

def infer_type(name):
    n = name.lower()
    if n in ("index","mode","level","channel","port","cid","bearer","n","i","p","stat"):
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
    cmd = r.get("command") or ""
    cmd_full = cmd.upper()
    if not cmd_full.startswith("AT+"):
        if cmd_full.startswith("+"):
            cmd_full = "AT" + cmd_full
        else:
            cmd_full = "AT+" + cmd_full
    text_parts = []
    if r.get("syntax"): text_parts.append(str(r["syntax"]))
    src = r.get("source") or {}
    if isinstance(src, dict) and src.get("quote"): text_parts.append(str(src["quote"]))
    sec_body = sections.get(cmd_full, "")
    if sec_body: text_parts.append(sec_body[:3000])
    text = " ".join(text_parts)
    names = TOKEN_RE.findall(text)
    if not names: continue
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

wp = sum(1 for r in records if isinstance(r, dict) and r.get("parameters"))
summary = {"total": len(records), "with_parameters": wp, "filled": filled}
(REPORTS / "_step_D9_dat01_params.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_01: total={len(records)} with_parameters={wp} filled={filled}")