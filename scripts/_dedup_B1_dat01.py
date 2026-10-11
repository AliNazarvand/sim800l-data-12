#!/usr/bin/env python3
"""Detect and merge duplicate commands in dat_01.
   Normalization: strip leading 'AT+' or '+', uppercase.
   Merge rule (R10): keep oldest (smallest id or earliest created_at),
   copy source/status/confidence from richer duplicate, drop duplicate."""
import sys, json, re
from pathlib import Path
try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr); sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml"))
    return c[0] if c else (DATA / (dat_id + ".yaml") if (DATA / (dat_id + ".yaml")).exists() else None)

def norm_cmd(cmd):
    if not cmd:
        return None
    s = str(cmd).strip().upper()
    if s.startswith("AT+"):
        s = s[3:]
    elif s.startswith("+"):
        s = s[1:]
    elif s.startswith("AT"):
        s = s[2:]
    return s

def id_sort_key(rid):
    # dat_01_0001 -> (0, 1) ; dat_01_0400 -> (0, 400)
    m = re.match(r"dat_01_(\d+)$", str(rid))
    if m:
        return (0, int(m.group(1)))
    return (1, str(rid))

p = find("dat_01")
if p is None:
    print("dat_01 not found"); sys.exit(1)
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list):
    records = [records]

print(f"Initial records: {len(records)}")

# گروه‌بندی بر اساس normalized command
groups = {}
for rec in records:
    if not isinstance(rec, dict):
        continue
    n = norm_cmd(rec.get("command"))
    if not n:
        continue
    groups.setdefault(n, []).append(rec)

duplicates_info = {}
merged_count = 0
deleted_ids = []
kept_ids = []

def score_record(rec):
    """بالاتر = بهتر. برای انتخاب منبع بهتر."""
    score = 0
    src = rec.get("source") or {}
    if isinstance(src, dict):
        if src.get("page"): score += 5
        if src.get("section"): score += 3
        if src.get("quote"): score += 2
        if src.get("date"): score += 1
    # رکورد partial با source بهتر از unknown
    st = rec.get("status")
    if st == "partial": score += 4
    elif st == "complete": score += 6
    elif st == "unknown": score += 0
    # پارامترها/پاسخ/مثال
    if rec.get("parameters"): score += 2
    if rec.get("response_success"): score += 2
    if rec.get("response_error"): score += 1
    if rec.get("examples"): score += 1
    return score

new_records = []
seen_keys = set()
for rec in records:
    if not isinstance(rec, dict):
        new_records.append(rec); continue
    n = norm_cmd(rec.get("command"))
    if not n or n not in groups or len(groups[n]) == 1:
        new_records.append(rec)
        continue
    if n in seen_keys:
        # این رکورد تکراری است؛ ولی باید تصمیم بگیریم کدام بماند
        continue
    seen_keys.add(n)
    group = groups[n]
    # انتخاب رکورد اصلی: کوچک‌ترین id
    group_sorted_by_id = sorted(group, key=lambda r: id_sort_key(r.get("id", "")))
    primary = group_sorted_by_id[0]
    # انتخاب بهترین منبع: بالاترین score
    group_sorted_by_score = sorted(group, key=lambda r: score_record(r), reverse=True)
    best = group_sorted_by_score[0]

    # ادغام: primary را نگه می‌داریم، فیلدهای منبع/وضعیت را از best می‌گیریم
    merged = dict(primary)
    # کپی source از best
    if best.get("source"):
        merged["source"] = best["source"]
    # status: ارتقا بده اگر best بهتر بود
    order = {"unknown": 0, "inferred": 1, "partial": 2, "complete": 3, "deferred": 4, "blocked": 5, "example-only": 6}
    if order.get(best.get("status",""), 0) > order.get(merged.get("status",""), 0):
        merged["status"] = best["status"]
    # confidence: بیشترین
    try:
        c1 = float(merged.get("confidence") or 0.0)
        c2 = float(best.get("confidence") or 0.0)
        merged["confidence"] = max(c1, c2)
    except Exception:
        pass
    # پارامترها/پاسخ/مثال: اگر primary خالی بود و best داشت
    for k in ("parameters","response_success","response_error","examples","related_urcs","related_states","related_commands"):
        if not merged.get(k) and best.get(k):
            merged[k] = best[k]
    # برای یکسان بودن command در کانتکست، AT+ را حفظ می‌کنیم اگر primary نداشت
    merged["updated_at"] = best.get("updated_at") or merged.get("updated_at")

    new_records.append(merged)
    kept_ids.append(merged.get("id"))
    for other in group_sorted_by_id[1:]:
        deleted_ids.append(other.get("id"))
        merged_count += 1

    duplicates_info[n] = {
        "group_size": len(group),
        "kept_id": merged.get("id"),
        "deleted_ids": [o.get("id") for o in group_sorted_by_id[1:]],
        "kept_command": merged.get("command"),
        "best_source_page": (best.get("source") or {}).get("page") if isinstance(best.get("source"), dict) else None,
    }

# نوشتن دوباره
with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(new_records, f, allow_unicode=True, sort_keys=False,
                   default_flow_style=False, width=1000)

report = {
    "file": p.name,
    "before": len(records),
    "after": len(new_records),
    "merged_removed": merged_count,
    "duplicates_groups": len(duplicates_info),
    "kept_ids": kept_ids[:200],
    "deleted_ids": deleted_ids[:200],
    "details": duplicates_info,
}
(REPORTS / "_step_B1_duplicates.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"Before: {len(records)}  After: {len(new_records)}  Removed duplicates: {merged_count}")
print(f"Duplicate groups: {len(duplicates_info)}")