#!/usr/bin/env python3
"""
extract_at_manual_full.py
استخراج تمام AT commands از فایل متن SIM800 Series_AT Command Manual.

- الگوها: خطوطی که با AT+ یا AT شروع می‌شوند
- افزودن به dat_01 فقط commandهای جدید
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[ERROR] pip install pyyaml"); sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
SRC_TXT = ROOT / "sources" / "extracted" / "SIM800 Series_AT Command Manual_V1.01.txt"
DATA = ROOT / "data"

# الگوی command: AT+XXX یا ATXXX (شروع سطر)
CMD_RE = re.compile(r"\b(AT\+[A-Z0-9><_]+|ATA|ATD|ATE|ATH|ATI|ATL|ATM|ATO|ATP|ATQ|ATS\d+|ATV|ATX|ATZ|AT\+A/?)\b")
# استخراج فقط نام پایه بدون پارامترها
BASE_RE = re.compile(r"^(AT\+[A-Z0-9><]+)")

def canonical_command(raw: str) -> str:
    """تبدیل AT+CMGS به +CMGS، ATA به +ATA (با + پیشوند برای سازگاری)"""
    s = raw.strip().upper()
    if s.startswith("AT+"):
        return s[2:]  # حذف AT → +CMGS
    if s.startswith("AT") and len(s) > 2:
        return "+" + s  # ATA → +ATA
    return s

def extract_from_txt(path: Path) -> set[str]:
    """خواندن txt و استخراج همه commandهای متمایز"""
    if not path.exists():
        print(f"[ERROR] {path} یافت نشد"); return set()
    text = path.read_text(encoding="utf-8", errors="ignore")
    # پیدا کردن همه AT+XXX
    found = set()
    for m in re.finditer(r"\bAT\+([A-Z][A-Z0-9><_]{1,30})\b", text):
        raw = "AT+" + m.group(1)
        # فیلتر کردن متغیرهای placeholder
        if "<" in raw or ">" in raw:
            continue
        found.add(canonical_command(raw))
    # AT (بدون +) مثل ATA, ATD, ATE, ...
    for m in re.finditer(r"\bAT([A-Z])\b", text):
        letter = m.group(1)
        if letter in "ADEFHILMOQTVXZ" or letter.isdigit():
            found.add("+AT" + letter)
    return found

def load_existing_dat01():
    """بارگذاری commandهای فعلی در dat_01"""
    existing = set()
    for yml in DATA.rglob("*.yaml"):
        try:
            data = yaml.safe_load(yml.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict): continue
        for r in (data.get("records") or []):
            if isinstance(r, dict) and isinstance(r.get("id"), str) and r["id"].startswith("dat_01_"):
                c = r.get("command")
                if c:
                    existing.add(canonical_command(str(c)))
    return existing

def main():
    print("=== EXTRACT AT COMMANDS FROM MANUAL ===")
    if not SRC_TXT.exists():
        print(f"[ERROR] فایل txt یافت نشد: {SRC_TXT}")
        print("[HINT] ابتدا python scripts/extract_pdf.py را اجرا کنید")
        sys.exit(1)

    commands = extract_from_txt(SRC_TXT)
    existing = load_existing_dat01()
    missing = sorted(commands - existing)

    print(f"Commands یافت‌شده در txt : {len(commands)}")
    print(f"Commands فعلی در dat_01   : {len(existing)}")
    print(f"Commands گمشده            : {len(missing)}")

    if missing:
        print("\nنمونه‌ای از گمشده‌ها:")
        for c in missing[:30]:
            print(f"  {c}")

    # ذخیره لیست گمشده‌ها برای افزودن توسط اسکریپت بعدی
    out = ROOT / "reports" / "MISSING_COMMANDS.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(missing), encoding="utf-8")
    print(f"\n[SAVED] {out}")

if __name__ == "__main__":
    main()
