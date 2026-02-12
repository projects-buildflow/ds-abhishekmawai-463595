"""Tests for Task 1.2: Data Deduplication Bug Fix

Objective: Fix remove_duplicates() to identify duplicates by email (case-insensitive)
           and keep the record with highest total_orders.

This test DECISIVELY verifies:
1. Function exists and is callable
2. Function correctly identifies case-insensitive email duplicates
3. Function keeps the record with highest total_orders
4. Function handles edge cases (no duplicates, empty df)
"""

import pytest
import pandas as pd
import sys
from pathlib import Path


@pytest.fixture
def sample_data_with_duplicates():
    """Create sample data with email duplicates (different casings)."""
    return pd.DataFrame({
        'customer_id': [1001, 1002, 1003, 1004, 1005],
        'name': ['Rahul Kumar', 'Priya Sharma', 'RAHUL KUMAR', 'Priya Sharma', 'Amit Singh'],
        'email': [
            'rahul.kumar@email.com',      # Rahul - 5 orders
            'priya.sharma@email.com',      # Priya - 3 orders
            'RAHUL.KUMAR@EMAIL.COM',       # Rahul duplicate (caps) - 6 orders (KEEP THIS)
            'Priya.Sharma@Email.Com',      # Priya duplicate (mixed) - 7 orders (KEEP THIS)
            'amit.singh@email.com',        # Amit - unique
        ],
        'total_orders': [5, 3, 6, 7, 2],
        'total_spent': [2500.0, 1800.0, 3100.0, 3500.0, 900.0],
    })


@pytest.fixture
def sample_data_no_duplicates():
    """Create sample data with no duplicates."""
    return pd.DataFrame({
        'customer_id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'email': ['alice@test.com', 'bob@test.com', 'charlie@test.com'],
        'total_orders': [10, 20, 30],
    })


@pytest.fixture
def student_module(student_folder):
    """Import the student's clean_data module."""
    if not student_folder:
        pytest.skip("Student folder not provided")

    module_path = Path(student_folder) / "submissions"
    clean_data_file = module_path / "clean_data.py"

    if not clean_data_file.exists():
        pytest.fail(
            f"clean_data.py not found at {clean_data_file}\n\n"
            "Create the file with your remove_duplicates() function:\n"
            "  submissions/clean_data.py"
        )

    # Add to path and import
    sys.path.insert(0, str(module_path))
    try:
        import clean_data
        return clean_data
    except ImportError as e:
        pytest.fail(f"Could not import clean_data.py: {e}")
    except SyntaxError as e:
        pytest.fail(f"Syntax error in clean_data.py: {e}")


class TestFunctionExists:
    """Verify the remove_duplicates function exists."""

    def test_module_has_remove_duplicates(self, student_module):
        """clean_data.py must have a remove_duplicates function."""
        assert hasattr(student_module, 'remove_duplicates'), (
            "clean_data.py must define a function called 'remove_duplicates'.\n\n"
            "Expected signature:\n"
            "  def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:"
        )

    def test_remove_duplicates_is_callable(self, student_module):
        """remove_duplicates must be a callable function."""
        assert callable(student_module.remove_duplicates), (
            "'remove_duplicates' exists but is not a function.\n"
            "Make sure it's defined as: def remove_duplicates(df):"
        )


class TestBasicFunctionality:
    """Test that remove_duplicates works correctly."""

    def test_returns_dataframe(self, student_module, sample_data_with_duplicates):
        """Function must return a pandas DataFrame."""
        result = student_module.remove_duplicates(sample_data_with_duplicates)

        assert isinstance(result, pd.DataFrame), (
            f"remove_duplicates() returned {type(result).__name__}, expected DataFrame.\n"
            "Make sure your function returns a pandas DataFrame."
        )

    def test_removes_duplicate_emails(self, student_module, sample_data_with_duplicates):
        """Function must remove duplicate emails (case-insensitive)."""
        result = student_module.remove_duplicates(sample_data_with_duplicates)

        # Original has 5 rows, 2 duplicates (Rahul x2, Priya x2, Amit x1)
        # After dedup: should have 3 unique customers
        assert len(result) == 3, (
            f"Expected 3 unique customers, got {len(result)}.\n\n"
            "The sample data has:\n"
            "  - Rahul Kumar: 2 records with different email casings\n"
            "  - Priya Sharma: 2 records with different email casings\n"
            "  - Amit Singh: 1 record (unique)\n\n"
            "Your function should identify duplicates by email (case-insensitive)."
        )

    def test_keeps_highest_total_orders(self, student_module, sample_data_with_duplicates):
        """Function must keep record with highest total_orders for each duplicate."""
        result = student_module.remove_duplicates(sample_data_with_duplicates)

        # Normalize emails for checking
        # Check Rahul was kept with 6 orders (not 5)
        rahul_rows = result[result['email'].str.lower() == 'rahul.kumar@email.com']
        assert len(rahul_rows) == 1, "Should have exactly one Rahul record"
        assert rahul_rows.iloc[0]['total_orders'] == 6, (
            f"Kept Rahul with {rahul_rows.iloc[0]['total_orders']} orders, expected 6.\n"
            "When duplicates exist, keep the record with HIGHEST total_orders."
        )

        # Check Priya was kept with 7 orders (not 3)
        priya_rows = result[result['email'].str.lower() == 'priya.sharma@email.com']
        assert len(priya_rows) == 1, "Should have exactly one Priya record"
        assert priya_rows.iloc[0]['total_orders'] == 7, (
            f"Kept Priya with {priya_rows.iloc[0]['total_orders']} orders, expected 7.\n"
            "When duplicates exist, keep the record with HIGHEST total_orders."
        )


class TestEdgeCases:
    """Test edge cases and robustness."""

    def test_handles_no_duplicates(self, student_module, sample_data_no_duplicates):
        """Function should preserve all rows when there are no duplicates."""
        result = student_module.remove_duplicates(sample_data_no_duplicates)

        assert len(result) == len(sample_data_no_duplicates), (
            f"With no duplicates, expected {len(sample_data_no_duplicates)} rows, got {len(result)}.\n"
            "Function should return all rows when there are no duplicates."
        )

    def test_handles_empty_dataframe(self, student_module):
        """Function should handle empty DataFrame gracefully."""
        empty_df = pd.DataFrame({
            'customer_id': [],
            'email': [],
            'total_orders': [],
        })

        try:
            result = student_module.remove_duplicates(empty_df)
            assert len(result) == 0, "Empty input should return empty output"
        except Exception as e:
            pytest.fail(f"Function crashed on empty DataFrame: {e}")

    def test_preserves_all_columns(self, student_module, sample_data_with_duplicates):
        """Function must preserve all original columns."""
        result = student_module.remove_duplicates(sample_data_with_duplicates)

        original_cols = set(sample_data_with_duplicates.columns)
        result_cols = set(result.columns)

        assert result_cols == original_cols, (
            f"Output columns don't match input.\n"
            f"Missing: {original_cols - result_cols}\n"
            f"Extra: {result_cols - original_cols}"
        )

    def test_handles_single_row(self, student_module):
        """Function should handle single-row DataFrame."""
        single_row = pd.DataFrame({
            'customer_id': [1],
            'email': ['test@test.com'],
            'total_orders': [5],
        })

        result = student_module.remove_duplicates(single_row)
        assert len(result) == 1, "Single row should return single row"


class TestDataIntegrity:
    """Verify data integrity is maintained."""

    def test_does_not_modify_input(self, student_module, sample_data_with_duplicates):
        """Function should not modify the input DataFrame."""
        original_copy = sample_data_with_duplicates.copy()

        _ = student_module.remove_duplicates(sample_data_with_duplicates)

        assert sample_data_with_duplicates.equals(original_copy), (
            "Function modified the input DataFrame!\n"
            "Your function should not alter the original. Use df = df.copy() first."
        )

    def test_result_has_unique_emails(self, student_module, sample_data_with_duplicates):
        """Result should have no duplicate emails (case-insensitive)."""
        result = student_module.remove_duplicates(sample_data_with_duplicates)

        # Normalize and check for duplicates
        normalized_emails = result['email'].str.lower()
        duplicates = normalized_emails[normalized_emails.duplicated()]

        assert len(duplicates) == 0, (
            f"Result still has duplicate emails: {duplicates.tolist()}\n"
            "All emails should be unique (case-insensitive) after deduplication."
        )
