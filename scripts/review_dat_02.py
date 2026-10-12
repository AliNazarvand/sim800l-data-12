#!/usr/bin/env python3
"""Interactive review tool for dat_02_urc.yaml suspect records.

Modes:
  review  -- (default) walk through suspect records, classify each
  apply   -- apply previously saved decisions to data files
  status  -- show current decisions summary

Usage:
  python scripts/review_dat_02.py           # review mode
  python scripts/review_dat_02.py apply     # apply saved decisions
  python scripts/review_dat_02.py status    # show status

Decisions:
  K = Keep (it's a real URC; remove "suspected" note)
  M = Move (it's an AT command; move to dat_01)
  D = Delete (invalid or duplicate; remove from dat_02)
  S = Skip (leave as-is for now)
  Q = Quit and save

The review mode does NOT modify data files. It only saves decisions to:
  reports/_dat_02_review.yaml
"""
import re
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[FATAL] PyYAML required. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

DAT_02 = DATA / "dat_02_urc.yaml"
DAT_01 = DATA / "dat_01_at_command.yaml"
DECISIONS = REPORTS / "_dat_02_review.yaml"


def load_yaml(path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    return data if isinstance(data, list) else []


def is_suspect(record):
    """A suspect record has notes mentioning 'suspected' or 'not urc'."""
    if not isinstance(record, dict):
        return False
    notes = str(record.get("notes", "")).lower()
    return ("suspected" in notes or "not urc" in notes
            or "needs manual" in notes)


def load_decisions():
    if not DECISIONS.exists():
        return {}
    try:
        with DECISIONS.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_decisions(decisions):
    DECISIONS.parent.mkdir(parents=True, exist_ok=True)
    with DECISIONS.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(decisions, fh, allow_unicode=True, sort_keys=True)


def cmd_status():
    decisions = load_decisions()
    counts = {"keep": 0, "move": 0, "delete": 0, "skip": 0}
    for v in decisions.values():
        if v in counts:
            counts[v] += 1
    print(f"Decisions file: {DECISIONS}")
    print(f"Total decisions: {len(decisions)}")
    print(f"  Keep:   {counts['keep']}")
    print(f"  Move:   {counts['move']}")
    print(f"  Delete: {counts['delete']}")
    print(f"  Skip:   {counts['skip']}")
    return 0


def cmd_review():
    records = load_yaml(DAT_02)
    suspects = [r for r in records if is_suspect(r)]
    print(f"Total dat_02 records: {len(records)}")
    print(f"Suspect records: {len(suspects)}")
    print()

    decisions = load_decisions()
    print(f"Previously saved decisions: {len(decisions)}")
    print()

    print("Commands:")
    print("  [K]eep   -- keep as URC (remove 'suspected' note)")
    print("  [M]ove   -- move to dat_01 (it's an AT command)")
    print("  [D]elete -- remove from dat_02 (invalid/duplicate)")
    print("  [S]kip   -- leave for later")
    print("  [Q]uit   -- stop review (saves so far)")
    print()

    processed = 0
    for i, rec in enumerate(suspects):
        rid = rec.get("id", f"unknown_{i}")

        if rid in decisions and decisions[rid] != "skip":
            print(f"[{i+1}/{len(suspects)}] {rid} -- already decided: {decisions[rid]}")
            continue

        print(f"\n{'='*72}")
        print(f"[{i+1}/{len(suspects)}] {rid}")
        print(f"{'='*72}")
        print(yaml.safe_dump(rec, sort_keys=False, allow_unicode=True).rstrip())
        print(f"{'='*72}")

        try:
            answer = input("Decision? [K]eep / [M]ove / [D]elete / [S]kip / [Q]uit > ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\n[Interrupted]")
            break

        if answer == "Q":
            print("Quitting review.")
            break
        elif answer == "K":
            decisions[rid] = "keep"
        elif answer == "M":
            decisions[rid] = "move"
        elif answer == "D":
            confirm = input("  Confirm delete? Type DELETE to confirm: ").strip()
            if confirm == "DELETE":
                decisions[rid] = "delete"
            else:
                print("  Not confirmed, marking as skip.")
                decisions[rid] = "skip"
        elif answer == "S":
            decisions[rid] = "skip"
        else:
            print("  Invalid input, marking as skip.")
            decisions[rid] = "skip"

        save_decisions(decisions)
        processed += 1

    print(f"\n{'='*72}")
    print(f"Session processed: {processed} records")
    print(f"Decisions saved to: {DECISIONS}")
    print(f"\nTo see summary: python scripts/review_dat_02.py status")
    print(f"To apply:       python scripts/review_dat_02.py apply")
    print(f"\nNOTE: No data files were modified during review.")
    return 0


def cmd_apply():
    decisions = load_decisions()
    if not decisions:
        print("[WARN] No decisions to apply.")
        return 0

    # Filter to actionable decisions
    actionable = {k: v for k, v in decisions.items()
                  if v in ("keep", "move", "delete")}
    if not actionable:
        print("[WARN] No actionable decisions (only 'skip' present).")
        return 0

    print(f"Applying {len(actionable)} decisions to data files...")
    print()

    # Read dat_02
    records = load_yaml(DAT_02)
    if not records:
        print("[FATAL] dat_02 is empty or unreadable.")
        return 1

    # Build a lookup by id
    by_id = {r.get("id"): r for r in records if isinstance(r, dict)}

    # Prepare categories
    keep_ids = [k for k, v in actionable.items() if v == "keep"]
    move_ids = [k for k, v in actionable.items() if v == "move"]
    delete_ids = [k for k, v in actionable.items() if v == "delete"]

    print(f"  Keep:   {len(keep_ids)} records")
    print(f"  Move:   {len(move_ids)} records")
    print(f"  Delete: {len(delete_ids)} records")
    print()

    # Move records go to dat_01 (as commands)
    dat_01_records = load_yaml(DAT_01)
    moved_count = 0
    for rid in move_ids:
        rec = by_id.get(rid)
        if not rec:
            continue
        # Build an AT-command record from the URC-shaped record
        urc_string = str(rec.get("urc_string", "")).strip()
        if not urc_string:
            continue
        cmd_str = urc_string
        if cmd_str.startswith("AT+"):
            cmd_str = cmd_str[3:]
        elif cmd_str.startswith("AT"):
            cmd_str = cmd_str[2:]
        if cmd_str.startswith("+"):
            pass
        else:
            cmd_str = "+" + cmd_str

        new_id = f"dat_01_{9000 + moved_count:04d}"
        new_rec = {
            "id": new_id,
            "category": rec.get("category", "General"),
            "command": cmd_str,
            "mode": "write",
            "syntax": urc_string,
            "parameters": rec.get("parameters", []),
            "response_success": "OK",
            "response_error": "",
            "examples": rec.get("examples", []),
            "related_urcs": [],
            "related_states": [],
            "related_commands": [],
            "firmware_min": "unknown",
            "firmware_max": "unknown",
            "source": rec.get("source", {}),
            "source_type": rec.get("source_type", "primary"),
            "confidence": rec.get("confidence", 0.5),
            "status": "partial",
            "conflicts": [],
            "notes": f"Moved from dat_02 ({rid}) during manual review on {rec.get('updated_at', '')}",
            "tags": ["moved-from-dat02"],
            "applicable_models": ["SIM800L"],
            "created_at": rec.get("created_at", ""),
            "updated_at": rec.get("updated_at", ""),
        }
        dat_01_records.append(new_rec)
        moved_count += 1

    # Rebuild dat_02: remove move+delete, keep keep+skip
    new_dat_02 = []
    for r in records:
        if not isinstance(r, dict):
            continue
        rid = r.get("id")
        if rid in move_ids or rid in delete_ids:
            continue
        if rid in keep_ids:
            # Remove "suspected" from notes
            notes = str(r.get("notes", ""))
            r["notes"] = re.sub(
                r"(?i)suspected[^.]*\.\s*", "", notes
            ).strip()
            if not r["notes"]:
                r["notes"] = "Verified as URC during manual review."
            r["status"] = "partial"
            r["updated_at"] = __import__("datetime").datetime.utcnow().strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
        new_dat_02.append(r)

    # Write files
    with DAT_01.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(dat_01_records, fh, sort_keys=False,
                       allow_unicode=True, default_flow_style=False)
    with DAT_02.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(new_dat_02, fh, sort_keys=False,
                       allow_unicode=True, default_flow_style=False)

    print(f"  dat_01: {len(dat_01_records)} records (added {moved_count})")
    print(f"  dat_02: {len(new_dat_02)} records (removed {len(move_ids) + len(delete_ids)})")
    print()
    print("Done. Run validate.py to verify schema compliance:")
    print("  python scripts/validate.py")
    return 0


def main():
    mode = "review"
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()

    if mode == "review":
        return cmd_review()
    elif mode == "apply":
        return cmd_apply()
    elif mode == "status":
        return cmd_status()
    else:
        print(f"[ERROR] Unknown mode: {mode}")
        print("Usage: review_dat_02.py [review|apply|status]")
        return 1


if __name__ == "__main__":
    sys.exit(main())