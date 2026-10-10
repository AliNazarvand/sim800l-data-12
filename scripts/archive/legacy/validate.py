#!/usr/bin/env python3
"""اعتبارسنجی داده‌های sim800l-data."""
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "pyyaml"])
    import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

FORBIDDEN = {"synthetic", "example-only"}
VALID_STATUS = {"complete","partial","unknown","inferred","blocked","deferred"}
VALID_SRC_TYPE = {"primary","secondary","external"}
REQUIRED = ["id","category","source","source_type","confidence","status","applicable_models","created_at","updated_at"]

errors = []
warnings = []
per_file = {}

def main():
    files = sorted(DATA.glob("*.yaml"))
    print(f"بررسی {len(files)} فایل...")
    for p in files:
        try:
            with open(p, encoding="utf-8") as f:
                data = yaml.safe_load(f) or []
        except Exception as e:
            errors.append(f"[YAML] {p.name}: {e}")
            continue
        if not isinstance(data, list):
            errors.append(f"[SHAPE] {p.name}: باید لیست باشد")
            continue
        per_file[p.name] = len(data)
        seen_ids = set()
        for idx, rec in enumerate(data):
            if not isinstance(rec, dict):
                errors.append(f"[REC] {p.name}[{idx}]")
                continue
            for f in REQUIRED:
                if f not in rec:
                    errors.append(f"[REQ] {p.name}[{idx}]: فیلد '{f}' ندارد")
            rid = rec.get("id")
            if rid in seen_ids:
                errors.append(f"[DUP] {p.name}: id تکراری {rid}")
            seen_ids.add(rid)
            st = rec.get("status")
            if st in FORBIDDEN:
                errors.append(f"[STATUS] {p.name}/{rid}: status ممنوع '{st}'")
            if st and st not in VALID_STATUS:
                errors.append(f"[STATUS] {p.name}/{rid}: status نامعتبر '{st}'")
            stp = rec.get("source_type")
            if stp and stp not in VALID_SRC_TYPE:
                errors.append(f"[SRC] {p.name}/{rid}: source_type نامعتبر")
            am = rec.get("applicable_models") or []
            if "SIM800L" not in am:
                errors.append(f"[MODEL] {p.name}/{rid}: SIM800L ندارد")

    REPORTS.mkdir(parents=True, exist_ok=True)
    out = [f"# VALIDATION_REPORT\n", f"> auto-generated at {NOW}\n"]
    out.append(f"## خلاصه\n")
    out.append(f"- فایل‌های بررسی‌شده: {len(files)}")
    out.append(f"- خطاها: {len(errors)}")
    out.append(f"- هشدارها: {len(warnings)}")
    out.append("\n## تعداد رکورد در هر فایل\n")
    for k in sorted(per_file.keys()):
        out.append(f"- {k}: {per_file[k]}")

    if errors:
        out.append("\n## خطاها\n")
        for e in errors[:200]:
            out.append(f"- ❌ {e}")
    if warnings:
        out.append("\n## هشدارها\n")
        for w in warnings[:200]:
            out.append(f"- ⚠ {w}")

    (REPORTS / "VALIDATION_REPORT.md").write_text("\n".join(out), encoding="utf-8")

    if errors:
        print(f"❌ {len(errors)} خطا")
        return 1
    print("✅ بدون خطا")
    return 0

if __name__ == "__main__":
    sys.exit(main())