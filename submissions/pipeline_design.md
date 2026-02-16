# Data Ingestion and Processing Pipeline Design

## Overview
This pipeline is designed to serve as a reliable bridge between raw external CSV data sources and a structured analytical environment. Its primary objective is to automate the ingestion of distributed data files, ensuring that every record processed meets strict quality standards while maintaining a high degree of operational visibility. By decoupling extraction from transformation, the system can scale to handle varying file volumes without compromising the integrity of the downstream datasets.

The pipeline operates on a batch-processing model, typically triggered on a schedule or by the arrival of new files. It addresses the inherent "messiness" of external data—such as inconsistent quoting, varying date formats, and missing values—by applying a rigorous validation layer before any business logic is executed. This proactive approach minimizes data corruption in the production environment and provides engineers with actionable feedback on source data quality.

## Data Flow
The data follows a linear but highly guarded path from external sources to the final persistence layer:

```text
[ External Sources ]
       |
       v (CSV Files)
+-----------------------+      +-----------------------+
|    Extraction Layer   | ---> |   Idempotency Store   |
| (Source Discovery)    |      | (File Hash Tracking)  |
+-----------+-----------+      +-----------+-----------+
            |                              |
            v (Raw Dataframes)             | (Check if processed)
+-----------------------+                  |
|   Validation Layer    | <----------------+
| (Schema & Integrity)  |
+-----------+-----------+
            |
            +------------> [ Dead Letter Queue (Corrupt Records) ]
            |
            v (Clean Data)
+-----------------------+
| Transformation Layer  |
| (Agg & Cleanse)       |
+-----------+-----------+
            |
            v (Final Output)
+-----------------------+      +-----------------------+
|     Loading Layer     | ---> |   Processed Files     |
| (Atomic Write)        |      | (Parquet/Versioned CSV)|
+-----------------------+      +-----------------------+
```

## Components
1.  **Source Extractor**: Responsible for scanning designated directories for new CSV files. It reads the files into memory using a stream-friendly approach to avoid Memory errors on large datasets. It also extracts metadata like file size and modification timestamps.
2.  **Idempotency Manager**: A stateful component that records the MD5 hash and filename of every successfully processed file. Before processing starts, it checks the current file against its registry to prevent redundant processing and duplicate data entries in the final output.
3.  **Data Validator**: Utilizes schema-on-read principles to enforce data types, check for required fields, and validate business constraints (e.g., non-negative prices). Records failing validation are siphoned off to a "Dead Letter" storage area for manual review.
4.  **Logic Transformer**: Performs the heavy lifting—data normalization, type casting (e.g., ISO-8601 string to DateTime objects), and multi-dimensional aggregations (e.g., daily sales totals by region and category).
5.  **Atomic Loader**: Handles the final persistence. To prevent data corruption, it writes data to a temporary location first and performs an atomic "move/rename" to the final destination, ensuring that partial failures don't leave partially written files.

## Error Handling
The pipeline follows a "fail-fast but recover-gracefully" philosophy to ensure reliability:
-   **Record-Level Errors**: If a specific row is corrupt (e.g., letters in a numeric "quantity" column), the `Data Validator` logs the specific error with the row index and moves that specific record to a Dead Letter Queue (DLQ). The rest of the batch continues processing to maximize throughput.
-   **File-Level Errors**: If a file is completely unreadable or the header is mismatched, the entire file is marked as "FAILED" in the tracking store, and an immediate high-priority alert is triggered.
-   **Transient Failures**: Network-related storage issues are handled via an exponential backoff retry strategy (retrying up to 3 times before giving up).
-   **Traceability**: Every error log includes a `run_id` and `file_name`, allowing engineers to trace any data anomaly back to its precise origin.

## Monitoring
Operational health is tracked through comprehensive logging and metric extraction:
-   **Structured Logging**: Every execution step (START, VALIDATE, TRANSFORM, LOAD, COMPLETE) is logged in JSON format to facilitate easy querying in log aggregators.
-   **Key Performance Indicators (KPIs)**:
    -   `records_ingested_count`: The raw volume of records received.
    -   `records_processed_count`: The volume of records successfully stored.
    -   `failure_rate_percent`: The ratio of DLQ records to total records; if this exceeds 5%, a notification is sent to the data quality team.
    -   `pipeline_latency`: The total wall-clock time for the run.
-   **Success Signals**: On completion, a `_SUCCESS` metadata file is written alongside the output. Downstream processes are instructed to only consume data where this signal is present.

## Technology Choices
-   **Python**: Chosen as the primary language due to its unparalleled ecosystem for data engineering and native support for all necessary CSV parsing libraries.
-   **Polars**: We have selected Polars over Pandas for the core engine. Polars provides a "lazy" evaluation API that optimizes query plans before execution, and its memory management is significantly more efficient for multi-gigabit CSV files.
-   **Pydantic**: Used for the Validation Layer. It provides a declarative way to define data schemas, offering high-performance type checking and automatic validation error generation.
-   **SQLite**: A lightweight, serverless database used by the Idempotency Manager to track processed file hashes. It provides ACID compliance for state tracking without the management overhead of a full database cluster.
-   **Loguru**: A specialized logging framework that handles rotating logs and asynchronous logging, ensuring that the pipeline's logging activity never becomes a performance bottleneck.
