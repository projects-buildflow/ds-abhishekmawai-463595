"""Tests for Task 4.1: Pipeline Architecture Design

Objective: Design a comprehensive data pipeline architecture document.

This test verifies:
1. Design document exists at the correct path
2. Document has substantial content (not a placeholder)
3. Document has all 6 required sections
4. Sections have meaningful depth
5. Document addresses pipeline-specific concerns
"""

import pytest
import re
from pathlib import Path


@pytest.fixture
def design_path(student_folder):
    """Get path to the design document."""
    if not student_folder:
        pytest.skip("Student folder not provided")
    return Path(student_folder) / "submissions" / "pipeline_design.md"


@pytest.fixture
def design_content(design_path):
    """Load the design document content."""
    if not design_path.exists():
        pytest.fail(
            f"Design document not found at {design_path}\n\n"
            "Create: submissions/pipeline_design.md"
        )
    return design_path.read_text()


class TestDocumentExists:
    """Verify design document exists and has substance."""

    def test_design_document_exists(self, design_path):
        """pipeline_design.md must exist."""
        assert design_path.exists(), (
            f"Design document not found at {design_path}\n\n"
            "Create: submissions/pipeline_design.md"
        )

    def test_document_has_substantial_content(self, design_content):
        """Document must have substantial content."""
        char_count = len(design_content)
        word_count = len(design_content.split())

        assert char_count >= 1000, (
            f"Document is too short ({char_count} characters).\n"
            "Expected a comprehensive architecture document with all required sections."
        )

        assert word_count >= 300, (
            f"Document has only {word_count} words.\n"
            "A proper architecture document needs more detail."
        )

    def test_document_is_markdown(self, design_content):
        """Document should be properly formatted markdown."""
        header_count = design_content.count('#')

        assert header_count >= 6, (
            f"Found only {header_count} headers.\n"
            "Use headers to organize your document into required sections."
        )


class TestRequiredSections:
    """Verify document has all required sections."""

    def test_has_overview_section(self, design_content):
        """Document must have an Overview section."""
        content_lower = design_content.lower()

        overview_keywords = ['overview', 'introduction', 'summary', 'purpose']
        has_overview = any(kw in content_lower for kw in overview_keywords)

        assert has_overview, (
            "Missing Overview section.\n"
            "Add: ## Overview\n"
            "Describe the pipeline's purpose and high-level architecture."
        )

    def test_has_data_flow_section(self, design_content):
        """Document must have a Data Flow section."""
        content_lower = design_content.lower()

        data_flow_keywords = ['data flow', 'flow diagram', 'pipeline flow', '\u2192', '->']
        has_data_flow = any(kw in content_lower for kw in data_flow_keywords)

        # Also check for ETL stages
        etl_keywords = ['extract', 'transform', 'load']
        found_etl = sum(1 for kw in etl_keywords if kw in content_lower)

        assert has_data_flow or found_etl >= 2, (
            "Missing Data Flow section.\n"
            "Add: ## Data Flow\n"
            "Show how data moves through the pipeline:\n"
            "Source \u2192 Extract \u2192 Transform \u2192 Load \u2192 Destination"
        )

    def test_has_components_section(self, design_content):
        """Document must have a Components section."""
        content_lower = design_content.lower()

        component_keywords = ['component', 'module', 'extractor', 'transformer', 'loader']
        found_components = sum(1 for kw in component_keywords if kw in content_lower)

        assert found_components >= 2, (
            "Missing Components section.\n"
            "Add: ## Components\n"
            "Describe each pipeline component:\n"
            "- Extractor: What it does, inputs, outputs\n"
            "- Transformer: What it does, inputs, outputs\n"
            "- Loader: What it does, inputs, outputs"
        )

    def test_has_error_handling_section(self, design_content):
        """Document must have an Error Handling section."""
        content_lower = design_content.lower()

        error_keywords = ['error', 'exception', 'fail', 'handling', 'retry', 'recover']
        found_error = sum(1 for kw in error_keywords if kw in content_lower)

        assert found_error >= 2, (
            "Missing Error Handling section.\n"
            "Add: ## Error Handling\n"
            "Describe how the pipeline handles:\n"
            "- Data validation errors\n"
            "- Missing or corrupt files\n"
            "- Partial failures"
        )

    def test_has_monitoring_section(self, design_content):
        """Document must have a Monitoring section."""
        content_lower = design_content.lower()

        monitoring_keywords = ['monitor', 'log', 'alert', 'metric', 'track', 'observ', 'health']
        found_monitoring = sum(1 for kw in monitoring_keywords if kw in content_lower)

        assert found_monitoring >= 2, (
            "Missing Monitoring section.\n"
            "Add: ## Monitoring\n"
            "Describe:\n"
            "- What metrics to track\n"
            "- How to know if pipeline is healthy\n"
            "- Alerting strategy"
        )

    def test_has_technology_choices(self, design_content):
        """Document must have Technology Choices section."""
        content_lower = design_content.lower()

        tech_keywords = [
            'technology', 'tech choice', 'tool', 'library', 'python',
            'pandas', 'sql', 'framework', 'database', 'chose', 'decision'
        ]
        found_tech = sum(1 for kw in tech_keywords if kw in content_lower)

        assert found_tech >= 2, (
            "Missing Technology Choices section.\n"
            "Add: ## Technology Choices\n"
            "Explain:\n"
            "- What tools/libraries you chose\n"
            "- Why you chose them\n"
            "- Trade-offs considered"
        )


class TestSectionContent:
    """Verify sections have meaningful content."""

    def test_data_flow_describes_stages(self, design_content):
        """Data flow should describe the ETL stages."""
        content_lower = design_content.lower()

        has_source = 'source' in content_lower or 'input' in content_lower or 'csv' in content_lower
        has_destination = 'destination' in content_lower or 'output' in content_lower or 'database' in content_lower

        assert has_source and has_destination, (
            "Data Flow section should describe:\n"
            "- Data source (where data comes from)\n"
            "- Data destination (where data goes)"
        )

    def test_components_have_descriptions(self, design_content):
        """Components should have descriptions of their responsibilities."""
        content_lower = design_content.lower()

        responsibility_indicators = [
            'responsible', 'handles', 'reads', 'writes', 'processes',
            'validates', 'cleans', 'outputs', 'takes', 'produces', 'returns'
        ]
        found = sum(1 for kw in responsibility_indicators if kw in content_lower)

        assert found >= 3, (
            "Components section needs more detail.\n"
            "For each component, describe:\n"
            "- What it does\n"
            "- What inputs it takes\n"
            "- What outputs it produces"
        )

    def test_has_diagram_or_visualization(self, design_content):
        """Document should include a diagram or flow visualization."""
        diagram_indicators = [
            '```', '\u2192', '->', '|', '+--', '\u250c', '\u2510',
            'mermaid', 'graph', 'flowchart',
            '.png', '.jpg', '.svg', '![',
        ]
        has_diagram = any(ind in design_content for ind in diagram_indicators)

        has_flow_list = '- Extract' in design_content or '1. Extract' in design_content

        assert has_diagram or has_flow_list, (
            "Document should include a visual representation of the pipeline.\n"
            "Options:\n"
            "- ASCII art diagram\n"
            "- Mermaid flowchart\n"
            "- Bullet point flow\n"
            "- Image/screenshot"
        )

    def test_document_is_professional(self, design_content):
        """Document should have professional structure."""
        section_pattern = r'^#{1,3}\s+\d*\.?\s*\w+'
        sections = re.findall(section_pattern, design_content, re.MULTILINE)

        assert len(sections) >= 5, (
            f"Found only {len(sections)} section headers.\n"
            "Organize document with clear section headers:\n"
            "## Overview\n"
            "## Data Flow\n"
            "## Components\n"
            "etc."
        )

    def test_reasonable_depth(self, design_content):
        """Document should have reasonable depth in each section."""
        sections = re.split(r'^#{1,3}\s+', design_content, flags=re.MULTILINE)

        substantial_sections = [s for s in sections if len(s.split()) > 30]

        assert len(substantial_sections) >= 4, (
            "Some sections are too brief.\n"
            "Each major section should have at least a few sentences of explanation."
        )


class TestPipelineSpecific:
    """Verify document addresses pipeline-specific concerns."""

    def test_addresses_idempotency(self, design_content):
        """Document should address idempotency (safe to re-run)."""
        content_lower = design_content.lower()

        idempotent_keywords = ['idempoten', 'rerun', 're-run', 'duplicate', 'repeat', 'safe to run again', 'overwrite']
        has_idempotency = any(kw in content_lower for kw in idempotent_keywords)

        assert has_idempotency, (
            "Document should address idempotency.\n"
            "Explain how re-running the pipeline won't create duplicate data.\n"
            "This is a key pipeline requirement."
        )

    def test_addresses_data_quality(self, design_content):
        """Document should address data quality validation."""
        content_lower = design_content.lower()

        quality_keywords = ['valid', 'quality', 'clean', 'check', 'verify', 'schema']
        found_quality = sum(1 for kw in quality_keywords if kw in content_lower)

        assert found_quality >= 2, (
            "Document should address data quality validation.\n"
            "Describe how the pipeline ensures data quality."
        )
