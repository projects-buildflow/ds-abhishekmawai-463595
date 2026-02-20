"""Tests for Task 2.3: Data Cleaning Pipeline

Validates cleaning of marketing_customers_raw.csv patterns.
"""

import pytest
import pandas as pd
import sys
from pathlib import Path


@pytest.fixture
def script_path(student_folder):
    """Get path to student's cleaning script folder."""
    if not student_folder:
        pytest.skip("Student folder not provided")
    return Path(student_folder) / "submissions"


@pytest.fixture
def clean_function(script_path):
    """Import and return the student's cleaning function."""
    script_file = script_path / "clean_customers.py"

    if not script_file.exists():
        pytest.fail(
            f"Cleaning script not found at {script_file}\n\n"
            "Create: submissions/clean_customers.py"
        )

    sys.path.insert(0, str(script_path))

    try:
        if 'clean_customers' in sys.modules:
            del sys.modules['clean_customers']

        from clean_customers import clean_customer_data
        return clean_customer_data
    except ImportError as e:
        pytest.fail(
            f"Could not import clean_customer_data: {e}\n\n"
            "Make sure your file defines: def clean_customer_data(input_path, output_path):"
        )
    except SyntaxError as e:
        pytest.fail(f"Syntax error in clean_customers.py: {e}")
    finally:
        if str(script_path) in sys.path:
            sys.path.remove(str(script_path))


@pytest.fixture
def sample_dirty_data(tmp_path):
    """Create sample dirty data matching real marketing_customers_raw.csv patterns."""
    dirty_df = pd.DataFrame({
        "full_name": [
            "  Rahul Kumar  ",       # 0: valid (strip whitespace)
            "  Priya Patel  ",       # 1: invalid age -> remove
            "",                      # 2: missing name -> remove
            "  Amit Shah  ",         # 3: invalid age -> remove
            "  Neha Gupta  ",        # 4: invalid email -> remove
            "  Sara Khan  ",         # 5: valid
            "  Vikram Singh  ",      # 6: valid
            "  Anita Joshi  ",       # 7: invalid age -> remove
            "  Raj Malhotra  ",      # 8: invalid date -> remove
            "  Meera Das  ",         # 9: duplicate email -> remove
            "  Arjun Nair  ",        # 10: valid
            "  Kavita Rao  ",        # 11: invalid email (no @) -> remove
        ],
        "email_address": [
            "rahul@gmail.com",
            "priya@yahoo.com",
            "someone@email.com",
            "amit@outlook.com",
            "",
            "sara@gmail.com",
            "vikram@email.com",
            "anita@hotmail.com",
            "raj@gmail.com",
            "sara@gmail.com",        # duplicate of row 5
            "arjun@outlook.com",
            "not-valid-email",       # no @
        ],
        "age": [28, -1, 35, 999, 42, 30, 25, 150, 33, 31, 27, 38],
        "gender": ["M", "F", "M", "M", "F", "F", "M", "F", "M", "F", "M", "F"],
        "phone_number": [
            "9876543210", "", "+914332181960", "1234567890", "9876543211",
            "", "9876543212", "9876543213", "9876543214", "", "9876543215", "9876543216",
        ],
        "location": [
            " Mumbai ", "Delhi", " Bangalore ", "Chennai", " Pune ",
            "Hyderabad", " Kolkata ", "Jaipur", " Lucknow ", "Delhi", " Surat ", "Nagpur",
        ],
        "country": ["India"] * 12,
        "date_joined": [
            "2023-05-17", "2022-02-24", "2023-11-28", "2024-01-12", "2023-08-16",
            "2022-04-25", "2024-03-21", "2023-09-04", "invalid-date", "2022-05-22",
            "2023-06-15", "2024-02-10",
        ],
        "lead_source": [
            "google_form", "facebook_lead", "webinar_signup", "email_capture",
            "partner_import", "google_form", "facebook_lead", "webinar_signup",
            "email_capture", "partner_import", "google_form", "facebook_lead",
        ],
        "utm_campaign": [
            "camp_113", "", "camp_790", "", "camp_414",
            "camp_774", "camp_862", "", "camp_632", "camp_630",
            "camp_100", "",
        ],
        "utm_medium": [
            "social", "organic", "email", "cpc", "",
            "social", "organic", "cpc", "email", "organic",
            "social", "cpc",
        ],
        "notes": [
            "", "follow up", "do not contact", "VIP", "",
            "", "follow up", "", "do not contact", "VIP",
            "", "follow up",
        ],
        "is_subscribed": [
            "True", "False", "True", "True", "True",
            "False", "True", "True", "False", "False",
            "True", "False",
        ],
    })

    input_file = tmp_path / "dirty_customers.csv"
    dirty_df.to_csv(input_file, index=False)
    return input_file


class TestScriptExists:
    """Verify the cleaning script exists and has required function."""

    def test_script_file_exists(self, script_path):
        """clean_customers.py must exist."""
        assert (script_path / "clean_customers.py").exists(), (
            "Script not found.\n"
            "Create: submissions/clean_customers.py"
        )

    def test_function_is_callable(self, clean_function):
        """clean_customer_data must be callable."""
        assert callable(clean_function)


class TestAgeValidation:
    """Verify pipeline handles invalid ages."""

    def test_no_negative_ages(self, clean_function, sample_dirty_data, tmp_path):
        """Output must have NO negative ages."""
        output_file = tmp_path / "cleaned.csv"
        clean_function(str(sample_dirty_data), str(output_file))
        cleaned = pd.read_csv(output_file)
        assert (cleaned["age"] >= 0).all(), (
            f"Found negative ages: {cleaned[cleaned['age'] < 0]['age'].tolist()}\n"
            "Remove rows where age < 0."
        )

    def test_no_unreasonable_ages(self, clean_function, sample_dirty_data, tmp_path):
        """Output must have NO ages over 120."""
        output_file = tmp_path / "cleaned.csv"
        clean_function(str(sample_dirty_data), str(output_file))
        cleaned = pd.read_csv(output_file)
        assert (cleaned["age"] <= 120).all(), (
            f"Found ages > 120: {cleaned[cleaned['age'] > 120]['age'].tolist()}\n"
            "Remove rows where age > 120."
        )


class TestEmailCleaning:
    """Verify pipeline handles invalid and duplicate emails."""

    def test_no_invalid_emails(self, clean_function, sample_dirty_data, tmp_path):
        """Output must have NO emails without @ (excluding missing values)."""
        output_file = tmp_path / "cleaned.csv"
        clean_function(str(sample_dirty_data), str(output_file))
        cleaned = pd.read_csv(output_file)
        has_email = cleaned["email_address"].notna() & (cleaned["email_address"] != "")
        emails_present = cleaned.loc[has_email, "email_address"]
        invalid = emails_present[~emails_present.str.contains("@", na=False)]
        assert len(invalid) == 0, (
            f"Found emails without @: {invalid.tolist()}\n"
            "Remove rows where email_address is present but has no @."
        )

    def test_no_duplicate_emails(self, clean_function, sample_dirty_data, tmp_path):
        """Output must have NO duplicate email addresses."""
        output_file = tmp_path / "cleaned.csv"
        clean_function(str(sample_dirty_data), str(output_file))
        cleaned = pd.read_csv(output_file)
        has_email = cleaned["email_address"].notna() & (cleaned["email_address"] != "")
        emails_present = cleaned.loc[has_email, "email_address"]
        duplicates = emails_present[emails_present.duplicated()]
        assert len(duplicates) == 0, (
            f"Found duplicate emails: {duplicates.tolist()}\n"
            "Use drop_duplicates(subset='email_address', keep='first')."
        )


class TestNameAndWhitespace:
    """Verify pipeline handles missing names and whitespace."""

    def test_no_missing_names(self, clean_function, sample_dirty_data, tmp_path):
        """Output must have NO empty/missing full_name values."""
        output_file = tmp_path / "cleaned.csv"
        clean_function(str(sample_dirty_data), str(output_file))
        cleaned = pd.read_csv(output_file)
        missing = cleaned["full_name"].isna() | (cleaned["full_name"].str.strip() == "")
        assert not missing.any(), "Found rows with missing or empty full_name."

    def test_names_stripped(self, clean_function, sample_dirty_data, tmp_path):
        """Output names must have no leading/trailing whitespace."""
        output_file = tmp_path / "cleaned.csv"
        clean_function(str(sample_dirty_data), str(output_file))
        cleaned = pd.read_csv(output_file)
        has_whitespace = cleaned["full_name"] != cleaned["full_name"].str.strip()
        assert not has_whitespace.any(), (
            f"Found names with whitespace: {cleaned.loc[has_whitespace, 'full_name'].tolist()}"
        )

    def test_locations_stripped(self, clean_function, sample_dirty_data, tmp_path):
        """Output locations must have no leading/trailing whitespace."""
        output_file = tmp_path / "cleaned.csv"
        clean_function(str(sample_dirty_data), str(output_file))
        cleaned = pd.read_csv(output_file)
        has_ws = cleaned["location"] != cleaned["location"].str.strip()
        assert not has_ws.any(), (
            f"Found locations with whitespace: {cleaned.loc[has_ws, 'location'].tolist()}"
        )


class TestDateValidation:
    """Verify pipeline handles invalid dates."""

    def test_no_invalid_dates(self, clean_function, sample_dirty_data, tmp_path):
        """Output must have NO invalid date strings."""
        output_file = tmp_path / "cleaned.csv"
        clean_function(str(sample_dirty_data), str(output_file))
        cleaned = pd.read_csv(output_file)
        parsed = pd.to_datetime(cleaned["date_joined"], errors="coerce")
        invalid = parsed.isna()
        assert not invalid.any(), (
            f"Found invalid dates: {cleaned.loc[invalid, 'date_joined'].tolist()}\n"
            "Remove rows where date_joined is not a valid date."
        )


class TestReport:
    """Verify the function returns a cleaning report."""

    def test_returns_dict(self, clean_function, sample_dirty_data, tmp_path):
        """clean_customer_data must return a dict."""
        output_file = tmp_path / "cleaned.csv"
        result = clean_function(str(sample_dirty_data), str(output_file))
        assert isinstance(result, dict), (
            f"Expected dict, got {type(result).__name__}.\n"
            'Return: {"rows_before": ..., "rows_after": ...}'
        )

    def test_report_has_counts(self, clean_function, sample_dirty_data, tmp_path):
        """Report must include rows_before and rows_after."""
        output_file = tmp_path / "cleaned.csv"
        result = clean_function(str(sample_dirty_data), str(output_file))
        assert "rows_before" in result, 'Report missing "rows_before" key'
        assert "rows_after" in result, 'Report missing "rows_after" key'
        assert result["rows_before"] == 12, f"rows_before should be 12, got {result['rows_before']}"
        assert result["rows_after"] < result["rows_before"], (
            f"rows_after ({result['rows_after']}) should be less than rows_before ({result['rows_before']})"
        )
