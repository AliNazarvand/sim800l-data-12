# DATA_DIFF

Generated: 1405-07-19 23:29:40

Compares three sources for the two flagged data files.
Also checks whether bkp2 record IDs are present in current.

## dat_01_at_command.yaml

| Source | Size (B) | Records | SHA256 (first 16) |
|--------|----------|---------|-------------------|
| current | 383429 | 334 | B7A4F891E2EC |
| bkp1    | 219138 | 306 | BF53B9FF2FE7 |
| bkp2    | 405816 | 334 | 4F74820A0A43 |

### Set comparison

- IDs in bkp2 but NOT in current: **0**
- IDs in current but NOT in bkp2: **0**
- IDs in bkp1 but NOT in current: **1**

---

## dat_07_hardware_reference.yaml

| Source | Size (B) | Records | SHA256 (first 16) |
|--------|----------|---------|-------------------|
| current | 69982 | 78 | CFD93961673F |
| bkp1    | 36645 | 59 | 28716AD8BE03 |
| bkp2    | 70359 | 78 | 32291F5B09D6 |

### Set comparison

- IDs in bkp2 but NOT in current: **0**
- IDs in current but NOT in bkp2: **0**
- IDs in bkp1 but NOT in current: **0**

---

