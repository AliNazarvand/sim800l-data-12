# Canonical Validator

**Declared on:** 2026-10-10
**Canonical validator:** `scripts/validate.py`
**Deprecated:** `tools/validate.py` (now a wrapper)
**Original preserved as:** `tools/validate.py.deprecated`

## Decision

After the A2 repair, `scripts/validate.py` passes with **0 errors** and is
schema-based. The previous `tools/validate.py` had hardcoded rules that
diverged from the actual data model, producing 287 false-positive errors.

## Comparison

| Aspect | scripts/validate.py | tools/validate.py (original) |
|---|---|---|
| Approach | Schema-based | Hardcoded checks |
| `_meta` field | Optional | Required (250+ false errors) |
| `status: blocked` | Accepted | Rejected (2 false errors) |
| `null` condition | Accepted | Rejected (30+ false errors) |
| Maintainability | High | Low |
| Pass rate after A2 | 0 errors | 287 errors |

## How to validate

```bash
python scripts/validate.py
```

Or via the pipeline orchestrator (Step 8), which now invokes the wrapper.

## Reversibility

See `DECISIONS_LOG.md` entry D-A3-001.
Backup: `_backup_a3_*/tools/validate.py.deprecated`.
