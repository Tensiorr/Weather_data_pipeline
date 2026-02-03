import os
import logging
import requests
from typing import Optional
from dotenv import load_dotenv
from ..config import load_config


load_dotenv()

class WeatherAPI:
    """
    Client for fetching weather data from OpenWeatherMap API.

    Attributes:
        api_key: OpenWeatherMap API key
        base_url: API endpoint URL
        timeout: Request timeout in seconds
    """
    def __init__(self, config: Optional[dict] = None):
        """
        Initialize WeatherAPI client.

        Args:
            config: Configuration dictionary. If None, loads from config.yaml

        Raises:
            Exception: If OPENWEATHER_API_KEY not found in environment
        """
        if config is None:
            config = load_config()

        self.logger = logging.getLogger(__name__)
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = config["api"]["base_url"]
        self.timeout = config['api']['timeout']
        if not self.api_key:
            raise Exception("OPENWEATHER_API_KEY not found in .env file.")

    def get_weather_data(self, cities: list[str]) -> list[dict]:
        """
        Fetch weather data for multiple cities.

        Args:
            cities: List of city names

        Returns:
            List of weather data dictionaries for successfully fetched cities

        Note:
            Skips cities with errors and logs them. Does not raise exceptions.
        """
        results = []

        for city in cities:
            self.logger.info("Starting request for %s", city)
            try:
                params = {
                    'q': city,
                    'appid': self.api_key
                }
                response = requests.get(self.base_url, params=params, timeout=self.timeout)

                if response.status_code != 200:
                    self.logger.error("Error %s for %s.", response.status_code, city)
                    continue

                data = response.json()
                results.append(data)
                self.logger.info("Fetched data for %s.", city)

            except requests.exceptions.Timeout:
                self.logger.error("Timeout error for %s.", city)
                continue

            except requests.exceptions.RequestException as e:
                self.logger.error("Request error for %s: %s", city, e)
                continue

            except ValueError:
                self.logger.error("Invalid JSON response for %s.", city)
                continue

        return results
