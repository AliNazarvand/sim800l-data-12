"""
v2: reads sources/extracted/tables/*/_raw/*.csv, produces real records for
dat_04 (timing), dat_07 (hardware), dat_15 (power).

Fixes vs v1:
  - much broader header classification (substring + regex fallback)
  - verbose per-CSV decision log to reports/_csv_classification.json
  - dat_07 dedup: prefer V2.02 over V1.00, record V1.00 in conflicts (R7, R20)
  - renumber IDs after dedup to keep them unique
"""
import sys, csv, re, json, datetime
from pathlib import Path
import yaml

NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def norm(s):
    if s is None: return ""
    return re.sub(r"\s+", " ", str(s).strip().lower())

# ---------- header classification ----------
PIN_NUM_HINTS   = ("pin", "ball", "pad", "terminal", "no.", "number", "#")
PIN_NAME_HINTS  = ("name", "signal", "symbol")
PIN_DESC_HINTS  = ("description", "function", "comment", "remarks", "note", "application")
PIN_IO_HINTS    = ("i/o", "io", "direction", "type")

CURRENT_HINTS   = ("current", "consumption", "icc", "power", "ma)", "(ma")
TIMING_RANGE_RE = re.compile(r"\b(min|max|typ|typical|minimum|maximum)\b")

def header_has_any(headers, hints):
    hs = [norm(h) for h in headers if h]
    for h in hs:
        for t in hints:
            if t in h:
                return True
    return False

def pick_col(headers, hints):
    hs = [norm(h) for h in headers if h]
    for i, h in enumerate(hs):
        for t in hints:
            if t in h:
                return i
    return None

def classify(headers):
    hs = [norm(h) for h in headers if h]
    if not hs: return "empty"
    has_pin = header_has_any(headers, PIN_NUM_HINTS)
    has_name = header_has_any(headers, PIN_NAME_HINTS)
    if has_pin and has_name:
        return "pin"
    if header_has_any(headers, CURRENT_HINTS):
        return "power"
    if any(TIMING_RANGE_RE.search(h) for h in hs):
        return "timing"
    return "unknown"

# ---------- CSV reader ----------
def parse_csv(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
            rows = [r for r in csv.reader(f) if any(c.strip() for c in r)]
    except Exception:
        return [], []
    if not rows: return [], []
    headers = rows[0]
    data = []
    for r in rows[1:]:
        if len(r) < len(headers):
            r = r + [""] * (len(headers) - len(r))
        data.append(dict(zip(headers, r)))
    return headers, data

def page_from_name(name):
    m = re.search(r"_p(\d+)", name)
    return int(m.group(1)) if m else None

def version_from_path(path):
    s = str(path).lower()
    if "hw_v2_02" in s: return "V2.02", "2015-07-27", "SIM800H&SIM800L_Hardware_Design"
    if "hw_v1_00" in s: return "V1.00", "2013-08-20", "SIM800L_Hardware_Design"
    return "unknown", "unknown", "unknown"

def make_common(ds_prefix, idx, src_name, src_version, src_date, page):
    return {
        "id": f"{ds_prefix}_{idx:04d}",
        "source": {"name": src_name, "version": src_version, "date": src_date,
                   "page": str(page) if page else "", "section": "", "quote": ""},
        "source_type": "primary",
        "confidence": 0.9,
        "status": "complete",
        "conflicts": [],
        "notes": "",
        "tags": ["auto-extracted", src_version],
        "applicable_models": ["SIM800L"],
        "created_at": NOW,
        "updated_at": NOW,
    }

def tofloat(x):
    if x is None: return None
    s = str(x).strip()
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    if not m: return None
    try: return float(m.group(0))
    except (TypeError, ValueError): return None

# ---------- emitters (return list of records without final IDs) ----------
def build_dat07(headers, rows, csvpath):
    out = []
    pin_col  = pick_col(headers, PIN_NUM_HINTS)
    name_col = pick_col(headers, PIN_NAME_HINTS)
    desc_col = pick_col(headers, PIN_DESC_HINTS)
    io_col   = pick_col(headers, PIN_IO_HINTS)
    if pin_col is None and name_col is None: return out
    version, date, name = version_from_path(csvpath)
    page = page_from_name(csvpath.name)
    for r in rows:
        vals = list(r.values())
        pin  = vals[pin_col].strip()  if pin_col  is not None and pin_col  < len(vals) else ""
        sig  = vals[name_col].strip() if name_col is not None and name_col < len(vals) else ""
        if not pin and not sig: continue
        out.append({
            "_version": version, "_name": name, "_date": date, "_page": page,
            "category": "Hardware",
            "name": sig or f"PIN_{pin}",
            "pin_number": pin,
            "direction": (vals[io_col].strip() if io_col is not None and io_col < len(vals) else ""),
            "voltage_min": None, "voltage_typ": None, "voltage_max": None,
            "current_typ": None, "current_max": None,
            "function": (vals[desc_col].strip() if desc_col is not None and desc_col < len(vals) else ""),
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
    for r in rows:
        vals = list(r.values())
        param = vals[param_col].strip() if param_col is not None and param_col < len(vals) else ""
        if not param: continue
        out.append({
            "_version": version, "_name": name, "_date": date, "_page": page,
            "category": "Timing",
            "parameter": param,
            "min": tofloat(vals[min_col]) if min_col is not None and min_col < len(vals) else None,
            "typ": tofloat(vals[typ_col]) if typ_col is not None and typ_col < len(vals) else None,
            "max": tofloat(vals[max_col]) if max_col is not None and max_col < len(vals) else None,
            "unit": (vals[unit_col].strip() if unit_col is not None and unit_col < len(vals) else ""),
            "condition": "",
            "related_command": None, "related_state": None, "related_urc": None,
        })
    return out

def build_dat15(headers, rows, csvpath):
    out = []
    mode_col = pick_col(headers, ("mode", "state", "parameter", "item", "condition", "operation", "scenario"))
    curr_col = pick_col(headers, ("current", "consumption", "icc"))
    version, date, name = version_from_path(csvpath)
    page = page_from_name(csvpath.name)
    for r in rows:
        vals = list(r.values())
        mode = vals[mode_col].strip() if mode_col is not None and mode_col < len(vals) else ""
        if not mode: continue
        curr_raw = vals[curr_col] if curr_col is not None and curr_col < len(vals) else ""
        v = tofloat(curr_raw)
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

# ---------- dedup dat_07 (prefer V2.02 over V1.00) ----------
def dedup_dat07(records):
    by_key = {}
    for r in records:
        key = (norm(r.get("pin_number", "")), norm(r.get("name", "")))
        if key == ("", ""): continue
        v = r.get("_version", "")
        if key not in by_key:
            by_key[key] = r
            continue
        existing = by_key[key]
        ev = existing.get("_version", "")
        if v == "V2.02" and ev == "V1.00":
            r.setdefault("conflicts", []).append({
                "source": {"name": existing.get("_name"), "version": ev,
                           "page": existing.get("_page"),
                           "note": "V1.00 superseded by V2.02"}
            })
            by_key[key] = r
        elif v == "V1.00" and ev == "V2.02":
            existing.setdefault("conflicts", []).append({
                "source": {"name": r.get("_name"), "version": v,
                           "page": r.get("_page"),
                           "note": "V1.00 variant"}
            })
        # same version duplicate: keep first
    return list(by_key.values())

# ---------- finalize: assign IDs and strip internal fields ----------
def finalize(records, prefix):
    out = []
    for i, r in enumerate(records, 1):
        r2 = dict(r)
        r2["id"] = f"{prefix}_{i:04d}"
        r2["source"] = {"name": r2.pop("_name"), "version": r2.pop("_version"),
                        "date": r2.pop("_date"), "page": str(r2.pop("_page") or ""),
                        "section": "", "quote": ""}
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
    stats = {"pin": 0, "timing": 0, "power": 0, "unknown": 0, "empty": 0, "skipped": 0}

    for c in csvs:
        headers, rows = parse_csv(c)
        cls = classify(headers)
        entry = {"csv": c.name, "classification": cls, "rows": len(rows),
                 "headers": headers[:8]}
        if cls == "pin":
            stats["pin"] += 1
            dat07_raw.extend(build_dat07(headers, rows, c))
            entry["emitted_to"] = "dat_07"
        elif cls == "timing":
            stats["timing"] += 1
            dat04_raw.extend(build_dat04(headers, rows, c))
            entry["emitted_to"] = "dat_04"
        elif cls == "power":
            stats["power"] += 1
            dat15_raw.extend(build_dat15(headers, rows, c))
            entry["emitted_to"] = "dat_15"
        elif cls == "empty":
            stats["empty"] += 1; entry["emitted_to"] = None
        else:
            stats["unknown"] += 1; entry["emitted_to"] = None
        log.append(entry)

    # dedup
    deduped07 = dedup_dat07(dat07_raw)

    final07 = finalize(deduped07, "dat_07")
    final04 = finalize(dat04_raw, "dat_04")
    final15 = finalize(dat15_raw, "dat_15")

    data_dir = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    def dump(path, records):
        with open(path, "w", encoding="utf-8") as f:
            if not records:
                f.write("[]\n")
            else:
                yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False)

    dump(data_dir / "dat_07_hardware_reference.yaml", final07)
    dump(data_dir / "dat_04_timing_timeout.yaml", final04)
    dump(data_dir / "dat_15_power_management.yaml", final15)

    summary = {
        "csv_files_scanned": len(csvs),
        "classification": stats,
        "dat_07_raw": len(dat07_raw),
        "dat_07_after_dedup": len(final07),
        "dat_07_dedup_removed": len(dat07_raw) - len(final07),
        "dat_04_records": len(final04),
        "dat_15_records": len(final15),
    }
    (root / "reports" / "_hw_extraction_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8")
    (root / "reports" / "_csv_classification.json").write_text(
        json.dumps(log, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()