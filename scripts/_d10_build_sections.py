#!/usr/bin/env python3
"""Build and cache section_index.json: command -> section body from AT Manual."""
import sys, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_EX = ROOT / "sources" / "extracted"
REPORTS = ROOT / "reports"

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

sections = {}
current_cmd = None
current_body = []
current_page = None
for pn, body in pages:
    for line in body.splitlines():
        s = line.strip()
        m = HEADER_RE.match(s)
        if m:
            if current_cmd:
                sections[current_cmd] = {"body": " ".join(current_body)[:4000], "page": current_page}
            current_cmd = m.group(2).strip().upper()
            current_body = []
            current_page = pn
        elif current_cmd and len(s) < 200:
            current_body.append(s)
if current_cmd:
    sections[current_cmd] = {"body": " ".join(current_body)[:4000], "page": current_page}

(REPORTS / "_section_index.json").write_text(json.dumps(sections, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"section index: {len(sections)} commands cached")