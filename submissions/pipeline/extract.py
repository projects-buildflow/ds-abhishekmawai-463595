import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def extract_csv(file_path: Path) -> pd.DataFrame:
    """Reads a CSV file and returns a pandas DataFrame. Handles the case where a file doesn't exist."""
    if not file_path.exists():
        logger.error(f"Extraction failed: File not found at {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        logger.info(f"Extracting data from {file_path}...")
        df = pd.read_csv(file_path)
        logger.info(f"Successfully extracted {len(df)} rows.")
        return df
    except Exception as e:
        logger.error(f"Error during extraction of {file_path}: {e}")
        raise
