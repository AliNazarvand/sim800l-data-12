#!/usr/bin/env python3
import sys, json, re
from pathlib import Path
from datetime import datetime, timezone
try:
    import yaml
except ImportError: sys.exit(2)
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"; SRC_EX = ROOT / "sources" / "extracted"; REPORTS = ROOT / "reports"
def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml")); return c[0] if c else None
def load_paged(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    pages = []; parts = re.split(r"<<<PAGE\s+(\d+)>>>", text)
    for i in range(1, len(parts) - 1, 2):
        try: num = int(parts[i])
        except Exception: continue
        pages.append((num, parts[i+1]))
    return pages
pages = load_paged(SRC_EX / "at_manual_v1_01_paged.txt")
HEADER_RE = re.compile(r"^\s*([0-9]+(?:\.[0-9]+){1,4})\s+(AT\+[A-Z0-9]+)\s+(.{2,120}?)\s*$")
URC_RE = re.compile(r"(\+[A-Z][A-Z0-9]{2,})")
cmd_urc_map = {}; current = None
for pn, body in pages:
    for line in body.splitlines():
        s = line.strip()
        m = HEADER_RE.match(s)
        if m:
            current = m.group(2).strip().upper(); continue
        if current:
            for tok in URC_RE.findall(s):
                cmd_urc_map.setdefault(current, set()).add(tok)
p = find("dat_02")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("related_urcs"): continue
    cmd = r.get("related_command") or ""
    cmd = cmd.upper()
    if not cmd.startswith("AT+") and cmd:
        cmd = "AT+" + cmd.lstrip("+")
    urcs = cmd_urc_map.get(cmd, set())
    if urcs:
        r["related_urcs"] = sorted(urcs)[:5]; r["updated_at"] = ts; filled += 1
with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
wu = sum(1 for r in records if isinstance(r, dict) and r.get("related_urcs"))
(REPORTS / "_step_D11_dat02_urcs.json").write_text(json.dumps({"total":len(records),"with_related_urcs":wu,"filled":filled}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_02: total={len(records)} with_related_urcs={wu} filled={filled}")