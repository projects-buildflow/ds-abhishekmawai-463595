"""Reusable cleaning for marketing customer data. Run whenever new data arrives."""

import pandas as pd


def clean_customer_data(input_path, output_path):
    """Read dirty CSV, clean it, save to output path, return a report."""
    df = pd.read_csv(input_path)
    rows_before = len(df)

    # Drop missing names first (empty or NaN), then strip so we don't turn NaN into "nan"
    missing_name = df["full_name"].isna() | (df["full_name"].astype(str).str.strip() == "")
    df = df[~missing_name]

    # Strip whitespace from full_name and location
    if "full_name" in df.columns:
        df["full_name"] = df["full_name"].astype(str).str.strip()
    if "location" in df.columns:
        df["location"] = df["location"].astype(str).str.strip()

    # Fix invalid ages: remove rows where age < 0 or age > 120
    if "age" in df.columns:
        df["age"] = pd.to_numeric(df["age"], errors="coerce")
        df = df[df["age"].isna() | ((df["age"] >= 0) & (df["age"] <= 120))]

    # Fix invalid emails: remove rows where email is present but has no @
    if "email_address" in df.columns:
        email_filled = df["email_address"].notna() & (df["email_address"].astype(str).str.strip() != "")
        email_has_at = df["email_address"].astype(str).str.contains("@", na=False)
        df = df[~(email_filled & ~email_has_at)]

    # Remove duplicate emails (keep first occurrence)
    if "email_address" in df.columns:
        df = df.drop_duplicates(subset=["email_address"], keep="first")

    # Fix invalid dates: remove rows where date_joined is not a valid date
    if "date_joined" in df.columns:
        parsed = pd.to_datetime(df["date_joined"], errors="coerce")
        df = df[parsed.notna()]

    df.to_csv(output_path, index=False)
    rows_after = len(df)

    return {
        "rows_before": rows_before,
        "rows_after": rows_after,
    }
