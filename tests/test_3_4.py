"""Tests for Task 3.4: Dashboard Creation

Validates:
- Dashboard screenshot exists and is a real image
- metrics.csv exists with correct format
- Required KPI metrics are present
- Numeric accuracy within tolerance of reference values
- Top products match actual top 5 from data
"""

import base64
import csv
import json
import pytest
from pathlib import Path

# Reference values are encoded to prevent casual reading
_REF = json.loads(base64.b64decode(
    "eyJ0b3RhbF9yZXZlbnVlIjogWzYzNjYxMDEyLCA0NDM3MzgxMF0sICJhY3RpdmVfY3VzdG"
    "9tZXJzIjogWzE4MzEsIDE1NjJdLCAiYXZnX29yZGVyX3ZhbHVlIjogWzg5OTcsIDg5ODVd"
    "LCAidG9wX3Byb2R1Y3RzIjogWyJzdGFuZGluZyBkZXNrIGVsZWN0cmljIiwgImVyZ29ub2"
    "1pYyBvZmZpY2UgY2hhaXIiLCAicG9ydGFibGUgbW9uaXRvciAxNS42XCIiLCAibm9pc2Ug"
    "Y2FuY2VsbGluZyBoZWFkcGhvbmVzIiwgInVzYiBtaWNyb3Bob25lIHBvZGNhc3QiXSwgIn"
    "RvbGVyYW5jZXMiOiB7InRvdGFsX3JldmVudWUiOiAwLjE1LCAiYWN0aXZlX2N1c3RvbWVy"
    "cyI6IDAuMiwgImF2Z19vcmRlcl92YWx1ZSI6IDAuMTUsICJ0b3BfcHJvZHVjdHNfbWluX2"
    "1hdGNoIjogM319"
).decode())


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


def _check_numeric_metric(metrics_data, key, label):
    """Check a numeric metric against obfuscated reference values."""
    if metrics_data is None:
        pytest.skip("metrics.csv not found")
    if key not in metrics_data:
        pytest.skip(f"{key} not in metrics.csv")

    try:
        student_val = float(metrics_data[key].replace(",", ""))
    except ValueError:
        pytest.fail(
            f"Could not parse {key} value: '{metrics_data[key]}'\n"
            f"Expected a number."
        )

    refs = _REF[key]
    tol = _REF["tolerances"][key]

    match = any(abs(student_val - r) / r <= tol for r in refs)

    assert match, (
        f"{label} value {student_val:,.2f} is outside the expected range.\n\n"
        f"Check your calculation. Make sure you're using the correct columns\n"
        f"from the source data."
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
        """Total revenue should be within tolerance of reference value."""
        _check_numeric_metric(metrics_data, "total_revenue", "Total revenue")

    def test_active_customers_accuracy(self, metrics_data):
        """Active customers should be within tolerance of reference value."""
        _check_numeric_metric(metrics_data, "active_customers", "Active customers")

    def test_avg_order_value_accuracy(self, metrics_data):
        """Average order value should be within tolerance of reference value."""
        _check_numeric_metric(metrics_data, "avg_order_value", "Avg order value")

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

        actual_top = _REF["top_products"]
        min_match = _REF["tolerances"]["top_products_min_match"]

        matches = 0
        for student_product in student_products:
            for actual in actual_top:
                if actual in student_product or student_product in actual:
                    matches += 1
                    break
                actual_words = set(actual.split())
                student_words = set(student_product.split())
                if len(actual_words & student_words) >= 2:
                    matches += 1
                    break

        assert matches >= min_match, (
            f"Only {matches} of your top 5 products match the expected list.\n"
            f"Need at least {min_match} matches.\n\n"
            "Hint: Top products are ranked by total revenue (price * quantity).\n"
            "Make sure you're joining orders with order_items and products."
        )
