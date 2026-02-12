"""Shared pytest configuration and fixtures for task tests."""

import os
import pytest
from pathlib import Path


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--student-folder",
        action="store",
        default=None,
        help="Path to student submission folder"
    )


@pytest.fixture
def student_folder(request):
    """
    Get path to student submission folder.

    Priority:
    1. --student-folder command line option
    2. STUDENT_FOLDER environment variable
    3. Repository root (default for GitHub Actions)
    """
    # Check command line option
    folder = request.config.getoption("--student-folder")
    if folder:
        return Path(folder)

    # Check environment variable
    folder = os.environ.get("STUDENT_FOLDER")
    if folder:
        return Path(folder)

    # Default to repo root (works in GitHub Actions)
    return Path(__file__).parent.parent


@pytest.fixture
def repo_root():
    """Get path to repository root."""
    return Path(__file__).parent.parent


@pytest.fixture
def data_path(repo_root):
    """Get path to shared data folder."""
    return repo_root / "data"


@pytest.fixture
def sample_customers(data_path):
    """Load sample customers data."""
    import pandas as pd

    csv_path = data_path / "customers.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return None


@pytest.fixture
def sample_orders(data_path):
    """Load sample orders data."""
    import pandas as pd

    csv_path = data_path / "orders.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return None


@pytest.fixture
def sample_products(data_path):
    """Load sample products data."""
    import pandas as pd

    csv_path = data_path / "products.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return None
