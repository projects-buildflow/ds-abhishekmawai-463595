import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def save_to_csv(df: pd.DataFrame, output_path: Path):
    """Saves a DataFrame to a CSV file. Ensures the destination folder exists."""
    if df.empty:
        logger.warning(f"Skipping save to {output_path}: DataFrame is empty.")
        return

    try:
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(output_path, index=False)
        logger.info(f"Successfully saved data to {output_path}")
    except Exception as e:
        logger.error(f"Failed to save data to {output_path}: {e}")
        raise
