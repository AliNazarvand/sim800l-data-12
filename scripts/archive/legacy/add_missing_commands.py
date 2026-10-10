#!/usr/bin/env python3
"""
add_missing_commands.py
افزودن commandهای گمشده (از MISSING_COMMANDS.txt) به dat_01.
"""
from __future__ import annotations
import sys
from pathlib import Path
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    print("[ERROR] pip install pyyaml"); sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
MISSING = ROOT / "reports" / "MISSING_COMMANDS.txt"
TARGET = ROOT / "data" / "dat_01_at_command.yaml"

def load_yaml(p):
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_yaml(p, data):
    with open(p, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False,
                  default_flow_style=False, width=1000)

def main():
    if not MISSING.exists():
        print(f"[SKIP] {MISSING} یافت نشد. ابتدا extract_at_manual_full.py اجرا شود.")
        return
    if not TARGET.exists():
        print(f"[ERROR] {TARGET} یافت نشد."); sys.exit(1)

    missing = [line.strip() for line in MISSING.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not missing:
        print("[SKIP] هیچ command گمشده‌ای ثبت نشده.")
        return

    data = load_yaml(TARGET)
    records = data.get("records") or []

    # محاسبه بیشترین id
    max_n = 0
    for r in records:
        if isinstance(r.get("id"), str) and r["id"].startswith("dat_01_"):
            try:
                n = int(r["id"].split("_")[2])
                max_n = max(max_n, n)
            except: pass

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    added = 0
    for cmd in missing:
        max_n += 1
        new_id = f"dat_01_{max_n:04d}"
        records.append({
            "id": new_id,
            "category": "ExtractedFromManual",
            "command": cmd,
            "description": "",
            "section": "-",
            "source": {
                "name": "SIM800 Series AT Command Manual",
                "version": "V1.01",
                "date": "2013-07-23",
                "section": "-",
            },
            "source_type": "primary",
            "confidence": 0.85,
            "status": "partial",
            "applicable_models": ["SIM800L"],
            "notes": "auto-extracted from manual txt; needs manual review",
            "tags": ["at_command", "auto_extracted"],
            "created_at": now,
            "updated_at": now,
        })
        added += 1

    data["records"] = records
    save_yaml(TARGET, data)
    print(f"[OK] {added} command جدید به dat_01 افزوده شد (تعداد کل: {len(records)})")

if __name__ == "__main__":
    main()
