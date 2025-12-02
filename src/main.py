import logging

from ingestion.loader import load_data
from db.database import init_db
from db.save import save_data
from reporting.resports import save_metrics_csv_pdf

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


def main():
    """
    Execute the complete data processing pipeline.

    Full workflow:
    1. Load and validate CSV files from the data directory
    2. Compute all metrics and generate reports (CSV + PDF)
    3. Initialize the database schema
    4. Save validated data to the database

    Logs are written at each major step with timestamps.

    Raises:
        Exception: Propagates exceptions from data loading, processing, or database operations
    """
    logging.info("Starting data process")
    data = load_data()
    save_metrics_csv_pdf(data)
    init_db()
    save_data(data)
    logging.info("Data process completed")


if __name__ == "__main__":
    main()
