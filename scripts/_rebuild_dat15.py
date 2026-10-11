#!/usr/bin/env python3
"""Rebuild dat_15 power management:
   1. Annotate existing records by searching PDF text (V2.02 priority, then V1.00).
   2. Add new records for PDF-detected power parameters that are missing.
   Only documented data; no invented values."""
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

def find_data_file(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml"))
    if c:
        return c[0]
    p = DATA / (dat_id + ".yaml")
    return p if p.exists() else None

def load_paged(path):
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    pages = []
    parts = re.split(r"<<<PAGE\s+(\d+)>>>", text)
    for i in range(1, len(parts) - 1, 2):
        try:
            num = int(parts[i])
        except Exception:
            continue
        pages.append((num, parts[i + 1]))
    return pages

# کلیدواژه‌های قدرتمند برای power management
POWER_KEYWORDS = [
    "CSCLK", "Sleep", "sleep", "CFUN", "cfun",
    "DTR", "dtr", "Wake", "wake", "Wake-up", "wakeup",
    "Slow Clock", "slow clock", "RTC", "Deep Sleep", "deep sleep",
    "Power Consumption", "consumption", "mA", "uA",
    "RF off", "Minimum Functionality",
    "AT+CSCLK", "AT+CFUN",
    "Charge", "charger", "charging",
]

def find_occurrence(term, pages):
    if not term:
        return None
    pat = re.compile(r"\b" + re.escape(str(term).strip()) + r"\b", re.IGNORECASE)
    for page_no, body in pages:
        for line in body.splitlines():
            s = line.strip()
            if len(s) < 4:
                continue
            if pat.search(s):
                if any(k.lower() in s.lower() for k in ["power","sleep","cscLK","cfun","dtr","wake","rtc",
                                                          "clock","consumption","ma","ua","charge",
                                                          "mode","rf"]):
                    return (page_no, s)
    return None

def guess_section(line):
    l = line.lower()
    if "cscLK" in l or "sleep" in l: return "Sleep Mode"
    if "cfun" in l: return "CFUN"
    if "dtr" in l: return "DTR/Wake-up"
    if "rtc" in l or "slow clock" in l: return "Slow Clock / RTC"
    if "consumption" in l or " ma" in l or "ua" in l: return "Power Consumption"
    if "charge" in l: return "Charging"
    return "Power Management"

def main():
    dat15_path = find_data_file("dat_15")
    if dat15_path is None:
        print("dat_15 not found"); sys.exit(1)
    records = yaml.safe_load(dat15_path.read_text(encoding="utf-8")) or []
    if not isinstance(records, list):
        records = [records]

    v202 = load_paged(SRC_EX / "v2_02_paged.txt")
    v100 = load_paged(SRC_EX / "v1_00_paged.txt")
    print(f"V2.02 pages: {len(v202)}, V1.00 pages: {len(v100)}")

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    updated = 0
    unresolved = 0
    unresolved_ids = []

    existing_ids = set()
    for rec in records:
        if isinstance(rec, dict) and rec.get("id"):
            existing_ids.add(rec["id"])

    # --- annotate existing ---
    for rec in records:
        if not isinstance(rec, dict):
            continue
        # جستجو بر اساس parameter یا command یا mode
        search_terms = []
        for k in ("parameter", "command", "mode", "category"):
            v = rec.get(k)
            if v and isinstance(v, str):
                search_terms.append(v)
        hit = None
        version_used = "V2.02"
        for t in search_terms:
            hit = find_occurrence(t, v202)
            if hit:
                break
        if hit is None:
            for t in search_terms:
                hit = find_occurrence(t, v100)
                if hit:
                    version_used = "V1.00"
                    break
        if hit is None:
            unresolved += 1
            unresolved_ids.append(rec.get("id", "?"))
            continue
        page_no, line = hit
        src = rec.get("source") or {}
        if not isinstance(src, dict):
            src = {}
        if not src.get("page"):
            src["page"] = str(page_no)
        if not src.get("section"):
            src["section"] = guess_section(line)
        if not src.get("quote"):
            src["quote"] = line.strip()[:300]
        if not src.get("name"):
            src["name"] = ("SIM800H&SIM800L_Hardware_Design"
                           if version_used == "V2.02"
                           else "SIM800L_Hardware_Design")
        if not src.get("version"):
            src["version"] = version_used
        if not src.get("date"):
            src["date"] = "2015-07-27" if version_used == "V2.02" else "2013-08-20"
        rec["source"] = src
        if rec.get("status") == "unknown":
            rec["status"] = "partial"
        if rec.get("confidence") in (0.0, 0) and src.get("page") and src.get("quote"):
            rec["confidence"] = 0.5
        rec["updated_at"] = ts
        updated += 1

    # --- add new records for PDF-detected power params ---
    # Scanne V2.02 برای خطوطی که کلیدواژه power دارند و در هیچ id موجود نیستند
    added = 0
    new_ids = []
    seen_quotes = set()
    for rec in records:
        if isinstance(rec, dict):
            s = rec.get("source") or {}
            q = s.get("quote") if isinstance(s, dict) else None
            if q:
                seen_quotes.add(q.strip())

    counter = 9000  # شماره‌گذاری جدید برای جلوگیری از تعارض
    candidate_lines = []
    for page_no, body in v202:
        for line in body.splitlines():
            s = line.strip()
            if len(s) < 8 or len(s) > 200:
                continue
            # فقط خطوطی که کلیدواژه power دارند
            if not any(k.lower() in s.lower() for k in POWER_KEYWORDS):
                continue
            if s in seen_quotes:
                continue
            candidate_lines.append((page_no, s))
    # حذف تکراری‌ها
    uniq = []
    for pn, s in candidate_lines:
        if s not in [x[1] for x in uniq]:
            uniq.append((pn, s))

    for pn, s in uniq:
        counter += 1
        new_id = "dat_15_" + str(counter).zfill(4)
        while new_id in existing_ids:
            counter += 1
            new_id = "dat_15_" + str(counter).zfill(4)
        new_rec = {
            "id": new_id,
            "category": guess_section(s),
            "mode": None,
            "command": None,
            "parameter": s[:120],
            "value_min": None,
            "value_typ": None,
            "value_max": None,
            "unit": None,
            "condition": None,
            "wake_source": None,
            "related_commands": [],
            "related_states": [],
            "source": {
                "name": "SIM800H&SIM800L_Hardware_Design",
                "version": "V2.02",
                "date": "2015-07-27",
                "page": str(pn),
                "section": guess_section(s),
                "quote": s[:300],
            },
            "source_type": "primary",
            "confidence": 0.4,
            "status": "partial",
            "conflicts": [],
            "notes": "Auto-detected power-related line from V2.02; values need manual verification.",
            "applicable_models": ["SIM800L"],
            "tags": ["power", "auto-detected"],
            "created_at": ts,
            "updated_at": ts,
        }
        records.append(new_rec)
        existing_ids.add(new_id)
        new_ids.append(new_id)
        added += 1

    with dat15_path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False,
                       default_flow_style=False, width=1000)

    report = {
        "file": dat15_path.name,
        "total": len(records),
        "updated": updated,
        "added": added,
        "unresolved": unresolved,
        "unresolved_ids": unresolved_ids[:100],
        "new_ids": new_ids[:200],
        "v202_pages": len(v202),
        "v100_pages": len(v100),
    }
    (REPORTS / "_step_A2_dat15_rebuild.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"dat_15: total={len(records)} updated={updated} added={added} unresolved={unresolved}")

if __name__ == "__main__":
    main()