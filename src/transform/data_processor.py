from datetime import datetime
from typing import Any
import logging


def kelvin_to_celsius(kelvin: float) -> float:
    """Converter Kelvin to Celsius

    Args:
        kelvin: Temperature in Kelvin

    Returns:
        float: Temperature in Celsius
    """
    return kelvin - 273.15


def timestamp_to_datetime(timestamp: int) -> datetime:
    """Convert Unix timestamp to readable datetime string.

    Args:
        timestamp: Unix timestamp

    Returns:
        datetime: Datetime object
    """
    return datetime.fromtimestamp(timestamp)


def safe_get(data: dict, *keys, default: Any = None) -> Any:
    """
    Safely get nested dictionary value.

    Args:
        data: Dictionary to extract from
        *keys: Keys to traverse (e.g., 'main', 'temp')
        default: Value to return if key not found

    Returns:
        Value if found, default otherwise

    Example:
        safe_get(data, 'main', 'temp', default=0)
        # Equivalent to: data.get('main', {}).get('temp', 0)
    """
    logger = logging.getLogger(__name__)
    current = data
    for key in keys:
        if not isinstance(current, dict):
            logger.debug("Cannot traverse - current is %s, not dict (key=%s, path=%s)",
                         type(current).__name__, key, keys)
            return default
        current = current.get(key)
        if current is None:
            logger.debug("Key '%s' not found in path %s", key, keys)
            return default
    return current


def transform_weather_data(raw_data: dict) -> dict:
    """
    Transform raw API data to clean format.

    Args:
        raw_data: Raw JSON from OpenWeatherMap API

    Returns:
        dict: Cleaned and transformed data, or None if city name is missing
    """
    logger = logging.getLogger(__name__)
    city = safe_get(raw_data, 'name')

    if not city:
        logger.error("Missing city name in data")
        return None

    temp = safe_get(raw_data, 'main', 'temp')
    measurement_time = safe_get(raw_data, 'dt')
    humidity = safe_get(raw_data, 'main', 'humidity')
    pressure = safe_get(raw_data, 'main', 'pressure')
    wind_speed = safe_get(raw_data, 'wind', 'speed')

    if temp is None or measurement_time is None or humidity is None or pressure is None or wind_speed is None:
        logger.warning("Incomplete data for %s", city)

    result_dict = {
        "city": city,
        "temperature_celsius": kelvin_to_celsius(temp) if temp is not None else None,
        "measurement_time": timestamp_to_datetime(measurement_time) if measurement_time is not None else None,
        "humidity": humidity if humidity is not None else None,
        "pressure": pressure if pressure is not None else None,
        "wind_speed": wind_speed if wind_speed is not None else None
    }

    return result_dict
