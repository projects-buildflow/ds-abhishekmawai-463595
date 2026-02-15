"""Tests for Task 3.4: Dashboard Creation

Objective: Create a data visualization dashboard with key business metrics.

This test verifies:
1. Dashboard screenshot exists (PNG or JPG) and is a valid image
2. Screenshot has reasonable size and dimensions
3. metrics.csv exists with required KPI rows
4. KPI values cross-validated against source data (orders.csv, order_items.csv, products.csv)
"""

import pytest
from pathlib import Path


@pytest.fixture
def week3_path(student_folder):
    """Get path to student's submissions folder."""
    if not student_folder:
        pytest.fail("Student folder not provided")
    return Path(student_folder) / "submissions"


@pytest.fixture
def dashboard_screenshot(week3_path):
    """Find and return the dashboard screenshot path."""
    valid_extensions = [".png", ".jpg", ".jpeg"]

    for ext in valid_extensions:
        path = week3_path / f"dashboard{ext}"
        if path.exists():
            return path

    pytest.fail(
        "Dashboard screenshot not found.\n\n"
        "Save your dashboard as one of:\n"
        "- submissions/dashboard.png\n"
        "- submissions/dashboard.jpg\n"
        "- submissions/dashboard.jpeg"
    )


class TestDashboardExists:
    """Verify dashboard screenshot exists and is valid."""

    def test_screenshot_has_content(self, dashboard_screenshot):
        """Screenshot must have content (not an empty file)."""
        file_size = dashboard_screenshot.stat().st_size

        assert file_size > 1000, (
            f"Screenshot file is only {file_size} bytes.\n"
            "This seems too small. Make sure the file saved correctly."
        )

    def test_screenshot_is_reasonable_size(self, dashboard_screenshot):
        """Screenshot should be at least 10KB for a real dashboard image."""
        file_size = dashboard_screenshot.stat().st_size

        assert file_size > 10000, (
            f"Screenshot is only {file_size / 1024:.1f} KB.\n"
            "A dashboard screenshot should be larger.\n"
            "Make sure you captured the full dashboard, not a thumbnail."
        )

    def test_screenshot_not_too_large(self, dashboard_screenshot):
        """Screenshot shouldn't be excessively large."""
        file_size = dashboard_screenshot.stat().st_size
        max_size = 20 * 1024 * 1024  # 20MB

        assert file_size < max_size, (
            f"Screenshot is {file_size / (1024*1024):.1f} MB.\n"
            "This is quite large. Consider compressing the image."
        )

    def test_screenshot_is_valid_image_format(self, dashboard_screenshot):
        """Screenshot must be a valid image file (check magic bytes)."""
        with open(dashboard_screenshot, "rb") as f:
            header = f.read(12)

        is_png = header[:4] == b"\x89PNG"
        is_jpeg = header[:3] == b"\xff\xd8\xff"

        assert is_png or is_jpeg, (
            "File does not appear to be a valid image.\n"
            "Make sure to save as PNG or JPEG format.\n\n"
            "If using Power BI: File > Export > Export to PDF, then screenshot\n"
            "If using Streamlit: Take a browser screenshot"
        )


class TestDashboardDimensions:
    """Verify dashboard image has reasonable dimensions."""

    def test_image_has_reasonable_dimensions(self, dashboard_screenshot):
        """Image should have reasonable dimensions for a dashboard."""
        from PIL import Image

        img = Image.open(dashboard_screenshot)
        width, height = img.size

        assert width >= 600, (
            f"Image width is only {width}px.\n"
            "Dashboard screenshot should be at least 600px wide."
        )

        assert height >= 400, (
            f"Image height is only {height}px.\n"
            "Dashboard screenshot should be at least 400px tall."
        )


class TestMetricsBundle:
    """Validate metrics.csv against source data."""

    def test_metrics_csv_exists(self, week3_path):
        """metrics.csv must exist in submissions folder."""
        path = week3_path / "metrics.csv"
        assert path.exists(), (
            "metrics.csv not found in submissions/\n"
            "Export your dashboard KPIs to submissions/metrics.csv"
        )

    def test_metrics_csv_has_required_rows(self, week3_path):
        """metrics.csv must have all required metric rows."""
        import pandas as pd

        df = pd.read_csv(week3_path / "metrics.csv")
        required = {
            "total_revenue", "active_customers", "avg_order_value",
            "top_product_1", "top_product_2", "top_product_3",
            "top_product_4", "top_product_5",
        }
        found = set(df["metric"].str.strip().str.lower())
        missing = required - found
        assert not missing, f"Missing metrics in metrics.csv: {missing}"

    def test_total_revenue_matches_source(self, week3_path, data_path):
        """Total revenue must be within 5% of actual source data."""
        import pandas as pd

        orders = pd.read_csv(data_path / "orders.csv")
        expected = orders[orders["status"] == "delivered"]["total"].sum()

        metrics = pd.read_csv(week3_path / "metrics.csv")
        row = metrics[metrics["metric"].str.strip().str.lower() == "total_revenue"]
        submitted = float(row["value"].iloc[0])

        pct_diff = abs(submitted - expected) / expected
        assert pct_diff < 0.05, (
            f"Total revenue {submitted:,.2f} differs from expected {expected:,.2f} by {pct_diff:.1%}\n"
            "Check: are you summing the 'total' column for delivered orders?"
        )

    def test_active_customers_matches_source(self, week3_path, data_path):
        """Active customer count must be within 10% of actual."""
        import pandas as pd

        orders = pd.read_csv(data_path / "orders.csv")
        expected = orders[orders["status"] == "delivered"]["customer_id"].nunique()

        metrics = pd.read_csv(week3_path / "metrics.csv")
        row = metrics[metrics["metric"].str.strip().str.lower() == "active_customers"]
        submitted = int(float(row["value"].iloc[0]))

        pct_diff = abs(submitted - expected) / expected
        assert pct_diff < 0.10, (
            f"Active customers {submitted} differs from expected {expected} by {pct_diff:.1%}"
        )

    def test_avg_order_value_matches_source(self, week3_path, data_path):
        """Average order value must be within 5% of actual."""
        import pandas as pd

        orders = pd.read_csv(data_path / "orders.csv")
        delivered = orders[orders["status"] == "delivered"]
        expected = delivered["total"].mean()

        metrics = pd.read_csv(week3_path / "metrics.csv")
        row = metrics[metrics["metric"].str.strip().str.lower() == "avg_order_value"]
        submitted = float(row["value"].iloc[0])

        pct_diff = abs(submitted - expected) / expected
        assert pct_diff < 0.05, (
            f"Avg order value {submitted:,.2f} differs from expected {expected:,.2f} by {pct_diff:.1%}"
        )

    def test_top_products_match_source(self, week3_path, data_path):
        """At least 3 of top 5 products must match actual top 5."""
        import pandas as pd

        items = pd.read_csv(data_path / "order_items.csv")
        products = pd.read_csv(data_path / "products.csv")
        revenue = items.groupby("product_id")["item_total"].sum().reset_index()
        revenue = revenue.merge(
            products[["id", "name"]], left_on="product_id", right_on="id"
        )
        top5_expected = set(
            revenue.nlargest(5, "item_total")["name"].str.strip().str.lower()
        )

        metrics = pd.read_csv(week3_path / "metrics.csv")
        top_rows = metrics[
            metrics["metric"].str.strip().str.lower().str.startswith("top_product_")
        ]
        top5_submitted = set(top_rows["value"].str.strip().str.lower())

        overlap = top5_expected & top5_submitted
        assert len(overlap) >= 3, (
            f"Only {len(overlap)} of your top 5 products match the actual top 5.\n"
            f"Expected (any 3): {top5_expected}\n"
            f"Submitted: {top5_submitted}"
        )
