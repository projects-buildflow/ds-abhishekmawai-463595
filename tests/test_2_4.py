"""Tests for Task 2.4: Code Review Guidelines

Validates code review checklist for data cleaning pipelines.
"""

import pytest
import re
from pathlib import Path


@pytest.fixture
def checklist_path(student_folder):
    """Get path to the code review checklist file."""
    if not student_folder:
        pytest.skip("Student folder not provided")
    return Path(student_folder) / "submissions" / "code_review_checklist.md"


@pytest.fixture
def checklist_content(checklist_path):
    """Load checklist content."""
    if not checklist_path.exists():
        pytest.fail(
            f"Checklist not found at {checklist_path}\n\n"
            "Create: submissions/code_review_checklist.md"
        )
    return checklist_path.read_text()


class TestChecklistExists:
    """Verify the checklist file exists and has content."""

    def test_checklist_file_exists(self, checklist_path):
        """Checklist file must exist at the correct path."""
        assert checklist_path.exists(), (
            "Checklist not found.\n"
            "Create: submissions/code_review_checklist.md"
        )

    def test_checklist_has_substantial_content(self, checklist_content):
        """Checklist must have substantial content - not a placeholder."""
        word_count = len(checklist_content.split())
        assert word_count >= 200, (
            f"Checklist has only {word_count} words.\n"
            "A useful code review checklist needs at least 200 words."
        )


class TestChecklistItems:
    """Verify checklist has enough actionable items."""

    def test_has_at_least_15_checkbox_items(self, checklist_content):
        """Checklist must have at least 15 checkbox items."""
        checkbox_pattern = r'[-*]\s*\[\s*[xX\s]?\s*\]'
        checkboxes = re.findall(checkbox_pattern, checklist_content)
        assert len(checkboxes) >= 15, (
            f"Found only {len(checkboxes)} checklist items.\n"
            "A comprehensive code review checklist needs at least 15 items.\n\n"
            "Format items like:\n"
            "- [ ] Are null values handled before operations that fail on nulls?\n"
            "- [ ] Is there a check for duplicate records after cleaning?"
        )


class TestCategoryPresence:
    """Verify all 5 required categories are covered."""

    def _content_lower(self, checklist_content):
        return checklist_content.lower()

    def test_has_correctness_category(self, checklist_content):
        """Checklist must cover data correctness."""
        text = checklist_content.lower()
        assert any(term in text for term in [
            "correctness", "correct", "accuracy", "accurate",
            "input validation", "output validation", "output verification",
        ]), (
            "Missing 'Correctness' category.\n"
            "Add a section about data correctness checks "
            "(input validation, transformation logic, output verification)."
        )

    def test_has_robustness_category(self, checklist_content):
        """Checklist must cover error handling / robustness."""
        text = checklist_content.lower()
        assert any(term in text for term in [
            "robust", "error handling", "edge case", "exception",
            "null", "missing value", "empty",
        ]), (
            "Missing 'Error Handling / Robustness' category.\n"
            "Add a section about edge cases, null values, and exception handling."
        )

    def test_has_readability_category(self, checklist_content):
        """Checklist must cover code readability / quality."""
        text = checklist_content.lower()
        assert any(term in text for term in [
            "readability", "readable", "naming", "documentation",
            "comment", "code quality", "code style",
        ]), (
            "Missing 'Readability' category.\n"
            "Add a section about naming conventions, comments, and documentation."
        )

    def test_has_performance_category(self, checklist_content):
        """Checklist must cover performance."""
        text = checklist_content.lower()
        assert any(term in text for term in [
            "performance", "efficient", "efficiency", "memory",
            "scalab", "optimiz",
        ]), (
            "Missing 'Performance' category.\n"
            "Add a section about efficiency, memory usage, and scalability."
        )

    def test_has_testing_category(self, checklist_content):
        """Checklist must cover testing."""
        text = checklist_content.lower()
        assert any(term in text for term in [
            "testing", "test coverage", "unit test", "test case",
            "test data",
        ]), (
            "Missing 'Testing' category.\n"
            "Add a section about unit tests, test coverage, and test data."
        )


class TestCommonIssues:
    """Verify checklist includes common issues with examples."""

    def test_has_common_issues_section(self, checklist_content):
        """Checklist must have a common issues section."""
        text = checklist_content.lower()
        assert any(term in text for term in [
            "common issue", "common mistake", "common error",
            "common problem", "watch for", "pitfall",
            "issue 1", "issue 2", "issue 3",
        ]), (
            "Missing 'Common Issues' section.\n"
            "Add at least 3 common data cleaning mistakes with examples."
        )

    def test_has_at_least_3_issues(self, checklist_content):
        """Checklist must describe at least 3 common issues."""
        text = checklist_content.lower()
        issue_markers = (
            len(re.findall(r'###\s+issue', text))
            or len(re.findall(r'(?:^|\n)\d+\.\s+\*\*', checklist_content))
            or len(re.findall(r'###\s+\d+', text))
            or len(re.findall(r'\*\*(?:problem|issue|mistake|error)\b', text))
        )
        # Fallback: count subsections under common issues area
        if issue_markers < 3:
            # Count h3/h4 headings after a "common" heading
            sections = re.split(r'^#{1,2}\s+', checklist_content, flags=re.MULTILINE)
            for section in sections:
                if any(kw in section.lower() for kw in ["common", "pitfall", "watch for"]):
                    sub_headings = re.findall(r'^#{3,4}\s+', section, flags=re.MULTILINE)
                    bold_items = re.findall(r'\*\*.+?\*\*', section)
                    issue_markers = max(issue_markers, len(sub_headings), len(bold_items))
                    break

        assert issue_markers >= 3, (
            f"Found only {issue_markers} common issues described.\n"
            "List at least 3 common data cleaning mistakes with examples.\n\n"
            "Example format:\n"
            "### Issue 1: Mutating the original DataFrame\n"
            "**Problem:** Cleaning modifies the input data...\n"
            "**What to look for:** Check for .copy() usage..."
        )


class TestDataCleaningSpecificity:
    """Verify items are specific to data cleaning, not generic."""

    def test_mentions_data_cleaning_concepts(self, checklist_content):
        """Checklist should reference data cleaning concepts from Tasks 2.1-2.3."""
        text = checklist_content.lower()
        data_terms = [
            "dataframe", "csv", "null", "nan", "missing",
            "duplicate", "validation", "schema", "cleaning",
            "column", "row", "data type", "dtype",
            "whitespace", "strip", "pandas", "pandera",
        ]
        matches = [t for t in data_terms if t in text]
        assert len(matches) >= 4, (
            f"Only found {len(matches)} data-specific terms: {matches}\n"
            "Checklist items should be specific to data cleaning pipelines, "
            "not generic code review.\n"
            "Reference concepts like DataFrames, null handling, duplicates, "
            "validation schemas, etc."
        )
