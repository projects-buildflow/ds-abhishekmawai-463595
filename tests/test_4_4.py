"""Tests for Task 4.4: Final Presentation

Objective: Create a professional presentation summarizing your internship journey.

This test DECISIVELY verifies:
1. Presentation file exists (PDF preferred, PPTX accepted)
2. File is a valid PDF format
3. File size is reasonable (6-10 slides worth of content)
4. File is not too small (has actual content)
5. File is not excessively large

Note: Content quality (slide structure, visualizations, narrative) is assessed
by AI review, not these automated tests.
"""

import pytest
from pathlib import Path


@pytest.fixture
def week4_path(student_folder):
    """Get path to student's submissions folder."""
    if not student_folder:
        pytest.skip("Student folder not provided")
    return Path(student_folder) / "submissions"


@pytest.fixture
def presentation_path(week4_path):
    """Find the presentation file (PDF or PPTX)."""
    pdf_path = week4_path / "presentation.pdf"
    pptx_path = week4_path / "presentation.pptx"

    if pdf_path.exists():
        return pdf_path
    if pptx_path.exists():
        return pptx_path

    return None


class TestPresentationExists:
    """Verify presentation file exists."""

    def test_presentation_file_exists(self, week4_path, presentation_path):
        """Presentation file must exist."""
        assert presentation_path is not None, (
            "Presentation not found.\n\n"
            "Create one of:\n"
            "- presentation.pdf (preferred)\n"
            "- presentation.pptx\n\n"
            f"In folder: {week4_path}"
        )

    def test_prefers_pdf_format(self, week4_path):
        """PDF format is preferred over PPTX."""
        pdf_path = week4_path / "presentation.pdf"
        pptx_path = week4_path / "presentation.pptx"

        if not pdf_path.exists() and pptx_path.exists():
            # PPTX is accepted but PDF is better
            pass  # Note: Consider exporting to PDF for better compatibility


class TestFileValidity:
    """Verify the presentation file is valid."""

    def test_file_has_content(self, presentation_path):
        """Presentation file must have content."""
        if presentation_path is None:
            pytest.skip("Presentation not found")

        file_size = presentation_path.stat().st_size

        assert file_size > 5000, (
            f"Presentation file is only {file_size} bytes.\n"
            "This seems too small for a presentation with content."
        )

    def test_pdf_is_valid_format(self, presentation_path):
        """PDF file should have valid PDF header."""
        if presentation_path is None:
            pytest.skip("Presentation not found")

        if presentation_path.suffix.lower() != '.pdf':
            pytest.skip("Not a PDF file")

        with open(presentation_path, "rb") as f:
            header = f.read(5)

        assert header == b"%PDF-", (
            "File does not appear to be a valid PDF.\n"
            "Make sure to export your presentation as PDF format.\n\n"
            "In PowerPoint: File > Save As > PDF\n"
            "In Google Slides: File > Download > PDF"
        )

    def test_pptx_is_valid_format(self, presentation_path):
        """PPTX file should have valid PPTX header (ZIP-based)."""
        if presentation_path is None:
            pytest.skip("Presentation not found")

        if presentation_path.suffix.lower() != '.pptx':
            pytest.skip("Not a PPTX file")

        with open(presentation_path, "rb") as f:
            header = f.read(4)

        # PPTX is a ZIP file, should start with PK
        assert header[:2] == b"PK", (
            "File does not appear to be a valid PPTX.\n"
            "Make sure to save your presentation in PPTX format."
        )


class TestFileSize:
    """Verify presentation file size is reasonable."""

    def test_file_is_substantial(self, presentation_path):
        """Presentation should be at least 50KB (6+ slides with content)."""
        if presentation_path is None:
            pytest.skip("Presentation not found")

        file_size = presentation_path.stat().st_size
        min_size = 50 * 1024  # 50KB

        assert file_size >= min_size, (
            f"Presentation is only {file_size / 1024:.1f} KB.\n"
            "A presentation with 6-10 slides should be larger.\n"
            "Check that all slides exported correctly."
        )

    def test_file_is_not_excessive(self, presentation_path):
        """Presentation shouldn't be excessively large."""
        if presentation_path is None:
            pytest.skip("Presentation not found")

        file_size = presentation_path.stat().st_size
        max_size = 50 * 1024 * 1024  # 50MB

        assert file_size <= max_size, (
            f"Presentation is {file_size / (1024*1024):.1f} MB.\n"
            "This is quite large. Consider:\n"
            "- Compressing images\n"
            "- Using PNG instead of BMP\n"
            "- Reducing image resolution"
        )

    def test_file_suggests_multiple_slides(self, presentation_path):
        """File size should suggest multiple slides worth of content."""
        if presentation_path is None:
            pytest.skip("Presentation not found")

        file_size = presentation_path.stat().st_size

        # A 6-slide PDF should be at least 100KB typically
        min_expected = 100 * 1024  # 100KB

        if file_size < min_expected:
            # This is a warning, not a failure
            pass  # Note: File seems small for 6-10 slides


class TestPresentationRequirements:
    """Document presentation requirements for AI review.

    The AI reviewer will evaluate:
    1. Introduction slide (who you are, background)
    2. Journey section (path through the internship)
    3. Key Project deep dive (your best work)
    4. Learnings section (what you learned, challenges)
    5. Future section (what you want to learn next)
    6. At least one data visualization
    7. Minimal text (bullet points, not paragraphs)
    8. Professional design
    """

    def test_slide_count_requirements(self):
        """Presentation should have 6-10 slides."""
        MIN_SLIDES = 6
        MAX_SLIDES = 10
        assert MIN_SLIDES == 6
        assert MAX_SLIDES == 10

    def test_required_sections(self):
        """Presentation should include these sections."""
        required_sections = [
            "Introduction (who you are)",
            "Journey (your path)",
            "Key Project (deep dive)",
            "Learnings (what you learned)",
            "Future (next steps)",
        ]
        assert len(required_sections) == 5

    def test_design_requirements(self):
        """Presentation should follow design guidelines."""
        design_guidelines = [
            "Minimal text per slide (bullet points)",
            "At least one data visualization",
            "Consistent color scheme",
            "Readable fonts",
            "Professional layout",
        ]
        assert len(design_guidelines) == 5


class TestOptionalEnhancements:
    """Optional checks for enhanced presentations."""

    def test_notes_file_exists(self, week4_path):
        """Check if speaker notes file exists (optional)."""
        notes_path = week4_path / "presentation_notes.md"

        if notes_path.exists():
            # Great - they included speaker notes
            content = notes_path.read_text()
            if len(content) > 100:
                pass  # Good practice to have notes
        # This is optional - don't fail

    def test_supporting_materials_exist(self, week4_path):
        """Check if any supporting materials exist (optional)."""
        optional_files = [
            "presentation_notes.md",
            "demo_script.md",
            "references.md",
        ]

        found_files = [f for f in optional_files if (week4_path / f).exists()]

        if found_files:
            pass  # Nice to have supporting materials
        # This is optional - don't fail


class TestPDFContent:
    """Try to extract and verify PDF content if possible."""

    def test_pdf_has_multiple_pages(self, presentation_path):
        """PDF should have multiple pages (slides)."""
        if presentation_path is None:
            pytest.skip("Presentation not found")

        if presentation_path.suffix.lower() != '.pdf':
            pytest.skip("Not a PDF file")

        import PyPDF2

        with open(presentation_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            num_pages = len(reader.pages)

        assert num_pages >= 6, (
            f"PDF has only {num_pages} pages (slides).\n"
            "Presentation should have 6-10 slides."
        )
        assert num_pages <= 15, (
            f"PDF has {num_pages} pages.\n"
            "Presentation should be 6-10 slides. Consider condensing."
        )

    def test_pdf_is_not_empty_content(self, presentation_path):
        """PDF pages should have content (not blank)."""
        if presentation_path is None:
            pytest.skip("Presentation not found")

        if presentation_path.suffix.lower() != '.pdf':
            pytest.skip("Not a PDF file")

        import PyPDF2

        with open(presentation_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            if len(reader.pages) == 0:
                pytest.fail("PDF has no pages")

            first_page = reader.pages[0]
            text = first_page.extract_text() or ""

            assert len(text.strip()) >= 10, (
                "First page has very little text content.\n"
                "Make sure your slides have actual content."
            )

    def test_pdf_has_text_content(self, presentation_path):
        """At least 4 pages should have meaningful text."""
        if presentation_path is None:
            pytest.skip("Presentation not found")

        if presentation_path.suffix.lower() != '.pdf':
            pytest.skip("Not a PDF file")

        import PyPDF2

        with open(presentation_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            pages_with_text = 0
            for page in reader.pages:
                text = page.extract_text() or ""
                if len(text.strip()) > 20:
                    pages_with_text += 1

        assert pages_with_text >= 4, (
            f"Only {pages_with_text} pages have meaningful text.\n"
            "Each slide should have some text content."
        )
