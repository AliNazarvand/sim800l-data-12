#!/usr/bin/env python3
"""Diagnostic: inspect source file formats before writing extraction logic.

This script does NOT extract or modify anything. It only prints samples
so the operator can design correct extraction logic.

Usage:
    python scripts/diagnose_sources.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXTRACTED = ROOT / "sources" / "extracted"


def show_json_head(path: Path, n_lines: int = 50):
    print(f"\n=== {path.name} ===")
    if not path.exists():
        print("  [MISSING]")
        return
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        print(f"  [ERROR] {exc}")
        return
    print(f"  size: {len(raw)} bytes")
    # Try to parse and show structure
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict):
            keys = list(obj.keys())[:10]
            print(f"  top-level: dict with {len(obj)} keys")
            print(f"  sample keys: {keys}")
            for k in keys[:3]:
                v = obj[k]
                print(f"    '{k}' -> {type(v).__name__}: {repr(v)[:120]}")
        elif isinstance(obj, list):
            print(f"  top-level: list with {len(obj)} items")
            for item in obj[:3]:
                print(f"    -> {type(item).__name__}: {repr(item)[:120]}")
    except Exception as exc:
        print(f"  [not valid JSON] {exc}")
        print(f"  first 500 chars: {raw[:500]!r}")


def show_text_head(path: Path, n_lines: int = 60):
    print(f"\n=== {path.name} ===")
    if not path.exists():
        print("  [MISSING]")
        return
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception as exc:
        print(f"  [ERROR] {exc}")
        return
    print(f"  total lines: {len(lines)}")
    for i, ln in enumerate(lines[:n_lines], 1):
        print(f"  {i:4d} | {ln[:140]}")


def show_yaml_head(path: Path, n_lines: int = 25):
    print(f"\n=== {path.name} ===")
    if not path.exists():
        print("  [MISSING]")
        return
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception as exc:
        print(f"  [ERROR] {exc}")
        return
    print(f"  total lines: {len(lines)}")
    for i, ln in enumerate(lines[:n_lines], 1):
        print(f"  {i:4d} | {ln[:140]}")


def main():
    print("=== SOURCE DIAGNOSTIC ===")
    print(f"ROOT: {ROOT}")
    print(f"EXTRACTED: {EXTRACTED}")

    # AT index
    show_json_head(EXTRACTED / "_at_commands_index.json", 50)

    # HW text
    show_text_head(EXTRACTED / "hw_v2_02_full.txt", 80)

    # Reference: an existing dataset with records
    show_yaml_head(ROOT / "data" / "dat_02_urc.yaml", 25)

    print("\n=== Suggested next steps ===")
    print("1. Examine the format shown above.")
    print("2. Reuse existing scripts if compatible:")
    print("   - scripts/_rebuild_B1_dat01.py")
    print("   - scripts/_rebuild_dat07.py")
    print("3. Only write new extraction code if existing scripts are broken.")

    return 0


if __name__ == "__main__":
    sys.exit(main())