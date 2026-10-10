#!/usr/bin/env python3
"""
B1 Final: Full Rollback of A1 Auto-Extraction
==============================================
Restores data/ from the pre-A1 backup, documents the decision,
archives the failed A1 script, and re-validates.

This is a deliberate, honest rollback — not a fix. The A1 auto-extraction
approach failed on technical tables (RF, ESD, Absolute Max) because regex
parsing of extracted PDF text cannot reliably reconstruct multi-column
tables. The 60 records it added were either noise or duplicates.
"""

import sys, re, shutil, subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
NOW_ISO = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
NOW_DATE = datetime.now().strftime('%Y-%m-%d')

def log(msg, kind='info'):
    p = {'info': '  ', 'ok': '  [OK]   ', 'warn': '  [WARN] ', 'err': '  [ERR]  '}.get(kind, '  ')
    print(f"{p}{msg}")

# ---------------------------------------------------------------------------
# Step 1: Locate the pre-A1 backup
# ---------------------------------------------------------------------------
def find_backup():
    backups = sorted(
        ROOT.glob('_backup_extract_*'),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    if not backups:
        log("no _backup_extract_* found", 'err')
        return None
    return backups[0]

# ---------------------------------------------------------------------------
# Step 2: Restore data/ from backup
# ---------------------------------------------------------------------------
def restore_data(backup):
    log(f"Restoring data/ from: {backup.name}", 'info')
    src = backup / 'data'
    dst = ROOT / 'data'
    if not src.exists():
        log(f"backup missing data/ — aborting", 'err')
        return False

    # Remove current (noisy) data/
    if dst.exists():
        shutil.rmtree(dst)

    # Restore from backup
    shutil.copytree(src, dst)
    log("data/ restored to pre-A1 state", 'ok')
    return True

# ---------------------------------------------------------------------------
# Step 3: Verify noise is gone
# ---------------------------------------------------------------------------
def verify_clean():
    print("\n=== Verification ===")
    noise_files = [
        'data/hardware/esd_characteristics.yaml',
        'data/hardware/absolute_maximum.yaml',
        'data/hardware/operating_frequencies.yaml',
    ]
    for f in noise_files:
        if (ROOT / f).exists():
            log(f"STILL PRESENT: {f}", 'err')
        else:
            log(f"removed: {f}", 'ok')

    # Check rf_characteristics no longer has dat_07_0001..0011
    import yaml
    rf = ROOT / 'data' / 'hardware' / 'rf_characteristics.yaml'
    if rf.exists():
        data = yaml.safe_load(rf.read_text(encoding='utf-8')) or {}
        recs = data.get('records', data) if isinstance(data, dict) else data
        if isinstance(recs, list):
            noisy = [r for r in recs if isinstance(r, dict)
                     and re.match(r'dat_07_00(0[1-9]|1[01])$', str(r.get('id', '')))]
            if noisy:
                log(f"rf_characteristics still has {len(noisy)} noise records", 'err')
            else:
                log(f"rf_characteristics clean ({len(recs)} records)", 'ok')

    # Check states no longer has dat_05_0012..0017
    st = ROOT / 'data' / 'state_machine' / 'states.yaml'
    if st.exists():
        data = yaml.safe_load(st.read_text(encoding='utf-8')) or {}
        recs = data.get('records', data) if isinstance(data, dict) else data
        if isinstance(recs, list):
            noise = [r for r in recs if isinstance(r, dict)
                     and r.get('id', '') in {f'dat_05_{i:04d}' for i in range(12, 18)}]
            if noise:
                log(f"states still has {len(noise)} inferred records", 'err')
            else:
                log(f"states clean ({len(recs)} records)", 'ok')

# ---------------------------------------------------------------------------
# Step 4: Document the rollback
# ---------------------------------------------------------------------------
def document_rollback():
    print("\n=== Documentation ===")
    decisions = ROOT / 'DECISIONS_LOG.md'
    entry = f"""

## D-B1-001 — Rollback of A1 Auto-Extraction

- **Date:** {NOW_DATE}
- **Decision:** Full rollback of all 60 records added by the A1 auto-extraction
  (`scripts/_extract_a1.py`). No selective retention.
- **Reason:**
  - Regex-based extraction of multi-column PDF tables failed systematically.
  - **ESD** records were garbage: `SIM_VDD` (a pin name) parsed as 16V; part
    numbers like "ESDA6V1" parsed as 6V ESD ratings.
  - **Absolute Maximum** records were actually operating conditions, not abs max.
  - **Operating Frequencies** mixed Bluetooth tables (2402-2480 MHz) with GSM.
  - **RF Characteristics** produced broken labels like
    `"MHz (Operation Mode) -58" → value_typ: 36.0`.
  - **Autobaud step** (`dat_06_0007`) was a duplicate of existing `dat_06_0006`.
  - **6 inferred states** violated rule R4 (`status: partial, confidence: 0.7`
    instead of `status: inferred, confidence ≤ 0.5`).
  - ID generation bug: `next_id()` started from 1 instead of max+1, so new
    dat_07 records collided with existing `dat_07_0001..0011` range.
- **Actions taken:**
  1. Restored `data/` from `_backup_extract_*` (pre-A1 state).
  2. Removed noisy files: `esd_characteristics.yaml`, `absolute_maximum.yaml`,
     `operating_frequencies.yaml`.
  3. Archived `scripts/_extract_a1.py` → `scripts/archive/`.
  4. Re-validated with canonical `scripts/validate.py`.
- **Alternatives rejected:**
  - **Selective keep** (critique's B1): would preserve 6 inferred states that
    violate R4 and don't have clear PDF basis, plus a duplicate autobaud step.
    Not worth the R4 violation and conceptual noise.
  - **Fix the A1 output in place**: 60 records need cleanup; more error-prone
    than clean rollback.
  - **Upgrade to table-aware extraction (pdfplumber)**: requires original PDF
    structure, not plain text; out of scope for current state.
- **Lesson learned:**
  Auto-extraction from flattened PDF text is unreliable for technical tables.
  Future extraction must be manual for table-based parameters, or use
  structure-aware PDF parsing (pdfplumber, camelot) on the original PDF.
"""
    if decisions.exists():
        content = decisions.read_text(encoding='utf-8')
        if 'D-B1-001' not in content:
            decisions.write_text(content + entry, encoding='utf-8')
            log("DECISIONS_LOG.md updated (D-B1-001)", 'ok')
        else:
            log("DECISIONS_LOG.md already has D-B1-001 (idempotent)", 'ok')
    else:
        decisions.write_text("# Decisions Log\n" + entry, encoding='utf-8')
        log("DECISIONS_LOG.md created", 'ok')

    # Update reports/COVERAGE_REALITY.md note
    reality = ROOT / 'reports' / 'COVERAGE_REALITY.md'
    if reality.exists():
        content = reality.read_text(encoding='utf-8')
        if 'A1 auto-extraction' not in content:
            note = f"""

## Update — {NOW_DATE}

A1 auto-extraction was attempted and rolled back (see DECISIONS_LOG.md D-B1-001).
The 60 records it added were garbage (see reason). Current project state is
identical to the Session 12 baseline:

- **dat_04**: partial, ~95%
- **dat_05**: partial, ~80%
- **dat_06**: partial, ~83%
- **dat_07**: partial, ~70%
- **dat_15**: partial, ~95%

All other datasets remain blocked/deferred.
"""
            reality.write_text(content + note, encoding='utf-8')
            log("COVERAGE_REALITY.md updated", 'ok')

# ---------------------------------------------------------------------------
# Step 5: Archive the failed A1 script
# ---------------------------------------------------------------------------
def archive_a1():
    print("\n=== Archive A1 Script ===")
    src = ROOT / 'scripts' / '_extract_a1.py'
    if not src.exists():
        log("scripts/_extract_a1.py not found — nothing to archive", 'warn')
        return
    archive = ROOT / 'scripts' / 'archive'
    archive.mkdir(exist_ok=True)
    dst = archive / '_extract_a1.py.failed'
    if dst.exists():
        dst.unlink()
    shutil.move(str(src), str(dst))
    log(f"moved to: {dst.relative_to(ROOT)}", 'ok')

# ---------------------------------------------------------------------------
# Step 6: Re-validate
# ---------------------------------------------------------------------------
def revalidate():
    print("\n=== Re-run Canonical Validator ===")
    sp = ROOT / 'scripts' / 'validate.py'
    if not sp.exists():
        log("scripts/validate.py not found", 'err')
        return
    try:
        r = subprocess.run(
            [sys.executable, str(sp)],
            capture_output=True, text=True, cwd=str(ROOT), timeout=180
        )
        out = (r.stdout or '') + (r.stderr or '')
        for ln in out.splitlines():
            print(f"    {ln}")
        print(f"    --- exit code: {r.returncode} ---")
    except Exception as e:
        log(f"failed: {e}", 'err')

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 64)
    print("B1 Final: Full Rollback of A1 Auto-Extraction")
    print(f"Root: {ROOT}")
    print("=" * 64)

    bak = find_backup()
    if not bak:
        print("\nFATAL: no backup found. Cannot proceed.")
        return

    if not restore_data(bak):
        return

    verify_clean()
    document_rollback()
    archive_a1()
    revalidate()

    print("\n" + "=" * 64)
    print("B1 FINAL COMPLETE")
    print("=" * 64)
    print("Rolled back:  60 records from A1 auto-extraction")
    print("Restored:     data/ from pre-A1 backup")
    print("Archived:     scripts/_extract_a1.py → scripts/archive/")
    print("Documented:   DECISIONS_LOG.md (D-B1-001)")
    print("=" * 64)
    print("")
    print("Project state now (honest):")
    print("  ✅ Complete:  dat_04, dat_15")
    print("  ⚠️  Partial:   dat_05, dat_06, dat_07")
    print("  ❌ Blocked:   dat_01, 02, 03, 08, 09, 10, 11, 12, 13, 17, 18")
    print("  ⏸  Deferred: dat_14, dat_16")
    print("=" * 64)

if __name__ == '__main__':
    main()