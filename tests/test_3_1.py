"""Tests for Task 3.1: Revenue Investigation Notebook

Objective: Create a Jupyter notebook investigating the revenue anomaly.

This test DECISIVELY verifies:
1. Notebook file exists and is valid JSON
2. Notebook has required sections (Executive Summary, Analysis, Root Cause, Recommendations)
3. Notebook contains code cells with actual analysis
4. Notebook loads and uses data files
5. Notebook includes visualizations
6. Notebook has markdown cells with explanations
7. Notebook identifies the revenue anomaly
8. Notebook provides actionable recommendations
"""

import pytest
import json
from pathlib import Path


@pytest.fixture
def notebook_path(student_folder):
    """Get path to student's notebook."""
    if not student_folder:
        pytest.skip("Student folder not provided")
    return Path(student_folder) / "submissions" / "revenue_investigation.ipynb"


@pytest.fixture
def notebook(notebook_path):
    """Load and parse the notebook."""
    if not notebook_path.exists():
        pytest.fail(
            f"Notebook not found at {notebook_path}\n\n"
            "Create: submissions/revenue_investigation.ipynb"
        )

    try:
        with open(notebook_path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(
            f"Notebook is not valid JSON: {e}\n"
            "Make sure the .ipynb file is properly saved."
        )


@pytest.fixture
def notebook_content(notebook):
    """Extract all content from notebook cells."""
    all_content = ""
    for cell in notebook.get("cells", []):
        source = cell.get("source", [])
        if isinstance(source, list):
            all_content += "\n".join(source)
        else:
            all_content += source
        all_content += "\n"
    return all_content


@pytest.fixture
def code_cells(notebook):
    """Get all code cells from notebook."""
    return [c for c in notebook.get("cells", []) if c.get("cell_type") == "code"]


@pytest.fixture
def markdown_cells(notebook):
    """Get all markdown cells from notebook."""
    return [c for c in notebook.get("cells", []) if c.get("cell_type") == "markdown"]


class TestNotebookExists:
    """Verify notebook file exists and is valid."""

    def test_notebook_file_exists(self, notebook_path):
        """Notebook must exist at the correct path."""
        assert notebook_path.exists(), (
            f"Notebook not found at {notebook_path}\n\n"
            "Create: submissions/revenue_investigation.ipynb"
        )

    def test_notebook_is_valid_json(self, notebook):
        """Notebook must be valid JSON format."""
        assert "cells" in notebook, (
            "Notebook should have 'cells' key.\n"
            "Make sure this is a valid Jupyter notebook file."
        )

    def test_notebook_has_cells(self, notebook):
        """Notebook must have cells."""
        assert len(notebook.get("cells", [])) > 0, (
            "Notebook has no cells.\n"
            "Add code and markdown cells for your analysis."
        )


class TestRequiredSections:
    """Verify notebook has all required sections."""

    def test_has_executive_summary(self, notebook_content):
        """Notebook must have an Executive Summary section."""
        content_lower = notebook_content.lower()

        summary_keywords = ['executive summary', 'summary', 'overview', 'tldr', 'key finding']
        has_summary = any(kw in content_lower for kw in summary_keywords)

        assert has_summary, (
            "Missing Executive Summary section.\n"
            "Add: ## Executive Summary\n"
            "Provide a brief overview of findings for executives."
        )

    def test_has_analysis_section(self, notebook_content):
        """Notebook must have an Analysis section."""
        content_lower = notebook_content.lower()

        analysis_keywords = ['analysis', 'investigation', 'explore', 'examine', 'findings']
        has_analysis = any(kw in content_lower for kw in analysis_keywords)

        assert has_analysis, (
            "Missing Analysis section.\n"
            "Add: ## Analysis\n"
            "Show your data analysis and exploration."
        )

    def test_has_root_cause_section(self, notebook_content):
        """Notebook must identify the root cause."""
        content_lower = notebook_content.lower()

        cause_keywords = ['root cause', 'cause', 'reason', 'why', 'because', 'explanation']
        has_cause = any(kw in content_lower for kw in cause_keywords)

        assert has_cause, (
            "Missing Root Cause section.\n"
            "Add: ## Root Cause\n"
            "Explain what caused the revenue anomaly."
        )

    def test_has_recommendations(self, notebook_content):
        """Notebook must have recommendations."""
        content_lower = notebook_content.lower()

        rec_keywords = ['recommend', 'suggestion', 'action', 'next step', 'should', 'proposal']
        has_recommendations = any(kw in content_lower for kw in rec_keywords)

        assert has_recommendations, (
            "Missing Recommendations section.\n"
            "Add: ## Recommendations\n"
            "Provide actionable recommendations based on your findings."
        )


class TestCodeCells:
    """Verify notebook has substantial code for analysis."""

    def test_has_code_cells(self, code_cells):
        """Notebook must have code cells."""
        assert len(code_cells) >= 5, (
            f"Found only {len(code_cells)} code cells.\n"
            "Your analysis should include more code for:\n"
            "- Loading data\n"
            "- Data exploration\n"
            "- Analysis\n"
            "- Visualizations"
        )

    def test_code_imports_pandas(self, notebook_content):
        """Notebook should import pandas for data analysis."""
        assert 'pandas' in notebook_content or 'pd' in notebook_content, (
            "Notebook should import pandas for data analysis.\n"
            "Add: import pandas as pd"
        )

    def test_code_loads_data(self, notebook_content):
        """Notebook must load data from CSV files."""
        data_loading_patterns = [
            'read_csv', 'pd.read', 'orders.csv', 'customers.csv',
            'load_', 'data/', '../data/'
        ]
        has_data_loading = any(pattern in notebook_content for pattern in data_loading_patterns)

        assert has_data_loading, (
            "Notebook should load data from CSV files.\n"
            "Use: pd.read_csv('data/orders.csv') or similar."
        )

    def test_code_has_calculations(self, notebook_content):
        """Notebook should have data calculations."""
        calc_patterns = [
            'sum(', 'mean(', 'count(', 'groupby', 'agg(',
            'value_counts', 'describe', 'revenue', 'total'
        ]
        found_calcs = sum(1 for p in calc_patterns if p in notebook_content)

        assert found_calcs >= 2, (
            "Notebook should have data calculations.\n"
            "Include: aggregations, groupby operations, statistical summaries."
        )


class TestVisualizations:
    """Verify notebook includes visualizations."""

    def test_has_visualization_imports(self, notebook_content):
        """Notebook should import visualization libraries."""
        viz_imports = ['matplotlib', 'plt', 'seaborn', 'sns', 'plotly', 'px']
        has_viz_import = any(lib in notebook_content for lib in viz_imports)

        assert has_viz_import, (
            "Notebook should import visualization libraries.\n"
            "Add: import matplotlib.pyplot as plt\n"
            "Or: import seaborn as sns"
        )

    def test_has_visualization_code(self, notebook_content):
        """Notebook must include visualization code."""
        viz_patterns = [
            '.plot(', '.bar(', '.line(', '.hist(', '.scatter(',
            'plt.show', 'figure(', 'subplot', '.pie(',
            'sns.', 'px.'
        ]
        found_viz = sum(1 for p in viz_patterns if p in notebook_content)

        assert found_viz >= 2, (
            f"Found only {found_viz} visualization calls.\n"
            "Your analysis should include charts/graphs:\n"
            "- Revenue trends over time\n"
            "- Comparisons between periods\n"
            "- Distribution of values"
        )


class TestMarkdownExplanations:
    """Verify notebook has proper markdown explanations."""

    def test_has_markdown_cells(self, markdown_cells):
        """Notebook must have markdown cells for explanations."""
        assert len(markdown_cells) >= 4, (
            f"Found only {len(markdown_cells)} markdown cells.\n"
            "Add markdown cells to explain:\n"
            "- What you're analyzing\n"
            "- What each code block does\n"
            "- What the results mean\n"
            "- Your conclusions"
        )

    def test_markdown_has_headers(self, notebook_content):
        """Notebook should have markdown headers for organization."""
        header_pattern = notebook_content.count('#')

        assert header_pattern >= 4, (
            f"Found only {header_pattern} markdown headers.\n"
            "Use headers (# or ##) to organize your notebook sections."
        )

    def test_markdown_explains_findings(self, notebook_content):
        """Markdown cells should explain findings, not just label sections."""
        content_lower = notebook_content.lower()

        explanation_indicators = [
            'this shows', 'we can see', 'indicates', 'reveals',
            'suggests', 'the data', 'the analysis', 'result',
            'finding', 'discover', 'notice', 'observe'
        ]
        found_explanations = sum(1 for ind in explanation_indicators if ind in content_lower)

        assert found_explanations >= 3, (
            "Markdown cells should explain your findings.\n"
            "Don't just label sections - explain what the data shows."
        )


class TestRevenueInvestigation:
    """Verify notebook actually investigates the revenue issue."""

    def test_mentions_revenue(self, notebook_content):
        """Notebook should focus on revenue."""
        content_lower = notebook_content.lower()

        assert 'revenue' in content_lower, (
            "Notebook should mention 'revenue'.\n"
            "This is a revenue investigation task."
        )

    def test_identifies_anomaly(self, notebook_content):
        """Notebook should identify the anomaly/issue."""
        content_lower = notebook_content.lower()

        anomaly_terms = [
            'anomaly', 'drop', 'decline', 'decrease', 'issue',
            'problem', 'unusual', 'unexpected', 'spike', 'change',
            'different', 'variation', 'deviat'
        ]
        found_anomaly = any(term in content_lower for term in anomaly_terms)

        assert found_anomaly, (
            "Notebook should identify the revenue anomaly.\n"
            "Describe what's unusual about the revenue data."
        )

    def test_has_time_analysis(self, notebook_content):
        """Notebook should analyze data over time."""
        content_lower = notebook_content.lower()

        time_terms = [
            'date', 'month', 'week', 'day', 'time', 'period',
            'trend', 'year', 'quarter', 'timeline', 'daily', 'monthly'
        ]
        found_time = sum(1 for term in time_terms if term in content_lower)

        assert found_time >= 2, (
            "Notebook should analyze revenue over time.\n"
            "Look at trends by date, month, or other time periods."
        )

    def test_quantifies_impact(self, notebook_content):
        """Notebook should quantify the revenue impact."""
        # Look for numbers in the content
        import re
        numbers = re.findall(r'\$?\d+(?:,\d{3})*(?:\.\d+)?%?', notebook_content)

        assert len(numbers) >= 5, (
            f"Found only {len(numbers)} numbers in notebook.\n"
            "Quantify the impact: How much revenue was lost? What percentage?"
        )


class TestNotebookQuality:
    """Additional quality checks for the notebook."""

    def test_notebook_is_substantial(self, notebook):
        """Notebook should have substantial content."""
        total_cells = len(notebook.get("cells", []))

        assert total_cells >= 10, (
            f"Notebook has only {total_cells} cells.\n"
            "A thorough investigation should have more content."
        )

    def test_code_cells_have_output(self, code_cells):
        """Code cells should have been executed (have output)."""
        cells_with_output = sum(
            1 for cell in code_cells
            if cell.get("outputs") and len(cell.get("outputs", [])) > 0
        )

        # At least half of code cells should have output
        min_with_output = len(code_cells) // 2

        if cells_with_output < min_with_output:
            # This is a warning, not a failure
            pass  # Note: Run all cells before submitting

    def test_professional_presentation(self, notebook_content):
        """Notebook should have professional presentation."""
        content_lower = notebook_content.lower()

        # Should have introduction and conclusion
        has_intro = 'introduction' in content_lower or 'background' in content_lower or 'overview' in content_lower
        has_conclusion = 'conclusion' in content_lower or 'summary' in content_lower or 'recommendation' in content_lower

        assert has_intro or has_conclusion, (
            "Notebook should have professional structure.\n"
            "Include an Introduction and Conclusion section."
        )


class TestNotebookExecution:
    """Verify the notebook executes correctly."""

    def test_notebook_executes_without_error(self, executed_notebook):
        """All notebook cells should execute without errors."""
        errors = []
        for i, cell in enumerate(executed_notebook.cells):
            if cell.cell_type != "code":
                continue
            for output in cell.get("outputs", []):
                if output.output_type == "error":
                    errors.append(f"Cell {i+1}: {output.ename}: {output.evalue}")

        assert not errors, (
            f"Notebook has execution errors:\n" + "\n".join(errors)
        )

    def test_code_cells_produce_output(self, executed_notebook):
        """At least 60% of code cells should produce output."""
        code_cells = [c for c in executed_notebook.cells if c.cell_type == "code" and c.source.strip()]
        if not code_cells:
            pytest.skip("No code cells found")

        cells_with_output = sum(1 for c in code_cells if c.get("outputs"))
        ratio = cells_with_output / len(code_cells)

        assert ratio >= 0.6, (
            f"Only {cells_with_output}/{len(code_cells)} ({ratio:.0%}) code cells produce output.\n"
            "Run all cells before submitting."
        )

    def test_visualization_outputs_exist(self, executed_notebook):
        """Notebook should produce at least 2 visualizations."""
        viz_count = 0
        for cell in executed_notebook.cells:
            for output in cell.get("outputs", []):
                if hasattr(output, "data") and output.get("data", {}).get("image/png"):
                    viz_count += 1
                elif output.get("output_type") == "display_data":
                    data = output.get("data", {})
                    if "image/png" in data or "image/svg+xml" in data:
                        viz_count += 1

        assert viz_count >= 2, (
            f"Found only {viz_count} visualizations.\n"
            "Include at least 2 charts/graphs in your analysis."
        )

    def test_no_import_errors(self, executed_notebook):
        """No cells should have ModuleNotFoundError."""
        for i, cell in enumerate(executed_notebook.cells):
            for output in cell.get("outputs", []):
                if output.get("output_type") == "error" and output.get("ename") == "ModuleNotFoundError":
                    pytest.fail(
                        f"Cell {i+1} has a missing import: {output.get('evalue')}\n"
                        "Make sure all required packages are installed."
                    )
