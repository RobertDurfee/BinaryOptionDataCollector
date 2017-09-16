# BinaryOptionDataCollector
Python script for minute-by-minute collection of index and FOREX prices into a MySQL database.

**THIS NO LONGER WORKS. GOOGLE REMOVED A FEATURE REQUIRED BY THIS PROGRAM.**

### Disclaimer
This is not production-worthy code! View this simply as a proof-of-concept. Preconditions are implicit. No error checking exists.

### Initialization
To use this script, you must have a SQL server (syntax is MySQL by default). Run `CreateSchema.sql` and then `CreateTables.sql` on that server to create the default schema and tables. Once everything is created, replace `<CENSORED>` in the script with your username, password, and hostname, respectively.

### Defaults
Indices:
```
INDEXDJX:.DJI       Dow Jones Industrial Average
INDEXSP:.INX        S&P 500
INDEXNASDAQ:.IXIC   NASDAQ Composite
INDEXRUSSELL:RUT    Russell 2000
INDEXFTSE:XIN0      FTSE China 50 Index
INDEXFTSE:UKX       FTSE 100
INDEXFTSE:WIDEU     FTSE Germany Index
INDEXFTSE:JAPAN     FTSE Japan Index
```
Currencies:
```
CURRENCY:EURUSD     Euro (€) ⇨ US Dollar ($)
CURRENCY:GBPUSD     British Pound (£) ⇨ US Dollar ($)
CURRENCY:USDJPY     US Dollar ($) ⇨ Japanese Yen (¥)
CURRENCY:EURJPY     Euro (€) ⇨ Japanese Yen (¥)
CURRENCY:AUDUSD     Australian Dollar (A$) ⇨ US Dollar ($)
CURRENCY:USDCAD     US Dollar ($) ⇨ Canadian Dollar (CA$)
CURRENCY:GBPJPY     British Pound (£) ⇨ Japanese Yen (¥)
CURRENCY:USDCHF     US Dollar ($) ⇨ Swiss Franc (CHF)
CURRENCY:EURGBP     Euro (€) ⇨ British Pound (£)
CURRENCY:AUDJPY     Australian Dollar (A$) ⇨ Japanese Yen (¥)
```
Schema:
```
BinaryOptionData
```
Tables have the same name as the index or currency code used by Google Finance.

### Modifications
If you add an index, currency, or any other code from Google Finance, append it to both the `url` and `lastAddedDateTime` variables and create a new table with the code as the name in your `BinaryOptionsData` schema or append it to the `CreateTables.sql` file.

If you must change the schema name, find and replace it in all files `BinaryOptionsData` to ensure all are updated as this name is used frequently.
