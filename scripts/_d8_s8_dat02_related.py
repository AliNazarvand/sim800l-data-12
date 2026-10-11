#!/usr/bin/env python3
"""Fill dat_02 related_command from heading lines in AT Manual."""
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

# Build URC -> cmd mapping by scanning pages: URC appears in a section whose heading is AT+CMD
HEADER_RE = re.compile(r"^\s*([0-9]+(?:\.[0-9]+){1,4})\s+(AT\+[A-Z0-9]+)\s+(.{2,120}?)\s*$")
# URC token pattern
URC_TOKEN = re.compile(r"(\+[A-Z][A-Z0-9]{2,})\b")
urc_to_cmd = {}
current_cmd = None
for pn, body in pages:
    for line in body.splitlines():
        s = line.strip()
        m = HEADER_RE.match(s)
        if m:
            current_cmd = m.group(2).strip().upper()
            continue
        if current_cmd:
            for tok in URC_TOKEN.findall(s):
                tok = tok.upper()
                if tok not in urc_to_cmd:
                    urc_to_cmd[tok] = current_cmd

# Also inline: doc URC name from dat_02 record
def norm_urc(s):
    if not s: return None
    s = str(s).strip().upper()
    if s.startswith("AT+"): s = s[3:]
    elif s.startswith("+"): s = s[1:]
    return "+" + s

p = find("dat_02")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("related_command"): continue
    u = r.get("urc_string")
    full = norm_urc(u)
    if not full: continue
    cmd = urc_to_cmd.get(full)
    if cmd:
        r["related_command"] = cmd
        r["updated_at"] = ts
        filled += 1

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)

wc = sum(1 for r in records if isinstance(r, dict) and r.get("related_command"))
summary = {"total": len(records), "with_related_command": wc, "filled": filled}
(REPORTS / "_step_D8_dat02_related.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_02: total={len(records)} with_related_command={wc} filled={filled}")