#!/usr/bin/env python3
"""
extract_dat_07.py
استخراج pinهای SIM800L از جدول‌های hardware design (V2.02 با اولویت بر V1.00).

منابع:
  sources/extracted/tables/hw_v2_02/_raw/*.csv
  sources/extracted/tables/hw_v1_00/_raw/*.csv

خروجی:
  data/dat_07_hardware_reference.yaml
  reports/dat_07_REPORT.md
"""
import csv, re, sys, json
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import yaml

ROOT      = Path(__file__).resolve().parent.parent
RAW_V202  = ROOT / "sources" / "extracted" / "tables" / "hw_v2_02" / "_raw"
RAW_V100  = ROOT / "sources" / "extracted" / "tables" / "hw_v1_00" / "_raw"
OUT       = ROOT / "data" / "dat_07_hardware_reference.yaml"
REPORT    = ROOT / "reports" / "dat_07_REPORT.md"
SIDE      = ROOT / "reports" / "dat_07_EXTRACT.json"

def read_csv_safe(path):
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            rows = list(csv.reader(f))
        # فیلتر ردیف‌های خالی
        rows = [r for r in rows if any((c or "").strip() for c in r)]
        return rows
    except Exception:
        return []

def is_pin_table(rows):
    """آیا این CSV یک جدول pin است؟"""
    if len(rows) < 3: return False
    header = " ".join((c or "").strip().lower() for c in rows[0])
    # باید حداقل "pin" و یکی از "name"/"description"/"function"/"i/o" باشد
    if "pin" not in header: return False
    if not any(k in header for k in ["name", "signal", "description", "function", "i/o", "i/o", "type", "remark"]):
        return False
    return True

def detect_columns(header):
    """پیدا کردن اندیس ستون‌های pin/name/desc."""
    h = [(c or "").strip().lower() for c in header]
    def find(*keys):
        for i, col in enumerate(h):
            for k in keys:
                if k in col: return i
        return None
    pin_col  = find("pin no", "pin number", "pin#", "pin")
    name_col = find("signal name", "pin name", "name", "signal")
    desc_col = find("description", "function", "remark", "type")
    if pin_col  is None: pin_col = 0
    if name_col is None: name_col = 1 if len(h) > 1 else None
    if desc_col is None: desc_col = 2 if len(h) > 2 else None
    return pin_col, name_col, desc_col

PIN_NAME_RE = re.compile(r'^[A-Za-z][A-Za-z0-9_+\-/]*$')
NUMERIC_RE  = re.compile(r'^[0-9]+(\s*[-–]\s*[0-9]+)?$')

def parse_pin_table(rows):
    """استخراج (pin_number, name, description) از جدول."""
    header = rows[0]
    pin_col, name_col, desc_col = detect_columns(header)
    out = []
    for r in rows[1:]:
        if name_col is None or name_col >= len(r): continue
        pin = (r[pin_col].strip() if pin_col < len(r) else "")
        name = (r[name_col] or "").strip()
        desc = (r[desc_col].strip() if (desc_col is not None and desc_col < len(r)) else "")
        if not name: continue
        # نام باید شبیه نام pin باشد
        if not PIN_NAME_RE.match(name): continue
        # pin_number باید عددی یا ترکیبی باشد
        if pin and not (NUMERIC_RE.match(pin) or "," in pin or "/" in pin):
            # اگر pin عدد نبود، احتمالاً جدول pin نیست؛ ادامه می‌دهیم
            pass
        # فیلتر نویزهای متنی
        if len(name) > 20: continue
        if name.lower() in {"pin","name","signal","gnd","vcc","io","i/o","type"}: continue
        out.append((pin, name, desc))
    return out

def classify_pin(name, desc=""):
    n = (name or "").upper()
    d = (desc or "").upper()
    if "GND" in n or "GROUND" in n: return "Ground"
    if any(k in n for k in ["VBAT", "VCC", "VDD", "VRTC", "VDD_EXT", "VCHG"]): return "Power"
    if any(k in n for k in ["TXD", "RXD", "CTS", "RTS", "DTR", "DCD", "RI", "TXD_", "RXD_"]): return "UART"
    if "SIM" in n or "SIM" in d: return "SIM"
    if any(k in n for k in ["MICP", "MICN", "SPKP", "SPKN", "HP", "EAR", "MIC", "SPK", "REC", "AUDIO"]): return "Audio"
    if "ANT" in n or "RF" in n: return "Antenna" if "ANT" in n else "RF"
    if "PWRKEY" in n or "PWR_KEY" in n: return "PWRKEY"
    if "RESET" in n: return "Reset"
    if "STATUS" in n: return "STATUS"
    if "NETLIGHT" in n or "NETLIGHT" in d: return "NETLIGHT"
    if "GPIO" in n: return "GPIO"
    if "ADC" in n: return "ADC"
    if "PWM" in n: return "PWM"
    if "RTC" in n: return "RTC"
    if "USB" in n: return "USB"
    if "CHARGE" in n or "CHG" in n: return "Charge"
    return "Unclassified"

def find_tables(raw_dir):
    found = []
    for f in sorted(raw_dir.glob("*.csv")):
        rows = read_csv_safe(f)
        if is_pin_table(rows):
            parsed = parse_pin_table(rows)
            if parsed:
                found.append((f, parsed))
    return found

def main():
    if not RAW_V202.exists() and not RAW_V100.exists():
        print("ERROR: هیچ پوشه _raw یافت نشد.", file=sys.stderr); sys.exit(1)

    v202_tables = find_tables(RAW_V202) if RAW_V202.exists() else []
    v100_tables = find_tables(RAW_V100) if RAW_V100.exists() else []

    print(f"V2.02 pin tables: {len(v202_tables)}")
    for f, parsed in v202_tables:
        print(f"  - {f.name}: {len(parsed)} pins")
    print(f"V1.00 pin tables: {len(v100_tables)}")
    for f, parsed in v100_tables:
        print(f"  - {f.name}: {len(parsed)} pins")

    # ادغام با اولویت V2.02
    pins = {}  # key = name upper
    conflict_log = []

    for f, parsed in v202_tables:
        for pin, name, desc in parsed:
            key = name.upper()
            if key in pins:
                # در همان منبع یا تکرار — آخرین را نگه دار
                continue
            pins[key] = {
                "pin": pin, "name": name, "desc": desc,
                "src_file": f.name, "src_ver": "V2.02",
            }
    for f, parsed in v100_tables:
        for pin, name, desc in parsed:
            key = name.upper()
            if key in pins:
                # در V2.02 هست → نادیده گرفته می‌شود
                continue
            pins[key] = {
                "pin": pin, "name": name, "desc": desc,
                "src_file": f.name, "src_ver": "V1.00",
            }

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    records = []
    for idx, (key, info) in enumerate(sorted(pins.items()), start=1):
        rid = f"dat_07_{idx:04d}"
        ver = info["src_ver"]
        src_name = "SIM800H&SIM800L_Hardware_Design" if ver == "V2.02" else "SIM800L_Hardware_Design"
        src_date = "2015-07-27" if ver == "V2.02" else "2013-08-20"
        records.append({
            "id": rid,
            "category": classify_pin(info["name"], info["desc"]),
            "name": info["name"],
            "pin_number": info["pin"],
            "direction": "unknown",
            "voltage_min": None,
            "voltage_typ": None,
            "voltage_max": None,
            "current_typ": None,
            "current_max": None,
            "function": info["desc"] or "unknown",
            "alternate_function": None,
            "pull_up_down": None,
            "esd_rating": None,
            "impedance": None,
            "decoupling": None,
            "source": {
                "name": src_name,
                "version": ver,
                "date": src_date,
                "page": "auto",
                "section": "Pin Description",
                "quote": info["src_file"],
            },
            "source_type": "primary",
            "confidence": 0.7,
            "status": "partial",
            "conflicts": [],
            "notes": "Auto-extracted from pin table. Needs manual verification of direction/voltage/current and pin_number.",
            "applicable_models": ["SIM800L"],
            "tags": ["hardware", "pin", classify_pin(info["name"], info["desc"]).lower()],
            "created_at": now,
            "updated_at": now,
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, width=200)

    # گزارش
    cats = Counter(r["category"] for r in records)
    vers = Counter(r["source"]["version"] for r in records)
    lines = []
    lines.append("# dat_07_REPORT — Hardware Reference")
    lines.append("")
    lines.append(f"تاریخ: {now}")
    lines.append("")
    lines.append("## خلاصه")
    lines.append(f"- رکوردهای استخراج‌شده: **{len(records)}**")
    lines.append(f"- منبع V2.02: {vers.get('V2.02', 0)}")
    lines.append(f"- منبع V1.00: {vers.get('V1.00', 0)}")
    lines.append("")
    lines.append("## توزیع category")
    for cat, n in cats.most_common():
        lines.append(f"- {cat}: {n}")
    lines.append("")
    lines.append("## یادداشت")
    lines.append("- وضعیت دیتاست: `partial` (فیلدهای voltage/current/esd خودکار استخراج نشده‌اند).")
    lines.append("- تمام رکوردها از جدول‌های pin استخراج شده‌اند و `source` دارند.")
    lines.append("- برای رسیدن به `complete` نیاز به بازبینی دستی و تکمیل voltage/current از متن manual است.")
    lines.append("")
    lines.append("## کار باقی‌مانده")
    lines.append("1. بازبینی رکوردهای Unclassified و انتقال به دسته مناسب.")
    lines.append("2. تکمیل voltage_min/typ/max، current_typ/max از متن manual.")
    lines.append("3. تنظیم direction (input/output/power/ground) برای هر pin.")
    REPORT.write_text("\n".join(lines), encoding="utf-8")

    SIDE.write_text(json.dumps({
        "generated": now,
        "total": len(records),
        "by_version": dict(vers),
        "by_category": dict(cats),
        "records": [{"id": r["id"], "name": r["name"], "pin": r["pin_number"],
                     "category": r["category"], "src": r["source"]["version"]} for r in records],
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nWrote {len(records)} records to {OUT.name}")
    print(f"Report: {REPORT.name}")
    print(f"Sidecar: {SIDE.name}")

if __name__ == "__main__":
    main()