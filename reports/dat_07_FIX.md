# dat_07_FIX — اصلاح classification و تشخیص هم‌ارزها

تاریخ: 2026-10-10T20:40:22Z

## خلاصه
- کل رکوردها: **78**
- رکوردهای بازدسته‌بندی‌شده: **36**
- رکوردهای بدون تغییر: **42**
- هم‌ارزهای علامت‌گذاری‌شده: **12** جفت
- رکوردهای همچنان Unclassified: **0**

## توزیع category بعد از اصلاح
- Keypad: 20
- Audio: 16
- SIM: 12
- UART: 10
- GPIO: 3
- Power: 3
- USB: 3
- Ground: 2
- LED: 2
- I2C: 2
- NC: 1
- NETLIGHT: 1
- PWM: 1
- PWRKEY: 1
- STATUS: 1

## بازدسته‌بندی‌ها

| id | name | old | new |
|---|---|---|---|
| dat_07_0004 | C4 | Unclassified | Ground |
| dat_07_0005 | C5 | Unclassified | Ground |
| dat_07_0006 | C6 | Unclassified | NC |
| dat_07_0009 | COL0 | Unclassified | Keypad |
| dat_07_0010 | COL1 | Unclassified | Keypad |
| dat_07_0011 | COL2 | Unclassified | Keypad |
| dat_07_0012 | COL3 | Unclassified | Keypad |
| dat_07_0013 | COL4 | Unclassified | Keypad |
| dat_07_0020 | ISINK0 | Unclassified | LED |
| dat_07_0021 | ISINK1 | Unclassified | LED |
| dat_07_0022 | KBC0 | Unclassified | Keypad |
| dat_07_0023 | KBC1 | Unclassified | Keypad |
| dat_07_0024 | KBC2 | Unclassified | Keypad |
| dat_07_0025 | KBC3 | Unclassified | Keypad |
| dat_07_0026 | KBC4 | Unclassified | Keypad |
| dat_07_0027 | KBR0 | Unclassified | Keypad |
| dat_07_0028 | KBR1 | Unclassified | Keypad |
| dat_07_0029 | KBR2 | Unclassified | Keypad |
| dat_07_0030 | KBR3 | Unclassified | Keypad |
| dat_07_0031 | KBR4 | Unclassified | Keypad |
| dat_07_0037 | PCMCLK | Unclassified | Audio |
| dat_07_0038 | PCMIN | Unclassified | Audio |
| dat_07_0039 | PCMOUT | Unclassified | Audio |
| dat_07_0040 | PCMSYNC | Unclassified | Audio |
| dat_07_0041 | PCM_CLK | Unclassified | Audio |
| dat_07_0042 | PCM_IN | Unclassified | Audio |
| dat_07_0043 | PCM_OUT | Unclassified | Audio |
| dat_07_0044 | PCM_SYNC | Unclassified | Audio |
| dat_07_0048 | ROW0 | Unclassified | Keypad |
| dat_07_0049 | ROW1 | Unclassified | Keypad |
| dat_07_0050 | ROW2 | Unclassified | Keypad |
| dat_07_0051 | ROW3 | Unclassified | Keypad |
| dat_07_0052 | ROW4 | Unclassified | Keypad |
| dat_07_0055 | SCL | Unclassified | I2C |
| dat_07_0056 | SDA | Unclassified | I2C |
| dat_07_0077 | VBUS | Unclassified | Power |

## هم‌ارزهای علامت‌گذاری‌شده (only tagged، نه merged)

| V2.02 | V1.00 | id (V2.02) | id (V1.00) | دلیل |
|---|---|---|---|---|
| C1 | SIM_VDD | dat_07_0001 | dat_07_0063 | SIM card power supply |
| C2 | SIM_RST | dat_07_0002 | dat_07_0062 | SIM card reset |
| C3 | SIM_CLK | dat_07_0003 | dat_07_0058 | SIM card clock |
| C7 | SIM_DATA | dat_07_0007 | dat_07_0059 | SIM card data I/O |
| C8 | SIM_DET | dat_07_0008 | dat_07_0060 | SIM card detection |
| DCD | UART_DCD | dat_07_0015 | dat_07_0070 | UART Data Carrier Detect |
| DTR | UART_DTR | dat_07_0016 | dat_07_0071 | UART Data Terminal Ready |
| RI | UART_RI | dat_07_0047 | dat_07_0072 | UART Ring Indicator |
| PCMCLK | PCM_CLK | dat_07_0037 | dat_07_0041 | PCM clock |
| PCMIN | PCM_IN | dat_07_0038 | dat_07_0042 | PCM input |
| PCMOUT | PCM_OUT | dat_07_0039 | dat_07_0043 | PCM output |
| PCMSYNC | PCM_SYNC | dat_07_0040 | dat_07_0044 | PCM sync |

## یادداشت
- هیچ رکوردی حذف نشد.
- هم‌ارزها فقط با tag ``possible-duplicate`` و ``notes`` علامت‌گذاری شدند؛ ادغام نشدند.
- وضعیت دیتاست همچنان ``partial`` است.