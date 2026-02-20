
# Bug Report: AI-Generated Validator

## Bug 1: Case-Sensitive Email Validation
**Location**: Line 45-46, `_validate_email` method
**Problem**: The regex `r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'` only matches lowercase letters.
**Impact**: Valid emails with uppercase letters (e.g., `John.Doe@example.com`) are rejected as invalid.
**Fix**: Added `re.IGNORECASE` flag to the `re.match` call or updated regex to include `A-Z`.

## Bug 2: Crash on Missing or None Name
**Location**: Line 40, `_validate_name` method
**Problem**: `len(name)` is called directly. If `name` is `None` (which can happen if key is present but value is null, or passed explicitly), it raises `TypeError`. the `record.get("name", "")` default handles missing keys, but not explicit `None`.
**Impact**: The validator crashes with `TypeError: object of type 'NoneType' has no len()` instead of reporting an error.
**Fix**: Added checks for `None` and ensured `name` is a string before checking length.

## Bug 3: Crash on Non-String Phone Numbers
**Location**: Line 59-61, `_validate_phone` method
**Problem**: Code assumes `phone` is a string. If passed as an integer (e.g., `1234567890`), `phone.isdigit()` raises `AttributeError` and `len(phone)` raises `TypeError`.
**Impact**: The validator crashes when processing records where phone numbers were parsed as numbers (common in JSON/CSV parsing).
**Fix**: Converted `phone` to string using `str()` before validation.

## Bug 4: Incorrect Type Assumption for Age
**Location**: Line 51, `_validate_age` method
**Problem**: `record.get("age", 0)` returns an int default, but if the input has "25" (string), the comparison `age < 0` raises `TypeError` in Python 3.
**Impact**: Validator crashes on string inputs for age.
**Fix**: Cast `age` to `int` within a try-except block to handle string representations.

## Bug 5: Missing Negative Check for Total Spent
**Location**: Line 66, `_validate_total_spent` method
**Problem**: The method checks if `total_spent` is a number, but does not check for negative values which are invalid for "total spent".
**Impact**: Returns valid for logically impossible negative spending amounts.
**Fix**: Added a check for `amount < 0`.
