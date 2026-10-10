# Cross-Reference Gap Analysis

تحلیل ناسازگاری فرمت‌ها در فیلدهای کلیدی.

## نمونه command در dat_01

```
  'A/'
  'ATA'
  'ATD'
  'ATD><n>'
  'ATD><str>'
  'ATE'
  'ATH'
  'ATI'
  'ATL'
  'ATM'
  '+++'
  'ATO'
  'ATP'
  'ATQ'
  'ATS0'
  'ATS3'
  'ATS4'
  'ATS5'
  'ATS6'
  'ATS7'
```

## نمونه command در dat_09..17

### dat_09
```
  'AT+CMGD'
  'AT+CMGF'
  'AT+CMGL'
  'AT+CMGR'
  'AT+CMGS'
```

### dat_10
```
  'AT+CGATT'
  'AT+CGDCONT'
  'AT+CGQMIN'
  'AT+CGQREQ'
  'AT+CGACT'
```

### dat_11
```
  'AT+HTTPINIT'
  'AT+HTTPTERM'
  'AT+HTTPPARA'
  'AT+HTTPDATA'
  'AT+HTTPACTION'
```

### dat_12
```
  'AT+CALM'
  'AT+CALS'
  'AT+CRSL'
  'AT+CLVL'
  'AT+CMUT'
```

### dat_13
```
  'AT+CIMI'
  'AT+CLCK'
  'AT+CPIN'
  'AT+CPWD'
  'AT+CRSM'
```

### dat_15
```
  'AT+CFUN=0'
  'AT+CFUN=1'
  'AT+CFUN=4'
```

### dat_17
```
  '+SSLCFG'
  '+SSLSETCERT'
  '+SSLSETKEY'
  '+SSLOPEN'
  '+SSLSEND'
```

## نمونه related_command در dat_02

```
  dat_02_0001: 'dat_01_0042'
  dat_02_0002: 'dat_01_0051'
  dat_02_0003: 'dat_01_0062'
  dat_02_0004: 'dat_01_0063'
  dat_02_0005: 'dat_01_0079'
  dat_02_0006: 'dat_09_0008'
  dat_02_0007: 'dat_09_0008'
  dat_02_0008: 'dat_09_0008'
  dat_02_0009: 'dat_09_0008'
  dat_02_0010: 'dat_01_0054'
```

## نمونه related_commands در dat_03

```
  dat_03_0001: None
  dat_03_0002: None
  dat_03_0003: None
  dat_03_0004: None
  dat_03_0005: None
  dat_03_0006: None
  dat_03_0007: None
  dat_03_0008: None
  dat_03_0009: None
  dat_03_0010: None
```

## نمونه supported_commands در dat_08

```
  dat_08_0001: ['+CMGS', '+CMGR', '+CIPSTART', '+CIPSEND', '+CIPCLOSE', '+CSQ', '+CREG']
  dat_08_0002: ['+CMGS', '+CMGR', '+CIPSTART', '+CIPSEND', '+HTTPINIT', '+HTTPACTION']
  dat_08_0003: ['+HTTPINIT', '+FTPOPEN', '+SSLSETCERT', '+SSLSETKEY']
  dat_08_0004: ['+HTTPINIT', '+FTPOPEN', '+SSLSETCERT', '+SSLSETKEY', '+SSLRECV']
  dat_08_0005: ['+HTTPINIT', '+FTPOPEN', '+SSLSETCERT', '+SSLSETKEY', '+SSLRECV', '+SSLOPEN']
```

## نمونه related_states در dat_15

```
  dat_15_0001: None
  dat_15_0002: None
  dat_15_0003: None
  dat_15_0004: None
  dat_15_0005: None
  dat_15_0006: None
  dat_15_0007: None
  dat_15_0008: None
  dat_15_0009: None
  dat_15_0010: None
```

## نمونه state_name در dat_05

```
  dat_05_0001: 'OFF'
  dat_05_0002: 'POWER_ON'
  dat_05_0003: 'SIM_READY'
  dat_05_0004: 'NETWORK_SEARCH'
  dat_05_0005: 'REGISTERED'
  dat_05_0006: 'GPRS_STANDBY'
  dat_05_0007: 'PDP_ACTIVE'
  dat_05_0008: 'DATA_MODE'
  dat_05_0009: 'SMS_MODE'
  dat_05_0010: 'CALL_MODE'
  dat_05_0011: 'SLEEP'
  dat_05_0012: 'MINIMUM_FUNCTIONALITY'
  dat_05_0013: 'CHARGE'
  dat_05_0014: 'ERROR'
  dat_05_0001: 'Power off'
```
