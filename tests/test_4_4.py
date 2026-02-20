"""Tests for Task 4.4: Final Presentation

Objective: Create a professional PDF presentation summarizing your internship journey.
"""

import pytest
from pathlib import Path


@pytest.fixture
def submissions_path(student_folder):
    """Get path to student's submissions folder."""
    if not student_folder:
        pytest.skip("Student folder not provided")
    return Path(student_folder) / "submissions"


@pytest.fixture
def presentation_path(submissions_path):
    """Find the presentation PDF."""
    pdf_path = submissions_path / "presentation.pdf"
    if pdf_path.exists():
        return pdf_path
    return None


@pytest.fixture
def pdf_reader(presentation_path):
    """Load PDF with pypdf for content inspection."""
    if presentation_path is None:
        pytest.skip("Presentation not found")
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            pytest.skip("No PDF library available")
    import io
    return PdfReader(io.BytesIO(presentation_path.read_bytes()))


class TestPresentationExists:
    """Verify presentation file exists and is a valid PDF."""

    def test_presentation_file_exists(self, submissions_path, presentation_path):
        """submissions/presentation.pdf must exist."""
        assert presentation_path is not None, (
            "Presentation not found.\n\n"
            "Save your presentation as:\n"
            "  submissions/presentation.pdf\n\n"
            f"Looked in: {submissions_path}"
        )

    def test_pdf_valid_header(self, presentation_path):
        """PDF file should have a valid PDF header."""
        if presentation_path is None:
            pytest.skip("Presentation not found")
        with open(presentation_path, "rb") as f:
            header = f.read(5)
        assert header == b"%PDF-", (
            "File does not appear to be a valid PDF.\n"
            "Export your presentation as PDF format."
        )

    def test_file_is_substantial(self, presentation_path):
        """Presentation should be at least 50 KB."""
        if presentation_path is None:
            pytest.skip("Presentation not found")
        file_size = presentation_path.stat().st_size
        assert file_size >= 50 * 1024, (
            f"Presentation is only {file_size / 1024:.1f} KB.\n"
            "A 6+ slide presentation with content should be larger.\n"
            "Make sure all slides exported correctly."
        )


class TestPresentationContent:
    """Verify PDF has enough slides and text content."""

    def test_page_count(self, pdf_reader):
        """Presentation should have 6-15 pages (slides)."""
        count = len(pdf_reader.pages)
        assert 6 <= count <= 15, (
            f"Presentation has {count} pages.\n"
            "Expected 6-15 slides. Too few means missing sections; "
            "too many means slides may not be focused enough."
        )

    def test_pages_have_text(self, pdf_reader):
        """At least 4 pages should contain extractable text."""
        pages_with_text = 0
        for page in pdf_reader.pages:
            text = (page.extract_text() or "").strip()
            if len(text) > 20:
                pages_with_text += 1
        assert pages_with_text >= 4, (
            f"Only {pages_with_text} pages have meaningful text.\n"
            "At least 4 slides should contain readable text content.\n"
            "If your slides are image-heavy, add text or speaker notes."
        )

    def test_total_word_count(self, pdf_reader):
        """Presentation should have at least 80 words total."""
        all_text = ""
        for page in pdf_reader.pages:
            all_text += (page.extract_text() or "") + " "
        word_count = len(all_text.split())
        assert word_count >= 80, (
            f"Presentation has only ~{word_count} words.\n"
            "Expected at least 80 words across all slides.\n"
            "Add content to your slides — bullet points, descriptions, insights."
        )


class TestPresentationSections:
    """Verify required sections are present via keyword detection."""

    def test_required_sections(self, pdf_reader):
        """At least 4 of 5 required sections should be identifiable."""
        all_text = ""
        for page in pdf_reader.pages:
            all_text += (page.extract_text() or "") + " "
        text_lower = all_text.lower()

        section_keywords = {
            "introduction": ["introduction", "about me", "who i am", "my name", "background"],
            "journey": ["journey", "internship", "progression", "path", "experience", "week"],
            "project": ["project", "analysis", "pipeline", "dashboard", "built", "implemented"],
            "learning": ["learned", "learning", "challenge", "takeaway", "grew", "skill"],
            "future": ["future", "next", "goal", "plan", "continue", "career", "aspire"],
        }

        found = 0
        missing = []
        for section, keywords in section_keywords.items():
            if any(kw in text_lower for kw in keywords):
                found += 1
            else:
                missing.append(section)

        assert found >= 4, (
            f"Only {found}/5 required sections detected.\n"
            f"Missing: {', '.join(missing)}\n\n"
            "Your presentation should cover:\n"
            "1. Introduction — who you are\n"
            "2. Journey — your internship path\n"
            "3. Key Project — deep dive into your best work\n"
            "4. Learnings — what you learned, challenges overcome\n"
            "5. Future — what you want to learn next"
        )
