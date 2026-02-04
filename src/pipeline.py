import logging
from .extract.weather_api import WeatherAPI
from .transform.data_processor import transform_weather_data
from .load.db_loader import save_to_database
from .config import load_config
from .utils.logger import setup_logging
from typing import List, Dict, Optional


def extract_data() -> List[Dict]:
    """
    Extract: Fetch weather data from API.

    Returns:
        List of raw weather data dictionaries
    """
    config = load_config()
    setup_logging()
    logger = logging.getLogger(__name__)

    weather_api = WeatherAPI()
    cities_list = config["cities"]

    logger.info("Starting data extraction for %d cities", len(cities_list))
    data_from_API = weather_api.get_weather_data(cities_list)
    logger.info("Extracted %d records", len(data_from_API))

    return data_from_API


def transform_data_impl(raw_data: List[Dict]) -> List[Optional[Dict]]:
    """
    Transform: Clean and process raw weather data.

    Args:
        raw_data: List of raw weather data dictionaries

    Returns:
        List of transformed data dictionaries
    """
    logger = logging.getLogger(__name__)
    logger.info("Starting data transformation")

    result = []
    for i in raw_data:
        result.append(transform_weather_data(i))

    logger.info("Transformed %d records", len(result))
    return result


def transform_data(**context):
    """Airflow wrapper for transform."""
    ti = context['ti']
    raw_data = ti.xcom_pull(task_ids='extract_weather_data')
    return transform_data_impl(raw_data)


def load_data_impl(clean_data: List[Dict]) -> None:
    """
    Load: Save transformed data to database.

    Args:
        clean_data: List of transformed weather data dictionaries
    """
    logger = logging.getLogger(__name__)
    logger.info("Starting data load to database")

    save_to_database(clean_data)

    logger.info("Data load completed")


def load_data(**context):
    """Airflow wrapper for load."""
    ti = context['ti']
    clean_data = ti.xcom_pull(task_ids='transform_weather_data')
    return load_data_impl(clean_data)


if __name__ == "__main__":
    raw = extract_data()
    clean = transform_data_impl(raw)
    load_data_impl(clean)
