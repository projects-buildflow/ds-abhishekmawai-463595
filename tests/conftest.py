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
    folder = request.config.getoption("--student-folder")
    if folder:
        return Path(folder)

    folder = os.environ.get("STUDENT_FOLDER")
    if folder:
        return Path(folder)

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


def _load_csvs_into_duckdb(conn, data_dir, multiply=1):
    """Load CSV files into DuckDB tables, cleaning invalid dates.

    When multiply > 1, creates unique IDs per copy to preserve
    correct JOIN cardinality (avoids N*N fan-out from duplicate IDs).
    """
    for csv_path in [data_dir / f for f in ["products.csv", "categories.csv"]]:
        if csv_path.exists():
            name = csv_path.stem
            conn.execute(
                f"CREATE TABLE {name} AS SELECT * FROM read_csv_auto('{csv_path}')"
            )

    if multiply > 1:
        csv = data_dir / "customers.csv"
        if csv.exists():
            conn.execute(f"""
                CREATE TABLE customers AS
                SELECT customer_id + (s.i - 1) * 20000 AS customer_id,
                       first_name, last_name, email, phone, age, gender,
                       country, city, signup_date, signup_source, segment,
                       is_subscribed, total_orders, total_spent,
                       avg_order_value, last_order_date
                FROM read_csv_auto('{csv}') t
                CROSS JOIN generate_series(1, {multiply}) s(i)
            """)
        csv = data_dir / "orders.csv"
        if csv.exists():
            conn.execute(f"""
                CREATE TABLE orders AS
                SELECT order_id + (s.i - 1) * 200000 AS order_id,
                       customer_id + (s.i - 1) * 20000 AS customer_id,
                       order_date, order_time, status, payment_method,
                       subtotal, shipping, tax, total, items_count,
                       shipping_city, shipping_country
                FROM read_csv_auto('{csv}') t
                CROSS JOIN generate_series(1, {multiply}) s(i)
            """)
        csv = data_dir / "order_items.csv"
        if csv.exists():
            conn.execute(f"""
                CREATE TABLE order_items AS
                SELECT order_item_id || '_' || s.i AS order_item_id,
                       order_id + (s.i - 1) * 200000 AS order_id,
                       product_id, quantity, unit_price,
                       discount_percent, item_total
                FROM read_csv_auto('{csv}') t
                CROSS JOIN generate_series(1, {multiply}) s(i)
            """)
    else:
        for name in ["customers", "orders", "order_items"]:
            csv_path = data_dir / f"{name}.csv"
            if csv_path.exists():
                conn.execute(
                    f"CREATE TABLE {name} AS "
                    f"SELECT * FROM read_csv_auto('{csv_path}')"
                )

    # Clean invalid date strings so student SQL doesn't need TRY_CAST
    conn.execute("""
        UPDATE customers
        SET signup_date = NULL
        WHERE TRY_CAST(signup_date AS DATE) IS NULL
    """)


@pytest.fixture(scope="session")
def duckdb_conn():
    """Session-scoped DuckDB connection with all CSV data loaded."""
    import duckdb

    conn = duckdb.connect()
    data_dir = Path(__file__).parent.parent / "data"
    _load_csvs_into_duckdb(conn, data_dir, multiply=1)

    yield conn
    conn.close()


@pytest.fixture(scope="session")
def duckdb_conn_large():
    """Session-scoped DuckDB connection with 50x data for timing tests."""
    import duckdb

    conn = duckdb.connect()
    data_dir = Path(__file__).parent.parent / "data"
    _load_csvs_into_duckdb(conn, data_dir, multiply=50)

    yield conn
    conn.close()


@pytest.fixture
def run_sql(duckdb_conn):
    """Execute SQL and return a DataFrame."""
    def _run(sql):
        result = duckdb_conn.execute(sql)
        return result.fetchdf()

    return _run
