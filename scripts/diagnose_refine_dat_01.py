#!/usr/bin/env python3
"""
diagnose_refine_dat_01.py
تشخیص عمیق ۵۹ رکورد only_dat01 (فقط گزارش؛ بدون تغییر در data/).

برای هر رکورد A/B در dat_01_REFINE.json بررسی می‌کند:
  - متن manual (الگوهای مختلف AT command)
  - جداول استخراج‌شده (at_v1_01_ALL.tsv)
  - CSVهای _raw/ (اگر TSV ناقص بود)
و verdict واقعی می‌دهد:
  confirmed_noise, confirmed_parameter, likely_valid_table,
  likely_valid_colon, weak_at_signal
"""
import re, sys, json
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

ROOT        = Path(__file__).resolve().parent.parent
REFINE_JSON = ROOT / "reports" / "dat_01_REFINE.json"
MANUAL      = ROOT / "sources" / "extracted" / "SIM800 Series_AT Command Manual_V1.01.txt"
TABLES_TSV  = ROOT / "sources" / "extracted" / "tables" / "at_v1_01_ALL.tsv"
TABLES_RAW  = ROOT / "sources" / "extracted" / "tables" / "at_v1_01" / "_raw"
REPORT      = ROOT / "reports" / "dat_01_REFINE_DIAGNOSTIC.md"

if not REFINE_JSON.exists():
    print(f"ERROR: {REFINE_JSON} not found", file=sys.stderr); sys.exit(1)

data = json.loads(REFINE_JSON.read_text(encoding="utf-8"))
details = data.get("details", [])
if not details:
    print("ERROR: no details in REFINE_JSON", file=sys.stderr); sys.exit(1)

manual = MANUAL.read_text(encoding="utf-8", errors="ignore") if MANUAL.exists() else ""
tsv    = TABLES_TSV.read_text(encoding="utf-8", errors="ignore") if TABLES_TSV.exists() else ""

raw_text = ""
if TABLES_RAW.exists():
    chunks = []
    for f in TABLES_RAW.glob("*.csv"):
        try: chunks.append(f.read_text(encoding="utf-8", errors="ignore"))
        except Exception: pass
    raw_text = "\n".join(chunks)

def count_patterns(text, cmd):
    c = re.escape(cmd)
    return {
        "at_prefix":  len(re.findall(r'(?<![A-Z0-9])AT\+' + c + r'(?![A-Z0-9])', text, re.I)),
        "plus_equal": len(re.findall(r'(?<![A-Z0-9])\+' + c + r'\s*=', text)),
        "plus_query": len(re.findall(r'(?<![A-Z0-9])\+' + c + r'\s*\?', text)),
        "plus_colon": len(re.findall(r'(?<![A-Z0-9])\+' + c + r'\s*:', text)),
        "plus_comma": len(re.findall(r'(?<![A-Z0-9])\+' + c + r'\s*,', text)),
        "plus_space": len(re.findall(r'(?<![A-Z0-9])\+' + c + r'\s+[A-Z0-9<\[]', text)),
        "plus_eol":   len(re.findall(r'(?<![A-Z0-9])\+' + c + r'\s*(?:\r|\n|$)', text, re.M)),
        "as_param":   len(re.findall(r'<' + c + r'[\s,>]', text, re.I)),
    }

def table_evidence(cmd, tsv_text, raw_text):
    """آیا command در سلول جدول آمده؟"""
    c = re.escape(cmd)
    tsv_hit = False
    if tsv_text:
        # سلول TSV: با tab یا ابتدا/انتهای خط، یا داخل «+CMD»
        tsv_hit = bool(re.search(r'(?:^|\t)[+]?' + c + r'(?:\t|$|[,;\s])', tsv_text, re.I | re.M))
    raw_hit = False
    if raw_text:
        raw_hit = bool(re.search(r'(?:^|[\t,"])[+]?' + c + r'(?:[\t,"]|$|\s)', raw_text, re.I | re.M))
    return tsv_hit, raw_hit

results = []
for e in details:
    if e.get("category") not in ("A", "B"):
        continue
    cmd = (e.get("command") or "").lstrip("+").strip()
    if not cmd: continue

    mp = count_patterns(manual, cmd)
    tsv_hit, raw_hit = table_evidence(cmd, tsv, raw_text)

    at_any   = mp["at_prefix"] + mp["plus_equal"] + mp["plus_query"] + mp["plus_eol"]
    colon_any = mp["plus_colon"]
    param_any = mp["as_param"]

    # تصمیم verdict
    if tsv_hit or raw_hit:
        verdict = "likely_valid_table"
    elif colon_any >= 1:
        verdict = "likely_valid_colon"
    elif at_any >= 3:
        verdict = "likely_valid_text"
    elif at_any >= 1:
        verdict = "weak_at_signal"
    elif param_any >= 1:
        verdict = "confirmed_parameter"
    else:
        verdict = "confirmed_noise"

    results.append({
        "command":   e["command"],
        "id":        (e.get("ids") or ["?"])[0],
        "orig_cat":  e.get("category"),
        "verdict":   verdict,
        "manual_at": at_any,
        "manual_colon": colon_any,
        "manual_param": param_any,
        "in_tsv":    tsv_hit,
        "in_raw":    raw_hit,
        "context":   (e.get("context") or "")[:250],
    })

summary = Counter(r["verdict"] for r in results)
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

lines = []
lines.append("# dat_01_REFINE_DIAGNOSTIC")
lines.append("")
lines.append(f"تاریخ: {now}")
lines.append(f"منبع: `reports/dat_01_REFINE.json`")
lines.append("")
lines.append("## خلاصه")
lines.append("")
lines.append(f"- مجموع A+B بررسی‌شده: **{len(results)}**")
for k, v in sorted(summary.items(), key=lambda x: -x[1]):
    lines.append(f"- **{k}**: {v}")
lines.append("")
lines.append("## معنا verdictها و اقدام پیشنهادی")
lines.append("")
lines.append("| verdict | معنا | اقدام |")
lines.append("|---|---|---|")
lines.append("| `confirmed_noise` | هیچ اثری در manual یا table نیست | **حذف مطمئن** |")
lines.append("| `confirmed_parameter` | فقط به‌عنوان پارامتر `<CMD>` آمده | **حذف مطمئن** |")
lines.append("| `likely_valid_table` | فقط در جدول‌های استخراج‌شده هست | **نگه‌داشتن** (نقص classifier قبلی) |")
lines.append("| `likely_valid_colon` | به‌شکل `+CMD:` در متن هست | **نگه‌داشتن** |")
lines.append("| `likely_valid_text` | به‌شکل `+CMD` ≥۳ بار آمده | **نگه‌داشتن** |")
lines.append("| `weak_at_signal` | ۱-۲ بار `+CMD` آمده | **بازبینی دستی** |")
lines.append("")
lines.append("## جدول کامل (sorted by verdict)")
lines.append("")
lines.append("| command | id | orig_cat | verdict | manual_at | manual_colon | manual_param | tsv | raw |")
lines.append("|---|---|---|---|---|---|---|---|---|")
order = ["confirmed_noise", "confirmed_parameter", "weak_at_signal",
         "likely_valid_colon", "likely_valid_text", "likely_valid_table"]
def sort_key(r):
    try: return (order.index(r["verdict"]), r["command"])
    except ValueError: return (99, r["command"])
for r in sorted(results, key=sort_key):
    lines.append(f"| {r['command']} | {r['id']} | {r['orig_cat']} | {r['verdict']} | "
                 f"{r['manual_at']} | {r['manual_colon']} | {r['manual_param']} | "
                 f"{'✓' if r['in_tsv'] else '-'} | {'✓' if r['in_raw'] else '-'} |")
lines.append("")
lines.append("## نمونه‌های هر verdict (تا ۵ مورد)")
lines.append("")
for v in order:
    items = [r for r in results if r["verdict"] == v][:5]
    if not items: continue
    lines.append(f"### `{v}` — {len([x for x in results if x['verdict']==v])} رکورد")
    lines.append("")
    for r in items:
        ctx = r["context"][:180].replace("|", "\\|")
        lines.append(f"- **{r['command']}** (`{r['id']}`, orig={r['orig_cat']})")
        if ctx:
            lines.append(f"  > {ctx}")
    lines.append("")
lines.append("## یادداشت")
lines.append("")
lines.append("- این گزارش هیچ داده‌ای را از `data/dat_01_at_command.yaml` تغییر نداده است.")
lines.append("- برای اعمال حذف، از verdictهای `confirmed_noise` و `confirmed_parameter` استفاده شود.")
lines.append("- `weak_at_signal` را دستی بازبینی کنید.")

REPORT.write_text("\n".join(lines), encoding="utf-8")

print(f"Diagnostic: {len(results)} records checked")
for k, v in sorted(summary.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")
print(f"Report: {REPORT.name}")