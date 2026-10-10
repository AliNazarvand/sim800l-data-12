#!/usr/bin/env python3
"""
audit_dat_01.py
مقایسه commandهای dat_01 با فهرست مطالب (TOC) AT Manual V1.01.
خروجی: reports/dat_01_AUDIT.md
هیچ داده‌ای را تغییر نمی‌دهد — فقط گزارش می‌دهد.
"""
import re, sys
from pathlib import Path
from datetime import datetime, timezone
import yaml

ROOT    = Path(__file__).resolve().parent.parent
MANUAL  = ROOT / "sources" / "extracted" / "SIM800 Series_AT Command Manual_V1.01.txt"
DAT01   = ROOT / "data" / "dat_01_at_command.yaml"
REPORT  = ROOT / "reports" / "dat_01_AUDIT.md"

if not MANUAL.exists():
    print(f"ERROR: manual not found: {MANUAL}", file=sys.stderr); sys.exit(1)
if not DAT01.exists():
    print(f"ERROR: dat_01 not found: {DAT01}", file=sys.stderr); sys.exit(1)

text = MANUAL.read_text(encoding="utf-8", errors="ignore")

# ─── یافتن TOC ───
# الگوی خطوط TOC: متن + نقطه‌چین + شماره صفحه در انتهای خط
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

# fallback: اگر TOC با نقطه‌چین کم بود، از خود بخش فهرست استفاده کن
if len(toc_commands) < 30:
    # بخش ابتدایی فایل تا قبل از اولین "Chapter 1" یا "AT+"
    head = text[:200000]
    for m in re.findall(r'(?:\bAT)?\+([A-Z][A-Z0-9]{1,15})', head):
        toc_commands.add(m)

# ─── بارگذاری dat_01 ───
try:
    records = yaml.safe_load(DAT01.read_text(encoding="utf-8")) or []
    if not isinstance(records, list): records = [records]
except Exception as e:
    print(f"ERROR: yaml parse: {e}", file=sys.stderr); sys.exit(1)

dat01_cmds = {}
for r in records:
    if not isinstance(r, dict): continue
    c = (r.get("command") or "").lstrip("+").strip()
    if c:
        dat01_cmds.setdefault(c, []).append(r.get("id","?"))

dat01_set = set(dat01_cmds.keys())

# ─── مقایسه ───
in_both   = sorted(dat01_set & toc_commands)
only_01   = sorted(dat01_set - toc_commands)
only_toc  = sorted(toc_commands - dat01_set)

# پیشنهاد حذف/بررسی: آن‌هایی که در TOC نیستند
# پیشنهاد افزودن: آن‌هایی که در TOC هستند و در dat_01 نیستند

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
lines = []
lines.append("# dat_01_AUDIT — مقایسه با فهرست AT Manual V1.01")
lines.append("")
lines.append(f"تاریخ: {now}")
lines.append(f"منبع TOC: `sources/extracted/SIM800 Series_AT Command Manual_V1.01.txt`")
lines.append(f"خطوط TOC یافت‌شده: {len(toc_lines)}")
lines.append("")
lines.append("## آمار")
lines.append(f"- commandهای یکتای dat_01: **{len(dat01_set)}**")
lines.append(f"- commandهای یکتای TOC: **{len(toc_commands)}**")
lines.append(f"- مشترک: **{len(in_both)}**")
lines.append(f"- فقط در dat_01 (احتمالاً نویز/استخراج اشتباه): **{len(only_01)}**")
lines.append(f"- فقط در TOC (احتمالاً گم‌شده): **{len(only_toc)}**")
lines.append("")
lines.append("## پوشش تخمینی")
if len(toc_commands) > 0:
    cov = 100.0 * len(in_both) / len(toc_commands)
    lines.append(f"- تخمین پوشش: **{cov:.1f}%** (هدف پرامپت ۰۰۹: ≥ ۹۵٪)")
    lines.append(f"- وضعیت: {'✅ قابل قبول' if cov >= 95 else '❌ نیازمند بازبینی'}")
lines.append("")
lines.append(f"## فقط در dat_01 — کاندیدای بررسی/حذف ({len(only_01)})")
lines.append("")
lines.append("| command | id(ها) | دلیل احتمالی |")
lines.append("|---|---|---|")
for c in only_01:
    ids = ", ".join(dat01_cmds.get(c, [])[:3])
    reason = "در TOC نیست"
    lines.append(f"| +{c} | {ids} | {reason} |")
lines.append("")
lines.append(f"## فقط در TOC — کاندیدای افزودن ({len(only_toc)})")
lines.append("")
for c in only_toc:
    lines.append(f"- +{c}")
lines.append("")
lines.append("## یادداشت")
lines.append("- این گزارش هیچ داده‌ای را تغییر نداده است.")
lines.append("- برای اعمال، باید یک اسکریپت کوچک جداگانه نوشته شود.")
lines.append("- TOC ممکن است کامل نباشد؛ قبل از حذف، هر مورد دستی بررسی شود.")

REPORT.write_text("\n".join(lines), encoding="utf-8")

print(f"Audit: dat_01={len(dat01_set)} TOC={len(toc_commands)} both={len(in_both)} only_dat01={len(only_01)} only_TOC={len(only_toc)}")
if len(toc_commands) > 0:
    print(f"Coverage: {100.0*len(in_both)/len(toc_commands):.1f}%")
print(f"Report: {REPORT.name}")