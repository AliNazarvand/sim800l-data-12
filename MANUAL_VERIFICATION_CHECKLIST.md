# Manual Verification Checklist -- sim800l-data

_Generated: 2026-10-12_

> **Purpose:** These tasks **cannot** be automated. They require a human
> (or LLM with vision capability) reading the source PDFs and comparing
> against the YAML datasets.

## Prerequisites

- [ ] `SIM800 Series_AT Command Manual_V1.01.pdf` (source for dat_01/02/03/09/10/11/12/13/17)
- [ ] `SIM800H&SIM800L_Hardware_Design_V2.02.PDF` (source for dat_04/05/06/07/15)
- [ ] `SIM800L_Hardware_Design_V1.00.pdf` (secondary source for dat_04/05/06/07/15)
- [ ] A YAML editor (VS Code + Red Hat YAML extension recommended)
- [ ] A PDF reader with page navigation

## Step 1: Fix dat_01 AT Command format (30 min)

### 1.1 Open dat_01 and inspect

```powershell
cd "D:\Project\Electronic Project\Control Board SMS 2\Documents\New folder (2)\New 2\Datasheet\01 - sim800l-data\021"
notepad data\dat_01_at_command.yaml
```

### 1.2 Check 5 random records

For each record, look at the `command:` field. Answer:

- [ ] Does the command start with `+` (e.g., `+CGMI`)?
- [ ] Or does it start with `AT+` (e.g., `AT+CGMI`)?
- [ ] Or is the `+` completely missing (e.g., `CGMI`)?

Compare with the PDF: search for the command in `SIM800 Series AT Command Manual`.

### 1.3 Decision

- If ALL commands have `+`: mark dat_01 as `verified`.
- If SOME commands lack `+`: fix them with find/replace.
- If MOST lack `+`: **re-extract from `at_v1_01_full.txt`** (script needed).

## Step 2: Clean dat_02 URC (2-3 hours)

### 2.1 Identify suspect records

Run this in PowerShell to list all records with `Suspected` in notes:

```powershell
cd "D:\Project\Electronic Project\Control Board SMS 2\Documents\New folder (2)\New 2\Datasheet\01 - sim800l-data\021"
Select-String -Path data\dat_02_urc.yaml -Pattern 'Suspected' -Context 5,0
```

### 2.2 For each suspect record

- [ ] Look up `urc_string` in the AT Command Manual.
- [ ] If it is an AT command (not URC), either:
      - **Move** it to `dat_01_at_command.yaml` as a command, OR
      - **Delete** it from dat_02 (it belongs elsewhere).
- [ ] Fix truncated `trigger_event` fields.

## Step 3: Deduplicate dat_03 error codes (1 hour)

### 3.1 List duplicates

Run the audit script output (see `reports/DATA_INTEGRITY_REPORT.md`).

### 3.2 For each (CME/CMS, code) that appears >1 time

- [ ] Decide which record is canonical.
- [ ] Remove or merge the duplicates.
- [ ] Update `related_commands` to point to the canonical record.

## Step 4: Expand dat_07 pins (1-2 hours)

### 4.1 Open the Pin Description table

- Open `SIM800H&SIM800L_Hardware_Design_V2.02.PDF`
- Go to page 16 (Pin Description)
- Current dat_07 has 56 pins; the table has ~88.

### 4.2 For each missing pin

Create a new YAML record with this structure:

```yaml
- id: dat_07_NNNN
  category: <Power|UART|SIM|Audio|RF|GPIO|...>
  name: <PIN_NAME>
  pin_number: '<N>'
  direction: <input|output|bidirectional|power|ground>
  voltage_min: <float>
  voltage_typ: <float>
  voltage_max: <float>
  function: '<description from PDF>'
  source:
    name: SIM800H&SIM800L_Hardware_Design
    version: V2.02
    date: '2015-07-27'
    page: '16'
    section: Pin Description
  source_type: primary
  confidence: 0.9
  status: complete
  conflicts: []
  notes: ''
  tags: []
  applicable_models:
  - SIM800L
  created_at: '2026-10-12T13:05:47Z'
  updated_at: '2026-10-12T13:05:47Z'
```

## Step 5: Decide on 3 documented placeholders

dat_08, dat_16, dat_18 each have 1 placeholder record.

- [ ] **Option A:** Delete the placeholder. Dataset becomes empty.
- [ ] **Option B:** Keep the placeholder as documentation.
- [ ] Document your choice in `reports/DECISIONS_LOG.md`.

## Step 6: Re-run validation

```powershell
cd "D:\Project\Electronic Project\Control Board SMS 2\Documents\New folder (2)\New 2\Datasheet\01 - sim800l-data\021"
python scripts\validate.py
python scripts\cross_ref.py
python scripts\audit_data_integrity.py
```

All three should pass (or report expected remaining issues).

## Step 7: Only then, propagate to sim800l-driver

Once all steps above are complete and validated:

- [ ] Update `PROMPT_COMPLIANCE.md`: change data status to `VERIFIED`.
- [ ] Update `_session_state.json`: change affected datasets to `complete`.
- [ ] Tag a release: `git tag -a v1.0.0-verified`
- [ ] Proceed to `sim800l-driver`.