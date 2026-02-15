"""Tests for Task 3.4: Dashboard Creation

Validates:
- Dashboard screenshot exists and is a real image
- metrics.csv exists with correct format
- Required KPI metrics are present
- Numeric accuracy within tolerance of reference values
- Top products match actual top 5 from data
"""

import csv
import pytest
from pathlib import Path


@pytest.fixture
def submissions_path(student_folder):
    """Get path to student's submissions folder."""
    if not student_folder:
        pytest.skip("Student folder not provided")
    return Path(student_folder) / "submissions"


@pytest.fixture
def dashboard_screenshot(submissions_path):
    """Find and return the dashboard screenshot path."""
    valid_extensions = [".png", ".jpg", ".jpeg", ".gif", ".webp"]

    for ext in valid_extensions:
        path = submissions_path / f"dashboard{ext}"
        if path.exists():
            return path

    return None


@pytest.fixture
def metrics_data(submissions_path):
    """Load metrics.csv and return as dict {metric: value}."""
    csv_path = submissions_path / "metrics.csv"
    if not csv_path.exists():
        return None

    data = {}
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            metric = row.get("metric", "").strip().lower()
            value = row.get("value", "").strip()
            if metric:
                data[metric] = value
    return data


class TestDashboardExists:
    """Verify dashboard screenshot exists."""

    def test_dashboard_screenshot_exists(self, submissions_path, dashboard_screenshot):
        """Dashboard screenshot must exist."""
        assert dashboard_screenshot is not None, (
            "Dashboard screenshot not found.\n\n"
            "Save your dashboard as one of:\n"
            "- dashboard.png\n"
            "- dashboard.jpg\n"
            "- dashboard.jpeg\n\n"
            f"In folder: {submissions_path}"
        )

    def test_screenshot_has_content(self, dashboard_screenshot):
        """Screenshot must have content (not an empty file)."""
        if dashboard_screenshot is None:
            pytest.skip("Dashboard screenshot not found")

        file_size = dashboard_screenshot.stat().st_size

        assert file_size > 1000, (
            f"Screenshot file is only {file_size} bytes.\n"
            "This seems too small. Make sure the file saved correctly."
        )


class TestImageValidity:
    """Verify the screenshot is a valid image file."""

    def test_screenshot_is_reasonable_size(self, dashboard_screenshot):
        """Screenshot should be at least 10KB for a real dashboard image."""
        if dashboard_screenshot is None:
            pytest.skip("Dashboard screenshot not found")

        file_size = dashboard_screenshot.stat().st_size

        assert file_size > 10000, (
            f"Screenshot is only {file_size / 1024:.1f} KB.\n"
            "A dashboard screenshot should be larger.\n"
            "Make sure you captured the full dashboard, not a thumbnail."
        )


class TestMetricsCSV:
    """Validate metrics.csv file format and content."""

    def test_metrics_csv_exists(self, submissions_path):
        """metrics.csv must exist in submissions folder."""
        csv_path = submissions_path / "metrics.csv"
        assert csv_path.exists(), (
            "metrics.csv not found.\n\n"
            "Export your KPI values to submissions/metrics.csv with columns:\n"
            "metric,value\n\n"
            "See the task instructions for the required format."
        )

    def test_metrics_csv_format(self, submissions_path):
        """metrics.csv must have 'metric' and 'value' columns."""
        csv_path = submissions_path / "metrics.csv"
        if not csv_path.exists():
            pytest.skip("metrics.csv not found")

        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            headers = [h.strip().lower() for h in (reader.fieldnames or [])]

        assert "metric" in headers, (
            f"Missing 'metric' column in metrics.csv.\n"
            f"Found columns: {headers}\n"
            "Expected: metric,value"
        )
        assert "value" in headers, (
            f"Missing 'value' column in metrics.csv.\n"
            f"Found columns: {headers}\n"
            "Expected: metric,value"
        )

    def test_required_metrics_present(self, metrics_data):
        """All 8 required metric keys must be present."""
        if metrics_data is None:
            pytest.skip("metrics.csv not found or could not be parsed")

        required = [
            "total_revenue",
            "active_customers",
            "avg_order_value",
            "top_product_1",
            "top_product_2",
            "top_product_3",
            "top_product_4",
            "top_product_5",
        ]
        missing = [m for m in required if m not in metrics_data]

        assert not missing, (
            f"Missing required metrics in metrics.csv: {missing}\n\n"
            "Your metrics.csv must include all of:\n"
            + "\n".join(f"  - {m}" for m in required)
        )

    def test_total_revenue_accuracy(self, metrics_data):
        """Total revenue should be within 15% of reference value."""
        if metrics_data is None:
            pytest.skip("metrics.csv not found")
        if "total_revenue" not in metrics_data:
            pytest.skip("total_revenue not in metrics.csv")

        try:
            student_val = float(metrics_data["total_revenue"].replace(",", ""))
        except ValueError:
            pytest.fail(
                f"Could not parse total_revenue value: '{metrics_data['total_revenue']}'\n"
                "Expected a number like 63661012 or 63,661,012"
            )

        # Accept either all-orders (~63.7M) or delivered-only (~44.4M)
        ref_all = 63_661_012
        ref_delivered = 44_373_810
        tolerance = 0.15

        within_all = abs(student_val - ref_all) / ref_all <= tolerance
        within_delivered = abs(student_val - ref_delivered) / ref_delivered <= tolerance

        assert within_all or within_delivered, (
            f"Total revenue {student_val:,.0f} is not within 15% of expected.\n\n"
            f"Reference values:\n"
            f"  All orders:      ~63,661,012\n"
            f"  Delivered only:  ~44,373,810\n\n"
            "Check your revenue calculation. Common issues:\n"
            "- Using 'subtotal' instead of 'total'\n"
            "- Filtering out valid order statuses"
        )

    def test_active_customers_accuracy(self, metrics_data):
        """Active customers should be within 20% of reference value."""
        if metrics_data is None:
            pytest.skip("metrics.csv not found")
        if "active_customers" not in metrics_data:
            pytest.skip("active_customers not in metrics.csv")

        try:
            student_val = float(metrics_data["active_customers"].replace(",", ""))
        except ValueError:
            pytest.fail(
                f"Could not parse active_customers value: '{metrics_data['active_customers']}'\n"
                "Expected a number like 1831"
            )

        # Accept either all-orders (~1831) or delivered-only (~1562)
        ref_all = 1831
        ref_delivered = 1562
        tolerance = 0.20

        within_all = abs(student_val - ref_all) / ref_all <= tolerance
        within_delivered = abs(student_val - ref_delivered) / ref_delivered <= tolerance

        assert within_all or within_delivered, (
            f"Active customers {student_val:,.0f} is not within 20% of expected.\n\n"
            f"Reference values:\n"
            f"  All orders:      ~1,831\n"
            f"  Delivered only:  ~1,562\n\n"
            "Active customers = unique customer_id count in orders."
        )

    def test_avg_order_value_accuracy(self, metrics_data):
        """Average order value should be within 15% of reference value."""
        if metrics_data is None:
            pytest.skip("metrics.csv not found")
        if "avg_order_value" not in metrics_data:
            pytest.skip("avg_order_value not in metrics.csv")

        try:
            student_val = float(metrics_data["avg_order_value"].replace(",", ""))
        except ValueError:
            pytest.fail(
                f"Could not parse avg_order_value value: '{metrics_data['avg_order_value']}'\n"
                "Expected a number like 8997"
            )

        # Accept either all-orders (~8997) or delivered-only (~8985)
        ref_all = 8997
        ref_delivered = 8985
        tolerance = 0.15

        within_all = abs(student_val - ref_all) / ref_all <= tolerance
        within_delivered = abs(student_val - ref_delivered) / ref_delivered <= tolerance

        assert within_all or within_delivered, (
            f"Avg order value {student_val:,.2f} is not within 15% of expected.\n\n"
            f"Reference values:\n"
            f"  All orders:      ~8,997\n"
            f"  Delivered only:  ~8,985\n\n"
            "AOV = total revenue / number of orders."
        )

    def test_top_products_accuracy(self, metrics_data):
        """At least 3 of top 5 products should match actual top 5."""
        if metrics_data is None:
            pytest.skip("metrics.csv not found")

        student_products = []
        for i in range(1, 6):
            key = f"top_product_{i}"
            if key in metrics_data and metrics_data[key]:
                student_products.append(metrics_data[key].strip().lower())

        if not student_products:
            pytest.skip("No top_product entries found in metrics.csv")

        # Actual top 5 products by revenue from the dataset
        actual_top_5 = [
            "standing desk electric",
            "ergonomic office chair",
            "portable monitor 15.6\"",
            "noise cancelling headphones",
            "usb microphone podcast",
        ]

        matches = 0
        for student_product in student_products:
            for actual in actual_top_5:
                # Fuzzy match: check if either contains the other or significant overlap
                if actual in student_product or student_product in actual:
                    matches += 1
                    break
                # Also check key words (first 2+ words match)
                actual_words = set(actual.split())
                student_words = set(student_product.split())
                if len(actual_words & student_words) >= 2:
                    matches += 1
                    break

        assert matches >= 3, (
            f"Only {matches} of your top 5 products match the actual top 5.\n"
            f"Need at least 3 matches.\n\n"
            f"Your products: {student_products}\n\n"
            "Hint: Top products are ranked by total revenue (price * quantity).\n"
            "Make sure you're joining orders with order_items and products."
        )
