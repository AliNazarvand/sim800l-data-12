#!/usr/bin/env python3
"""Scan AT Manual V1.01 for structured AT command sections.
   Extracts: command, section number, section title, page, syntax line (if found).
   Does NOT modify any data file."""
import sys, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_EX = ROOT / "sources" / "extracted"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

def load_paged(path):
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    pages = []
    parts = re.split(r"<<<PAGE\s+(\d+)>>>", text)
    for i in range(1, len(parts) - 1, 2):
        try:
            num = int(parts[i])
        except Exception:
            continue
        pages.append((num, parts[i + 1]))
    return pages

pages = load_paged(SRC_EX / "at_manual_v1_01_paged.txt")

# الگوی header: "4.2.3 AT+CMGS Send Message" یا "4.2.3  AT+CMGS  Send Message"
# شماره بخش + AT+COMMAND + عنوان
HEADER_RE = re.compile(
    r"^\s*([0-9]+(?:\.[0-9]+){1,4})\s+(AT\+[A-Z0-9]+)\s+(.{2,120}?)\s*$"
)
# fallback: خطی که فقط AT+COMMAND + توضیح دارد
HEADER_RE2 = re.compile(
    r"^\s*(AT\+[A-Z0-9]{2,})\s+(.{2,120}?)\s*$"
)

commands = {}  # command -> record
current = None  # dict being built

def flush_current():
    global current
    if current and current.get("command"):
        cmd = current["command"]
        # اگر قبلاً بود، اطلاعات کامل‌تر را نگه دار
        if cmd not in commands:
            commands[cmd] = current
        else:
            existing = commands[cmd]
            # اگر current سکشن/صفحه بهتری دارد، آن را ترجیح بده
            if not existing.get("section") and current.get("section"):
                existing["section"] = current["section"]
            if not existing.get("syntax") and current.get("syntax"):
                existing["syntax"] = current["syntax"]
    current = None

# بخش‌های کلیدی که باید در اسکن نادیده گرفته شوند (فهرست مطالب، سرصفحه و غیره)
SKIP_PATTERNS = [
    re.compile(r"^AT\+[A-Z0-9]+\s*\.{3,}", re.IGNORECASE),  # فهرست مطالب
    re.compile(r"^\s*SIM800 Series_AT", re.IGNORECASE),      # سرصفحه/پاصفحه
    re.compile(r"^\s*$"),
]

for page_no, body in pages:
    for line in body.splitlines():
        s = line.strip()
        if len(s) < 6:
            continue
        skip = False
        for pat in SKIP_PATTERNS:
            if pat.match(s):
                skip = True; break
        if skip:
            continue

        m = HEADER_RE.match(s)
        if m:
            flush_current()
            current = {
                "command": m.group(2).strip(),
                "section_number": m.group(1).strip(),
                "section_title": m.group(3).strip()[:120],
                "page": page_no,
                "syntax": None,
                "quote": s[:280],
            }
            continue

        # داخل یک سکشن هستیم؟ دنبال خط syntax بگرد
        if current is not None:
            cmd = current.get("command", "")
            if not cmd:
                continue
            # خط syntax معمولاً با AT+COMMAND= یا AT+COMMAND? یا AT+COMMAND شروع می‌شود
            if not current.get("syntax"):
                cmd_base = cmd  # مثل AT+CMGS
                if s.startswith(cmd_base) and ("=" in s or "?" in s or s == cmd_base or s.startswith(cmd_base + " ")):
                    # فقط اگر شبیه syntax واقعی باشد
                    if len(s) < 240 and not s.lower().startswith("at+" + cmd_base.lower().replace("at+","")):
                        current["syntax"] = s[:240]
                    else:
                        current["syntax"] = s[:240]

        # fallback: AT+COMMAND بدون شماره بخش (بعضی بخش‌ها ممکن است اینطور باشند)
        if current is None:
            m2 = HEADER_RE2.match(s)
            if m2:
                cmd = m2.group(1).strip()
                # فقط اگر خط واقعاً شبیه تعریف باشد (نه فقط ذکر در متن)
                # شرط: خط خیلی کوتاه و شامل توضیح be
                if 8 < len(s) < 200 and cmd.count("+") == 1:
                    current = {
                        "command": cmd,
                        "section_number": None,
                        "section_title": m2.group(2).strip()[:120],
                        "page": page_no,
                        "syntax": None,
                        "quote": s[:280],
                    }

flush_current()

# حذف دستورات سطح پایه (فقط AT و ATI و ...)
for k in list(commands.keys()):
    if k in ("AT", "ATI", "ATZ", "ATE", "ATQ", "ATV", "ATX", "AT&C", "AT&D", "AT&S"):
        # اینها را نگه می‌داریم ولی علامت‌گذاری می‌کنیم
        pass

report = {
    "total_commands_found": len(commands),
    "commands": commands,
}
out = REPORTS / "_step_B1_at_manual_scan.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

print(f"AT command sections found: {len(commands)}")
samples = list(commands.items())[:15]
for k, v in samples:
    print(f"  {k}  p{v.get('page')}  [{v.get('section_number','-')}]  {v.get('section_title','')[:60]}")