#!/usr/bin/env python3
"""
apply_refine_dat_01.py
گام ۴.۱: حذف فقط رکوردهای confirmed_noise از data/dat_01_at_command.yaml
گام ۴.۲: علامت‌گذاری رکوردهای weak_at_signal با status=partial + notes.

منبع تصمیم: reports/dat_01_REFINE_DIAGNOSTIC.md (جدول کامل).
هیچ رکورد دیگری تغییر نمی‌کند.
"""
import re, sys, json
from pathlib import Path
from datetime import datetime, timezone
import yaml

ROOT     = Path(__file__).resolve().parent.parent
DIAG_MD  = ROOT / "reports" / "dat_01_REFINE_DIAGNOSTIC.md"
DAT01    = ROOT / "data" / "dat_01_at_command.yaml"
REPORT   = ROOT / "reports" / "dat_01_APPLY_REFINE.md"
SIDE     = ROOT / "reports" / "dat_01_APPLY_REFINE.json"

if not DIAG_MD.exists():
    print(f"ERROR: {DIAG_MD} not found", file=sys.stderr); sys.exit(1)
if not DAT01.exists():
    print(f"ERROR: {DAT01} not found", file=sys.stderr); sys.exit(1)

# ─── استخراج verdictها از جدول diagnostic ───
md = DIAG_MD.read_text(encoding="utf-8")
# ردیف‌های جدول کامل: | +CMD | dat_01_XXXX | A/B | verdict | ... |
row_re = re.compile(r'^\|\s*\+?([A-Z][A-Z0-9]{1,15})\s*\|\s*(dat_01_\d{4})\s*\|\s*([AB])\s*\|\s*([a-z_]+)\s*\|', re.M)
confirmed_noise = []   # (cmd, id)
weak_signal     = []   # (cmd, id)
for m in row_re.finditer(md):
    cmd, rid, cat, verdict = m.group(1), m.group(2), m.group(3), m.group(4)
    if verdict == "confirmed_noise":
        confirmed_noise.append((cmd, rid))
    elif verdict == "weak_at_signal":
        weak_signal.append((cmd, rid))

noise_ids = {rid for _, rid in confirmed_noise}
weak_ids  = {rid for _, rid in weak_signal}

print(f"Parsed diagnostic: confirmed_noise={len(confirmed_noise)} weak_at_signal={len(weak_signal)}")

# ─── بارگذاری dat_01 ───
data = yaml.safe_load(DAT01.read_text(encoding="utf-8")) or []
if not isinstance(data, list):
    data = [data]

before = len(data)
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ─── گام ۴.۱: حذف confirmed_noise ───
removed = []
kept = []
for r in data:
    if not isinstance(r, dict):
        kept.append(r); continue
    rid = r.get("id","")
    if rid in noise_ids:
        removed.append({"id": rid, "command": r.get("command","")})
        continue
    kept.append(r)

after_removal = len(kept)

# ─── گام ۴.۲: علامت‌گذاری weak_at_signal ───
tagged = []
for r in kept:
    if not isinstance(r, dict): continue
    rid = r.get("id","")
    if rid in weak_ids:
        r["status"] = "partial"
        old_note = (r.get("notes") or "").strip()
        marker = "manual verification vs TOC required — weak signal in manual text (see reports/dat_01_REFINE_DIAGNOSTIC.md)"
        if marker not in old_note:
            r["notes"] = (old_note + " | " + marker) if old_note else marker
        r["updated_at"] = now
        tag_list = r.get("tags") or []
        if "weak-signal" not in tag_list:
            tag_list.append("weak-signal")
            r["tags"] = tag_list
        tagged.append(rid)

# ─── ذخیره ───
DAT01.write_text(
    yaml.safe_dump(kept, allow_unicode=True, sort_keys=False, width=200, default_flow_style=False),
    encoding="utf-8"
)

# ─── گزارش ───
lines = []
lines.append("# dat_01_APPLY_REFINE")
lines.append("")
lines.append(f"تاریخ: {now}")
lines.append("")
lines.append("## خلاصه")
lines.append(f"- رکوردهای قبل از اعمال: **{before}**")
lines.append(f"- رکوردهای حذف‌شده (confirmed_noise): **{len(removed)}**")
lines.append(f"- رکوردهای علامت‌گذاری‌شده (weak_at_signal): **{len(tagged)}**")
lines.append(f"- رکوردهای بعد از اعمال: **{len(kept)}**")
lines.append("")
lines.append("## موارد حذف‌شده")
lines.append("")
lines.append("| id | command |")
lines.append("|---|---|")
for x in removed:
    lines.append(f"| {x['id']} | {x['command']} |")
lines.append("")
lines.append("## موارد علامت‌گذاری‌شده (status=partial, notes=weak-signal)")
lines.append("")
lines.append("| id |")
lines.append("|---|")
for rid in tagged:
    lines.append(f"| {rid} |")
lines.append("")
lines.append("## یادداشت")
lines.append("- هیچ رکورد weak_at_signal حذف نشد؛ فقط علامت‌گذاری شد.")
lines.append("- برای حذف بیشتر، منتظر بازبینی دستی مالک پروژه باشید.")
REPORT.write_text("\n".join(lines), encoding="utf-8")
SIDE.write_text(json.dumps({
    "generated": now,
    "before": before,
    "removed": removed,
    "tagged": tagged,
    "after": len(kept),
}, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Removed: {len(removed)}  Tagged: {len(tagged)}  Before: {before}  After: {len(kept)}")
print(f"Report: {REPORT.name}")