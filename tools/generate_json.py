#!/usr/bin/env python3
"""
Generate JSON from YAML files under data/**.

Emits strictly valid JSON (no // or # comments, which JSON forbids).
Because the project brief asks for a "AUTO-GENERATED — DO NOT EDIT" header
on every generated file, and JSON has no comment syntax, the marker is
carried inside the JSON as a reserved top-level key:

    {
      "_auto_generated": {
        "marker": "AUTO-GENERATED — DO NOT EDIT",
        "generator": "tools/generate_json.py"
      },
      ...payload...
    }

The file remains parseable by any standard JSON library. This decision is
documented in docs/validation_guide.md.

For every data/**/*.yaml - including _dataset_meta.yaml - a sibling .json
file is written. JSON files are auto-generated and must never be edited by
hand.

Use --check to verify in-sync state without writing.

Exit codes:
    0 - success / in-sync
    1 - drift (--check) or I/O error
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except Exception as exc:  # pragma: no cover
    print(f"ERROR: missing dependency: {exc}", file=sys.stderr)
    print("Install with: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

MARKER = "AUTO-GENERATED — DO NOT EDIT"

def dump_json(obj) -> str:
    if not (isinstance(obj, dict) and "_auto_generated" in obj):
        obj = {
            "_auto_generated": {
                "marker": MARKER,
                "generator": "tools/generate_json.py",
            },
            **({} if not isinstance(obj, dict) else obj),
        }
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"

def process(path: Path, check: bool) -> int:
    with path.open("r", encoding="utf-8") as fh:
        obj = yaml.safe_load(fh)
    if obj is None:
        obj = {}
    target = path.with_suffix(".json")
    new_text = dump_json(obj)
    if check:
        if not target.exists():
            print(f"DRIFT: missing {target}", file=sys.stderr)
            return 1
        if target.read_text(encoding="utf-8") != new_text:
            print(f"DRIFT: {target} differs from {path.name}", file=sys.stderr)
            return 1
        return 0
    target.write_text(new_text, encoding="utf-8")
    print(f"wrote {target.relative_to(ROOT)}")
    return 0

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if not DATA.exists():
        print(f"ERROR: data/ not found under {ROOT}", file=sys.stderr)
        return 1

    rc = 0
    found_any = False
    for p in sorted(DATA.rglob("*.yaml")):
        found_any = True
        try:
            r = process(p, args.check)
        except Exception as exc:
            print(f"ERROR processing {p}: {exc}", file=sys.stderr)
            r = 1
        if r != 0:
            rc = r

    if args.check and rc == 0:
        print("OK: JSON files are in sync with their YAML sources."
              if found_any else "OK: no data YAMLs to check.")
    return rc

if __name__ == "__main__":
    sys.exit(main())