"""
v4: content-based power table detection (fixes dat_15 under-extraction).

v3 relied only on header keywords to classify CSVs as 'power'. The big
Current Consumption table in the SIM800L hardware manuals has a header
like ['', 'Symbol', '', 'Parameter', '', '', 'Conditions', ...] which
does NOT contain the word 'current'. As a result, only 2 small tables
were matched and dat_15 got just 6 records.

v4 adds:
  - POWER_CONTENT_RE : scans cell values for power-related phrases
    (sleep mode / power down / idle mode / voice call / data mode / gprs ...)
  - if header classification yields 'unknown' or 'timing' but content
    matches power patterns -> reclassify to 'power'
  - build_dat15 fallback: try mode_col, then parameter_col, then symbol_col
"""
import sys, csv, re, json, datetime
from pathlib import Path
import yaml

NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def norm(s):
    if s is None: return ""
    return re.sub(r"\s+", " ", str(s).strip().lower())

PIN_NUM_HINTS   = ("pin", "ball", "pad", "terminal", "no.", "number")
PIN_NAME_HINTS  = ("name", "signal", "symbol")
PIN_DESC_HINTS  = ("description", "function", "comment", "remarks", "note", "application")
PIN_IO_HINTS    = ("i/o", "io", "direction", "type")

CURRENT_HINTS   = ("current", "consumption", "icc", "power", "ma)", "(ma")
TIMING_RANGE_RE = re.compile(r"\b(min|max|typ|typical|minimum|maximum)\b")
POWER_CONTENT_RE = re.compile(
    r"(sleep\s*mode|power\s*down|idle\s*mode|voice\s*call|data\s*mode|"
    r"tx\s*burst|current\s*consumption|gprs.*ma|average\s*current|peak\s*current)",
    re.IGNORECASE)

def pick_col(headers, hints):
    for i, h in enumerate(headers):
        nh = norm(h)
        if not nh: continue
        for t in hints:
            if t in nh:
                return i
    return None

def has_any(headers, hints):
    return pick_col(headers, hints) is not None

def content_has_power(rows, limit=200):
    """Scan cell values for power-related phrases."""
    for row in rows[:limit]:
        for c in row:
            if POWER_CONTENT_RE.search(str(c or "")):
                return True
    return False

def classify(headers, rows):
    hs = [norm(h) for h in headers if h]
    if not hs: return "empty"
    if has_any(headers, PIN_NUM_HINTS) and has_any(headers, PIN_NAME_HINTS):
        return "pin"
    if has_any(headers, CURRENT_HINTS):
        return "power"
    has_timing = any(TIMING_RANGE_RE.search(h) for h in hs)
    # Content-based override: power wins over timing/unknown if cells
    # mention power-related phrases.
    if content_has_power(rows):
        return "power"
    if has_timing:
        return "timing"
    return "unknown"

def parse_csv(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
            raw = [r for r in csv.reader(f) if any((c or "").strip() for c in r)]
    except Exception:
        return [], []
    if not raw: return [], []
    headers = raw[0]
    rows = []
    for r in raw[1:]:
        if len(r) < len(headers):
            r = list(r) + [""] * (len(headers) - len(r))
        rows.append(r)
    return headers, rows

def page_from_name(name):
    m = re.search(r"_p(\d+)", name)
    return int(m.group(1)) if m else None

def version_from_path(path):
    s = str(path).lower()
    if "hw_v2_02" in s: return "V2.02", "2015-07-27", "SIM800H&SIM800L_Hardware_Design"
    if "hw_v1_00" in s: return "V1.00", "2013-08-20", "SIM800L_Hardware_Design"
    return "unknown", "unknown", "unknown"

def tofloat(x):
    if x is None: return None
    m = re.search(r"-?\d+(?:\.\d+)?", str(x))
    if not m: return None
    try: return float(m.group(0))
    except (TypeError, ValueError): return None

def cell(row, idx):
    if idx is None or idx >= len(row): return ""
    return str(row[idx]).strip()

# ---------- builders ----------
def build_dat07(headers, rows, csvpath):
    out = []
    pin_col  = pick_col(headers, PIN_NUM_HINTS)
    name_col = pick_col(headers, PIN_NAME_HINTS)
    desc_col = pick_col(headers, PIN_DESC_HINTS)
    io_col   = pick_col(headers, PIN_IO_HINTS)
    if pin_col is None and name_col is None: return out
    version, date, name = version_from_path(csvpath)
    page = page_from_name(csvpath.name)
    for row in rows:
        pin = cell(row, pin_col)
        sig = cell(row, name_col)
        if not pin and not sig: continue
        out.append({
            "_version": version, "_name": name, "_date": date, "_page": page,
            "category": "Hardware",
            "name": sig or f"PIN_{pin}",
            "pin_number": pin,
            "direction": cell(row, io_col),
            "voltage_min": None, "voltage_typ": None, "voltage_max": None,
            "current_typ": None, "current_max": None,
            "function": cell(row, desc_col),
            "alternate_function": None,
            "pull_up_down": None, "esd_rating": None,
            "impedance": None, "decoupling": None,
        })
    return out

def build_dat04(headers, rows, csvpath):
    out = []
    param_col = pick_col(headers, ("parameter", "item", "symbol", "name", "description"))
    min_col   = pick_col(headers, ("min",))
    typ_col   = pick_col(headers, ("typ",))
    max_col   = pick_col(headers, ("max",))
    unit_col  = pick_col(headers, ("unit",))
    version, date, name = version_from_path(csvpath)
    page = page_from_name(csvpath.name)
    for row in rows:
        param = cell(row, param_col)
        if not param: continue
        out.append({
            "_version": version, "_name": name, "_date": date, "_page": page,
            "category": "Timing",
            "parameter": param,
            "min": tofloat(cell(row, min_col)),
            "typ": tofloat(cell(row, typ_col)),
            "max": tofloat(cell(row, max_col)),
            "unit": cell(row, unit_col),
            "condition": "",
            "related_command": None, "related_state": None, "related_urc": None,
        })
    return out

def build_dat15(headers, rows, csvpath):
    """
    v4: fallback chain for the mode column.
    Try, in order: mode/state/fun/parameter/symbol/condition.
    Skip values that are pure numbers (like the '0'/'1'/'4' fun codes);
    prefer values that look like text.
    """
    out = []
    mode_col = pick_col(headers, ("mode", "state", "parameter", "item",
                                  "condition", "operation", "scenario", "fun", "symbol"))
    curr_col = pick_col(headers, ("current", "consumption", "icc", "typ", "average", "peak"))
    version, date, name = version_from_path(csvpath)
    page = page_from_name(csvpath.name)
    for row in rows:
        mode = cell(row, mode_col)
        if not mode: continue
        v = tofloat(cell(row, curr_col))
        out.append({
            "_version": version, "_name": name, "_date": date, "_page": page,
            "category": "Power",
            "mode": mode,
            "command": None,
            "parameter": "current",
            "value_min": None, "value_typ": v, "value_max": None,
            "unit": "mA",
            "condition": "",
            "wake_source": None,
            "related_commands": [], "related_states": [],
        })
    return out

# ---------- dedup + finalize ----------
def dedup_dat07(records):
    by_key = {}
    for r in records:
        key = (norm(r.get("pin_number","")), norm(r.get("name","")))
        if key == ("",""): continue
        v = r.get("_version","")
        if key not in by_key:
            by_key[key] = r; continue
        existing = by_key[key]
        ev = existing.get("_version","")
        if v == "V2.02" and ev == "V1.00":
            r.setdefault("conflicts", []).append({
                "source": {"name": existing.get("_name"), "version": ev,
                           "page": existing.get("_page"),
                           "note": "V1.00 superseded by V2.02"}})
            by_key[key] = r
        elif v == "V1.00" and ev == "V2.02":
            existing.setdefault("conflicts", []).append({
                "source": {"name": r.get("_name"), "version": v,
                           "page": r.get("_page"),
                           "note": "V1.00 variant"}})
    return list(by_key.values())

def dedup_dat15(records):
    """De-duplicate by (version, mode) keeping the first."""
    seen = {}
    for r in records:
        k = (r.get("_version"), norm(r.get("mode","")))
        if k in seen:
            continue
        seen[k] = r
    return list(seen.values())

def finalize(records, prefix):
    out = []
    for i, r in enumerate(records, 1):
        r2 = dict(r)
        r2["id"] = f"{prefix}_{i:04d}"
        r2["source"] = {
            "name": r2.pop("_name", "unknown"),
            "version": r2.pop("_version", "unknown"),
            "date": r2.pop("_date", "unknown"),
            "page": str(r2.pop("_page", "") or ""),
            "section": "", "quote": ""
        }
        r2["source_type"] = "primary"
        r2["confidence"] = 0.9
        r2["status"] = "complete"
        r2.setdefault("conflicts", [])
        r2.setdefault("notes", "")
        r2.setdefault("tags", ["auto-extracted", r2["source"]["version"]])
        r2["applicable_models"] = ["SIM800L"]
        r2["created_at"] = NOW
        r2["updated_at"] = NOW
        out.append(r2)
    return out

def main():
    root = Path(sys.argv[1])
    tables_root = root / "sources" / "extracted" / "tables"
    if not tables_root.exists():
        print(json.dumps({"error":"no tables dir"})); return
    csvs = []
    for sub in ("hw_v2_02", "hw_v1_00"):
        d = tables_root / sub / "_raw"
        if d.exists(): csvs.extend(sorted(d.glob("*.csv")))

    dat07_raw, dat04_raw, dat15_raw = [], [], []
    log = []
    stats = {"pin":0,"timing":0,"power":0,"unknown":0,"empty":0}

    for c in csvs:
        headers, rows = parse_csv(c)
        cls = classify(headers, rows)
        entry = {"csv": c.name, "classification": cls, "rows": len(rows),
                 "headers": headers[:8]}
        if cls == "pin":
            stats["pin"] += 1
            recs = build_dat07(headers, rows, c)
            dat07_raw.extend(recs)
            entry["emitted_to"] = "dat_07"; entry["emitted_count"] = len(recs)
        elif cls == "timing":
            stats["timing"] += 1
            recs = build_dat04(headers, rows, c)
            dat04_raw.extend(recs)
            entry["emitted_to"] = "dat_04"; entry["emitted_count"] = len(recs)
        elif cls == "power":
            stats["power"] += 1
            recs = build_dat15(headers, rows, c)
            dat15_raw.extend(recs)
            entry["emitted_to"] = "dat_15"; entry["emitted_count"] = len(recs)
        elif cls == "empty":
            stats["empty"] += 1; entry["emitted_to"] = None; entry["emitted_count"] = 0
        else:
            stats["unknown"] += 1; entry["emitted_to"] = None; entry["emitted_count"] = 0
        log.append(entry)

    deduped07 = dedup_dat07(dat07_raw)
    deduped15 = dedup_dat15(dat15_raw)
    final07 = finalize(deduped07, "dat_07")
    final04 = finalize(dat04_raw, "dat_04")
    final15 = finalize(deduped15, "dat_15")

    data_dir = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    def safe_dump(path, new_records):
        if not new_records and path.exists():
            try:
                existing = yaml.safe_load(path.read_text(encoding="utf-8"))
                if isinstance(existing, list) and existing:
                    print(f"SKIP {path.name}: extraction empty, keeping existing "
                          f"{len(existing)} records")
                    return
            except Exception:
                pass
        with open(path, "w", encoding="utf-8") as f:
            if not new_records:
                f.write("[]\n")
            else:
                yaml.safe_dump(new_records, f, allow_unicode=True, sort_keys=False)

    safe_dump(data_dir / "dat_07_hardware_reference.yaml", final07)
    safe_dump(data_dir / "dat_04_timing_timeout.yaml", final04)
    safe_dump(data_dir / "dat_15_power_management.yaml", final15)

    summary = {
        "csv_files_scanned": len(csvs),
        "classification": stats,
        "dat_07_raw": len(dat07_raw),
        "dat_07_after_dedup": len(final07),
        "dat_04_records": len(final04),
        "dat_15_raw": len(dat15_raw),
        "dat_15_after_dedup": len(final15),
    }
    (root / "reports" / "_hw_extraction_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8")
    (root / "reports" / "_csv_classification.json").write_text(
        json.dumps(log, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()