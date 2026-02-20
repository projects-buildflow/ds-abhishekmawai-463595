"""
Troubleshooting Notes: Date Parsing Bug in data_loader.load_orders
"""

# Problem

## Problem

Order analytics were wrong because the `order_date` column was **not being
parsed correctly as dates** in the original loader. In some cases, dates were
left as strings, parsed as `NaT` (missing), or interpreted as the wrong
calendar date, which breaks any time-based analysis.

## Symptoms

- **Non-datetime `order_date` column**
  - `orders["order_date"].dtype` was not `datetime64[ns]`.
  - Code expecting date operations (e.g. `.dt.year`) failed.
- **Presence of `NaT` values**
  - Some rows had `NaT` in `order_date` even though the CSV had valid dates.
- **Incorrect date values**
  - The first order date should be `2024-01-15`, but in the buggy version it
    could be parsed incorrectly or not at all.
- **Tests in `tests/test_1_3.py` failing**
  - `test_dates_are_parsed_correctly`
  - `test_no_nat_values`
  - `test_dates_have_correct_values`

## Root Cause

The original `src/data_loader.py` used `pd.read_csv` with a **mismatched
`date_format`**:

- The actual CSV data stores dates as ISO format: `YYYY-MM-DD`
  (e.g. `2024-01-15`).
- The buggy loader specified `date_format="%m/%d/%Y"` (US-style
  `MM/DD/YYYY`).
- Because the specified format did not match the real data, pandas either:
  - produced `NaT` values, or
  - misinterpreted valid dates, depending on the input.

This is exactly the issue described in the comments of the template loader:
**wrong date format causes incorrect parsing**.

## Solution

The fix was implemented in `submissions/data_loader.py` in the
`load_orders` function. The key changes:

1. **Use the correct format (or let pandas infer it)**
   - The fixed version calls:
     - `pd.read_csv(..., parse_dates=["order_date"], date_format="%Y-%m-%d")`
       for ISO `YYYY-MM-DD`, or
     - simply `pd.read_csv(..., parse_dates=["order_date"])` and lets pandas
       infer the format from the data.
2. **Keep `parse_dates=["order_date"]`**
   - This ensures `order_date` is parsed as a datetime column on load.
3. **Leave the rest of the loader behavior unchanged**
   - File existence checks and path handling are the same, so only the
     date-parsing behavior changed.

After this change:

- `order_date` is a `datetime64[ns]` column.
- There are **no `NaT` values** for valid dates in the CSV.
- The first date correctly parses as `2024-01-15`, satisfying `test_1_3.py`.

## How to Prevent

- **Match `date_format` to actual data**
  - Only specify `date_format` when you are certain of the on-disk format.
  - Otherwise, prefer `parse_dates` without `date_format` and validate the
    result.
- **Write tests around dates**
  - Verify:
    - the dtype is datetime,
    - there are no unexpected `NaT` values,
    - a few sample dates match exactly.
- **Read the source data before hard-coding formats**
  - Inspect a few raw lines from the CSV to confirm the date pattern.
- **Document intentional bugs and their fixes**
  - As done here, describe both the incorrect behavior and the corrected
    behavior so future maintainers understand the change.

## Related Links

- Tests that validate the behavior: `tests/test_1_3.py`
- Fixed loader implementation: `submissions/data_loader.py`
- Original buggy reference: `src/data_loader.py`
