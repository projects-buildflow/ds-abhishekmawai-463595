import pandas as pd
import logging

logger = logging.getLogger(__name__)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans data by dropping invalid rows (missing IDs or critical values)
    and fixing data types.
    """
    initial_count = len(df)
    
    # Drop rows missing critical columns
    # Assuming 'order_id', 'order_date', and 'total' are critical
    critical_cols = ['order_id', 'order_date', 'total']
    # Check which critical columns actually exist in the dataframe
    actual_critical_cols = [col for col in critical_cols if col in df.columns]
    
    df = df.dropna(subset=actual_critical_cols)
    
    # Process order_date if it exists
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        df = df.dropna(subset=['order_date'])
    
    # Process total if it exists
    if 'total' in df.columns:
        df['total'] = pd.to_numeric(df['total'], errors='coerce')
        df = df.dropna(subset=['total'])
        
    cleaned_count = len(df)
    logger.info(f"Data cleaning complete: {initial_count} -> {cleaned_count} rows.")
    return df

def aggregate_daily_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Computes total revenue aggregated by day."""
    if 'order_date' not in df.columns or 'total' not in df.columns:
        logger.warning("Required columns for daily revenue aggregation missing.")
        return pd.DataFrame()
        
    revenue = df.groupby('order_date')['total'].sum().reset_index()
    revenue = revenue.rename(columns={'total': 'daily_revenue'})
    # Sort by date
    revenue = revenue.sort_values('order_date')
    logger.info(f"Computed daily revenue for {len(revenue)} days.")
    return revenue

def aggregate_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Computes order counts and revenue by region (shipping_country)."""
    region_col = 'shipping_country'
    if region_col not in df.columns:
        logger.warning(f"Column '{region_col}' missing. Cannot aggregate by region.")
        return pd.DataFrame()
        
    # Handle possible empty regions
    df[region_col] = df[region_col].fillna('Unknown')
    
    region_stats = df.groupby(region_col).agg({
        'order_id': 'count',
        'total': 'sum'
    }).reset_index()
    
    region_stats = region_stats.rename(columns={
        'order_id': 'order_count',
        'total': 'total_revenue'
    })
    logger.info(f"Computed statistics for {len(region_stats)} regions.")
    return region_stats
