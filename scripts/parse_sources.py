#!/usr/bin/env python3
"""استخراج رکورد از منابع متنی (AT Manual + PDFهای سخت‌افزاری)."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXTRACTED = ROOT / "sources" / "extracted"

def read_text(name):
    p = EXTRACTED / name
    if not p.exists():
        return ""
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

def find_at_commands(text):
    """پیدا کردن AT+XXX با کانتکست."""
    commands = {}
    # Split by pages to keep context
    pages = re.split(r'=== PAGE \d+ ===', text)
    for page_idx, page in enumerate(pages, 1):
        for m in re.finditer(r'AT\+([A-Z][A-Z0-9_]*)', page):
            cmd = "+" + m.group(1)
            if cmd not in commands:
                start = max(0, m.start() - 200)
                end = min(len(page), m.end() + 600)
                commands[cmd] = {
                    "first_seen_page": page_idx,
                    "context": page[start:end].strip(),
                }
    return commands

def main():
    at_manual = read_text("SIM800 Series_AT Command Manual_V1.01.txt")
    if not at_manual:
        # fallback نام فایل دیگر
        for name in EXTRACTED.glob("*AT*Command*Manual*.txt"):
            at_manual = name.read_text(encoding="utf-8", errors="ignore")
            break
    cmds = find_at_commands(at_manual)
    print(f"found {len(cmds)} AT commands in AT manual")
    # Save raw index for populate_all
    import json
    idx = ROOT / "sources" / "extracted" / "_at_commands_index.json"
    idx.write_text(json.dumps(cmds, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"saved: {idx}")
    return 0

if __name__ == "__main__":
    sys.exit(main())