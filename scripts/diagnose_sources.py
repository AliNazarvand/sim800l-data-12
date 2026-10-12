#!/usr/bin/env python3
"""Diagnostic: inspect source file formats before designing extraction logic.

Does NOT extract or modify anything. Only prints samples.

Usage:
    python scripts/diagnose_sources.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXTRACTED = ROOT / "sources" / "extracted"


def show_json(path: Path):
    print(f"\n=== {path.name} ===")
    if not path.exists():
        print("  [MISSING]"); return
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        print(f"  [ERROR] {exc}"); return
    print(f"  size: {len(raw)} bytes")
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict):
            keys = list(obj.keys())[:10]
            print(f"  dict with {len(obj)} keys; sample: {keys}")
            for k in keys[:3]:
                v = obj[k]
                print(f"    '{k}' -> {type(v).__name__}: {repr(v)[:120]}")
        elif isinstance(obj, list):
            print(f"  list with {len(obj)} items")
            for item in obj[:3]:
                print(f"    -> {type(item).__name__}: {repr(item)[:120]}")
    except Exception as exc:
        print(f"  [not JSON] {exc}")
        print(f"  first 500: {raw[:500]!r}")


def show_text(path: Path, n: int = 80):
    print(f"\n=== {path.name} ===")
    if not path.exists():
        print("  [MISSING]"); return
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception as exc:
        print(f"  [ERROR] {exc}"); return
    print(f"  total lines: {len(lines)}")
    for i, ln in enumerate(lines[:n], 1):
        print(f"  {i:4d} | {ln[:140]}")


def show_yaml(path: Path, n: int = 30):
    print(f"\n=== {path.name} ===")
    if not path.exists():
        print("  [MISSING]"); return
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception as exc:
        print(f"  [ERROR] {exc}"); return
    print(f"  total lines: {len(lines)}")
    for i, ln in enumerate(lines[:n], 1):
        print(f"  {i:4d} | {ln[:140]}")


def main():
    print("=== SOURCE DIAGNOSTIC ===")
    print(f"ROOT: {ROOT}")

    show_json(EXTRACTED / "_at_commands_index.json")
    show_text(EXTRACTED / "hw_v2_02_full.txt", 80)
    show_text(EXTRACTED / "hw_v1_00_full.txt", 40)
    show_yaml(ROOT / "data" / "dat_02_urc.yaml", 30)

    print("\n=== Suggested next steps ===")
    print("1. Review the formats shown above.")
    print("2. Reuse existing scripts if compatible:")
    print("   - scripts/_rebuild_B1_dat01.py")
    print("   - scripts/_rebuild_dat07.py")
    print("   - scripts/extract_at_commands.py")
    print("   - scripts/extract_dat_07.py")
    print("3. Write new extraction only if existing scripts are broken.")
    return 0


if __name__ == "__main__":
    sys.exit(main())