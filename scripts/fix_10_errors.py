#!/usr/bin/env python3
"""
fix_10_errors.py
- dat_06.schema.yaml: dependency_step -> string, pattern ^dat_06_[0-9]{4}$
- dat_09_sms.yaml: record dat_09_0014 mode 'write' -> 'text'
"""
import re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
DATA    = ROOT / "data"


def fix_dat06_schema():
    path = SCHEMAS / "dat_06.schema.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    props = data.get("properties", {})
    dep = props.get("dependency_step")
    if not isinstance(dep, dict):
        print("  [dat_06] dependency_step not found in schema; skipped")
        return False

    # Force type to [string, "null"]
    old = dep.get("type")
    dep["type"] = ["string", "null"]
    # Add pattern if missing
    if "pattern" not in dep:
        dep["pattern"] = "^dat_06_[0-9]{4}$"

    out = yaml.safe_dump(data, default_flow_style=False, allow_unicode=True,
                         sort_keys=False, width=1000)
    path.write_text(out, encoding="utf-8")
    print(f"  [dat_06] dependency_step type: {old} -> ['string','null']; pattern added")
    return True


def fix_dat09_record():
    path = DATA / "dat_09_sms.yaml"
    text = path.read_text(encoding="utf-8")

    # Locate the block for id: dat_09_0014 and print it
    print("  --- BEFORE: dat_09_0014 block ---")
    lines = text.splitlines()
    start = None
    for i, l in enumerate(lines):
        if re.match(r"^-\s+id:\s*dat_09_0014\s*$", l):
            start = i
            break
    if start is None:
        print("  [dat_09] dat_09_0014 not found")
        return False

    # Find end (next '- id:' or EOF)
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if re.match(r"^-\s+id:", lines[j]):
            end = j
            break

    for l in lines[start:end]:
        print("    " + l)

    # Replace mode
    replaced = False
    for k in range(start, end):
        m = re.match(r"^(\s+mode:\s*)(\S+)(.*)$", lines[k])
        if m:
            old_val = m.group(2)
            lines[k] = f"{m.group(1)}text{m.group(3)}"
            replaced = True
            print(f"    [dat_09] mode: {old_val} -> text")
            break

    if not replaced:
        print("  [dat_09] 'mode' not found in dat_09_0014; skipped")
        return False

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Show AFTER block
    text2 = path.read_text(encoding="utf-8").splitlines()
    print("  --- AFTER: dat_09_0014 block ---")
    start2 = None
    for i, l in enumerate(text2):
        if re.match(r"^-\s+id:\s*dat_09_0014\s*$", l):
            start2 = i
            break
    end2 = len(text2)
    for j in range(start2 + 1, len(text2)):
        if re.match(r"^-\s+id:", text2[j]):
            end2 = j
            break
    for l in text2[start2:end2]:
        print("    " + l)
    return True


def main():
    print("Fixing remaining errors...")
    a = fix_dat06_schema()
    print()
    b = fix_dat09_record()
    print()
    print(f"dat_06 schema changed: {a}")
    print(f"dat_09 record changed: {b}")


if __name__ == "__main__":
    main()
