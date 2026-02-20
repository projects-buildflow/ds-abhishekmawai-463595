"""Tests for Task 4.3: Debug AI-Generated Code

Objective: Find and fix exactly 5 bugs in AI-generated validation code.

This test verifies:
1. Fixed validator file exists
2. Bug report documents all 5 bugs
3. Fixed code accepts valid data
4. Fixed code rejects invalid data
5. Code quality standards are met
"""

import pytest
import re
import sys
from pathlib import Path


@pytest.fixture
def student_submissions_path(student_folder):
    """Get path to student's submissions folder."""
    if not student_folder:
        pytest.skip("Student folder not provided")
    return Path(student_folder) / "submissions"


@pytest.fixture
def validator_module(student_submissions_path):
    """Import the student's fixed validator module."""
    validator_file = student_submissions_path / "fixed_validator.py"

    if not validator_file.exists():
        pytest.fail(
            f"fixed_validator.py not found at {validator_file}\n\n"
            "Create the file with your corrected validation code."
        )

    sys.path.insert(0, str(student_submissions_path))
    try:
        if 'fixed_validator' in sys.modules:
            del sys.modules['fixed_validator']

        import fixed_validator
        return fixed_validator
    except SyntaxError as e:
        pytest.fail(f"Syntax error in fixed_validator.py: {e}")
    except ImportError as e:
        pytest.fail(f"Could not import fixed_validator.py: {e}")


@pytest.fixture
def validate_func(validator_module):
    """Get the validation function from the module."""
    func_names = ['validate_customer', 'validate', 'validate_data', 'check_customer']

    for name in func_names:
        if hasattr(validator_module, name):
            return getattr(validator_module, name)

    if hasattr(validator_module, 'DataValidator'):
        validator = validator_module.DataValidator()
        for name in ['validate', 'validate_customer', 'check']:
            if hasattr(validator, name):
                return getattr(validator, name)

    pytest.fail(
        "Could not find validation function in fixed_validator.py.\n"
        "Define a function called 'validate_customer' or a class 'DataValidator' with a 'validate' method."
    )


def _is_valid(result):
    """Check if a validation result indicates valid data."""
    return (
        result is True or
        result is None or
        (isinstance(result, dict) and result.get('valid', False) is True) or
        (isinstance(result, dict) and not result.get('errors'))
    )


def _is_invalid(result):
    """Check if a validation result indicates invalid data."""
    return (
        result is False or
        (isinstance(result, dict) and result.get('valid', True) is False) or
        (isinstance(result, dict) and bool(result.get('errors')))
    )


# -- Helpers to build test records --

def _valid_record(**overrides):
    """Return a known-good record, optionally overriding fields."""
    base = {
        "customer_id": "C001",
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "age": 30,
        "phone": "1234567890",
        "total_spent": 150.00,
    }
    base.update(overrides)
    return base


# ================================================================
# FILE EXISTENCE
# ================================================================

class TestFilesExist:
    """Verify required files exist."""

    def test_fixed_validator_exists(self, student_submissions_path):
        """fixed_validator.py must exist."""
        path = student_submissions_path / "fixed_validator.py"
        assert path.exists(), (
            "fixed_validator.py not found.\n"
            "Create this file with your corrected validation code."
        )

    def test_bug_report_exists(self, student_submissions_path):
        """bug_report.md must exist."""
        path = student_submissions_path / "bug_report.md"
        assert path.exists(), (
            "bug_report.md not found.\n"
            "Create this file documenting all 5 bugs you found."
        )


# ================================================================
# BUG REPORT QUALITY
# ================================================================

class TestBugReportContent:
    """Verify the bug report documents all 5 bugs with detail."""

    def test_report_documents_five_bugs(self, student_submissions_path):
        """Bug report must document exactly 5 bugs."""
        report_path = student_submissions_path / "bug_report.md"
        if not report_path.exists():
            pytest.skip("Bug report not found")

        content = report_path.read_text()

        bug_patterns = [
            r'(?:bug|issue|error)\s*#?\s*([1-5])',
            r'^#{1,3}\s*([1-5])\.',
            r'^\s*([1-5])\.\s+\w',
            r'\*\*([1-5])\*\*',
        ]

        found_bugs = set()
        for pattern in bug_patterns:
            matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
            found_bugs.update(int(m) for m in matches if m.isdigit())

        section_count = len(re.findall(r'^#{1,3}\s*(?:bug|issue)', content, re.MULTILINE | re.IGNORECASE))
        if section_count >= 5:
            found_bugs = {1, 2, 3, 4, 5}

        assert len(found_bugs) >= 5, (
            f"Bug report appears to document only {len(found_bugs)} bug(s).\n"
            "The original code has exactly 5 bugs. Document all of them.\n\n"
            "Recommended format:\n"
            "## Bug 1: [Name]\n"
            "**Problem:** ...\n"
            "**Fix:** ..."
        )

    def test_report_has_explanations(self, student_submissions_path):
        """Bug report must explain what was wrong and how it was fixed."""
        report_path = student_submissions_path / "bug_report.md"
        if not report_path.exists():
            pytest.skip("Bug report not found")

        content = report_path.read_text().lower()

        keywords = [
            'problem', 'issue', 'wrong', 'incorrect', 'bug', 'error',
            'should', 'instead', 'because', 'fix', 'solution', 'changed',
            'location', 'impact', 'line',
        ]

        found = sum(1 for kw in keywords if kw in content)

        assert found >= 6, (
            "Bug report needs more detail.\n"
            "For each bug, explain:\n"
            "  - Where it is (Location)\n"
            "  - What is wrong (Problem)\n"
            "  - What could go wrong (Impact)\n"
            "  - How you fixed it (Fix)"
        )

    def test_report_is_substantial(self, student_submissions_path):
        """Bug report must have at least 150 words."""
        report_path = student_submissions_path / "bug_report.md"
        if not report_path.exists():
            pytest.skip("Bug report not found")

        content = report_path.read_text()
        word_count = len(content.split())

        assert word_count >= 150, (
            f"Bug report is too short ({word_count} words).\n"
            "Provide detailed explanations for each of the 5 bugs."
        )


# ================================================================
# VALID DATA ACCEPTANCE
# ================================================================

class TestValidatorAcceptsValidData:
    """Verify the fixed validator correctly accepts valid data."""

    def test_accepts_standard_valid_record(self, validate_func):
        """Validator should accept a completely valid record."""
        try:
            result = validate_func(_valid_record())
            assert _is_valid(result), f"Validator rejected valid data. Result: {result}"
        except Exception as e:
            pytest.fail(f"Validator crashed on valid data: {e}")

    def test_accepts_boundary_valid_ages(self, validate_func):
        """Validator should accept ages clearly within range."""
        for age in [0, 1, 18, 65, 99, 119]:
            try:
                result = validate_func(_valid_record(age=age))
                assert _is_valid(result), (
                    f"Validator rejected valid age {age}. Result: {result}"
                )
            except Exception as e:
                pytest.fail(f"Validator crashed on age {age}: {e}")

    def test_accepts_mixed_case_email(self, validate_func):
        """Validator should accept emails regardless of case."""
        emails = ["Alice@Example.COM", "BOB@TEST.ORG", "User.Name@Domain.Co"]
        for email in emails:
            try:
                result = validate_func(_valid_record(email=email))
                assert _is_valid(result), (
                    f"Validator rejected valid email '{email}'. Result: {result}\n"
                    "Email validation should be case-insensitive."
                )
            except Exception as e:
                pytest.fail(f"Validator crashed on email '{email}': {e}")

    def test_accepts_zero_total_spent(self, validate_func):
        """Validator should accept zero total_spent (new customer)."""
        try:
            result = validate_func(_valid_record(total_spent=0.0))
            assert _is_valid(result), (
                f"Validator rejected zero total_spent. Result: {result}"
            )
        except Exception as e:
            pytest.fail(f"Validator crashed on zero total_spent: {e}")


# ================================================================
# INVALID DATA REJECTION
# ================================================================

class TestValidatorRejectsInvalidData:
    """Verify the fixed validator correctly rejects invalid data."""

    @staticmethod
    def _call_validator(validate_func, record):
        """Call the validator, returning the result or None if it raised."""
        try:
            return validate_func(record)
        except (ValueError, TypeError, KeyError, RuntimeError):
            return None  # exception counts as rejection

    def test_rejects_boundary_age(self, validate_func):
        """Validator should reject age at the upper boundary (120+)."""
        for age in [120, 150, 999]:
            result = self._call_validator(validate_func, _valid_record(age=age))
            if result is not None:
                assert _is_invalid(result), (
                    f"Validator accepted age={age} which should be invalid.\n"
                    f"Result: {result}"
                )

    def test_rejects_negative_age(self, validate_func):
        """Validator should reject negative ages."""
        result = self._call_validator(validate_func, _valid_record(age=-5))
        if result is not None:
            assert _is_invalid(result), (
                f"Validator accepted negative age. Result: {result}"
            )

    def test_rejects_empty_phone(self, validate_func):
        """Validator should reject an empty phone string."""
        result = self._call_validator(validate_func, _valid_record(phone=""))
        if result is not None:
            assert _is_invalid(result), (
                f"Validator accepted empty phone string.\n"
                f"Result: {result}\n"
                "Phone is a required field and must not be empty."
            )

    def test_rejects_negative_total_spent(self, validate_func):
        """Validator should reject negative monetary values."""
        for amount in [-1.0, -100.0, -0.01]:
            result = self._call_validator(validate_func, _valid_record(total_spent=amount))
            if result is not None:
                assert _is_invalid(result), (
                    f"Validator accepted total_spent={amount}.\n"
                    f"Result: {result}\n"
                    "Monetary values cannot be negative."
                )

    def test_rejects_whitespace_only_name(self, validate_func):
        """Validator should reject names that are only whitespace."""
        for name in ["   ", "\t", "\n", "  \t  "]:
            result = self._call_validator(validate_func, _valid_record(name=name))
            if result is not None:
                assert _is_invalid(result), (
                    f"Validator accepted whitespace-only name.\n"
                    f"Result: {result}\n"
                    "Names must contain actual characters."
                )

    def test_rejects_invalid_email_format(self, validate_func):
        """Validator should reject malformed emails."""
        bad_emails = ["notanemail", "missing@tld", "@nodomain.com", ""]
        for email in bad_emails:
            result = self._call_validator(validate_func, _valid_record(email=email))
            if result is not None:
                assert _is_invalid(result), (
                    f"Validator accepted invalid email '{email}'. Result: {result}"
                )

    def test_rejects_non_digit_phone(self, validate_func):
        """Validator should reject phone numbers with non-digit characters."""
        bad_phones = ["123-456-7890", "abcdefghij", "12345678901"]
        for phone in bad_phones:
            result = self._call_validator(validate_func, _valid_record(phone=phone))
            if result is not None:
                assert _is_invalid(result), (
                    f"Validator accepted invalid phone '{phone}'. Result: {result}"
                )



# ================================================================
# CODE QUALITY
# ================================================================

class TestCodeQuality:
    """Verify the fixed code meets quality standards."""

    def test_no_syntax_errors(self, validator_module):
        """Fixed code should import without syntax errors."""
        assert validator_module is not None

    def test_has_docstrings(self, student_submissions_path):
        """Fixed code should have docstrings."""
        validator_file = student_submissions_path / "fixed_validator.py"
        if not validator_file.exists():
            pytest.skip("Validator file not found")

        content = validator_file.read_text()
        has_docstrings = '"""' in content or "'''" in content

        assert has_docstrings, (
            "fixed_validator.py should have docstrings.\n"
            "Document your functions explaining what they do."
        )

    def test_handles_crash_gracefully(self, validate_func):
        """Validator should not crash on unusual but non-malicious input."""
        edge_cases = [
            _valid_record(age=0),
            _valid_record(total_spent=0),
            _valid_record(phone="0000000000"),
        ]
        for record in edge_cases:
            try:
                validate_func(record)
            except Exception as e:
                pytest.fail(
                    f"Validator crashed on edge-case input: {e}\n"
                    f"Record: {record}"
                )
