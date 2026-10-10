#!/usr/bin/env python3
"""Cross-reference helper between datasets.

Reads data/*.yaml and builds simple lookup maps. Reports missing references.
"""
import os
import glob
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

def load(name):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    return doc.get("records", []) if isinstance(doc, dict) else doc

def main():
    at_commands = {r.get("command") for r in load("dat_01_at_command.yaml")}
    print("dat_01 commands:", len(at_commands))
    for fname in sorted(glob.glob(os.path.join(DATA, "*.yaml"))):
        if fname.endswith("dat_01_at_command.yaml"):
            continue
        base = os.path.basename(fname)
        recs = load(base)
        misses = []
        for r in recs:
            for cmdk in ("command", "related_command", "related_commands"):
                v = r.get(cmdk)
                if isinstance(v, str) and v.startswith("+") and v not in at_commands:
                    misses.append((r.get("id"), v))
                elif isinstance(v, list):
                    for x in v:
                        if isinstance(x, str) and x.startswith("+") and x not in at_commands:
                            misses.append((r.get("id"), x))
        if misses:
            print(f"{base}: {len(misses)} unresolved command refs")

if __name__ == "__main__":
    main()