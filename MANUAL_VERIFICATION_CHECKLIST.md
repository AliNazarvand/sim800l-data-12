# Manual Verification Checklist -- sim800l-data

_Generated: 2026-10-12_

> **Prerequisites:** Source PDFs must be available.
> All commands assume you are in the project root directory.

## Already Verified (no action needed)

- [x] **dat_01 format** -- 334/334 commands have `+` prefix (v13 audit)
- [x] **dat_03 uniqueness** -- 255/255 unique `(error_type, code)` pairs

## Step 1: Review dat_02 URCs (2-3 hours) -- REQUIRED

A helper script has been created to make this efficient:
`scripts/review_dat_02.py`

### 1.1 Start the interactive review

```powershell
python scripts\review_dat_02.py
```

### 1.2 For each of the 188 suspect records

The tool shows the record and asks you to classify:

- **[K]eep** -- it IS a URC (e.g., `+CMTI`, `RING`, `+CREG`)
- **[M]ove** -- it's an AT command, not a URC (e.g., `+CAAS`, `+CADC`)
- **[D]elete** -- invalid or duplicate (requires typing `DELETE` to confirm)
- **[S]kip** -- leave as-is for now
- **[Q]uit** -- stop and save progress

Open `SIM800 Series_AT Command Manual_V1.01.pdf` in another window to check each command.

### 1.3 Check progress any time

```powershell
python scripts\review_dat_02.py status
```

### 1.4 When review is complete, apply decisions

```powershell
python scripts\review_dat_02.py apply
python scripts\validate.py
```

Decisions are saved in `reports/_dat_02_review.yaml` -- safe to interrupt and resume.

## Step 2: Expand dat_07 pins (1-2 hours) -- REQUIRED

### 2.1 Read the Pin Description table

- Open `SIM800H&SIM800L_Hardware_Design_V2.02.PDF`
- Navigate to page 16 (Pin Description table)
- Currently 56 of ~88 pins are present

### 2.2 For each missing pin

Append to `data\dat_07_hardware_reference.yaml`:

```yaml
- id: dat_07_NNNN
  category: <Power|UART|SIM|Audio|RF|GPIO|...>
  name: <PIN_NAME>
  pin_number: '<N>'
  direction: <input|output|bidirectional|power|ground>
  function: '<description from PDF>'
  source:
    name: SIM800H&SIM800L_Hardware_Design
    version: V2.02
    date: '2015-07-27'
    page: '16'
    section: Pin Description
  source_type: primary
  confidence: 0.9
  status: partial
  conflicts: []
  notes: ''
  tags: []
  applicable_models:
  - SIM800L
  created_at: '2026-10-12T00:00:00Z'
  updated_at: '2026-10-12T00:00:00Z'
```

## Step 3: Decide on 3 placeholders (15 min) -- OPTIONAL

dat_08, dat_16, dat_18 each have 1 placeholder record.

- [ ] **Option A:** Delete the placeholder (dataset becomes empty).
- [ ] **Option B:** Keep it as documentation (current state).
- [ ] Record your decision in `reports\DECISIONS_LOG.md`.

## Step 4: Final validation

```powershell
python scripts\validate.py
python scripts\cross_ref.py
python scripts\audit_data_integrity.py
```

## Step 5: Propagate to `sim800l-driver`

Only after all steps above are complete:

- [ ] Update `PROMPT_COMPLIANCE.md`: change dat_02/dat_07 to `verified`.
- [ ] Tag a release: `git tag -a v1.0.0-verified`
- [ ] Proceed to `sim800l-driver`.