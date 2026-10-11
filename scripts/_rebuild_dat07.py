#!/usr/bin/env python3
"""Rebuild dat_07_hardware_reference.yaml using existing pin list + source info
extracted from V2.02 (priority) then V1.00. Does not invent new data."""
import sys, json, re
from pathlib import Path
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr); sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SRC_EX = ROOT / "sources" / "extracted"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

def find(dat_id):
    c = sorted(DATA.glob(f"{dat_id}_*.yaml"))
    return c[0] if c else (DATA / f"{dat_id}.yaml" if (DATA / f"{dat_id}.yaml").exists() else None)

def load_paged(path):
    """Return list of (page_number, text) tuples."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    pages = []
    parts = re.split(r"<<<PAGE\s+(\d+)>>>", text)
    # parts = ['', '1', 'body1', '2', 'body2', ...]
    for i in range(1, len(parts) - 1, 2):
        try:
            num = int(parts[i])
        except Exception:
            continue
        pages.append((num, parts[i + 1]))
    return pages

def find_pin_occurrence(pin_name, pages):
    """Return (page_no, line) of the first strong occurrence of pin_name in text."""
    if not pin_name:
        return None
    pat = re.compile(r"\b" + re.escape(str(pin_name).strip()) + r"\b", re.IGNORECASE)
    for page_no, body in pages:
        for line in body.splitlines():
            stripped = line.strip()
            if len(stripped) < 3:
                continue
            if pat.search(stripped):
                # فقط خطوطی که شبیه تعریف پین هستند
                if any(k in stripped for k in ["GND","VBAT","VDD","TXD","RXD","PWRKEY","RESET",
                                                "SIM","MIC","SPK","GPIO","ADC","RF","ANT","STATUS",
                                                "NET","DTR","RI","CTS","RTS","DCD","VDD_EXT",
                                                "Charge","RTC","VDD","ADC","GND","Pin","pin"]):
                    return (page_no, stripped)
    return None

def guess_section(line):
    l = line.lower()
    if "power" in l or "vbat" in l or "gnd" in l: return "Power Supply"
    if "sim" in l: return "SIM Interface"
    if "uart" in l or "txd" in l or "rxd" in l: return "UART Interface"
    if "audio" in l or "mic" in l or "spk" in l: return "Audio Interface"
    if "rf" in l or "antenna" in l: return "RF Interface"
    if "pwrkey" in l or "reset" in l or "status" in l: return "Control Signals"
    if "gpio" in l or "adc" in l: return "GPIO/ADC"
    return "Hardware Reference"

def main():
    dat07_path = find("dat_07")
    if dat07_path is None:
        print("dat_07 not found"); sys.exit(1)
    records = yaml.safe_load(dat07_path.read_text(encoding="utf-8")) or []
    if not isinstance(records, list):
        records = [records]

    v202 = load_paged(SRC_EX / "v2_02_paged.txt")
    v100 = load_paged(SRC_EX / "v1_00_paged.txt")
    print(f"V2.02 pages: {len(v202)}, V1.00 pages: {len(v100)}")

    updated = 0
    unresolved = 0
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    unresolved_ids = []

    for rec in records:
        if not isinstance(rec, dict):
            continue
        name = rec.get("name") or ""
        pin_number = rec.get("pin_number") or ""
        if not name:
            continue
        # جستجو در V2.02 سپس V1.00
        hit = find_pin_occurrence(name, v202)
        version_used = "V2.02"
        if hit is None and pin_number:
            hit = find_pin_occurrence(str(pin_number), v202)
        if hit is None:
            hit = find_pin_occurrence(name, v100)
            version_used = "V1.00"
        if hit is None and pin_number:
            hit = find_pin_occurrence(str(pin_number), v100)
            version_used = "V1.00"
        if hit is None:
            unresolved += 1
            unresolved_ids.append(rec.get("id", "?"))
            continue
        page_no, line = hit
        rec.setdefault("source", {})
        if not isinstance(rec["source"], dict):
            rec["source"] = {}
        # فقط اگر قبلاً خالی بود پر شود (حفظ اطلاعات قبلی اگر معتبر بودند)
        existing_src = rec["source"]
        if not existing_src.get("page"):
            existing_src["page"] = str(page_no)
        if not existing_src.get("section"):
            existing_src["section"] = guess_section(line)
        if not existing_src.get("quote"):
            existing_src["quote"] = line.strip()[:300]
        if not existing_src.get("name"):
            existing_src["name"] = "SIM800H&SIM800L_Hardware_Design" if version_used == "V2.02" else "SIM800L_Hardware_Design"
        if not existing_src.get("version"):
            existing_src["version"] = version_used
        if not existing_src.get("date"):
            existing_src["date"] = "2015-07-27" if version_used == "V2.02" else "2013-08-20"
        rec["source"] = existing_src
        # اگر قبلاً unknown بود، حالا partial
        if rec.get("status") == "unknown":
            rec["status"] = "partial"
        if rec.get("confidence") in (0.0, 0) and existing_src.get("page") and existing_src.get("quote"):
            rec["confidence"] = 0.5
        rec["updated_at"] = ts
        updated += 1

    with dat07_path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False,
                       default_flow_style=False, width=1000)

    report = {
        "file": dat07_path.name,
        "total": len(records),
        "updated": updated,
        "unresolved": unresolved,
        "unresolved_ids": unresolved_ids[:100],
        "v202_pages": len(v202),
        "v100_pages": len(v100)
    }
    (REPORTS / "_step2_dat07_rebuild.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"dat_07: updated={updated}, unresolved={unresolved}, total={len(records)}")

if __name__ == "__main__":
    main()