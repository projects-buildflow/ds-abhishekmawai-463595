"""Tests for Task 2.2: Validation Schema using Pandera

Objective: Create a Pandera schema that validates customer data quality.

This test DECISIVELY verifies:
1. Schema file exists and can be imported
2. Schema is a valid Pandera DataFrameSchema
3. Schema validates clean data successfully
4. Schema REJECTS negative ages (invalid)
5. Schema REJECTS invalid email formats
6. Schema REJECTS missing required fields
7. Schema handles edge cases appropriately
8. Schema has all required column definitions
"""

import pytest
import pandas as pd
import sys
from pathlib import Path


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

    # Add path to import
    sys.path.insert(0, str(schema_path))

    try:
        # Clear cached module if exists
        if 'customer_schema' in sys.modules:
            del sys.modules['customer_schema']

        from customer_schema import customer_schema
        return customer_schema
    except ImportError as e:
        pytest.fail(
            f"Could not import customer_schema: {e}\n\n"
            "Make sure your file defines: customer_schema = pa.DataFrameSchema(...)"
        )
    except SyntaxError as e:
        pytest.fail(f"Syntax error in customer_schema.py: {e}")
    finally:
        if str(schema_path) in sys.path:
            sys.path.remove(str(schema_path))


class TestSchemaExists:
    """Verify schema file exists and is properly structured."""

    def test_schema_file_exists(self, schema_path):
        """customer_schema.py must exist."""
        schema_file = schema_path / "customer_schema.py"
        assert schema_file.exists(), (
            f"Schema file not found at {schema_file}\n\n"
            "Create: submissions/customer_schema.py"
        )

    def test_schema_is_pandera_dataframe_schema(self, customer_schema):
        """Schema must be a Pandera DataFrameSchema."""
        import pandera as pa

        assert isinstance(customer_schema, pa.DataFrameSchema), (
            f"customer_schema is {type(customer_schema).__name__}, expected pa.DataFrameSchema.\n"
            "Define: customer_schema = pa.DataFrameSchema({...})"
        )


class TestSchemaValidatesCleanData:
    """Verify schema accepts valid, clean data."""

    def test_accepts_complete_valid_record(self, customer_schema):
        """Schema should accept a completely valid customer record."""
        valid_df = pd.DataFrame({
            "customer_id": ["C001"],
            "name": ["Alice Johnson"],
            "age": [30],
            "email": ["alice@example.com"],
            "phone": ["9876543210"],
            "city": ["Mumbai"],
            "signup_date": ["2024-01-15"],
            "gender": ["F"],
        })

        try:
            validated = customer_schema.validate(valid_df)
            assert len(validated) == 1, "Validated DataFrame should have 1 row"
        except Exception as e:
            pytest.fail(f"Schema rejected valid data: {e}")

    def test_accepts_multiple_valid_records(self, customer_schema):
        """Schema should accept multiple valid records."""
        valid_df = pd.DataFrame({
            "customer_id": ["C001", "C002", "C003"],
            "name": ["Alice Johnson", "Bob Smith", "Charlie Brown"],
            "age": [25, 35, 45],
            "email": ["alice@example.com", "bob@test.org", "charlie@company.co"],
            "phone": ["9876543210", "8765432109", "7654321098"],
            "city": ["Mumbai", "Delhi", "Bangalore"],
            "signup_date": ["2024-01-15", "2024-02-20", "2024-03-10"],
            "gender": ["F", "M", "M"],
        })

        try:
            validated = customer_schema.validate(valid_df)
            assert len(validated) == 3, "Validated DataFrame should have 3 rows"
        except Exception as e:
            pytest.fail(f"Schema rejected valid data: {e}")

    def test_accepts_edge_case_valid_ages(self, customer_schema):
        """Schema should accept boundary valid ages (18, 100)."""
        valid_df = pd.DataFrame({
            "customer_id": ["C001", "C002"],
            "name": ["Young Adult", "Centenarian"],
            "age": [18, 100],  # Edge cases - should be valid
            "email": ["young@test.com", "old@test.com"],
            "phone": ["1111111111", "2222222222"],
            "city": ["City A", "City B"],
            "signup_date": ["2024-01-01", "2024-01-02"],
            "gender": ["F", "M"],
        })

        try:
            validated = customer_schema.validate(valid_df)
            assert len(validated) == 2
        except Exception as e:
            pytest.fail(f"Schema rejected valid edge case ages: {e}")


class TestSchemaRejectsInvalidData:
    """Verify schema correctly rejects invalid data."""

    def test_rejects_negative_age(self, customer_schema):
        """Schema MUST reject negative ages."""
        import pandera as pa

        invalid_df = pd.DataFrame({
            "customer_id": ["C001"],
            "name": ["Test User"],
            "age": [-5],  # INVALID: negative age
            "email": ["test@example.com"],
            "phone": ["9876543210"],
            "city": ["Mumbai"],
            "signup_date": ["2024-01-15"],
            "gender": ["M"],
        })

        with pytest.raises(pa.errors.SchemaError) as exc_info:
            customer_schema.validate(invalid_df)

        error_str = str(exc_info.value).lower()
        assert "age" in error_str, (
            "Schema should fail on age validation for negative values.\n"
            "Add age validation: pa.Column(int, pa.Check.ge(0))"
        )

    def test_rejects_unreasonable_age(self, customer_schema):
        """Schema MUST reject unreasonably high ages (>120)."""
        import pandera as pa

        invalid_df = pd.DataFrame({
            "customer_id": ["C001"],
            "name": ["Test User"],
            "age": [150],  # INVALID: unreasonably high
            "email": ["test@example.com"],
            "phone": ["9876543210"],
            "city": ["Mumbai"],
            "signup_date": ["2024-01-15"],
            "gender": ["M"],
        })

        with pytest.raises(pa.errors.SchemaError) as exc_info:
            customer_schema.validate(invalid_df)

        error_str = str(exc_info.value).lower()
        assert "age" in error_str, (
            "Schema should fail on age validation for values > 120.\n"
            "Add age validation: pa.Check.le(120)"
        )

    def test_rejects_invalid_email_format(self, customer_schema):
        """Schema MUST reject invalid email formats."""
        import pandera as pa

        invalid_df = pd.DataFrame({
            "customer_id": ["C001"],
            "name": ["Test User"],
            "age": [25],
            "email": ["not-an-email"],  # INVALID: no @ symbol
            "phone": ["9876543210"],
            "city": ["Mumbai"],
            "signup_date": ["2024-01-15"],
            "gender": ["M"],
        })

        with pytest.raises(pa.errors.SchemaError) as exc_info:
            customer_schema.validate(invalid_df)

        error_str = str(exc_info.value).lower()
        assert "email" in error_str, (
            "Schema should fail on email validation.\n"
            "Add email validation with regex: pa.Check.str_matches(r'.*@.*\\..*')"
        )

    def test_rejects_email_without_domain(self, customer_schema):
        """Schema should reject email without proper domain."""
        import pandera as pa

        invalid_df = pd.DataFrame({
            "customer_id": ["C001"],
            "name": ["Test User"],
            "age": [25],
            "email": ["user@"],  # INVALID: no domain
            "phone": ["9876543210"],
            "city": ["Mumbai"],
            "signup_date": ["2024-01-15"],
            "gender": ["M"],
        })

        with pytest.raises(pa.errors.SchemaError) as exc_info:
            customer_schema.validate(invalid_df)

        # Should catch this as invalid email
        assert exc_info.value is not None


class TestSchemaRequiredColumns:
    """Verify schema defines all required columns."""

    def test_has_customer_id_column(self, customer_schema):
        """Schema must define customer_id column."""
        assert "customer_id" in customer_schema.columns, (
            "Schema missing 'customer_id' column definition."
        )

    def test_has_name_column(self, customer_schema):
        """Schema must define name column."""
        assert "name" in customer_schema.columns, (
            "Schema missing 'name' column definition."
        )

    def test_has_age_column(self, customer_schema):
        """Schema must define age column."""
        assert "age" in customer_schema.columns, (
            "Schema missing 'age' column definition."
        )

    def test_has_email_column(self, customer_schema):
        """Schema must define email column."""
        assert "email" in customer_schema.columns, (
            "Schema missing 'email' column definition."
        )

    def test_age_column_has_checks(self, customer_schema):
        """Age column must have validation checks."""
        age_column = customer_schema.columns.get("age")

        if age_column:
            # Check if there are any checks defined
            has_checks = len(age_column.checks) > 0

            assert has_checks, (
                "Age column has no validation checks.\n"
                "Add checks like: pa.Check.ge(0), pa.Check.le(120)"
            )

    def test_email_column_has_checks(self, customer_schema):
        """Email column must have validation checks."""
        email_column = customer_schema.columns.get("email")

        if email_column:
            has_checks = len(email_column.checks) > 0

            assert has_checks, (
                "Email column has no validation checks.\n"
                "Add checks like: pa.Check.str_matches(r'.+@.+\\..+')"
            )


class TestSchemaHandlesEdgeCases:
    """Verify schema handles edge cases appropriately."""

    def test_rejects_empty_dataframe_columns_missing(self, customer_schema):
        """Schema should reject DataFrame with missing required columns."""
        import pandera as pa

        incomplete_df = pd.DataFrame({
            "customer_id": ["C001"],
            "name": ["Test"],
            # Missing: age, email, phone, city, signup_date, gender
        })

        with pytest.raises(pa.errors.SchemaError):
            customer_schema.validate(incomplete_df)

    def test_accepts_valid_gender_values(self, customer_schema):
        """Schema should accept valid gender values if gender validation exists."""
        valid_df = pd.DataFrame({
            "customer_id": ["C001", "C002"],
            "name": ["Alice", "Bob"],
            "age": [25, 30],
            "email": ["alice@test.com", "bob@test.com"],
            "phone": ["1111111111", "2222222222"],
            "city": ["City A", "City B"],
            "signup_date": ["2024-01-01", "2024-01-02"],
            "gender": ["F", "M"],
        })

        try:
            validated = customer_schema.validate(valid_df)
            assert len(validated) == 2
        except Exception as e:
            pytest.fail(f"Schema rejected valid gender values: {e}")


class TestSchemaCodeQuality:
    """Verify schema code quality."""

    def test_schema_file_has_imports(self, schema_path):
        """Schema file should have proper imports."""
        schema_file = schema_path / "customer_schema.py"
        if not schema_file.exists():
            pytest.skip("Schema file not found")

        content = schema_file.read_text()

        assert "pandera" in content, (
            "Schema file should import pandera.\n"
            "Add: import pandera as pa"
        )

    def test_schema_has_docstring_or_comments(self, schema_path):
        """Schema file should have documentation."""
        schema_file = schema_path / "customer_schema.py"
        if not schema_file.exists():
            pytest.skip("Schema file not found")

        content = schema_file.read_text()

        has_docstring = '"""' in content or "'''" in content
        has_comments = '#' in content

        assert has_docstring or has_comments, (
            "Schema file should have documentation.\n"
            "Add a docstring or comments explaining the validation rules."
        )
