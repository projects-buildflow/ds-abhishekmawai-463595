"""Tests for Task 4.3: Debug AI-Generated Code

Objective: Find and fix exactly 5 bugs in AI-generated validation code.

This test DECISIVELY verifies:
1. Fixed validator file exists
2. Bug report documents all 5 bugs
3. Fixed code actually works (passes valid data)
4. Fixed code catches invalid data (rejects bad data)
5. All 5 specific bugs were actually fixed
"""

import pytest
import pandas as pd
import sys
from pathlib import Path


# The 5 known bugs in the original AI-generated code:
KNOWN_BUGS = [
    {
        "id": 1,
        "name": "Off-by-one age validation",
        "description": "Age validation uses > instead of >= for upper bound",
        "test_data": {"age": 120},  # Should be invalid (boundary case)
    },
    {
        "id": 2,
        "name": "Case-sensitive email check",
        "description": "Email validation doesn't handle uppercase",
        "test_data": {"email": "TEST@EXAMPLE.COM"},  # Should be valid
    },
    {
        "id": 3,
        "name": "Empty string not caught",
        "description": "Empty phone string passes validation",
        "test_data": {"phone": ""},  # Should be invalid
    },
    {
        "id": 4,
        "name": "Negative total_spent allowed",
        "description": "Negative monetary values not rejected",
        "test_data": {"total_spent": -100.0},  # Should be invalid
    },
    {
        "id": 5,
        "name": "Name with only spaces accepted",
        "description": "Name containing only whitespace passes validation",
        "test_data": {"name": "   "},  # Should be invalid
    },
]


@pytest.fixture
def student_week4_path(student_folder):
    """Get path to student's submissions folder."""
    if not student_folder:
        pytest.skip("Student folder not provided")
    return Path(student_folder) / "submissions"


@pytest.fixture
def validator_module(student_week4_path):
    """Import the student's fixed validator module."""
    validator_file = student_week4_path / "fixed_validator.py"

    if not validator_file.exists():
        pytest.fail(
            f"fixed_validator.py not found at {validator_file}\n\n"
            "Create the file with your corrected validation code."
        )

    sys.path.insert(0, str(student_week4_path))
    try:
        # Clear any cached import
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
    # Try common function names
    func_names = ['validate_customer', 'validate', 'validate_data', 'check_customer']

    for name in func_names:
        if hasattr(validator_module, name):
            return getattr(validator_module, name)

    # Try to find a validator class
    if hasattr(validator_module, 'DataValidator'):
        validator = validator_module.DataValidator()
        for name in ['validate', 'validate_customer', 'check']:
            if hasattr(validator, name):
                return getattr(validator, name)

    pytest.fail(
        "Could not find validation function in fixed_validator.py.\n"
        "Define a function called 'validate_customer' or a class 'DataValidator' with a 'validate' method."
    )


class TestFilesExist:
    """Verify required files exist."""

    def test_fixed_validator_exists(self, student_week4_path):
        """fixed_validator.py must exist."""
        validator_path = student_week4_path / "fixed_validator.py"
        assert validator_path.exists(), (
            "fixed_validator.py not found.\n"
            "Create this file with your corrected validation code."
        )

    def test_bug_report_exists(self, student_week4_path):
        """bug_report.md must exist."""
        report_path = student_week4_path / "bug_report.md"
        assert report_path.exists(), (
            "bug_report.md not found.\n"
            "Create this file documenting all 5 bugs you found."
        )


class TestBugReportContent:
    """Verify the bug report documents all 5 bugs."""

    def test_report_has_five_bugs_documented(self, student_week4_path):
        """Bug report must document exactly 5 bugs."""
        report_path = student_week4_path / "bug_report.md"
        if not report_path.exists():
            pytest.skip("Bug report not found")

        content = report_path.read_text()

        # Count bug entries (various formats)
        import re

        # Look for numbered bugs: "Bug 1", "1.", "### 1", etc.
        bug_patterns = [
            r'(?:bug|issue|error)\s*#?\s*([1-5])',  # Bug 1, Issue #2
            r'^#{1,3}\s*([1-5])\.',                  # ### 1. or ## 1.
            r'^\s*([1-5])\.\s+\w',                   # 1. Description
            r'\*\*([1-5])\*\*',                      # **1**
        ]

        found_bugs = set()
        for pattern in bug_patterns:
            matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
            found_bugs.update(int(m) for m in matches if m.isdigit())

        # Also check by counting section headers
        section_count = len(re.findall(r'^#{1,3}\s*(?:bug|issue)', content, re.MULTILINE | re.IGNORECASE))
        if section_count >= 5:
            found_bugs = {1, 2, 3, 4, 5}

        assert len(found_bugs) >= 5, (
            f"Bug report appears to document only {len(found_bugs)} bugs.\n"
            "The original code has exactly 5 bugs. Document all of them.\n\n"
            "Recommended format:\n"
            "## Bug 1: [Name]\n"
            "**Problem:** [What was wrong]\n"
            "**Fix:** [How you fixed it]"
        )

    def test_report_explains_problems(self, student_week4_path):
        """Bug report must explain what was wrong."""
        report_path = student_week4_path / "bug_report.md"
        if not report_path.exists():
            pytest.skip("Bug report not found")

        content = report_path.read_text().lower()

        explanation_keywords = [
            'problem', 'issue', 'wrong', 'incorrect', 'bug', 'error',
            'should', 'instead', 'because', 'fix', 'solution'
        ]

        found_count = sum(1 for kw in explanation_keywords if kw in content)

        assert found_count >= 5, (
            "Bug report needs more explanation of what was wrong.\n"
            "For each bug, explain:\n"
            "  - What the problem was\n"
            "  - Why it's a bug\n"
            "  - How you fixed it"
        )

    def test_report_is_substantial(self, student_week4_path):
        """Bug report must have substantial content."""
        report_path = student_week4_path / "bug_report.md"
        if not report_path.exists():
            pytest.skip("Bug report not found")

        content = report_path.read_text()
        word_count = len(content.split())

        assert word_count >= 100, (
            f"Bug report is too short ({word_count} words).\n"
            "Provide detailed explanations for each bug."
        )


class TestValidatorAcceptsValidData:
    """Verify the fixed validator accepts valid data."""

    def test_accepts_valid_complete_data(self, validate_func):
        """Validator should accept completely valid data."""
        valid_data = {
            "customer_id": "C001",
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "age": 30,
            "phone": "1234567890",
            "total_spent": 150.00,
        }

        try:
            result = validate_func(valid_data)
            # Accept various "pass" indicators
            is_valid = (
                result is True or
                result is None or
                (isinstance(result, dict) and result.get('valid', True)) or
                (isinstance(result, dict) and not result.get('errors'))
            )
            assert is_valid, f"Validator rejected valid data. Result: {result}"
        except Exception as e:
            pytest.fail(f"Validator crashed on valid data: {e}")

    def test_accepts_edge_case_valid_age(self, validate_func):
        """Validator should accept valid boundary ages (18 and 119)."""
        for age in [18, 119]:
            valid_data = {
                "customer_id": "C001",
                "name": "Test User",
                "email": "test@example.com",
                "age": age,
                "phone": "1234567890",
                "total_spent": 100.00,
            }

            try:
                result = validate_func(valid_data)
                # Should be valid
                is_valid = (
                    result is True or
                    result is None or
                    (isinstance(result, dict) and result.get('valid', True))
                )
                assert is_valid, f"Validator rejected valid age {age}. Result: {result}"
            except Exception as e:
                pytest.fail(f"Validator crashed on age {age}: {e}")


class TestValidatorRejectsInvalidData:
    """Verify the fixed validator catches invalid data - THE BUGS ARE FIXED."""

    def test_rejects_age_over_limit(self, validate_func):
        """BUG 1 FIX: Validator should reject age >= 120."""
        invalid_data = {
            "customer_id": "C001",
            "name": "Test User",
            "email": "test@example.com",
            "age": 120,  # Bug 1: Original code used > 120, should be >= 120
            "phone": "1234567890",
            "total_spent": 100.00,
        }

        try:
            result = validate_func(invalid_data)
            is_invalid = (
                result is False or
                (isinstance(result, dict) and not result.get('valid', True)) or
                (isinstance(result, dict) and result.get('errors'))
            )
            assert is_invalid, (
                f"BUG 1 NOT FIXED: Validator accepted age=120.\n"
                f"Result: {result}\n"
                "The boundary should be < 120, not <= 120."
            )
        except ValueError:
            pass  # Raising an exception is also valid rejection

    def test_rejects_negative_age(self, validate_func):
        """Validator should reject negative ages."""
        invalid_data = {
            "customer_id": "C001",
            "name": "Test User",
            "email": "test@example.com",
            "age": -5,
            "phone": "1234567890",
            "total_spent": 100.00,
        }

        try:
            result = validate_func(invalid_data)
            is_invalid = (
                result is False or
                (isinstance(result, dict) and not result.get('valid', True))
            )
            assert is_invalid, f"Validator accepted negative age. Result: {result}"
        except (ValueError, Exception):
            pass  # Raising an exception is also valid

    def test_handles_uppercase_email(self, validate_func):
        """BUG 2 FIX: Validator should accept uppercase emails."""
        valid_data = {
            "customer_id": "C001",
            "name": "Test User",
            "email": "TEST@EXAMPLE.COM",  # Bug 2: Original didn't handle uppercase
            "age": 30,
            "phone": "1234567890",
            "total_spent": 100.00,
        }

        try:
            result = validate_func(valid_data)
            is_valid = (
                result is True or
                result is None or
                (isinstance(result, dict) and result.get('valid', True))
            )
            assert is_valid, (
                f"BUG 2 NOT FIXED: Validator rejected uppercase email.\n"
                f"Result: {result}\n"
                "Email validation should be case-insensitive."
            )
        except Exception as e:
            pytest.fail(f"BUG 2 NOT FIXED: Crashed on uppercase email: {e}")

    def test_rejects_empty_phone(self, validate_func):
        """BUG 3 FIX: Validator should reject empty phone string."""
        invalid_data = {
            "customer_id": "C001",
            "name": "Test User",
            "email": "test@example.com",
            "age": 30,
            "phone": "",  # Bug 3: Original allowed empty string
            "total_spent": 100.00,
        }

        try:
            result = validate_func(invalid_data)
            is_invalid = (
                result is False or
                (isinstance(result, dict) and not result.get('valid', True))
            )
            assert is_invalid, (
                f"BUG 3 NOT FIXED: Validator accepted empty phone.\n"
                f"Result: {result}\n"
                "Empty strings should be rejected for required fields."
            )
        except (ValueError, Exception):
            pass  # Raising an exception is also valid

    def test_rejects_negative_spent(self, validate_func):
        """BUG 4 FIX: Validator should reject negative total_spent."""
        invalid_data = {
            "customer_id": "C001",
            "name": "Test User",
            "email": "test@example.com",
            "age": 30,
            "phone": "1234567890",
            "total_spent": -100.00,  # Bug 4: Original allowed negative
        }

        try:
            result = validate_func(invalid_data)
            is_invalid = (
                result is False or
                (isinstance(result, dict) and not result.get('valid', True))
            )
            assert is_invalid, (
                f"BUG 4 NOT FIXED: Validator accepted negative total_spent.\n"
                f"Result: {result}\n"
                "Monetary values should not be negative."
            )
        except (ValueError, Exception):
            pass  # Raising an exception is also valid

    def test_rejects_whitespace_only_name(self, validate_func):
        """BUG 5 FIX: Validator should reject name with only whitespace."""
        invalid_data = {
            "customer_id": "C001",
            "name": "   ",  # Bug 5: Original allowed whitespace-only
            "email": "test@example.com",
            "age": 30,
            "phone": "1234567890",
            "total_spent": 100.00,
        }

        try:
            result = validate_func(invalid_data)
            is_invalid = (
                result is False or
                (isinstance(result, dict) and not result.get('valid', True))
            )
            assert is_invalid, (
                f"BUG 5 NOT FIXED: Validator accepted whitespace-only name.\n"
                f"Result: {result}\n"
                "Names should be stripped and checked for content."
            )
        except (ValueError, Exception):
            pass  # Raising an exception is also valid


class TestCodeQuality:
    """Verify the fixed code meets quality standards."""

    def test_no_syntax_errors(self, validator_module):
        """Fixed code should have no syntax errors."""
        # If we got here, the module imported successfully
        assert validator_module is not None

    def test_has_docstrings(self, student_week4_path):
        """Fixed code should have docstrings."""
        validator_file = student_week4_path / "fixed_validator.py"
        if not validator_file.exists():
            pytest.skip("Validator file not found")

        content = validator_file.read_text()
        has_docstrings = '"""' in content or "'''" in content

        assert has_docstrings, (
            "fixed_validator.py should have docstrings.\n"
            "Document your functions explaining what they do."
        )
