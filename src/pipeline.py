import logging

from extract.weather_api import WeatherAPI
from transform.data_processor import transform_weather_data
from load.db_loader import save_to_database
from config import load_config
from utils.logger import setup_logging

config = load_config()
setup_logging()

logger = logging.getLogger(__name__)

weather_api = WeatherAPI()
cities_list = config['cities']
data_from_API = weather_api.get_weather_data(cities_list)
logger.info("All data fetched, starting transformation")
result = []
for i in data_from_API:
    result.append(transform_weather_data(i))

save_to_database(result)

logger.info("Pipeline finished! Processed %s cities", len(result))