"""Tests for Task 1.4: Document the Fix - Troubleshooting Guide

Objective: Create a professional troubleshooting document for the date bug.

This test DECISIVELY verifies:
1. Document file exists at the correct path
2. Document has professional structure with required sections
3. Document explains the PROBLEM clearly (symptoms, impact)
4. Document identifies the ROOT CAUSE (why it happened)
5. Document describes the SOLUTION (how it was fixed)
6. Document includes PREVENTION tips (how to avoid in future)
7. Document includes code examples
8. Document is substantive (not a minimal effort)
"""

import pytest
import re
from pathlib import Path


@pytest.fixture
def doc_path(student_folder):
    """Get path to the troubleshooting document."""
    if not student_folder:
        pytest.skip("Student folder not provided")
    return Path(student_folder) / "submissions" / "troubleshooting_date_bug.md"


@pytest.fixture
def doc_content(doc_path):
    """Load the troubleshooting document content."""
    if not doc_path.exists():
        pytest.fail(
            f"Document not found at {doc_path}\n\n"
            "Create: submissions/troubleshooting_date_bug.md"
        )
    return doc_path.read_text()


class TestDocumentExists:
    """Verify the troubleshooting document exists and has substance."""

    def test_document_file_exists(self, doc_path):
        """Troubleshooting document must exist at the correct path."""
        assert doc_path.exists(), (
            f"Document not found at {doc_path}\n\n"
            "Create: submissions/troubleshooting_date_bug.md"
        )

    def test_document_has_substantial_content(self, doc_content):
        """Document must have substantial content - not a placeholder."""
        char_count = len(doc_content)
        word_count = len(doc_content.split())

        assert char_count >= 500, (
            f"Document is too short ({char_count} characters).\n"
            "Expected a detailed troubleshooting guide with all required sections."
        )

        assert word_count >= 150, (
            f"Document has only {word_count} words.\n"
            "A professional troubleshooting document needs more detail."
        )

    def test_document_is_markdown(self, doc_content):
        """Document should be properly formatted markdown."""
        has_headers = '#' in doc_content
        header_count = doc_content.count('#')

        assert has_headers, (
            "Document should use markdown headers (# or ##) to organize sections."
        )

        assert header_count >= 4, (
            f"Found only {header_count} headers. "
            "Use headers to separate: Problem, Root Cause, Solution, Prevention."
        )


class TestProblemDescription:
    """Verify document clearly describes the problem."""

    def test_has_problem_section(self, doc_content):
        """Document must have a section describing the problem/symptoms."""
        content_lower = doc_content.lower()

        problem_keywords = ['problem', 'issue', 'symptom', 'bug', 'error']
        has_problem = any(kw in content_lower for kw in problem_keywords)

        assert has_problem, (
            "Missing Problem/Symptoms section.\n"
            "Add: ## Problem\n"
            "Describe what users/developers experienced."
        )

    def test_describes_date_issue(self, doc_content):
        """Document must clearly mention this is a date-related issue."""
        content_lower = doc_content.lower()

        assert 'date' in content_lower, (
            "Document should clearly mention 'date' since this is about a date parsing bug."
        )

    def test_describes_specific_symptoms(self, doc_content):
        """Document should describe specific symptoms of the bug."""
        content_lower = doc_content.lower()

        symptom_indicators = [
            'nat', 'not a time', 'null', 'none', 'missing',
            'incorrect', 'wrong', 'parse', 'failed', 'invalid'
        ]
        found_symptoms = sum(1 for s in symptom_indicators if s in content_lower)

        assert found_symptoms >= 2, (
            "Document should describe specific symptoms.\n"
            "What happened when the bug occurred? (e.g., NaT values, incorrect dates)"
        )


class TestRootCause:
    """Verify document explains the root cause."""

    def test_has_root_cause_section(self, doc_content):
        """Document must explain WHY the bug happened."""
        content_lower = doc_content.lower()

        cause_keywords = ['cause', 'why', 'reason', 'because', 'root cause', 'origin']
        has_cause = any(kw in content_lower for kw in cause_keywords)

        assert has_cause, (
            "Missing Root Cause section.\n"
            "Add: ## Root Cause\n"
            "Explain WHY the bug happened (e.g., format mismatch, parsing logic error)."
        )

    def test_mentions_technical_cause(self, doc_content):
        """Document should mention technical details of what went wrong."""
        content_lower = doc_content.lower()

        # Common technical causes for date parsing bugs
        technical_keywords = [
            'format', 'parse', 'pd.to_datetime', 'strftime', 'strptime',
            'dayfirst', 'yearfirst', 'read_csv', 'parse_dates',
            '%y', '%m', '%d', 'ymd', 'dmy', 'mdy'
        ]
        found_technical = any(kw in content_lower for kw in technical_keywords)

        assert found_technical, (
            "Document should explain the technical cause.\n"
            "Mention what specifically went wrong (date format, parsing function, etc.)."
        )


class TestSolution:
    """Verify document describes the solution."""

    def test_has_solution_section(self, doc_content):
        """Document must describe HOW the bug was fixed."""
        content_lower = doc_content.lower()

        solution_keywords = ['solution', 'fix', 'resolve', 'correct', 'change', 'update']
        has_solution = any(kw in content_lower for kw in solution_keywords)

        assert has_solution, (
            "Missing Solution section.\n"
            "Add: ## Solution\n"
            "Describe exactly how you fixed the bug."
        )

    def test_has_code_examples(self, doc_content):
        """Document must include code examples showing the fix."""
        # Check for code blocks
        has_code_block = '```' in doc_content
        has_inline_code = '`' in doc_content and doc_content.count('`') >= 4

        # Check for indented code (4 spaces)
        lines = doc_content.split('\n')
        has_indented_code = any(line.startswith('    ') and line.strip() for line in lines)

        assert has_code_block or has_indented_code or has_inline_code, (
            "Document should include code examples.\n"
            "Show the broken code and the fixed code using markdown code blocks:\n"
            "```python\n# Your code here\n```"
        )

    def test_shows_before_after(self, doc_content):
        """Document should ideally show before/after comparison."""
        content_lower = doc_content.lower()

        comparison_keywords = ['before', 'after', 'original', 'fixed', 'old', 'new', 'was', 'now']
        found_comparison = sum(1 for kw in comparison_keywords if kw in content_lower)

        assert found_comparison >= 2, (
            "Document should show before/after comparison.\n"
            "Show what the code looked like before and after the fix."
        )


class TestPrevention:
    """Verify document includes prevention tips."""

    def test_has_prevention_section(self, doc_content):
        """Document must include tips to prevent similar issues."""
        content_lower = doc_content.lower()

        prevention_keywords = [
            'prevent', 'avoid', 'future', 'best practice', 'lesson',
            'tip', 'recommend', 'should', 'always', 'never'
        ]
        found_prevention = sum(1 for kw in prevention_keywords if kw in content_lower)

        assert found_prevention >= 2, (
            "Missing Prevention section.\n"
            "Add: ## Prevention / Lessons Learned\n"
            "What can developers do to avoid similar bugs in the future?"
        )


class TestDocumentQuality:
    """Additional quality checks for professional documentation."""

    def test_professional_structure(self, doc_content):
        """Document should have a professional structure."""
        # Check for numbered or bulleted lists
        has_lists = bool(re.search(r'^\s*[-*•]|\d+\.', doc_content, re.MULTILINE))

        # Check for multiple sections
        section_count = len(re.findall(r'^#{1,3}\s+\w+', doc_content, re.MULTILINE))

        assert section_count >= 3 or has_lists, (
            "Document should have a professional structure.\n"
            "Use headers to organize and bullet points for readability."
        )

    def test_complete_explanation(self, doc_content):
        """Document should provide a complete explanation someone could follow."""
        word_count = len(doc_content.split())

        # Should have enough detail to be useful
        assert word_count >= 200, (
            f"Document has only {word_count} words.\n"
            "A complete troubleshooting guide that someone could follow needs more detail.\n"
            "Aim for 300+ words covering all required sections."
        )

    def test_actionable_content(self, doc_content):
        """Document should be actionable - someone can use it to fix the bug."""
        content_lower = doc_content.lower()

        # Should have action verbs
        action_keywords = [
            'use', 'add', 'change', 'update', 'set', 'specify',
            'check', 'verify', 'ensure', 'run', 'test'
        ]
        found_actions = sum(1 for kw in action_keywords if kw in content_lower)

        assert found_actions >= 3, (
            "Document should be actionable.\n"
            "Include specific steps someone can follow to identify and fix the bug."
        )

    def test_not_just_copy_paste(self, doc_content):
        """Document should not be a simple copy-paste from generic sources."""
        content_lower = doc_content.lower()

        # Should mention task-specific context
        specific_keywords = [
            'order', 'customer', 'cartly', 'csv', 'dataframe', 'pandas',
            'load_orders', 'data_loader', 'task 1.3', '1.3'
        ]
        found_specific = sum(1 for kw in specific_keywords if kw in content_lower)

        # Not a hard requirement but good to have context
        if found_specific < 1:
            # Just note - don't fail
            pass
