"""
Data loading utilities for Cartly analytics.

This module provides functions for loading data from CSV files with proper
type handling and date parsing.

NOTE: This file has an intentional bug in the date parsing!
Task 1.3 asks students to fix this bug.
"""

import pandas as pd
from pathlib import Path


def load_orders(data_path: str = None) -> pd.DataFrame:
    """
    Load orders data from CSV with date parsing.

    Args:
        data_path: Path to the orders CSV file. If None, uses default location.

    Returns:
        DataFrame with orders data, including parsed date columns.

    Example:
        >>> orders = load_orders()
        >>> orders['order_date'].dtype
        datetime64[ns]
    """
    if data_path is None:
        # Default path relative to this file
        data_path = Path(__file__).parent.parent / "data" / "orders.csv"
    else:
        data_path = Path(data_path)

    if not data_path.exists():
        raise FileNotFoundError(f"Orders file not found: {data_path}")

    # BUG: Wrong date format specified!
    # The actual data uses YYYY-MM-DD format, but we're specifying MM/DD/YYYY
    # This causes dates to be parsed incorrectly or as NaT
    # Students should fix this by using the correct format or letting pandas infer
    df = pd.read_csv(
        data_path,
        parse_dates=['order_date'],
        date_format='%m/%d/%Y',  # BUG: Should be '%Y-%m-%d' or removed entirely
    )

    return df


def load_customers(data_path: str = None) -> pd.DataFrame:
    """
    Load customers data from CSV.

    Args:
        data_path: Path to the customers CSV file. If None, uses default location.

    Returns:
        DataFrame with customers data.

    Example:
        >>> customers = load_customers()
        >>> 'email' in customers.columns
        True
    """
    if data_path is None:
        data_path = Path(__file__).parent.parent / "data" / "customers.csv"
    else:
        data_path = Path(data_path)

    if not data_path.exists():
        raise FileNotFoundError(f"Customers file not found: {data_path}")

    df = pd.read_csv(data_path)
    return df


def load_products(data_path: str = None) -> pd.DataFrame:
    """
    Load products data from CSV.

    Args:
        data_path: Path to the products CSV file. If None, uses default location.

    Returns:
        DataFrame with products data.
    """
    if data_path is None:
        data_path = Path(__file__).parent.parent / "data" / "products.csv"
    else:
        data_path = Path(data_path)

    if not data_path.exists():
        raise FileNotFoundError(f"Products file not found: {data_path}")

    df = pd.read_csv(data_path)
    return df
