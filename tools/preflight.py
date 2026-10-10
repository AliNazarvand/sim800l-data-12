#!/usr/bin/env python3
"""
Preflight check for sim800l-data.

Verifies that the two primary source PDFs are reachable from the repository
root (or from sources/, pdfs/, or the parent folder).

Exit codes:
    0 - both PDFs found
    1 - at least one PDF missing
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CANDIDATE_DIRS = [
    ROOT,
    ROOT / "sources",
    ROOT / "pdfs",
    ROOT.parent,
]

PDFS = {
    "V1.00": ["SIM800L_Hardware_Design_V1.00.pdf",
              "SIM800L_Hardware_Design_V1.00.PDF"],
    "V2.02": ["SIM800H&SIM800L_Hardware_Design_V2.02.pdf",
              "SIM800H&SIM800L_Hardware_Design_V2.02.PDF"],
}

def find(names):
    for d in CANDIDATE_DIRS:
        for n in names:
            p = d / n
            if p.is_file():
                return p
    return None

def main() -> int:
    missing = []
    for ver, names in PDFS.items():
        p = find(names)
        if p is None:
            missing.append((ver, names[0]))
        else:
            print(f"OK   [{ver}] {p}")
    if missing:
        print("\nMISSING SOURCE PDFs:", file=sys.stderr)
        for ver, n in missing:
            print(f"  [{ver}] {n}", file=sys.stderr)
        print("\nPlace the PDFs in one of:", file=sys.stderr)
        for d in CANDIDATE_DIRS:
            print(f"  - {d}", file=sys.stderr)
        return 1
    print("\nAll primary source PDFs are present.")
    return 0

if __name__ == "__main__":
    sys.exit(main())