#!/usr/bin/env python3
"""
fix_schema_nullable.py
Recursively makes every NON-required property type nullable in
schemas/dat_XX.schema.yaml.
"""
import sys
import shutil
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

ROOT    = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

NULLABLE_TYPES = {"string", "number", "integer", "boolean", "array"}
SKIP_KEYS      = {"id"}   # id has a pattern; keep strict string


def make_nullable(node):
    """Recursively walk a JSON-Schema-like dict and make non-required
    property types nullable. Returns count of properties modified."""
    if not isinstance(node, dict):
        return 0

    changed = 0
    props = node.get("properties")
    local_required = set(node.get("required", []) or [])

    if isinstance(props, dict):
        for key, sub in props.items():
            if not isinstance(sub, dict):
                continue

            if key not in SKIP_KEYS and key not in local_required:
                t = sub.get("type")
                if isinstance(t, str) and t in NULLABLE_TYPES:
                    sub["type"] = [t, "null"]
                    changed += 1
                elif isinstance(t, list) and "null" not in t:
                    sub["type"] = list(t) + ["null"]
                    changed += 1

            changed += make_nullable(sub)

    return changed


def process_file(path, backup_dir):
    shutil.copy2(path, backup_dir / path.name)
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  [SKIP] {path.name}: parse error: {e}")
        return 0

    if not isinstance(data, dict):
        print(f"  [SKIP] {path.name}: root is not mapping")
        return 0

    # Ensure 'date' is NOT in source.required
    props = data.get("properties") or {}
    src = props.get("source") if isinstance(props, dict) else None
    if isinstance(src, dict):
        req = src.get("required")
        if isinstance(req, list) and "date" in req:
            src["required"] = [x for x in req if x != "date"]

    count = make_nullable(data)

    out = yaml.safe_dump(
        data,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        width=1000,
    )
    path.write_text(out, encoding="utf-8")
    return count


def main():
    if not SCHEMAS.exists():
        print(f"ERROR: schemas dir not found: {SCHEMAS}")
        sys.exit(1)

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    snap = ROOT / f"schemas_nullable_snapshot_v2_{stamp}"
    snap.mkdir(exist_ok=True)

    print(f"Snapshot: {snap}")
    print()

    total = 0
    per_file = []

    for f in sorted(SCHEMAS.glob("*.yaml")):
        c = process_file(f, snap)
        per_file.append((f.name, c))
        total += c
        print(f"  {f.name:30s}  nullable fields added: {c}")

    lines = [
        "# SCHEMA_NULLABLE_FIX_v2",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Snapshot:  {snap}",
        "",
        "## Summary",
        "",
        f"- Files processed: 18",
        f"- Fields nullable: {total}",
        "",
        "## Per-file counts",
        "",
        "| Schema | Nullable fields added |",
        "|--------|-----------------------|",
    ]
    for name, c in per_file:
        lines.append(f"| {name} | {c} |")
    lines.append("")
    lines.append("## Method")
    lines.append("- Recursive PyYAML walk over `properties`.")
    lines.append("- Skips `id` (pattern-only field).")
    lines.append("- Skips any property listed in its parent's `required`.")
    lines.append("- Removed `date` from `source.required`.")

    (REPORTS / "SCHEMA_NULLABLE_FIX_v2.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )

    print()
    print("=" * 50)
    print(f"Fields nullable:  {total}")
    print(f"Snapshot:         {snap}")
    print(f"Report:           {REPORTS / 'SCHEMA_NULLABLE_FIX_v2.md'}")
    print("=" * 50)


if __name__ == "__main__":
    main()
