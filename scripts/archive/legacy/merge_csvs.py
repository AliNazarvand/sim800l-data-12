#!/usr/bin/env python3
"""
merge_csvs.py — ادغام تمام CSVهای tables/ به 3 فایل TSV per-PDF.
Idempotent: اگر فایل ALL.tsv وجود دارد، دوباره ادغام نمی‌کند.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TABLES = ROOT / "sources" / "extracted" / "tables"

GROUPS = {
    "at_v1_01": "at_v1_01_ALL.tsv",
    "v2_02":    "v2_02_ALL.tsv",
    "v1_00":    "v1_00_ALL.tsv",
}

def is_meaningful_row(row):
    """ردیف معنادار: حداقل 2 سلول با محتوای ≥2 کاراکتر."""
    nonempty = [c.strip() for c in row if c and len(c.strip()) >= 2]
    return len(nonempty) >= 2

def merge_group(prefix, out_name):
    out_path = TABLES / out_name
    sources = sorted(TABLES.glob(f"{prefix}_p*_t*.csv"))
    if not sources:
        return (0, 0)
    if out_path.exists():
        # idempotent: count rows and return
        try:
            with open(out_path, encoding="utf-8") as f:
                n = sum(1 for _ in f)
        except Exception:
            n = 0
        return (0, n)
    rows_written = 0
    with open(out_path, "w", encoding="utf-8", newline="") as fout:
        w = csv.writer(fout, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        w.writerow(["page", "table_idx", "row_text"])
        for csv_path in sources:
            # نام فایل: prefix_p{page}_t{idx}.csv
            stem = csv_path.stem  # e.g. at_v1_01_p314_t2
            parts = stem.split("_")
            page = ""
            t_idx = ""
            for i, p in enumerate(parts):
                if p.startswith("p") and p[1:].isdigit():
                    page = p[1:]
                if p.startswith("t") and p[1:].isdigit():
                    t_idx = p[1:]
            try:
                with open(csv_path, encoding="utf-8", errors="ignore") as fin:
                    for row in csv.reader(fin, delimiter="\t"):
                        if not row:
                            continue
                        if not is_meaningful_row(row):
                            continue
                        row_text = " | ".join(c.strip() for c in row if c and c.strip())
                        if len(row_text) < 4:
                            continue
                        w.writerow([page, t_idx, row_text])
                        rows_written += 1
            except Exception as e:
                print(f"  err reading {csv_path.name}: {e}", file=sys.stderr)
    return (len(sources), rows_written)

def main():
    if not TABLES.exists():
        print("tables dir not found")
        return 0
    print(f"tables/ currently has {len(list(TABLES.glob('*.csv')))} CSV files")
    total_src = 0
    total_rows = 0
    summary = {}
    for prefix, out_name in GROUPS.items():
        n_src, n_rows = merge_group(prefix, out_name)
        print(f"  {prefix} -> {out_name}: src={n_src}, rows={n_rows}")
        summary[prefix] = {"src": n_src, "rows": n_rows}
        total_src += n_src
        total_rows += n_rows
    print(f"total sources: {total_src}, total rows: {total_rows}")
    import json
    (ROOT / "scripts" / "_v5_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False), encoding="utf-8")
    return 0

if __name__ == "__main__":
    sys.exit(main())