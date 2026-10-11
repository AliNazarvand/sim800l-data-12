#!/usr/bin/env python3
"""Build reports/CROSS_REF_REPORT.md from _validation_summary.json L3 errors."""
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
summary_path = REPORTS / "_validation_summary.json"

ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

if not summary_path.exists():
    (REPORTS / "CROSS_REF_REPORT.md").write_text(
        "# CROSS_REF_REPORT\n\n"
        f"Generated: {ts}\n\n"
        "No validation summary available. Run scripts/validate.py first.\n",
        encoding="utf-8"
    )
    print("No summary; empty CROSS_REF_REPORT written.")
    raise SystemExit(0)

data = json.loads(summary_path.read_text(encoding="utf-8"))
errors = data.get("errors", [])
l3 = [e for e in errors if e.get("level") == 3]

# Group by dataset and by command
by_ds = {}
by_cmd = {}
samples = {}
for e in l3:
    ds = e.get("dataset", "?")
    err = e.get("error", "")
    by_ds[ds] = by_ds.get(ds, 0) + 1
    # Extract command token from message
    cmd = ""
    if "command " in err:
        try:
            cmd = err.split("command ", 1)[1].split(" ", 1)[0]
        except Exception:
            cmd = "?"
    elif "related_command " in err:
        try:
            cmd = err.split("related_command ", 1)[1].split(" ", 1)[0]
        except Exception:
            cmd = "?"
    key = (ds, cmd)
    by_cmd[key] = by_cmd.get(key, 0) + 1
    if ds not in samples:
        samples[ds] = []
    if len(samples[ds]) < 5:
        samples[ds].append(e.get("record", "?"))

lines = [
    "# CROSS_REF_REPORT",
    "",
    f"Generated: {ts}",
    "",
    "## خلاصه",
    "",
    f"- مجموع خطاهای سطح ۳ (Cross-ref): {len(l3)}",
    "- این خطاها زمانی رفع می‌شوند که `dat_01` به وضعیت complete برسد (خوشه B).",
    "",
    "## توزیع بر اساس دیتاست",
    "",
    "| دیتاست | تعداد | نمونه رکورد |",
    "|---|---|---|",
]
for ds in sorted(by_ds.keys()):
    lines.append(f"| {ds} | {by_ds[ds]} | {', '.join(samples.get(ds, [])[:3])} |")
lines.append("")
lines.append("## توزیع بر اساس (دیتاست، command)")
lines.append("")
lines.append("| دیتاست | command | تعداد |")
lines.append("|---|---|---|")
for (ds, cmd) in sorted(by_cmd.keys(), key=lambda x: (x[0], -by_cmd[x])):
    lines.append(f"| {ds} | {cmd} | {by_cmd[(ds, cmd)]} |")
lines.append("")

(REPORTS / "CROSS_REF_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
print(f"CROSS_REF_REPORT.md written: {len(l3)} L3 errors, {len(by_ds)} datasets affected")