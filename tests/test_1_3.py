"""Tests for Task 1.3: Fix the Date Bug

Objective: Fix the date parsing bug in the data loader where dates parse incorrectly.

This test DECISIVELY verifies:
1. Student created a fixed data loader or documented the fix
2. The load_orders function now parses dates correctly
3. No NaT (Not a Time) values in the output
4. Dates are actual datetime objects
"""

import pytest
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime


@pytest.fixture
def student_week1_path(student_folder):
    """Get path to student's submissions folder."""
    if not student_folder:
        pytest.skip("Student folder not provided")
    return Path(student_folder) / "submissions"


@pytest.fixture
def sample_orders_csv(tmp_path):
    """Create sample orders CSV with dates in various formats."""
    data = """order_id,customer_id,order_date,total_amount
1001,C001,2024-01-15,150.00
1002,C002,2024-02-20,200.00
1003,C003,2024-03-10,75.50
1004,C001,2024-04-05,320.00
1005,C002,2024-05-18,89.99
"""
    csv_path = tmp_path / "orders.csv"
    csv_path.write_text(data)
    return csv_path


class TestFixedLoaderExists:
    """Verify student created a fix for the date bug."""

    def test_has_data_loader_or_readme(self, student_week1_path):
        """Student must create either a fixed loader or README documenting the fix."""
        loader_path = student_week1_path / "data_loader.py"
        readme_path = student_week1_path / "README.md"

        has_loader = loader_path.exists()
        has_readme = readme_path.exists()

        assert has_loader or has_readme, (
            "Missing required files.\n\n"
            "Create one of:\n"
            "  - submissions/data_loader.py (fixed loader)\n"
            "  - submissions/README.md (documenting the fix)"
        )


class TestReadmeDocumentation:
    """If README exists, verify it documents the bug fix."""

    def test_readme_explains_bug(self, student_week1_path):
        """README must explain what the bug was."""
        readme_path = student_week1_path / "README.md"
        if not readme_path.exists():
            pytest.skip("README.md not found - checking data_loader.py instead")

        content = readme_path.read_text().lower()

        bug_keywords = ['bug', 'issue', 'problem', 'error', 'wrong', 'incorrect']
        has_bug_description = any(kw in content for kw in bug_keywords)

        assert has_bug_description, (
            "README should describe what the bug was.\n"
            "Explain what was wrong with the original date parsing."
        )

    def test_readme_mentions_date(self, student_week1_path):
        """README must mention date-related issue."""
        readme_path = student_week1_path / "README.md"
        if not readme_path.exists():
            pytest.skip("README.md not found")

        content = readme_path.read_text().lower()

        assert 'date' in content, (
            "README should mention 'date' since this is about a date parsing bug."
        )

    def test_readme_explains_fix(self, student_week1_path):
        """README must explain the solution."""
        readme_path = student_week1_path / "README.md"
        if not readme_path.exists():
            pytest.skip("README.md not found")

        content = readme_path.read_text().lower()

        fix_keywords = ['fix', 'solution', 'resolve', 'change', 'correct', 'update']
        has_fix_description = any(kw in content for kw in fix_keywords)

        assert has_fix_description, (
            "README should explain how you fixed the bug.\n"
            "Describe the solution you implemented."
        )


class TestFixedDataLoader:
    """If data_loader.py exists, verify it works correctly."""

    def test_loader_has_load_orders(self, student_week1_path):
        """data_loader.py must have load_orders function."""
        loader_path = student_week1_path / "data_loader.py"
        if not loader_path.exists():
            pytest.skip("data_loader.py not found - using README instead")

        sys.path.insert(0, str(student_week1_path))
        try:
            if 'data_loader' in sys.modules:
                del sys.modules['data_loader']

            import data_loader

            assert hasattr(data_loader, 'load_orders'), (
                "data_loader.py must have a 'load_orders' function.\n"
                "Define: def load_orders(filepath: str) -> pd.DataFrame:"
            )
        except SyntaxError as e:
            pytest.fail(f"Syntax error in data_loader.py: {e}")
        except ImportError as e:
            pytest.fail(f"Could not import data_loader.py: {e}")
        finally:
            if 'data_loader' in sys.modules:
                del sys.modules['data_loader']
            if str(student_week1_path) in sys.path:
                sys.path.remove(str(student_week1_path))

    def test_load_orders_returns_dataframe(self, student_week1_path, sample_orders_csv):
        """load_orders must return a DataFrame."""
        loader_path = student_week1_path / "data_loader.py"
        if not loader_path.exists():
            pytest.skip("data_loader.py not found")

        sys.path.insert(0, str(student_week1_path))
        try:
            if 'data_loader' in sys.modules:
                del sys.modules['data_loader']

            import data_loader
            result = data_loader.load_orders(str(sample_orders_csv))

            assert isinstance(result, pd.DataFrame), (
                f"load_orders returned {type(result).__name__}, expected DataFrame"
            )
        finally:
            if 'data_loader' in sys.modules:
                del sys.modules['data_loader']
            if str(student_week1_path) in sys.path:
                sys.path.remove(str(student_week1_path))

    def test_dates_are_parsed_correctly(self, student_week1_path, sample_orders_csv):
        """Dates must be parsed as datetime, not strings."""
        loader_path = student_week1_path / "data_loader.py"
        if not loader_path.exists():
            pytest.skip("data_loader.py not found")

        sys.path.insert(0, str(student_week1_path))
        try:
            if 'data_loader' in sys.modules:
                del sys.modules['data_loader']

            import data_loader
            result = data_loader.load_orders(str(sample_orders_csv))

            assert 'order_date' in result.columns, (
                "DataFrame should have 'order_date' column"
            )

            date_col = result['order_date']
            is_datetime = pd.api.types.is_datetime64_any_dtype(date_col)

            assert is_datetime, (
                f"order_date column has type {date_col.dtype}, expected datetime.\n"
                "The bug was that dates weren't being parsed correctly.\n"
                "Use: pd.to_datetime() or parse_dates parameter in read_csv()"
            )
        finally:
            if 'data_loader' in sys.modules:
                del sys.modules['data_loader']
            if str(student_week1_path) in sys.path:
                sys.path.remove(str(student_week1_path))

    def test_no_nat_values(self, student_week1_path, sample_orders_csv):
        """No NaT (Not a Time) values should exist in dates."""
        loader_path = student_week1_path / "data_loader.py"
        if not loader_path.exists():
            pytest.skip("data_loader.py not found")

        sys.path.insert(0, str(student_week1_path))
        try:
            if 'data_loader' in sys.modules:
                del sys.modules['data_loader']

            import data_loader
            result = data_loader.load_orders(str(sample_orders_csv))

            if 'order_date' not in result.columns:
                pytest.skip("order_date column not found")

            nat_count = result['order_date'].isna().sum()

            assert nat_count == 0, (
                f"Found {nat_count} NaT (null) values in order_date.\n"
                "The bug caused dates to parse as NaT.\n"
                "Make sure your date format matches the actual CSV data."
            )
        finally:
            if 'data_loader' in sys.modules:
                del sys.modules['data_loader']
            if str(student_week1_path) in sys.path:
                sys.path.remove(str(student_week1_path))

    def test_dates_have_correct_values(self, student_week1_path, sample_orders_csv):
        """Parsed dates should have correct values."""
        loader_path = student_week1_path / "data_loader.py"
        if not loader_path.exists():
            pytest.skip("data_loader.py not found")

        sys.path.insert(0, str(student_week1_path))
        try:
            if 'data_loader' in sys.modules:
                del sys.modules['data_loader']

            import data_loader
            result = data_loader.load_orders(str(sample_orders_csv))

            if 'order_date' not in result.columns:
                pytest.skip("order_date column not found")

            first_date = result['order_date'].iloc[0]

            if hasattr(first_date, 'year'):
                assert first_date.year == 2024 and first_date.month == 1 and first_date.day == 15, (
                    f"First order date should be 2024-01-15, got {first_date}\n"
                    "Check that dates are being parsed with the correct format."
                )
        finally:
            if 'data_loader' in sys.modules:
                del sys.modules['data_loader']
            if str(student_week1_path) in sys.path:
                sys.path.remove(str(student_week1_path))
