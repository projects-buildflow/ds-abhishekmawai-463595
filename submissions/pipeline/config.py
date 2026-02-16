from pathlib import Path

# Base directory of the project (assuming config.py is in submissions/pipeline/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Data directories
DATA_DIR = BASE_DIR / "data"
PIPELINE_DIR = BASE_DIR / "submissions" / "pipeline"
OUTPUT_DIR = PIPELINE_DIR / "output"

# File paths
RAW_DATA_FILES = {
    "orders": DATA_DIR / "orders.csv",
    "customers": DATA_DIR / "customers.csv",
}
