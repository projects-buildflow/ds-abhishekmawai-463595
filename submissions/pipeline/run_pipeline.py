import logging
import sys
from pathlib import Path

# Fix path to allow local imports
sys.path.append(str(Path(__file__).parent))

import config
import extract
import transform
import load

def setup_logging():
    """Configures the logging module."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def run_pipeline():
    """
    Orchestrates the ETL pipeline:
    1. Extract data from raw CSV files.
    2. Transform data (clean and aggregate).
    3. Load results into processed CSV files.
    """
    logger = logging.getLogger("DataPipeline")
    logger.info("Pipeline started.")
    
    try:
        # Phase 1: EXTRACTION
        logger.info("--- Extraction Phase ---")
        orders_path = config.RAW_DATA_FILES["orders"]
        df_orders = extract.extract_csv(orders_path)
        
        # Phase 2: TRANSFORMATION
        logger.info("--- Transformation Phase ---")
        df_orders_clean = transform.clean_data(df_orders)
        
        # Aggregation 1: Daily Revenue
        df_daily_revenue = transform.aggregate_daily_revenue(df_orders_clean)
        
        # Aggregation 2: Regional Statistics
        df_region_stats = transform.aggregate_by_region(df_orders_clean)
        
        # Phase 3: LOADING
        logger.info("--- Loading Phase ---")
        load.save_to_csv(df_daily_revenue, config.OUTPUT_DIR / "daily_revenue.csv")
        load.save_to_csv(df_region_stats, config.OUTPUT_DIR / "region_stats.csv")
        
        logger.info("Pipeline completed successfully!")
        
    except FileNotFoundError as fnf:
        logger.error(f"Critical Error: A required file was not found. {fnf}")
    except Exception as e:
        logger.error(f"Pipeline failed unexpectedly: {e}")
        # Re-raise or exit depending on how this is called
        raise

if __name__ == "__main__":
    setup_logging()
    try:
        run_pipeline()
    except KeyboardInterrupt:
        print("\nPipeline stopped by user.")
    except Exception:
        sys.exit(1)
