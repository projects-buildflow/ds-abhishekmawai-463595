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
    # Handle empty input explicitly
    if df.empty:
        return df.copy()

    # Work on a copy so we don't mutate the caller's DataFrame
    dedup_df = df.copy()

    # Normalize email casing for comparison
    dedup_df["_email_lower"] = dedup_df["email"].str.lower()

    # Preserve original row order while selecting the highest total_orders per email
    dedup_df["_orig_index"] = dedup_df.index

    # Sort so that, within each email group, the row with the highest total_orders comes first
    dedup_df = dedup_df.sort_values(
        by=["_email_lower", "total_orders"],
        ascending=[True, False],
    )

    # Drop duplicates keeping the row with the highest total_orders for each email
    dedup_df = dedup_df.drop_duplicates(subset="_email_lower", keep="first")

    # Restore original order of the remaining rows
    dedup_df = dedup_df.sort_values(by="_orig_index")

    # Clean up helper columns
    dedup_df = dedup_df.drop(columns=["_email_lower", "_orig_index"])

    return dedup_df