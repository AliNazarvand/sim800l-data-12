#!/usr/bin/env python3
"""
refine_dat_01.py
طبقه‌بندی 59 رکورد only_dat01 در سه دسته:
  A. parameter       — فقط به‌عنوان پارامتر در متن manual آمده
  B. context-mismatch — در متن manual هست ولی در context غیر-command
  C. valid-but-not-in-TOC — با AT+CMD در بدنه manual هست اما در TOC نیست
خروجی: reports/dat_01_REFINE.md
هیچ داده‌ای تغییر نمی‌کند.
"""
import re, sys, json
from pathlib import Path
from datetime import datetime, timezone
import yaml

ROOT   = Path(__file__).resolve().parent.parent
MANUAL = ROOT / "sources" / "extracted" / "SIM800 Series_AT Command Manual_V1.01.txt"
DAT01  = ROOT / "data" / "dat_01_at_command.yaml"
REPORT = ROOT / "reports" / "dat_01_REFINE.md"
SIDE   = ROOT / "reports" / "dat_01_REFINE.json"

if not MANUAL.exists():
    print(f"ERROR: manual not found: {MANUAL}", file=sys.stderr); sys.exit(1)
if not DAT01.exists():
    print(f"ERROR: dat_01 not found: {DAT01}", file=sys.stderr); sys.exit(1)

text = MANUAL.read_text(encoding="utf-8", errors="ignore")

# ─── همان TOC detection که در audit_dat_01 ───
toc_lines = []
for line in text.splitlines():
    s = line.strip()
    if not s: continue
    if not re.search(r'\.{3,}\s*\d+\s*$', s): continue
    toc_lines.append(s)

toc_commands = set()
for l in toc_lines:
    for m in re.findall(r'(?:\bAT)?\+([A-Z][A-Z0-9]{1,15})', l):
        toc_commands.add(m)
if len(toc_commands) < 30:
    for m in re.findall(r'(?:\bAT)?\+([A-Z][A-Z0-9]{1,15})', text[:200000]):
        toc_commands.add(m)

# ─── بارگذاری dat_01 ───
records = yaml.safe_load(DAT01.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]

dat01_cmds = {}
for r in records:
    if not isinstance(r, dict): continue
    c = (r.get("command") or "").lstrip("+").strip()
    if c:
        dat01_cmds.setdefault(c, []).append(r.get("id","?"))

only_dat01 = sorted(set(dat01_cmds.keys()) - toc_commands)

# ─── الگوها برای طبقه‌بندی ───
def classify(cmd):
    c = re.escape(cmd)
    # AT+CMD با مرز کلمه
    at_prefix = len(re.findall(r'(?<![A-Z0-9])AT\+' + c + r'(?![A-Z0-9])', text, re.I))
    # +CMD= (write form)
    with_equal = len(re.findall(r'(?<![A-Z0-9])\+' + c + r'\s*=', text))
    # +CMD? (read form)
    with_q = len(re.findall(r'(?<![A-Z0-9])\+' + c + r'\s*\?', text))
    # +CMD<CR> یا +CMD (exec form) در خط جدید
    with_at_line = len(re.findall(r'(?:^|\n)\s*(?:AT)?\+' + c + r'\s*(?:[\r\n<])', text))
    # <CMD> به‌عنوان placeholder پارامتر
    as_param_angle = len(re.findall(r'<' + c + r'>', text, re.I))
    # <CMD, ...> یا <CMD1>
    as_param_multi = len(re.findall(r'<' + c + r'[\s,>]', text, re.I))
    # به‌عنوان پارامتر در ستون جدول (شروع ستون، بدون +)
    as_column = len(re.findall(r'(?:\t|\|)\s*' + c + r'\s*(?:\t|\|)', text, re.I))

    at_total = at_prefix + with_equal + with_q + with_at_line
    param_total = as_param_angle + as_param_multi + as_column

    if at_total >= 3:
        return "C", at_total, param_total
    if at_total == 0 and param_total > 0:
        return "A", at_total, param_total
    if at_total == 0 and param_total == 0:
        return "B", at_total, param_total
    # مرزی: at_total در {1,2} → به B (مشکوک) می‌رود
    return "B", at_total, param_total

def first_context(cmd, radius=200):
    m = re.search(r'(?<![A-Z0-9])(?:AT)?\+' + re.escape(cmd) + r'(?![A-Z0-9])', text)
    if not m:
        m = re.search(r'<' + re.escape(cmd) + r'>', text, re.I)
    if not m:
        return ""
    s = max(0, m.start() - radius)
    e = min(len(text), m.end() + radius)
    ctx = text[s:e].replace("\r"," ").replace("\n"," ")
    ctx = re.sub(r"\s+", " ", ctx).strip()
    return ctx[:400]

A, B, C = [], [], []
details = []
for cmd in only_dat01:
    cat, at_c, par_c = classify(cmd)
    entry = {
        "command": f"+{cmd}",
        "ids": dat01_cmds.get(cmd, []),
        "category": cat,
        "at_occurrences": at_c,
        "param_occurrences": par_c,
        "context": first_context(cmd),
    }
    details.append(entry)
    if cat == "A": A.append(cmd)
    elif cat == "B": B.append(cmd)
    else: C.append(cmd)

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
lines = []
lines.append("# dat_01_REFINE — طبقه‌بندی ۵۹ رکورد only_dat01")
lines.append("")
lines.append(f"تاریخ: {now}")
lines.append(f"منبع: `sources/extracted/SIM800 Series_AT Command Manual_V1.01.txt`")
lines.append("")
lines.append("## خلاصه")
lines.append("")
lines.append(f"- کل رکوردهای only_dat01: **{len(only_dat01)}**")
lines.append(f"- دسته A (parameter — کاندیدای حذف): **{len(A)}**")
lines.append(f"- دسته B (context-mismatch — کاندیدای حذف): **{len(B)}**")
lines.append(f"- دسته C (valid-but-not-in-TOC — کاندیدای نگه‌داشتن): **{len(C)}**")
lines.append("")
lines.append("## معیارها")
lines.append("")
lines.append("| دسته | معیار | اقدام پیشنهادی |")
lines.append("|---|---|---|")
lines.append("| A | `AT+CMD` در بدنه manual ≤ 2 بار **و** `<CMD>` به‌عنوان پارامتر | حذف |")
lines.append("| B | `AT+CMD` = 0 **و** هیچ placeholder پارامتری هم نبود → context غلط | حذف |")
lines.append("| C | `AT+CMD` در بدنه ≥ 3 بار → احتمالاً command واقعی که از TOC جا افتاده | نگه‌داشتن |")
lines.append("")
lines.append(f"## دسته A — پارامتر (کاندیدای حذف) — {len(A)}")
lines.append("")
lines.append("| command | id | at_count | param_count |")
lines.append("|---|---|---|---|")
for e in details:
    if e["category"] == "A":
        lines.append(f"| {e['command']} | {', '.join(e['ids'][:2])} | {e['at_occurrences']} | {e['param_occurrences']} |")
lines.append("")
lines.append(f"## دسته B — context-mismatch (کاندیدای حذف) — {len(B)}")
lines.append("")
lines.append("| command | id | at_count | param_count |")
lines.append("|---|---|---|---|")
for e in details:
    if e["category"] == "B":
        lines.append(f"| {e['command']} | {', '.join(e['ids'][:2])} | {e['at_occurrences']} | {e['param_occurrences']} |")
lines.append("")
lines.append(f"## دسته C — معتبر اما گم‌شده از TOC (نگه‌داشتن) — {len(C)}")
lines.append("")
lines.append("| command | id | at_count | param_count |")
lines.append("|---|---|---|---|")
for e in details:
    if e["category"] == "C":
        lines.append(f"| {e['command']} | {', '.join(e['ids'][:2])} | {e['at_occurrences']} | {e['param_occurrences']} |")
lines.append("")
lines.append("## نمونه context (۱۰ مورد اول هر دسته)")
lines.append("")
for cat_name, items in [("A", A), ("B", B), ("C", C)]:
    lines.append(f"### دسته {cat_name} — نمونه")
    lines.append("")
    shown = 0
    for e in details:
        if e["category"] != cat_name: continue
        if shown >= 10: break
        lines.append(f"- **{e['command']}** (`{', '.join(e['ids'][:1])}`):")
        lines.append(f"  > {e['context']}")
        lines.append("")
        shown += 1
lines.append("## یادداشت")
lines.append("")
lines.append("- این گزارش هیچ داده‌ای را از `data/dat_01_at_command.yaml` حذف نکرده است.")
lines.append("- برای اعمال حذف، باید یک اسکریپت جداگانه با تأیید صریح مالک پروژه اجرا شود.")
lines.append("- توصیه: قبل از حذف، دسته A و B دستی sample review شوند.")

REPORT.write_text("\n".join(lines), encoding="utf-8")
SIDE.write_text(json.dumps({
    "generated": now,
    "totals": {"only_dat01": len(only_dat01), "A": len(A), "B": len(B), "C": len(C)},
    "details": details
}, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Refine: only_dat01={len(only_dat01)} A={len(A)} B={len(B)} C={len(C)}")
print(f"Report: {REPORT.name}  Sidecar: {SIDE.name}")