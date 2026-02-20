import pandas as pd

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate customers based on email (case-insensitive).
    Keep the record with the highest total_orders.

    Args:
        df: DataFrame with customer data

    Returns:
        DataFrame with duplicates removed
    """


    return dedup_df