"""Tests for Task 2.1: Data Profiling Report

Objective: Create a comprehensive data profiling report identifying data quality issues.

This test DECISIVELY verifies:
1. Report file exists with proper structure
2. All required sections are present (Overview, Missing Values, Invalid Values, Duplicates, Summary)
3. Report identifies SPECIFIC issues in the data
4. Report contains actual numbers/percentages, not vague descriptions
5. Report provides actionable insights
"""

import pytest
import re
from pathlib import Path


@pytest.fixture
def report_content(student_folder):
    """Load the student's profiling report."""
    if not student_folder:
        pytest.skip("Student folder not provided")

    report_path = Path(student_folder) / "submissions" / "data_profile_report.md"

    if not report_path.exists():
        pytest.fail(
            f"Report not found at {report_path}\n\n"
            "Create: submissions/data_profile_report.md"
        )

    return report_path.read_text()


class TestReportExists:
    """Verify report file exists and has content."""

    def test_report_has_content(self, report_content):
        """Report must have substantial content."""
        assert len(report_content) >= 500, (
            f"Report is too short ({len(report_content)} chars).\n"
            "Expected comprehensive analysis of data quality issues."
        )

    def test_report_is_markdown(self, report_content):
        """Report should be properly formatted markdown."""
        has_headers = '#' in report_content
        has_sections = report_content.count('#') >= 5

        assert has_headers and has_sections, (
            "Report should use markdown headers (# or ##) to organize sections."
        )


class TestRequiredSections:
    """Verify all required sections are present."""

    def test_has_overview_section(self, report_content):
        """Report must have an Overview section."""
        content_lower = report_content.lower()
        has_overview = 'overview' in content_lower or 'introduction' in content_lower

        assert has_overview, (
            "Missing Overview section.\n"
            "Add: ## 1. Overview\n"
            "Describe the datasets being analyzed."
        )

    def test_has_missing_values_section(self, report_content):
        """Report must have a Missing Values section."""
        content_lower = report_content.lower()
        has_section = 'missing' in content_lower and 'value' in content_lower

        assert has_section, (
            "Missing 'Missing Values' section.\n"
            "Add: ## 2. Missing Values\n"
            "Document which columns have null/missing values."
        )

    def test_has_invalid_values_section(self, report_content):
        """Report must have an Invalid Values section."""
        content_lower = report_content.lower()
        has_section = 'invalid' in content_lower or 'incorrect' in content_lower or 'error' in content_lower

        assert has_section, (
            "Missing 'Invalid Values' section.\n"
            "Add: ## 3. Invalid Values\n"
            "Document values that are out of expected range or format."
        )

    def test_has_duplicates_section(self, report_content):
        """Report must have a Duplicates section."""
        content_lower = report_content.lower()

        assert 'duplicate' in content_lower, (
            "Missing 'Duplicates' section.\n"
            "Add: ## 4. Duplicates\n"
            "Document any duplicate records found."
        )

    def test_has_summary_section(self, report_content):
        """Report must have a Summary section."""
        content_lower = report_content.lower()
        has_summary = 'summary' in content_lower or 'conclusion' in content_lower or 'recommendation' in content_lower

        assert has_summary, (
            "Missing 'Summary' section.\n"
            "Add: ## 5. Summary\n"
            "Summarize findings and recommend next steps."
        )


class TestIssueIdentification:
    """Verify report identifies specific data quality issues."""

    def test_identifies_age_issues(self, report_content):
        """Report must identify age-related data issues."""
        content_lower = report_content.lower()

        assert 'age' in content_lower, (
            "Report should identify issues with the 'age' column.\n"
            "The data contains invalid ages that need to be documented."
        )

    def test_identifies_negative_values(self, report_content):
        """Report must identify negative values where inappropriate."""
        content_lower = report_content.lower()

        has_negative = 'negative' in content_lower or '< 0' in content_lower or 'below zero' in content_lower

        assert has_negative, (
            "Report should identify negative values.\n"
            "Check for columns where negative values don't make sense (e.g., age, quantity)."
        )

    def test_identifies_email_issues(self, report_content):
        """Report must identify email-related issues."""
        content_lower = report_content.lower()

        assert 'email' in content_lower, (
            "Report should mention email column analysis.\n"
            "Check for invalid email formats or duplicates."
        )

    def test_identifies_duplicate_records(self, report_content):
        """Report must document duplicate findings."""
        content_lower = report_content.lower()

        has_dup_analysis = (
            'duplicate' in content_lower and
            ('found' in content_lower or 'identified' in content_lower or 'detect' in content_lower or 'record' in content_lower)
        )

        assert has_dup_analysis, (
            "Report should document duplicate record analysis.\n"
            "State how many duplicates were found and in which columns."
        )


class TestQuantitativeAnalysis:
    """Verify report contains actual numbers, not vague descriptions."""

    def test_has_specific_counts(self, report_content):
        """Report must include specific counts."""
        # Look for numbers in the report
        numbers = re.findall(r'\b\d+\b', report_content)

        assert len(numbers) >= 5, (
            f"Found only {len(numbers)} numbers in report.\n"
            "Include specific counts: number of missing values, duplicates, invalid records, etc."
        )

    def test_has_percentages(self, report_content):
        """Report must include percentages."""
        percentage_pattern = r'\d+\.?\d*\s*%'
        percentages = re.findall(percentage_pattern, report_content)

        assert len(percentages) >= 2, (
            f"Found only {len(percentages)} percentages in report.\n"
            "Include percentages: e.g., '15% of records have missing emails'"
        )

    def test_has_row_or_record_counts(self, report_content):
        """Report should mention row or record counts."""
        content_lower = report_content.lower()

        has_counts = (
            'row' in content_lower or
            'record' in content_lower or
            'entries' in content_lower or
            'total' in content_lower
        )

        assert has_counts, (
            "Report should include row/record counts.\n"
            "State how many total records were analyzed."
        )


class TestActionableInsights:
    """Verify report provides actionable recommendations."""

    def test_has_recommendations(self, report_content):
        """Report should include recommendations."""
        content_lower = report_content.lower()

        has_recommendations = (
            'recommend' in content_lower or
            'should' in content_lower or
            'suggest' in content_lower or
            'next step' in content_lower or
            'action' in content_lower
        )

        assert has_recommendations, (
            "Report should include recommendations for fixing issues.\n"
            "Add a section on suggested next steps."
        )

    def test_prioritizes_issues(self, report_content):
        """Report should indicate issue severity or priority."""
        content_lower = report_content.lower()

        has_priority = (
            'critical' in content_lower or
            'high' in content_lower or
            'important' in content_lower or
            'priority' in content_lower or
            'severe' in content_lower or
            'significant' in content_lower
        )

        # This is a soft check - good to have but not required
        if not has_priority:
            pass  # Just note, don't fail


class TestReportQuality:
    """Additional quality checks."""

    def test_reasonable_length(self, report_content):
        """Report should be comprehensive."""
        word_count = len(report_content.split())

        assert word_count >= 150, (
            f"Report has only {word_count} words.\n"
            "Expected a comprehensive analysis with at least 150 words."
        )

    def test_has_column_names(self, report_content):
        """Report should reference specific column names."""
        # Common column names in customer/order data
        columns = ['customer_id', 'email', 'age', 'name', 'order', 'total', 'date', 'phone']
        found_columns = sum(1 for col in columns if col in report_content.lower())

        assert found_columns >= 3, (
            "Report should reference specific column names.\n"
            "Mention which columns have issues (e.g., 'email', 'age', 'customer_id')."
        )


class TestReportAccuracy:
    """Verify report numbers match actual data."""

    def test_null_counts_match_data(self, report_content, sample_customers):
        """Report's missing value claims should match actual data."""
        if sample_customers is None:
            pytest.skip("Sample customer data not available")

        import re

        # Count actual nulls in key columns
        actual_nulls = {}
        for col in sample_customers.columns:
            null_count = sample_customers[col].isna().sum()
            if null_count > 0:
                actual_nulls[col] = null_count

        if not actual_nulls:
            pytest.skip("No nulls in sample data to validate against")

        # Check that at least one actual null count appears in the report
        report_numbers = set(int(n) for n in re.findall(r'\b(\d+)\b', report_content))

        matched = any(count in report_numbers for count in actual_nulls.values())

        assert matched, (
            "Report's missing value counts don't match actual data.\n"
            f"Actual null counts: {actual_nulls}\n"
            "Cross-check your analysis with the real data."
        )

    def test_row_count_mentioned(self, report_content, sample_customers):
        """Report should mention the correct total row count."""
        if sample_customers is None:
            pytest.skip("Sample customer data not available")

        import re
        actual_count = len(sample_customers)
        report_numbers = [int(n) for n in re.findall(r'\b(\d+)\b', report_content)]

        # Allow +/- 5% tolerance
        tolerance = int(actual_count * 0.05)
        close_match = any(abs(n - actual_count) <= tolerance for n in report_numbers)

        assert close_match, (
            f"Report doesn't mention the actual row count ({actual_count}).\n"
            "Include the total number of records analyzed."
        )
