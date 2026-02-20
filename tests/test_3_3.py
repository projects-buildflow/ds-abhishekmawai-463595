"""Tests for Task 3.3: Query Optimization

Validates the optimized SQL query and optimization notes.
Executes both original and optimized queries to verify correctness,
then compares execution time on 50x-scaled data.
"""

import pytest
import re
import time
from pathlib import Path


@pytest.fixture
def submissions_path(student_folder):
    """Get path to student's submissions folder."""
    if not student_folder:
        pytest.skip("Student folder not provided")
    return Path(student_folder) / "submissions"


@pytest.fixture
def optimized_sql_path(submissions_path):
    """Path to the optimized query file."""
    return submissions_path / "optimized_query.sql"


@pytest.fixture
def notes_path(submissions_path):
    """Path to the optimization notes file."""
    return submissions_path / "optimization_notes.md"


@pytest.fixture
def optimized_sql(optimized_sql_path):
    """Load the optimized SQL query."""
    if not optimized_sql_path.exists():
        pytest.fail(
            f"SQL file not found at {optimized_sql_path}\n\n"
            "Create: submissions/optimized_query.sql"
        )
    return optimized_sql_path.read_text()


@pytest.fixture
def optimization_notes(notes_path):
    """Load the optimization notes."""
    if not notes_path.exists():
        pytest.fail(
            f"Notes file not found at {notes_path}\n\n"
            "Create: submissions/optimization_notes.md"
        )
    return notes_path.read_text()


@pytest.fixture
def original_sql(student_folder):
    """Load the original slow query."""
    slow_path = Path(student_folder) / "data" / "slow_query.sql"
    if not slow_path.exists():
        pytest.skip("Original slow_query.sql not found in data/")
    return slow_path.read_text()


class TestFilesExist:
    """Verify required files exist."""

    def test_optimized_sql_exists(self, optimized_sql_path):
        """optimized_query.sql must exist."""
        assert optimized_sql_path.exists(), (
            f"SQL file not found at {optimized_sql_path}\n\n"
            "Create: submissions/optimized_query.sql"
        )

    def test_optimization_notes_exist(self, notes_path):
        """optimization_notes.md must exist."""
        assert notes_path.exists(), (
            f"Notes file not found at {notes_path}\n\n"
            "Create: submissions/optimization_notes.md"
        )


class TestQueryContent:
    """Verify the optimized query has valid content."""

    def test_query_has_substance(self, optimized_sql):
        """Query must have meaningful content."""
        assert len(optimized_sql.strip()) > 50, (
            "Optimized query file is too short.\n"
            "Write a complete, optimized SQL query."
        )

    def test_query_is_valid_sql(self, optimized_sql):
        """Query must have valid SQL structure."""
        sql_lower = optimized_sql.lower()
        assert 'select' in sql_lower, "Query must have a SELECT statement."
        assert 'from' in sql_lower, "Query must have a FROM clause."


class TestExecution:
    """Execute both queries and compare results."""

    def test_optimized_query_executes(self, optimized_sql, run_sql):
        """Optimized query must execute without errors."""
        try:
            df = run_sql(optimized_sql)
        except Exception as e:
            pytest.fail(
                f"Optimized query failed to execute:\n{e}\n\n"
                "Make sure your SQL is valid and uses the correct "
                "table/column names (customers, orders, order_items, "
                "products, categories)."
            )
        assert len(df) > 0, (
            "Optimized query returned no rows.\n"
            "It should return the same results as the original query."
        )

    def test_same_row_count(self, optimized_sql, original_sql, run_sql):
        """Optimized query must return the same number of rows."""
        try:
            df_orig = run_sql(original_sql)
            df_opt = run_sql(optimized_sql)
        except Exception as e:
            pytest.skip(f"Could not execute both queries: {e}")

        assert len(df_opt) == len(df_orig), (
            f"Row count mismatch: original={len(df_orig)}, "
            f"optimized={len(df_opt)}.\n"
            "Your optimized query must return the same results."
        )

    def test_same_customers(self, optimized_sql, original_sql, run_sql):
        """Optimized query must return the same customer_ids."""
        try:
            df_orig = run_sql(original_sql)
            df_opt = run_sql(optimized_sql)
        except Exception as e:
            pytest.skip(f"Could not execute both queries: {e}")

        if 'customer_id' not in df_orig.columns or 'customer_id' not in df_opt.columns:
            pytest.skip("customer_id column not found in results")

        orig_ids = set(df_orig['customer_id'])
        opt_ids = set(df_opt['customer_id'])
        assert orig_ids == opt_ids, (
            f"Customer mismatch.\n"
            f"Original has {len(orig_ids)} unique customers, "
            f"optimized has {len(opt_ids)}.\n"
            f"Missing from optimized: {orig_ids - opt_ids or 'none'}\n"
            f"Extra in optimized: {opt_ids - orig_ids or 'none'}\n\n"
            "Your optimized query must return the same customers."
        )

    def test_query_is_different(self, optimized_sql, original_sql):
        """Optimized query must differ from the original."""
        def normalize(s):
            return re.sub(r'\s+', ' ', s.strip().lower())

        assert normalize(optimized_sql) != normalize(original_sql), (
            "Your optimized query is identical to the original.\n"
            "You need to actually optimize it -- remove anti-patterns like\n"
            "nested subqueries, SELECT *, and correlated ORDER BY."
        )

    def test_optimized_is_faster(self, optimized_sql, original_sql, duckdb_conn_large):
        """Optimized query must run faster than original on scaled data."""
        RUNS = 3
        REQUIRED_SPEEDUP = 1.15

        def median_time(conn, sql):
            times = []
            for _ in range(RUNS):
                start = time.perf_counter()
                conn.execute(sql).fetchall()
                times.append(time.perf_counter() - start)
            return sorted(times)[RUNS // 2]

        try:
            t_slow = median_time(duckdb_conn_large, original_sql)
            t_fast = median_time(duckdb_conn_large, optimized_sql)
        except Exception as e:
            pytest.skip(f"Could not run timing comparison: {e}")

        speedup = t_slow / t_fast if t_fast > 0 else 0
        assert speedup >= REQUIRED_SPEEDUP, (
            f"Optimized query is not faster enough.\n"
            f"Original: {t_slow*1000:.0f}ms, Optimized: {t_fast*1000:.0f}ms "
            f"(speedup: {speedup:.2f}x, need {REQUIRED_SPEEDUP}x).\n\n"
            "Your query should use JOINs instead of nested subqueries,\n"
            "avoid SELECT *, and remove the correlated ORDER BY subquery."
        )


class TestNotes:
    """Verify optimization notes explain the changes."""

    def test_notes_have_substance(self, optimization_notes):
        """Notes must have at least 100 words."""
        word_count = len(optimization_notes.split())
        assert word_count >= 100, (
            f"Notes have only {word_count} words.\n"
            "Explain:\n"
            "- What made the original query slow\n"
            "- What changes you made\n"
            "- Why your changes improve performance"
        )

    def test_notes_explain_optimizations(self, optimization_notes):
        """Notes should mention specific optimization techniques."""
        content = optimization_notes.lower()
        techniques = [
            'join', 'cte', 'common table', 'subquer', 'index',
            'select *', 'column', 'correlat', 'nest', 'where',
            'date(', 'function', 'sarg',
        ]
        matches = [t for t in techniques if t in content]
        assert len(matches) >= 2, (
            f"Notes should discuss specific optimization techniques.\n"
            "Mention what you changed: JOINs vs subqueries, "
            "explicit columns vs SELECT *, avoiding DATE() on columns, etc."
        )
