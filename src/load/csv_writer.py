import csv
from datetime import datetime
from pathlib import Path
from typing import Optional
import logging


def save_to_csv(
    data: list[dict], output_dir: str = "data/", filename: Optional[str] = None
) -> None:
    """
    Save transformed weather data to CSV file.

    Args:
        data: List of transformed weather dictionaries
        output_dir: Directory to save CSV file
        filename: CSV filename (if None, generate with timestamp)
    """
    logger = logging.getLogger(__name__)

    if not data:
        logger.warning("No data to save")
        return

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    if filename is None:
        filename = f"weather_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

    filepath = Path(output_dir) / filename

    clean_data = [record for record in data if record is not None]

    if not clean_data:
        logger.warning("No valid data to save (all records failed transformation)")
        return

    if len(clean_data) < len(data):
        logger.warning("Skipped %d invalid records", len(data) - len(clean_data))

    try:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            fieldnames = clean_data[0].keys() if clean_data else []
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(clean_data)
        logger.info("Saved %d records to %s", len(clean_data), filepath)
    except Exception as e:
        logger.error("Failed to save CSV to %s: %s", filepath, e)
        raise
