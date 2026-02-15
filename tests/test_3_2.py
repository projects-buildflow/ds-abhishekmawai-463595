"""Tests for Task 3.2: SQL Cohort Analysis

Validates the cohort analysis SQL query for structure, correctness,
and execution against the actual data.
"""

import pytest
import re
from pathlib import Path


@pytest.fixture
def sql_path(student_folder):
    """Get path to the cohort analysis SQL file."""
    if not student_folder:
        pytest.skip("Student folder not provided")
    return Path(student_folder) / "submissions" / "cohort_analysis.sql"


@pytest.fixture
def sql_content(sql_path):
    """Load the student's SQL file content."""
    if not sql_path.exists():
        pytest.fail(
            f"SQL file not found at {sql_path}\n\n"
            "Create: submissions/cohort_analysis.sql"
        )
    return sql_path.read_text()


class TestStaticChecks:
    """Basic structural validation of the SQL file."""

    def test_sql_file_has_content(self, sql_content):
        """SQL file must have meaningful content."""
        assert len(sql_content.strip()) > 50, (
            "SQL file appears too short.\n"
            "Write a complete cohort analysis query."
        )

    def test_has_select_statement(self, sql_content):
        """Query must have a SELECT statement."""
        assert re.search(r'\bSELECT\b', sql_content, re.IGNORECASE), (
            "Missing SELECT statement.\n"
            "Your query should SELECT cohort columns and retention counts."
        )

    def test_has_group_by(self, sql_content):
        """Cohort analysis requires GROUP BY."""
        assert re.search(r'\bGROUP\s+BY\b', sql_content, re.IGNORECASE), (
            "Missing GROUP BY clause.\n"
            "Cohort analysis requires grouping by cohort month."
        )


class TestStructure:
    """Validate query uses appropriate techniques."""

    def test_uses_date_truncation(self, sql_content):
        """Query should extract month from dates."""
        content = sql_content.upper()
        has_month_extraction = any(pattern in content for pattern in [
            'DATE_TRUNC', 'STRFTIME', 'TO_CHAR', 'EXTRACT(',
            "FORMAT(", "DATEPART(", "DATE_FORMAT(",
            "SUBSTR(", "LEFT(",
        ])
        assert has_month_extraction, (
            "Query should extract month from order dates.\n\n"
            "Use DATE_TRUNC('month', order_date) or equivalent\n"
            "to group customers into monthly cohorts."
        )

    def test_counts_distinct_customers(self, sql_content):
        """Query should count distinct customers."""
        content = sql_content.lower()
        has_count = 'count(' in content and (
            'distinct' in content or 'customer' in content
        )
        assert has_count, (
            "Query should COUNT DISTINCT customers for retention.\n\n"
            "Use: COUNT(DISTINCT customer_id)"
        )


class TestExecution:
    """Execute the query against DuckDB and validate results."""

    def test_query_executes(self, sql_content, run_sql):
        """Query must execute without errors."""
        try:
            df = run_sql(sql_content)
        except Exception as e:
            pytest.fail(
                f"Query failed to execute:\n{e}\n\n"
                "Make sure your SQL is valid and references the correct "
                "table/column names (customers, orders, order_items, etc.)."
            )
        assert len(df) > 0, (
            "Query returned no rows.\n"
            "Your cohort analysis should return at least one cohort."
        )

    def test_has_cohort_column(self, sql_content, run_sql):
        """Results must have a cohort month column."""
        df = run_sql(sql_content)
        cols_lower = [c.lower() for c in df.columns]
        has_cohort = any(
            'cohort' in c or 'month' in c or 'period' in c
            for c in cols_lower
        )
        assert has_cohort, (
            f"Expected a cohort/month column. Found: {list(df.columns)}\n\n"
            "Name your cohort column something like 'cohort_month'."
        )

    def test_has_retention_columns(self, sql_content, run_sql):
        """Results must have retention period columns (month_0, month_1, etc.)."""
        df = run_sql(sql_content)
        cols_lower = [c.lower() for c in df.columns]
        retention_pattern = re.compile(r'(month|m|period|p|retention)[\s_]?[0-5]')
        retention_cols = [c for c in cols_lower if retention_pattern.search(c)]
        assert len(retention_cols) >= 2, (
            f"Expected retention columns (month_0, month_1, ...). Found: {list(df.columns)}\n\n"
            "Your output should have columns like month_0, month_1, ... month_5\n"
            "showing how many customers from each cohort returned."
        )

    def test_retention_decreases(self, sql_content, run_sql):
        """Month 0 retention should be >= month 1 (sanity check)."""
        df = run_sql(sql_content)
        cols_lower = {c.lower(): c for c in df.columns}

        retention_pattern = re.compile(r'(month|m|period|p|retention)[\s_]?(\d)')
        col_map = {}
        for col_lower, col_orig in cols_lower.items():
            match = retention_pattern.search(col_lower)
            if match:
                col_map[int(match.group(2))] = col_orig

        if 0 not in col_map or 1 not in col_map:
            pytest.skip("Could not identify month_0 and month_1 columns")

        m0 = df[col_map[0]].dropna()
        m1 = df[col_map[1]].dropna()
        if len(m0) == 0 or len(m1) == 0:
            pytest.skip("Retention columns are empty")

        assert m0.sum() >= m1.sum(), (
            f"Month 0 total ({m0.sum()}) should be >= Month 1 total ({m1.sum()}).\n"
            "Retention typically decreases over time. Check your logic."
        )

    def test_returns_multiple_cohorts(self, sql_content, run_sql):
        """Query should return multiple cohort rows."""
        df = run_sql(sql_content)
        assert len(df) >= 3, (
            f"Query returned only {len(df)} row(s).\n"
            "A cohort analysis should show multiple monthly cohorts (at least 3)."
        )
