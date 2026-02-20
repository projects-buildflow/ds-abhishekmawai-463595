"""Tests for Task 2.2: Validation Schema with Pandera

Validates customer data schema against marketing_customers_raw.csv patterns.
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path


VALID_ROW = {
    "full_name": "Rahul Kumar",
    "email_address": "rahul@gmail.com",
    "age": 28,
    "gender": "M",
    "phone_number": "9876543210",
    "location": "Mumbai",
    "country": "India",
    "date_joined": "2023-05-17",
    "lead_source": "google_form",
    "utm_campaign": "camp_113",
    "utm_medium": "social",
    "notes": "",
    "is_subscribed": "True",
}


def make_df(**overrides):
    """Create a single-row DataFrame from VALID_ROW with optional overrides."""
    row = {**VALID_ROW, **overrides}
    return pd.DataFrame([row])


@pytest.fixture
def schema_path(student_folder):
    """Get path to student's schema file."""
    if not student_folder:
        pytest.skip("Student folder not provided")
    return Path(student_folder) / "submissions"


@pytest.fixture
def customer_schema(schema_path):
    """Import and return the student's customer schema."""
    schema_file = schema_path / "customer_schema.py"

    if not schema_file.exists():
        pytest.fail(
            f"Schema file not found at {schema_file}\n\n"
            "Create: submissions/customer_schema.py"
        )

    sys.path.insert(0, str(schema_path))

    try:
        if 'customer_schema' in sys.modules:
            del sys.modules['customer_schema']

        from customer_schema import customer_schema
        return customer_schema
    except ImportError as e:
        pytest.fail(
            f"Could not import customer_schema: {e}\n\n"
            "Make sure your file defines: customer_schema = pa.DataFrameSchema({...})"
        )
    except SyntaxError as e:
        pytest.fail(f"Syntax error in customer_schema.py: {e}")
    finally:
        if str(schema_path) in sys.path:
            sys.path.remove(str(schema_path))


@pytest.fixture
def validate_fn(schema_path):
    """Import and return the student's validate_customers function."""
    sys.path.insert(0, str(schema_path))
    try:
        if 'customer_schema' in sys.modules:
            del sys.modules['customer_schema']
        from customer_schema import validate_customers
        return validate_customers
    except ImportError:
        pytest.skip("validate_customers function not found")
    finally:
        if str(schema_path) in sys.path:
            sys.path.remove(str(schema_path))


class TestSchemaExists:
    """Verify schema file exists and is properly structured."""

    def test_schema_file_exists(self, schema_path):
        """customer_schema.py must exist."""
        assert (schema_path / "customer_schema.py").exists(), (
            "Schema file not found.\n"
            "Create: submissions/customer_schema.py"
        )

    def test_schema_is_pandera_dataframe_schema(self, customer_schema):
        """Schema must be a Pandera DataFrameSchema."""
        import pandera as pa
        assert isinstance(customer_schema, pa.DataFrameSchema), (
            f"customer_schema is {type(customer_schema).__name__}, expected pa.DataFrameSchema"
        )


class TestRejectsInvalidData:
    """Verify schema correctly rejects invalid data."""

    def test_rejects_negative_age(self, customer_schema):
        """Schema MUST reject negative ages (like -1 found in real data)."""
        import pandera as pa
        with pytest.raises(pa.errors.SchemaError):
            customer_schema.validate(make_df(age=-1))

    def test_rejects_unreasonable_age(self, customer_schema):
        """Schema MUST reject ages > 120 (like 999 found in real data)."""
        import pandera as pa
        with pytest.raises(pa.errors.SchemaError):
            customer_schema.validate(make_df(age=999))

    def test_rejects_invalid_email(self, customer_schema):
        """Schema MUST reject emails without @ (like 'not-valid-email' in real data)."""
        import pandera as pa
        with pytest.raises(pa.errors.SchemaError):
            customer_schema.validate(make_df(email_address="not-valid-email"))

    def test_rejects_invalid_gender(self, customer_schema):
        """Schema MUST reject gender values not in [M, F, Other]."""
        import pandera as pa
        with pytest.raises(pa.errors.SchemaError):
            customer_schema.validate(make_df(gender="Unknown"))

    def test_rejects_invalid_date_format(self, customer_schema):
        """Schema MUST reject date_joined that isn't YYYY-MM-DD format."""
        import pandera as pa
        with pytest.raises(pa.errors.SchemaError):
            customer_schema.validate(make_df(date_joined="invalid-date"))


class TestAcceptsValidData:
    """Verify schema accepts valid data."""

    def test_accepts_valid_row(self, customer_schema):
        """Schema must accept a fully valid row."""
        result = customer_schema.validate(make_df())
        assert len(result) == 1

    def test_accepts_nullable_fields(self, customer_schema):
        """Schema must accept rows where optional fields are null."""
        df = make_df(
            full_name=np.nan,
            phone_number=np.nan,
            utm_campaign=np.nan,
            utm_medium=np.nan,
            notes=np.nan,
        )
        result = customer_schema.validate(df)
        assert len(result) == 1


class TestValidateFunction:
    """Verify validate_customers function exists."""

    def test_validate_customers_callable(self, validate_fn):
        """validate_customers must be callable."""
        assert callable(validate_fn)

    def test_validate_customers_returns_dataframe(self, validate_fn):
        """validate_customers(df) should return a DataFrame for valid data."""
        result = validate_fn(make_df())
        assert isinstance(result, pd.DataFrame)
