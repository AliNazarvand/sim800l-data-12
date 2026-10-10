#!/usr/bin/env python3
"""
fix_dat_07_classification.py
اصلاح classification رکوردهای Unclassified در dat_07 و تشخیص duplicates.

- هیچ رکوردی حذف نمی‌شود.
- فقط فیلد category، tags، notes، updated_at به‌روز می‌شوند.
- گزارش: reports/dat_07_FIX.md
"""
import sys, json
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import yaml

ROOT    = Path(__file__).resolve().parent.parent
DAT07   = ROOT / "data" / "dat_07_hardware_reference.yaml"
REPORT  = ROOT / "reports" / "dat_07_FIX.md"
SIDE    = ROOT / "reports" / "dat_07_FIX.json"

# ─── دسته‌بندی جدید ───
def classify_v2(name, desc=""):
    n = (name or "").upper()
    d = (desc or "").upper()
    # Ground
    if "GND" in n or "GROUND" in d or "CONNECT TO GND" in d:
        return "Ground"
    # Not Connected
    if "NOT CONNECT" in d or "NOT CONNECTED" in d or n in {"NC"}:
        return "NC"
    # Power
    if any(k in n for k in ["VBAT", "VCC", "VDD", "VRTC", "VCHG", "VBUS"]):
        return "Power"
    # PCM / Audio
    if "PCM" in n or any(k in n for k in ["MICP","MICN","SPKP","SPKN","MIC","SPK","EAR","REC"]):
        return "Audio"
    # I2C
    if n in {"SCL", "SDA"} or "I2C" in d:
        return "I2C"
    # LED sink
    if n.startswith("ISINK"):
        return "LED"
    # Keypad (mark as possibly SIM800H-only)
    if any(n.startswith(p) for p in ("COL", "ROW", "KBC", "KBR")):
        return "Keypad"
    # UART
    if any(k in n for k in ["TXD", "RXD", "CTS", "RTS", "DTR", "DCD", "RI"]):
        return "UART"
    # SIM
    if "SIM" in n or "SIM" in d:
        return "SIM"
    # USB
    if "USB" in n:
        return "USB"
    # GPIO / PWM / ADC
    if "GPIO" in n: return "GPIO"
    if "PWM" in n: return "PWM"
    if "ADC" in n: return "ADC"
    # Named pins
    if "PWRKEY" in n: return "PWRKEY"
    if "RESET" in n: return "Reset"
    if "STATUS" in n: return "STATUS"
    if "NETLIGHT" in n: return "NETLIGHT"
    return "Unclassified"

# ─── نگاشت هم‌ارزها ───
# هم‌ارزها بر اساس دانش pinout SIM800L LGA (استاندارد SIMCom)
EQUIV = [
    # (V2.02 name, V1.00 name, reason)
    ("C1", "SIM_VDD", "SIM card power supply"),
    ("C2", "SIM_RST", "SIM card reset"),
    ("C3", "SIM_CLK", "SIM card clock"),
    ("C7", "SIM_DATA", "SIM card data I/O"),
    ("C8", "SIM_DET", "SIM card detection"),
    ("DCD", "UART_DCD", "UART Data Carrier Detect"),
    ("DTR", "UART_DTR", "UART Data Terminal Ready"),
    ("RI", "UART_RI", "UART Ring Indicator"),
    ("PCMCLK", "PCM_CLK", "PCM clock"),
    ("PCMIN", "PCM_IN", "PCM input"),
    ("PCMOUT", "PCM_OUT", "PCM output"),
    ("PCMSYNC", "PCM_SYNC", "PCM sync"),
]

def main():
    if not DAT07.exists():
        print(f"ERROR: {DAT07} not found", file=sys.stderr); sys.exit(1)

    data = yaml.safe_load(DAT07.read_text(encoding="utf-8")) or []
    if not isinstance(data, list):
        data = [data]

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    reclassified = []
    unchanged = 0
    still_unclassified = []

    # نام → رکورد (برای تشخیص هم‌ارز)
    by_name = {}
    for r in data:
        if isinstance(r, dict):
            by_name[(r.get("name") or "").upper()] = r

    # ─── اصلاح classification ───
    for r in data:
        if not isinstance(r, dict): continue
        old_cat = r.get("category", "Unclassified")
        new_cat = classify_v2(r.get("name",""), r.get("function",""))
        if old_cat != new_cat:
            r["category"] = new_cat
            r["updated_at"] = now
            tags = r.get("tags") or []
            tags = [t for t in tags if t not in {"unclassified"}]
            if new_cat.lower() not in tags:
                tags.append(new_cat.lower())
            r["tags"] = tags
            reclassified.append({
                "id": r.get("id",""),
                "name": r.get("name",""),
                "old": old_cat,
                "new": new_cat,
            })
        else:
            unchanged += 1
        if new_cat == "Unclassified":
            still_unclassified.append(r.get("name",""))

    # ─── تشخیص هم‌ارزها ───
    dup_pairs = []
    for a, b, reason in EQUIV:
        if a in by_name and b in by_name:
            rec_a = by_name[a]
            rec_b = by_name[b]
            # فقط اگر واقعاً دو رکورد جداگانه هستند
            if rec_a.get("id") != rec_b.get("id"):
                # علامت‌گذاری
                for rec, other in [(rec_a, rec_b), (rec_b, rec_a)]:
                    notes = rec.get("notes") or ""
                    marker = f"possible_duplicate_of: {other.get('id')}"
                    if marker not in notes:
                        rec["notes"] = (notes + " | " + marker) if notes else marker
                    rec["updated_at"] = now
                    tags = rec.get("tags") or []
                    if "possible-duplicate" not in tags:
                        tags.append("possible-duplicate")
                        rec["tags"] = tags
                dup_pairs.append({
                    "v202": a, "v100": b,
                    "id_v202": rec_a.get("id"),
                    "id_v100": rec_b.get("id"),
                    "reason": reason,
                })

    # ─── ذخیره ───
    DAT07.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=200, default_flow_style=False),
        encoding="utf-8"
    )

    # ─── گزارش ───
    cats = Counter(r.get("category","?") for r in data if isinstance(r, dict))

    lines = []
    lines.append("# dat_07_FIX — اصلاح classification و تشخیص هم‌ارزها")
    lines.append("")
    lines.append(f"تاریخ: {now}")
    lines.append("")
    lines.append("## خلاصه")
    lines.append(f"- کل رکوردها: **{len(data)}**")
    lines.append(f"- رکوردهای بازدسته‌بندی‌شده: **{len(reclassified)}**")
    lines.append(f"- رکوردهای بدون تغییر: **{unchanged}**")
    lines.append(f"- هم‌ارزهای علامت‌گذاری‌شده: **{len(dup_pairs)}** جفت")
    lines.append(f"- رکوردهای همچنان Unclassified: **{len(still_unclassified)}**")
    lines.append("")
    lines.append("## توزیع category بعد از اصلاح")
    for c, n in cats.most_common():
        lines.append(f"- {c}: {n}")
    lines.append("")
    lines.append("## بازدسته‌بندی‌ها")
    lines.append("")
    lines.append("| id | name | old | new |")
    lines.append("|---|---|---|---|")
    for x in reclassified:
        lines.append(f"| {x['id']} | {x['name']} | {x['old']} | {x['new']} |")
    lines.append("")
    lines.append("## هم‌ارزهای علامت‌گذاری‌شده (only tagged، نه merged)")
    lines.append("")
    lines.append("| V2.02 | V1.00 | id (V2.02) | id (V1.00) | دلیل |")
    lines.append("|---|---|---|---|---|")
    for d in dup_pairs:
        lines.append(f"| {d['v202']} | {d['v100']} | {d['id_v202']} | {d['id_v100']} | {d['reason']} |")
    lines.append("")
    if still_unclassified:
        lines.append("## همچنان Unclassified (نیازمند بازبینی دستی)")
        for n in still_unclassified:
            lines.append(f"- {n}")
        lines.append("")
    lines.append("## یادداشت")
    lines.append("- هیچ رکوردی حذف نشد.")
    lines.append("- هم‌ارزها فقط با tag ``possible-duplicate`` و ``notes`` علامت‌گذاری شدند؛ ادغام نشدند.")
    lines.append("- وضعیت دیتاست همچنان ``partial`` است.")
    REPORT.write_text("\n".join(lines), encoding="utf-8")

    SIDE.write_text(json.dumps({
        "generated": now,
        "total": len(data),
        "reclassified_count": len(reclassified),
        "dup_pairs_count": len(dup_pairs),
        "still_unclassified": still_unclassified,
        "by_category": dict(cats),
        "reclassified": reclassified,
        "dup_pairs": dup_pairs,
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Total: {len(data)}  Reclassified: {len(reclassified)}  DupPairs: {len(dup_pairs)}  Still-Unclassified: {len(still_unclassified)}")
    print(f"Report: {REPORT.name}")

if __name__ == "__main__":
    main()