# Data Cleaning Pipeline - Code Review Checklist

## Overview

Use this checklist when reviewing data cleaning code (e.g. scripts that read raw data, apply transformations, and write cleaned output). It helps catch correctness bugs, robustness gaps, and maintainability issues before pipelines run in production. It is based on lessons from data profiling (2.1), schema validation (2.2), and cleaning pipeline implementation (2.3).

---

## 1. Data Correctness

### Input Validation

- [ ] **Expected columns exist** – Code checks for required columns (e.g. `"full_name" in df.columns`) before using them, or fails fast with a clear message if they are missing.
- [ ] **Input row count is captured** – `rows_before` (or equivalent) is recorded at read time so the report can show how many rows were dropped.
- [ ] **No silent column assumptions** – The pipeline does not assume column order or optional columns without checking; missing optional columns are handled (e.g. skip that step or log).
- [ ] **File/format is validated** – Read step handles empty files, wrong delimiters, or encoding issues (e.g. `pd.read_csv(..., encoding=...)`) and does not silently produce empty or wrong DataFrames.

### Transformation Logic

- [ ] **Order of operations is correct** – Critical order is respected (e.g. drop rows with missing `full_name` *before* calling `.str.strip()`, so NaN is not converted to the string `"nan"`).
- [ ] **Nulls handled before string/numeric ops** – Any `.str` or numeric operation is guarded so nulls are handled explicitly (e.g. `isna()` checks, `errors="coerce"`) and do not produce wrong or misleading values.
- [ ] **Business rules match schema** – Ranges and rules (e.g. age in [0, 120], email contains `@`, date format YYYY-MM-DD) align with the validation schema used downstream.
- [ ] **Deduplication is explicit** – If duplicates are removed, the subset (e.g. `email_address`) and `keep` (e.g. `keep="first"`) are clearly chosen and documented.

### Output Validation

- [ ] **Cleaned output passes schema** – Cleaned data can be validated with the same Pandera (or equivalent) schema used for “clean” data; reviewer can run `validate_customers(cleaned_df)`.
- [ ] **No invalid values remain** – Spot-check: no negative ages, no ages > 120, no non-empty emails without `@`, no invalid date strings in date columns.
- [ ] **Row counts are consistent** – `rows_after` in the report matches `len(df)` after cleaning and matches the number of rows in the written file.

---

## 2. Error Handling

- [ ] **Missing or bad input path** – Pipeline handles missing file or unreadable path (e.g. raise with clear message or return error report) instead of raising a raw stack trace.
- [ ] **Empty DataFrame after read** – Code does not assume at least one row; either handles empty input or fails with a clear, intentional message.
- [ ] **Type coercion failures** – Numeric/date parsing uses `errors="coerce"` (or equivalent) and invalid values are either dropped or handled explicitly, not left as NaT/wrong types.
- [ ] **Edge cases for “optional” fields** – Rows where optional fields (e.g. email, phone) are null are handled correctly (e.g. “invalid email” rule applies only when email is *present* but invalid).
- [ ] **Write failures** – Output path is writable; if writing fails (e.g. disk full, permission), the pipeline does not claim success (e.g. return report only after successful write).

---

## 3. Code Quality

### Readability

- [ ] **Steps are named and ordered** – Cleaning steps are easy to follow (e.g. “drop missing names”, “strip whitespace”, “fix invalid ages”) via comments or small functions.
- [ ] **No magic numbers in business logic** – Constants like age bounds (0, 120) or date formats are named (e.g. `MIN_AGE`, `MAX_AGE`) or documented where they appear.
- [ ] **One concern per block** – Each logical step (e.g. name cleaning, email validation, deduplication) is grouped so a reviewer can verify it in isolation.

### Documentation

- [ ] **Module/docstring describes purpose** – Top-level comment or docstring says what the pipeline does, when to run it (e.g. “whenever new data arrives”), and main inputs/outputs.
- [ ] **Function contract is clear** – `clean_customer_data(input_path, output_path)` (or equivalent) documents parameters and return value (e.g. report dict with `rows_before`, `rows_after`).
- [ ] **Non-obvious decisions explained** – Any non-obvious choice (e.g. why drop invalid rows vs impute, why `keep="first"` for duplicates) is briefly commented.

---

## 4. Performance

- [ ] **Avoid unnecessary copies** – Large DataFrames are not copied unnecessarily; filtering and assignments are done in a way that does not double memory (e.g. reassign `df = df[mask]` rather than multiple full copies if not needed).
- [ ] **Column presence checks are cheap** – Checks like `if "col" in df.columns` are used so optional steps are skipped without loading extra data.
- [ ] **Single pass where possible** – If multiple filters can be combined (e.g. one boolean mask for “valid row”), consider it for very large data; for typical CSV sizes (e.g. 10k rows), clarity can trump micro-optimization.
- [ ] **Output write is intentional** – Writing once at the end (e.g. `df.to_csv(output_path, index=False)`) is preferred over repeated writes; no debug left that writes on every row.

---

## 5. Testing

- [ ] **Unit tests use realistic dirty data** – Tests include rows with missing names, invalid ages (-1, 999), invalid emails (no `@`), invalid dates, duplicates, and leading/trailing whitespace, mirroring real raw data.
- [ ] **Tests assert invariants, not just “no crash”** – Tests check that output has no negative ages, no ages > 120, no duplicate emails, no missing names, stripped strings, and no invalid date strings.
- [ ] **Report is tested** – At least one test asserts that the function returns a dict with `rows_before` and `rows_after`, and that `rows_after <= rows_before` after cleaning.
- [ ] **Schema used in tests** – Cleaned output is validated with the same schema (e.g. `validate_customers(cleaned_df)`) in tests or in review to ensure pipeline and schema stay in sync.
- [ ] **Date parsing is tested** – If the pipeline or loader parses dates, tests verify dtype (e.g. datetime), no unexpected NaT for valid inputs, and that a known date string parses to the expected value.

---

## Common Issues to Watch For

### Issue 1: Turning NaN into the string `"nan"` with string methods

**Problem:** Calling `.astype(str)` or `.str.strip()` on a column that contains NaN can turn NaN into the literal string `"nan"`. Later checks like `== ""` then miss these, and “empty” names can slip through.

**What to look for:** Any use of `df["col"].str.*` or `df["col"].astype(str)` without first handling nulls (e.g. drop nulls for that column, or use `fillna("")` only when intentional).

**Fix:** Handle nulls first (e.g. `missing = df["full_name"].isna() | (df["full_name"].astype(str).str.strip() == "")` and drop those rows), or use checks that treat NaN explicitly (e.g. `isna()` before string ops).

---

### Issue 2: Date format mismatch (wrong `date_format` or no parsing)

**Problem:** Using `parse_dates` with a `date_format` that does not match the actual data (e.g. `%m/%d/%Y` when data is `YYYY-MM-DD`) produces NaT or wrong dates. Downstream code then fails or produces incorrect analytics.

**What to look for:** `pd.read_csv(..., parse_dates=[...], date_format=...)` or `pd.to_datetime(..., format=...)` — confirm the format string matches a sample of the raw data. Also check that date columns are not left as strings when they are used in date operations.

**Fix:** Inspect raw data (e.g. first few rows of the CSV), set `date_format` to match (e.g. `"%Y-%m-%d"` for ISO), or omit `date_format` and let pandas infer, then add tests that assert dtype and sample date values.

---

### Issue 3: Applying “invalid value” rules to missing/optional fields

**Problem:** Code that removes “invalid” emails by checking “no `@`” can incorrectly drop rows where email is null or empty, if the check does not distinguish “present but invalid” from “missing.”

**What to look for:** Logic like “drop rows where email doesn’t contain `@`” without first restricting to rows where email is non-null and non-empty.

**Fix:** Only apply the invalid-email rule where email is present (e.g. `email_filled = df["email_address"].notna() & (df["email_address"].astype(str).str.strip() != "")` then `invalid = email_filled & ~email_has_at`; drop only rows where `invalid` is True).

---

### Issue 4: Order of operations changing which rows get dropped

**Problem:** Filtering in the wrong order can drop too many or too few rows. For example, stripping names before dropping missing names can turn NaN into `"nan"` and then later steps may treat them as valid; or dropping by one column before cleaning another can leave invalid values in the other column.

**What to look for:** Review the sequence of filters and transforms. Confirm that “drop bad/missing” steps happen before any transform that could change the meaning of “missing” or “invalid” (e.g. drop missing names before stripping; validate and drop invalid dates after other cleans so counts are consistent).

**Fix:** Document the intended order (e.g. in comments or a small design note) and align code to it: typically validate/drop bad rows first, then normalize (strip, coerce types), then deduplicate, then write and report.

---

### Issue 5: Cleaning pipeline and schema out of sync

**Problem:** The Pandera (or other) schema says “age in [0, 120]” or “email contains @”, but the cleaning pipeline does not enforce the same rules. Cleaned data then fails schema validation in tests or downstream.

**What to look for:** Schema and cleaning code live in different files; after changing one, the other was not updated. No test runs the cleaned output through the schema.

**Fix:** Run `validate_customers(cleaned_df)` (or equivalent) in tests on the pipeline output. When adding or changing a schema rule, add or update the corresponding cleaning step and vice versa. Keep a short comment in the pipeline linking to the schema (e.g. “Must match customer_schema checks”).

---

## Quick Reference

| Category      | Key Question |
|---------------|--------------|
| Correctness   | Does the pipeline actually fix the data issues identified in profiling and satisfy the schema? |
| Robustness   | What happens with empty input, nulls, wrong types, and invalid/missing optional fields? |
| Readability   | Could a new team member follow the steps and understand why each transform is applied? |
| Performance  | Is the pipeline efficient enough for production data volume (e.g. 10k–1M rows)? |
| Testing      | How do we know it works? (dirty-sample tests, schema validation, report assertions, date tests.) |
