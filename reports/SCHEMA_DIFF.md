# SCHEMA_DIFF

Generated: 1405-07-19 23:29:39

Compares first 15 lines of each schema file across three sources:
- **current** = `schemas/` in the project (Git-restored)
- **bkp1**    = `D:\Project\Electronic Project\Control Board SMS 2\Documents\New folder (2)\New 2\Datasheet\01 - sim800l-data\sim800l-data-backup-14050718-235606\schemas\`
- **bkp2**    = `D:\Project\Electronic Project\Control Board SMS 2\Documents\New folder (2)\New 2\Datasheet\01 - sim800l-data\sim800l-data-backup-14050719114050\schemas\`

Also lists key differences in top-level YAML keys.

## dat_01.schema.yaml

| Source | Size (B) | SHA256 (first 16) |
|--------|----------|-------------------|
| current | 877 | F359A15F415D |
| bkp1    | 1629 | 18924548F0CA |
| bkp2    | 877 | F359A15F415D |

### First 15 lines — current
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_01
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

### First 15 lines — bkp1
```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "dat_01"
type: object
required: [id, category, source, source_type, confidence, status, applicable_models, created_at, updated_at]
properties:
  id:
    type: string
    pattern: "^dat_01_[0-9]{4}$"
  category:
    type: string
  source:
    type: object
    required: [name, version, date]
    properties:
      name: {type: string}
```

### First 15 lines — bkp2
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_01
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

---

## dat_02.schema.yaml

| Source | Size (B) | SHA256 (first 16) |
|--------|----------|-------------------|
| current | 877 | C465E2C01852 |
| bkp1    | 1441 | 45DC694DF096 |
| bkp2    | 877 | C465E2C01852 |

### First 15 lines — current
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_02
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

### First 15 lines — bkp1
```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "dat_02"
type: object
required: [id, category, source, source_type, confidence, status, applicable_models, created_at, updated_at]
properties:
  id:
    type: string
    pattern: "^dat_02_[0-9]{4}$"
  category:
    type: string
  source:
    type: object
    required: [name, version, date]
    properties:
      name: {type: string}
```

### First 15 lines — bkp2
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_02
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

---

## dat_03.schema.yaml

| Source | Size (B) | SHA256 (first 16) |
|--------|----------|-------------------|
| current | 877 | 320295420C8B |
| bkp1    | 1366 | FB966DE6AFF6 |
| bkp2    | 877 | 320295420C8B |

### First 15 lines — current
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_03
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

### First 15 lines — bkp1
```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "dat_03"
type: object
required: [id, category, source, source_type, confidence, status, applicable_models, created_at, updated_at]
properties:
  id:
    type: string
    pattern: "^dat_03_[0-9]{4}$"
  category:
    type: string
  source:
    type: object
    required: [name, version, date]
    properties:
      name: {type: string}
```

### First 15 lines — bkp2
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_03
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

---

## dat_04.schema.yaml

| Source | Size (B) | SHA256 (first 16) |
|--------|----------|-------------------|
| current | 877 | 12F3FD9D2043 |
| bkp1    | 1368 | E5C8E7775938 |
| bkp2    | 877 | 12F3FD9D2043 |

### First 15 lines — current
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_04
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

### First 15 lines — bkp1
```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "dat_04"
type: object
required: [id, category, source, source_type, confidence, status, applicable_models, created_at, updated_at]
properties:
  id:
    type: string
    pattern: "^dat_04_[0-9]{4}$"
  category:
    type: string
  source:
    type: object
    required: [name, version, date]
    properties:
      name: {type: string}
```

### First 15 lines — bkp2
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_04
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

---

## dat_05.schema.yaml

| Source | Size (B) | SHA256 (first 16) |
|--------|----------|-------------------|
| current | 877 | 52891FD9A507 |
| bkp1    | 1560 | DB69D2D9B617 |
| bkp2    | 877 | 52891FD9A507 |

### First 15 lines — current
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_05
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

### First 15 lines — bkp1
```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "dat_05"
type: object
required: [id, category, source, source_type, confidence, status, applicable_models, created_at, updated_at]
properties:
  id:
    type: string
    pattern: "^dat_05_[0-9]{4}$"
  category:
    type: string
  source:
    type: object
    required: [name, version, date]
    properties:
      name: {type: string}
```

### First 15 lines — bkp2
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_05
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

---

## dat_06.schema.yaml

| Source | Size (B) | SHA256 (first 16) |
|--------|----------|-------------------|
| current | 877 | 2300B03D9AA3 |
| bkp1    | 1380 | BAFE3D24E321 |
| bkp2    | 877 | 2300B03D9AA3 |

### First 15 lines — current
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_06
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

### First 15 lines — bkp1
```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "dat_06"
type: object
required: [id, category, source, source_type, confidence, status, applicable_models, created_at, updated_at]
properties:
  id:
    type: string
    pattern: "^dat_06_[0-9]{4}$"
  category:
    type: string
  source:
    type: object
    required: [name, version, date]
    properties:
      name: {type: string}
```

### First 15 lines — bkp2
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_06
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

---

## dat_07.schema.yaml

| Source | Size (B) | SHA256 (first 16) |
|--------|----------|-------------------|
| current | 877 | A215658F0AF0 |
| bkp1    | 1538 | 7BC7298F1234 |
| bkp2    | 877 | A215658F0AF0 |

### First 15 lines — current
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_07
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

### First 15 lines — bkp1
```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "dat_07"
type: object
required: [id, category, source, source_type, confidence, status, applicable_models, created_at, updated_at]
properties:
  id:
    type: string
    pattern: "^dat_07_[0-9]{4}$"
  category:
    type: string
  source:
    type: object
    required: [name, version, date]
    properties:
      name: {type: string}
```

### First 15 lines — bkp2
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_07
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

---

## dat_08.schema.yaml

| Source | Size (B) | SHA256 (first 16) |
|--------|----------|-------------------|
| current | 877 | 59A642E264AC |
| bkp1    | 1499 | 59806615294E |
| bkp2    | 877 | 59A642E264AC |

### First 15 lines — current
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_08
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

### First 15 lines — bkp1
```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "dat_08"
type: object
required: [id, category, source, source_type, confidence, status, applicable_models, created_at, updated_at]
properties:
  id:
    type: string
    pattern: "^dat_08_[0-9]{4}$"
  category:
    type: string
  source:
    type: object
    required: [name, version, date]
    properties:
      name: {type: string}
```

### First 15 lines — bkp2
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_08
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

---

## dat_09.schema.yaml

| Source | Size (B) | SHA256 (first 16) |
|--------|----------|-------------------|
| current | 877 | A9DBBEE6F70E |
| bkp1    | 1564 | E44CE7CEFDB7 |
| bkp2    | 877 | A9DBBEE6F70E |

### First 15 lines — current
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_09
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

### First 15 lines — bkp1
```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "dat_09"
type: object
required: [id, category, source, source_type, confidence, status, applicable_models, created_at, updated_at]
properties:
  id:
    type: string
    pattern: "^dat_09_[0-9]{4}$"
  category:
    type: string
  source:
    type: object
    required: [name, version, date]
    properties:
      name: {type: string}
```

### First 15 lines — bkp2
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_09
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

---

## dat_10.schema.yaml

| Source | Size (B) | SHA256 (first 16) |
|--------|----------|-------------------|
| current | 877 | 0B1BC739BA0C |
| bkp1    | 1470 | 955B02C27FBA |
| bkp2    | 877 | 0B1BC739BA0C |

### First 15 lines — current
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_10
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

### First 15 lines — bkp1
```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "dat_10"
type: object
required: [id, category, source, source_type, confidence, status, applicable_models, created_at, updated_at]
properties:
  id:
    type: string
    pattern: "^dat_10_[0-9]{4}$"
  category:
    type: string
  source:
    type: object
    required: [name, version, date]
    properties:
      name: {type: string}
```

### First 15 lines — bkp2
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_10
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

---

## dat_11.schema.yaml

| Source | Size (B) | SHA256 (first 16) |
|--------|----------|-------------------|
| current | 877 | 7BEEF2D6F6DB |
| bkp1    | 1415 | 549A981BA21C |
| bkp2    | 877 | 7BEEF2D6F6DB |

### First 15 lines — current
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_11
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

### First 15 lines — bkp1
```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "dat_11"
type: object
required: [id, category, source, source_type, confidence, status, applicable_models, created_at, updated_at]
properties:
  id:
    type: string
    pattern: "^dat_11_[0-9]{4}$"
  category:
    type: string
  source:
    type: object
    required: [name, version, date]
    properties:
      name: {type: string}
```

### First 15 lines — bkp2
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_11
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

---

## dat_12.schema.yaml

| Source | Size (B) | SHA256 (first 16) |
|--------|----------|-------------------|
| current | 877 | 6C9A00B50FEC |
| bkp1    | 1362 | 8AE6E9128480 |
| bkp2    | 877 | 6C9A00B50FEC |

### First 15 lines — current
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_12
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

### First 15 lines — bkp1
```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "dat_12"
type: object
required: [id, category, source, source_type, confidence, status, applicable_models, created_at, updated_at]
properties:
  id:
    type: string
    pattern: "^dat_12_[0-9]{4}$"
  category:
    type: string
  source:
    type: object
    required: [name, version, date]
    properties:
      name: {type: string}
```

### First 15 lines — bkp2
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_12
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

---

## dat_13.schema.yaml

| Source | Size (B) | SHA256 (first 16) |
|--------|----------|-------------------|
| current | 877 | 7EC52937EF65 |
| bkp1    | 1412 | B10E4ED63A29 |
| bkp2    | 877 | 7EC52937EF65 |

### First 15 lines — current
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_13
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

### First 15 lines — bkp1
```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "dat_13"
type: object
required: [id, category, source, source_type, confidence, status, applicable_models, created_at, updated_at]
properties:
  id:
    type: string
    pattern: "^dat_13_[0-9]{4}$"
  category:
    type: string
  source:
    type: object
    required: [name, version, date]
    properties:
      name: {type: string}
```

### First 15 lines — bkp2
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_13
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

---

## dat_14.schema.yaml

| Source | Size (B) | SHA256 (first 16) |
|--------|----------|-------------------|
| current | 877 | 2DE0B6A29B12 |
| bkp1    | 1388 | 3A9BAEE95E2C |
| bkp2    | 877 | 2DE0B6A29B12 |

### First 15 lines — current
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_14
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

### First 15 lines — bkp1
```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "dat_14"
type: object
required: [id, category, source, source_type, confidence, status, applicable_models, created_at, updated_at]
properties:
  id:
    type: string
    pattern: "^dat_14_[0-9]{4}$"
  category:
    type: string
  source:
    type: object
    required: [name, version, date]
    properties:
      name: {type: string}
```

### First 15 lines — bkp2
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_14
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

---

## dat_15.schema.yaml

| Source | Size (B) | SHA256 (first 16) |
|--------|----------|-------------------|
| current | 877 | A26AF732EB18 |
| bkp1    | 1481 | 14E37391E194 |
| bkp2    | 877 | A26AF732EB18 |

### First 15 lines — current
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_15
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

### First 15 lines — bkp1
```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "dat_15"
type: object
required: [id, category, source, source_type, confidence, status, applicable_models, created_at, updated_at]
properties:
  id:
    type: string
    pattern: "^dat_15_[0-9]{4}$"
  category:
    type: string
  source:
    type: object
    required: [name, version, date]
    properties:
      name: {type: string}
```

### First 15 lines — bkp2
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_15
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

---

## dat_16.schema.yaml

| Source | Size (B) | SHA256 (first 16) |
|--------|----------|-------------------|
| current | 877 | B53607D12D60 |
| bkp1    | 1253 | F04CFEBE0DF6 |
| bkp2    | 877 | B53607D12D60 |

### First 15 lines — current
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_16
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

### First 15 lines — bkp1
```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "dat_16"
type: object
required: [id, category, source, source_type, confidence, status, applicable_models, created_at, updated_at]
properties:
  id:
    type: string
    pattern: "^dat_16_[0-9]{4}$"
  category:
    type: string
  source:
    type: object
    required: [name, version, date]
    properties:
      name: {type: string}
```

### First 15 lines — bkp2
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_16
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

---

## dat_17.schema.yaml

| Source | Size (B) | SHA256 (first 16) |
|--------|----------|-------------------|
| current | 877 | 137B7E509598 |
| bkp1    | 1533 | BA11D4E44CC1 |
| bkp2    | 877 | 137B7E509598 |

### First 15 lines — current
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_17
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

### First 15 lines — bkp1
```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "dat_17"
type: object
required: [id, category, source, source_type, confidence, status, applicable_models, created_at, updated_at]
properties:
  id:
    type: string
    pattern: "^dat_17_[0-9]{4}$"
  category:
    type: string
  source:
    type: object
    required: [name, version, date]
    properties:
      name: {type: string}
```

### First 15 lines — bkp2
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_17
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

---

## dat_18.schema.yaml

| Source | Size (B) | SHA256 (first 16) |
|--------|----------|-------------------|
| current | 877 | 3A9C312DCD80 |
| bkp1    | 1346 | 5836BEC365BC |
| bkp2    | 877 | 3A9C312DCD80 |

### First 15 lines — current
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_18
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

### First 15 lines — bkp1
```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "dat_18"
type: object
required: [id, category, source, source_type, confidence, status, applicable_models, created_at, updated_at]
properties:
  id:
    type: string
    pattern: "^dat_18_[0-9]{4}$"
  category:
    type: string
  source:
    type: object
    required: [name, version, date]
    properties:
      name: {type: string}
```

### First 15 lines — bkp2
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: dat_18
type: object
required:
- id
- category
- source
- source_type
- confidence
- status
- applicable_models
properties:
  id:
    type: string
  category:
```

---

