#!/usr/bin/env python3
"""
tools/validate.py — DEPRECATED WRAPPER
=======================================
The original hardcoded validator was deprecated because it diverged from the
canonical schema-based validator. This wrapper delegates all validation to
scripts/validate.py.

Deprecated: see DECISIONS_LOG.md entry D-A3-001
Canonical:  see reports/VALIDATION_CANONICAL.md
Original:   tools/validate.py.deprecated (preserved for reference)
"""

import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "scripts" / "validate.py"

if not CANONICAL.exists():
    print(f"ERROR: canonical validator not found at {CANONICAL}", file=sys.stderr)
    sys.exit(2)

sys.exit(subprocess.call([sys.executable, str(CANONICAL)], cwd=str(ROOT)))
