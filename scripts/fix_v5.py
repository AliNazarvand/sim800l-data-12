"""
v5: fix dat_07 (remove section headers) and dat_15 (rebuild with real mode names),
    fix dat_14 source.page (external).
"""
import sys, yaml, datetime
from pathlib import Path

NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

SECTION_HEADERS = {
    "Power supply", "Power on/down",
    "Audio interfaces", "Audio Interfaces",
    "PCM interface", "PCM Interface",
    "Keypads interface", "Keypads Interface",
    "GPIO",
    "Serial port", "Serial Port",
    "Debug interface", "Debug Interface",
    "ADC", "PWM", "I2C",
    "SIM card interface", "SIM Card interface",
    "Antenna interface", "Antenna Interface",
    "Other", "NC",
}

def load(p):
    try:
        with open(p, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or []
    except Exception:
        return []

def save(p, data):
    with open(p, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)

# ---------- dat_07 ----------
def fix_dat_07(path):
    records = load(path)
    original = len(records)
    kept, removed = [], []
    for r in records:
        if not isinstance(r, dict):
            kept.append(r); continue
        pin  = str(r.get("pin_number", "") or "").strip()
        name = str(r.get("name", "") or "").strip()
        if pin and pin == name and pin in SECTION_HEADERS:
            removed.append(pin)
            continue
        kept.append(r)
    for i, r in enumerate(kept, 1):
        r["id"] = f"dat_07_{i:04d}"
        r["updated_at"] = NOW
    save(path, kept)
    return {"original": original, "kept": len(kept), "removed": removed}

# ---------- dat_15 ----------
def fix_dat_15(path):
    """
    Rebuild dat_15 using:
    - Table 8/7 (CFUN minimum functionality mode)
    - Table 49/48 (current consumption)
    Per R7: V2.02 wins; V1.00 recorded in conflicts.
    """
    P202 = {"name": "SIM800H&SIM800L_Hardware_Design", "version": "V2.02", "date": "2015-07-27"}
    P100 = {"name": "SIM800L_Hardware_Design",            "version": "V1.00", "date": "2013-08-20"}

    def src(pdf, page, section=""):
        return {"name": pdf["name"], "version": pdf["version"], "date": pdf["date"],
                "page": str(page), "section": section, "quote": ""}

    recs = []
    def add(idx, category, mode, command, value_typ, unit, condition,
            page, section, conflicts=None, notes="", related_states=None):
        r = {
            "id": f"dat_15_{idx:04d}",
            "category": category,
            "mode": mode,
            "command": command,
            "parameter": "current",
            "value_min": None,
            "value_typ": value_typ,
            "value_max": None,
            "unit": unit,
            "condition": condition,
            "wake_source": None,
            "related_commands": [command] if command else [],
            "related_states": related_states or [],
            "source": src(P202, page, section),
            "source_type": "primary",
            "confidence": 0.9,
            "status": "complete",
            "conflicts": conflicts or [],
            "notes": notes,
            "tags": ["power", "current-consumption"],
            "applicable_models": ["SIM800L"],
            "created_at": NOW,
            "updated_at": NOW,
        }
        recs.append(r)
        return r

    # --- CFUN minimum functionality table (V2.02 Table 8 / V1.00 Table 7) ---
    cfun_v1 = {0: 0.796, 1: 1.02, 4: 0.892}  # V1.00 values from page 27
    add(1, "Minimum Functionality",
        "Minimum functionality (AT+CFUN=0)", "AT+CFUN=0",
        0.83, "mA", "sleep mode (BS-PA-MFRMS=9)", 26,
        "Table 8: The current consumption of Minimum Functionality Mode",
        conflicts=[{"source": {"name": P100["name"], "version": P100["version"],
                                "page": "27", "note": f"V1.00 reported {cfun_v1[0]} mA"}}],
        notes=f"V1.00 value: {cfun_v1[0]} mA",
        related_states=["MINIMUM_FUNCTIONALITY", "SLEEP"])
    add(2, "Minimum Functionality",
        "Full functionality (AT+CFUN=1)", "AT+CFUN=1",
        1.04, "mA", "sleep mode (BS-PA-MFRMS=9)", 26,
        "Table 8: The current consumption of Minimum Functionality Mode",
        conflicts=[{"source": {"name": P100["name"], "version": P100["version"],
                                "page": "27", "note": f"V1.00 reported {cfun_v1[1]} mA"}}],
        notes=f"V1.00 value: {cfun_v1[1]} mA",
        related_states=["FULL_FUNCTIONALITY", "SLEEP"])
    add(3, "Minimum Functionality",
        "Flight mode / RF off (AT+CFUN=4)", "AT+CFUN=4",
        0.92, "mA", "sleep mode (BS-PA-MFRMS=9)", 26,
        "Table 8: The current consumption of Minimum Functionality Mode",
        conflicts=[{"source": {"name": P100["name"], "version": P100["version"],
                                "page": "27", "note": f"V1.00 reported {cfun_v1[4]} mA"}}],
        notes=f"V1.00 value: {cfun_v1[4]} mA",
        related_states=["FLIGHT_MODE", "SLEEP"])

    # --- Current consumption table (V2.02 Table 49, page 60) ---
    sect = "Table 49: Current consumption (VBAT=3.8V)"
    add(4, "Power Consumption",
        "Power down mode", None,
        0.175, "mA", "Typical 150-200 uA", 60, sect,
        notes="150 uA (min) - 200 uA (max)")
    add(5, "Power Consumption",
        "Sleep mode (AT+CFUN=1, BS-PA-MFRMS=9)", "AT+CFUN=1",
        1.04, "mA", "sleep mode", 60, sect)
    add(6, "Power Consumption",
        "Sleep mode (AT+CFUN=1, BS-PA-MFRMS=5)", "AT+CFUN=1",
        1.14, "mA", "sleep mode", 60, sect)
    add(7, "Power Consumption",
        "Sleep mode (AT+CFUN=1, BS-PA-MFRMS=2)", "AT+CFUN=1",
        1.57, "mA", "sleep mode", 60, sect)
    for i, band in enumerate(["GSM850", "EGSM900", "DCS1800", "PCS1900"], start=8):
        add(i, "Power Consumption",
            f"Idle mode (AT+CFUN=1, {band})", "AT+CFUN=1",
            17.38, "mA", f"idle mode, {band}", 60, sect)
    for i, (band, v) in enumerate([("GSM850", 221.11), ("EGSM900", 238.44),
                                    ("DCS1800", 157.48), ("PCS1900", 159.22)], start=12):
        add(i, "Power Consumption",
            f"Voice call (PCL=5, {band})", None,
            v, "mA", f"voice call, {band}, PCL=5", 60, sect)
    for i, (mode_txt, band, v) in enumerate([
        ("Data mode GPRS (1Rx,4Tx)", "GSM850", 491.79),
        ("Data mode GPRS (1Rx,4Tx)", "EGSM900", 529.84),
        ("Data mode GPRS (1Rx,4Tx)", "DCS1800", 333.16),
        ("Data mode GPRS (1Rx,4Tx)", "PCS1900", 336.28),
        ("Data mode GPRS (3Rx,2Tx)", "GSM850", 359.75),
        ("Data mode GPRS (3Rx,2Tx)", "EGSM900", 385.73),
        ("Data mode GPRS (3Rx,2Tx)", "DCS1800", 250.54),
        ("Data mode GPRS (3Rx,2Tx)", "PCS1900", 251.30),
        ("Data mode GPRS (4Rx,1Tx)", "GSM850", 233.87),
        ("Data mode GPRS (4Rx,1Tx)", "EGSM900", 249.85),
        ("Data mode GPRS (4Rx,1Tx)", "DCS1800", 174.13),
        ("Data mode GPRS (4Rx,1Tx)", "PCS1900", 174.94),
    ], start=16):
        add(i, "Power Consumption",
            f"{mode_txt} ({band})", None,
            v, "mA", f"{mode_txt}, {band}", 60, sect)
    add(28, "Power Consumption",
        "Peak current (during Tx burst)", None,
        2000.0, "mA", "During Tx burst", 60, sect,
        notes="Reported as 2.0 A in PDF; converted to mA for unit consistency.")

    save(path, recs)
    return {"count": len(recs)}

# ---------- dat_14 ----------
def fix_dat_14(path):
    """
    dat_14 uses external mcc-mnc.com — no PDF pages. Set source.page='external'
    and add explanatory note. Keep status as-is (unknown/partial).
    """
    records = load(path)
    changed = 0
    for r in records:
        if not isinstance(r, dict): continue
        src = r.get("source") or {}
        if not src.get("page"):
            src["page"] = "external"
            r["source"] = src
            notes = r.get("notes") or ""
            if "external source (mcc-mnc.com)" not in notes:
                r["notes"] = (notes + "; " if notes else "") + "external source (mcc-mnc.com)"
            r["updated_at"] = NOW
            changed += 1
    if changed:
        save(path, records)
    return {"changed": changed}

# ---------- main ----------
def main():
    root = Path(sys.argv[1])
    data = root / "data"

    print("=" * 60)
    print(" FIX v5")
    print("=" * 60)

    r07 = fix_dat_07(data / "dat_07_hardware_reference.yaml")
    print(f"\n[dat_07] original={r07['original']}  kept={r07['kept']}")
    if r07["removed"]:
        print(f"  removed section-header rows:")
        for s in r07["removed"]:
            print(f"    - {s}")

    r15 = fix_dat_15(data / "dat_15_power_management.yaml")
    print(f"\n[dat_15] rebuilt with {r15['count']} records")

    r14 = fix_dat_14(data / "dat_14_operator_apn.yaml")
    print(f"\n[dat_14] source.page fixed on {r14['changed']} records")

if __name__ == "__main__":
    main()